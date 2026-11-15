import os
import numpy as np
import pygame
import rapi
import noesis
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_compression_s3tc import *
from OpenGL.GL.ARB.multisample import *
from NoesisAnimator import Animator

PIXELFORMAT_TO_OPENGL_INTERNAL_TYPE = {
    noesis.NOESISTEX_DXT1: GL_COMPRESSED_RGBA_S3TC_DXT1_EXT,
    noesis.NOESISTEX_DXT3: GL_COMPRESSED_RGBA_S3TC_DXT3_EXT,
    noesis.NOESISTEX_DXT5: GL_COMPRESSED_RGBA_S3TC_DXT5_EXT,
    noesis.NOESISTEX_RGB24: GL_RGB,
    noesis.NOESISTEX_RGBA32: GL_RGBA,
    noesis.NOESISTEX_UNKNOWN: GL_RGBA
}

CUBE_FACES = [GL_TEXTURE_CUBE_MAP_POSITIVE_X, GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
              GL_TEXTURE_CUBE_MAP_POSITIVE_Y, GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
              GL_TEXTURE_CUBE_MAP_POSITIVE_Z, GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]

STRIP_RESTART = (0xFFFF, 0xFFFFFFFF)


def triangulate(indices, shape):
    """Index buffer -> (n, 3) triangle list. Strips restart on 0xFFFF / 0xFFFFFFFF."""
    if shape in (noesis.RPGEO_TRIANGLE_STRIP, noesis.RPGEO_TRIANGLE_STRIP_FLIPPED):
        tris, strip = [], []
        flip = 1 if shape == noesis.RPGEO_TRIANGLE_STRIP_FLIPPED else 0
        for v in list(indices) + [0xFFFF]:
            if v in STRIP_RESTART:
                for i in range(len(strip) - 2):
                    a, b, c = strip[i], strip[i + 1], strip[i + 2]
                    if a == b or b == c or a == c:
                        continue
                    tris.append((a, b, c) if (i + flip) % 2 == 0 else (b, a, c))
                strip = []
            else:
                strip.append(v)
        return np.array(tris, dtype=np.uint32).reshape(-1, 3)
    if shape == noesis.RPGEO_TRIANGLE_FAN:
        idx = list(indices)
        return np.array([(idx[0], idx[i], idx[i + 1]) for i in range(1, len(idx) - 1)],
                        dtype=np.uint32).reshape(-1, 3)
    idx = np.array(indices, dtype=np.uint32)
    return idx[:len(idx) - len(idx) % 3].reshape(-1, 3)


class MeshBuffers:
    """Vertex arrays for one NoeMesh, with optional skinning data."""

    def __init__(self, mesh, boneCount):
        self.material = mesh.matName
        self.positions = np.array(mesh.positions, dtype=np.float32).reshape(-1, 3)
        n = len(self.positions)
        normals = getattr(mesh, "normals", None)
        self.normals = (np.array(normals, dtype=np.float32).reshape(-1, 3) if normals and len(normals) == n
                        else np.zeros((n, 3), dtype=np.float32))
        uvs = getattr(mesh, "uvs", None)
        self.uvs = (np.array([uv[:2] for uv in uvs], dtype=np.float32) if uvs and len(uvs) == n
                    else np.zeros((n, 2), dtype=np.float32))
        colors = getattr(mesh, "colors", None)
        self.colors = None
        if colors and len(colors) == n:
            c = np.array([tuple(x)[:4] for x in colors], dtype=np.float32)
            if c.shape[1] == 3:
                c = np.hstack([c, np.ones((n, 1), np.float32)])
            self.colors = c
        self.triangles = triangulate(mesh.indices, mesh.shape)
        self.skinned = False
        weights = getattr(mesh, "weights", None)
        indices = getattr(mesh, "boneIndexBuffer", None)
        if boneCount and weights and indices and len(weights) == n and len(indices) == n:
            boneMap = list(mesh.boneMap) if getattr(mesh, "boneMap", None) else None
            local = np.array(indices, dtype=np.int64).reshape(n, -1)
            w = np.array(weights, dtype=np.float32).reshape(n, -1)
            k = min(local.shape[1], w.shape[1])
            local, w = local[:, :k], w[:, :k]
            if boneMap:
                lut = np.array(boneMap + [0], dtype=np.int64)
                local = lut[np.clip(local, 0, len(boneMap))]
            local = np.clip(local, 0, boneCount - 1)
            total = w.sum(axis=1, keepdims=True)
            total[total == 0] = 1.0
            self.boneIndices, self.boneWeights = local, w / total
            self.skinned = True
        self.drawPositions, self.drawNormals = self.positions, self.normals

    def skin(self, palette):
        """palette: (bones, 4, 4) row-vector skinning matrices."""
        if not self.skinned:
            return
        m = np.einsum("vk,vkij->vij", self.boneWeights, palette[self.boneIndices])
        p = self.positions
        self.drawPositions = (np.einsum("vj,vji->vi", p, m[:, :3, :3]) + m[:, 3, :3]).astype(np.float32)
        nrm = np.einsum("vj,vji->vi", self.normals, m[:, :3, :3])
        self.drawNormals = nrm.astype(np.float32)

    def bindPose(self):
        self.drawPositions, self.drawNormals = self.positions, self.normals


class NoesisLoader:
    def __init__(self, model):
        self.modelMats = model.modelMats
        self.meshes = model.meshes
        self.loadedTextures = {}
        self.flipX = False
        self.flipY = False
        self.flipZ = False
        self.flipU = False
        self.flipV = False
        self.scale = 3
        self.blending = True
        self.loadTextures = True
        self.animator = Animator(model)
        boneCount = self.animator.skeleton.count if self.animator.skeleton else 0
        self.buffers = [MeshBuffers(m, boneCount) for m in self.meshes]
        self.textureIds = {}
        self.textureTargets = {}

        if not glInitTextureCompressionS3TcEXT():
            print('ERROR: glInitTextureCompressionS3TcEXT not supported')
        if not glInitMultisampleARB():
            print('ERROR: glInitMultisampleARB not supported')

        if self.animator.anims:
            print('Animations: ' + ', '.join('%s (%d frames)' % (a.name, a.numFrames) for a in self.animator.anims))

    # kept for compatibility with older viewer code: textures are prepared here
    def render(self):
        glEnable(GL_MULTISAMPLE_ARB)
        for buf in self.buffers:
            self.textureIds[id(buf)] = self.materialTexture(buf.material) if self.loadTextures else None
            buf.alphaTest, buf.blend = self.materialBlend(buf.material)

    def materialBlend(self, materialName):
        """(alpha test threshold or None, (src, dst) GL blend factors or None for opaque)."""
        material = None
        if materialName and self.modelMats:
            material = next((x for x in self.modelMats.matList if x.name == materialName), None)
        if material is None:
            return None, (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) if self.blending else None
        alphaTest = getattr(material, "alphaTest", None) or None
        src, dst = getattr(material, "blendSrc", None), getattr(material, "blendDst", None)
        if src and dst:
            blend = (globals().get(src, GL_SRC_ALPHA), globals().get(dst, GL_ONE_MINUS_SRC_ALPHA))
        elif getattr(material, "defaultBlend", 1) == 0 or not self.blending:
            blend = None
        else:
            blend = (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        return alphaTest, blend

    def update(self, seconds):
        self.animator.advance(seconds)
        palette = self.animator.skinMatrices()
        for buf in self.buffers:
            if palette is not None:
                buf.skin(palette)
            else:
                buf.bindPose()

    def draw(self):
        glFrontFace(GL_CCW)
        glEnable(GL_NORMALIZE)
        glPushMatrix()
        glScalef(self.scale * (-1 if self.flipX else 1), self.scale * (-1 if self.flipY else 1),
                 self.scale * (-1 if self.flipZ else 1))
        if self.flipU or self.flipV:
            glMatrixMode(GL_TEXTURE)
            glPushMatrix()
            glTranslatef(1 if self.flipU else 0, 1 if self.flipV else 0, 0)
            glScalef(-1 if self.flipU else 1, -1 if self.flipV else 1, 1)
            glMatrixMode(GL_MODELVIEW)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        # opaque meshes first, then translucent ones without depth writes, so transparent
        # texels never hide what's behind them
        order = [b for b in self.buffers if getattr(b, "blend", None) is None] + \
                [b for b in self.buffers if getattr(b, "blend", None) is not None]
        for buf in order:
            if not len(buf.triangles):
                continue
            if getattr(buf, "blend", None) is not None:
                glEnable(GL_BLEND)
                glBlendFunc(*buf.blend)
                glDepthMask(GL_FALSE)
            else:
                glDisable(GL_BLEND)
                glDepthMask(GL_TRUE)
            if getattr(buf, "alphaTest", None):
                glEnable(GL_ALPHA_TEST)
                glAlphaFunc(GL_GREATER, buf.alphaTest)
            else:
                glDisable(GL_ALPHA_TEST)
            tex = self.textureIds.get(id(buf))
            if tex is not None:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, tex)
            else:
                glDisable(GL_TEXTURE_2D)
            if buf.colors is not None:
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(4, GL_FLOAT, 0, buf.colors)
            else:
                glDisableClientState(GL_COLOR_ARRAY)
                glColor4f(1.0, 1.0, 1.0, 1.0)
            glVertexPointer(3, GL_FLOAT, 0, buf.drawPositions)
            glNormalPointer(GL_FLOAT, 0, buf.drawNormals)
            glTexCoordPointer(2, GL_FLOAT, 0, buf.uvs)
            glDrawElements(GL_TRIANGLES, buf.triangles.size, GL_UNSIGNED_INT, buf.triangles)
        glDisableClientState(GL_COLOR_ARRAY)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDepthMask(GL_TRUE)
        glDisable(GL_ALPHA_TEST)
        if self.flipU or self.flipV:
            glMatrixMode(GL_TEXTURE)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def materialTexture(self, materialName):
        if not materialName or not self.modelMats:
            return None
        material = next((x for x in self.modelMats.matList if x.name == materialName), None)
        textureName = material and material.texName
        if not textureName:
            return None
        texture = next((x for x in self.modelMats.texList if x.name == textureName), None)
        if texture is not None:
            textureId = self.loadNoeTexture(texture)
        else:
            textureId = self.loadFileTexture(textureName)
        if textureId is None:
            print('Texture not found: ' + textureName)
        return textureId

    def textureByName(self, name):
        """GL texture for a model texture name (2D or cube), loading it on first use."""
        if not self.modelMats:
            return None
        texture = next((x for x in self.modelMats.texList if x.name == name), None)
        return self.loadNoeTexture(texture) if texture is not None else self.loadFileTexture(name)

    def loadFileTexture(self, name):
        if name in self.loadedTextures:
            return self.loadedTextures[name]

        modelDirectory = rapi.getDirForFilePath( rapi.getLastCheckedName() )
        filename = modelDirectory + name

        if not os.path.isfile(filename):
            print('File not found: ' + filename)
            return None

        surf = pygame.image.load(filename)
        bitsize = surf.get_bitsize()

        if bitsize ==  24:
            data = pygame.image.tostring(surf, 'RGB')
            internalType = GL_RGB
        elif bitsize == 32:
            data = pygame.image.tostring(surf, 'RGBA')
            internalType = GL_RGBA
        else:
            print('Unknown bit size: ' + str(bitsize))
            return None

        width, height = surf.get_rect().size

        return self.loadTextureFromData(name, data, width, height, internalType)

    def loadNoeTexture(self, texture):
        name = texture.name

        if name in self.loadedTextures:
            return self.loadedTextures[name]

        width = texture.width
        height = texture.height
        data = texture.pixelData
        pixelType = texture.pixelType
        internalType = PIXELFORMAT_TO_OPENGL_INTERNAL_TYPE.get(pixelType)
        if internalType is None:
            print('Unsupported texture pixel type %s: %s' % (pixelType, name))
            return None
        if getattr(texture, "flags", 0) & getattr(noesis, "NTEXFLAG_CUBEMAP", 0):
            return self.loadCubeFromData(name, data, width, height, internalType)

        return self.loadTextureFromData(texture.name, data, width, height, internalType)

    def loadCubeFromData(self, name, data, width, height, internalType):
        """Cube map: the six faces (+X -X +Y -Y +Z -Z) stored one after another."""
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureId)
        size = len(data) // 6
        for i, target in enumerate(CUBE_FACES):
            face = bytes(data[i * size:(i + 1) * size])
            if internalType in (GL_RGB, GL_RGBA):
                glTexImage2D(target, 0, internalType, width, height, 0, internalType, GL_UNSIGNED_BYTE, face)
            else:
                glCompressedTexImage2D(target, 0, internalType, width, height, 0, face)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        for wrap in (GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_WRAP_R):
            glTexParameteri(GL_TEXTURE_CUBE_MAP, wrap, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
        self.loadedTextures[name] = textureId
        self.textureTargets[textureId] = GL_TEXTURE_CUBE_MAP
        return textureId

    def loadTextureFromData(self, name, data, width, height, internalType):
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        if internalType == GL_RGB or internalType == GL_RGBA:
            glTexImage2D(GL_TEXTURE_2D, 0, internalType, width, height, 0, internalType, GL_UNSIGNED_BYTE, data)
        else:
            glCompressedTexImage2D(GL_TEXTURE_2D, 0, internalType, width, height, 0, data)

        self.loadedTextures[name] = textureId
        return textureId
