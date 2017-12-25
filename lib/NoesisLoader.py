import os
import pygame
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_compression_s3tc import *
from OpenGL.GL.ARB.multisample import *
import rapi

SHAPE_TO_GL_OBJECT = {
    'RPGEO_TRIANGLE': GL_TRIANGLES,
    'RPGEO_TRIANGLE_STRIP': GL_TRIANGLE_STRIP
}

PIXELFORMAT_TO_OPENGL_INTERNAL_TYPE = {
    'NOESISTEX_DXT1': GL_COMPRESSED_RGBA_S3TC_DXT1_EXT,
    'NOESISTEX_DXT3': GL_COMPRESSED_RGBA_S3TC_DXT3_EXT,
    'NOESISTEX_DXT5': GL_COMPRESSED_RGBA_S3TC_DXT5_EXT,
    'NOESISTEX_RGB24': GL_RGB,
    'NOESISTEX_RGBA32': GL_RGBA,
    'NOESISTEX_UNKNOWN': GL_RGBA
}

class NoesisLoader:
    def __init__(self, rpgContext):
        self.rpgContext = rpgContext
        self.loadedTextures = {}
        self.flipX = False
        self.flipY = False
        self.flipZ = False
        self.flipU = False
        self.flipV = False
        self.scale = 3
        self.blending = True
        self.loadTextures = True

        if not glInitTextureCompressionS3TcEXT():
            print('ERROR: glInitTextureCompressionS3TcEXT not supported')
        if not glInitMultisampleARB():
            print('ERROR: glInitMultisampleARB not supported')

    def render(self):
        self.gl_list = glGenLists(1)
        glEnable(GL_MULTISAMPLE_ARB)

        glNewList(self.gl_list, GL_COMPILE)

        if self.blending:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)

        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for mesh in self.rpgContext.meshes:
            vertices = mesh.positions
            normals = mesh.normals
            material = mesh.matName
            faceBuffer = mesh.indices
            shape = mesh.shape
            uvs = mesh.uvs

            if self.loadTextures:
                noeMaterials = self.rpgContext.models[-1].modelMats
                materials = noeMaterials.matList
                if material:
                    material = next(x for x in materials if x.name == material)
                    textures = noeMaterials.texList
                    textureName = material and material.texName
                    if textureName:
                        texture = None
                        loadedTextureId = None

                        if textures != []:
                            texture = next(x for x in textures if x.name == textureName)

                        if texture != None:
                            loadedTextureId = self.loadNoeTexture(texture)
                        else:
                            loadedTextureId = self.loadFileTexture(textureName)

                        if loadedTextureId != None:
                            glBindTexture(GL_TEXTURE_2D, loadedTextureId)
                        else:
                            print('Texture not found: ' + textureName)

            glBegin(SHAPE_TO_GL_OBJECT[shape])

            for face in faceBuffer:
                if face == 65535: # TODO: handle other types
                    glEnd()
                    glBegin(SHAPE_TO_GL_OBJECT[shape])
                    continue

                normal = normals[face]
                vertex = vertices[face]
                uv = uvs[face]

                scale = self.scale
                flipX = -1 if self.flipX else 1
                flipY = -1 if self.flipY else 1
                flipZ = -1 if self.flipZ else 1

                x = normal[0] * flipX * scale
                y = normal[1] * flipY * scale
                z = normal[2] * flipZ * scale

                glNormal3fv([x, y, z])

                u = (1 - uv[0] if self.flipU else uv[0])
                v = (1 - uv[1] if self.flipV else uv[1])

                glTexCoord2fv([u, v])

                x = vertex[0] * flipX * scale
                y = vertex[1] * flipY * scale
                z = vertex[2] * flipZ * scale

                glVertex3fv([x, y, z])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
        return self

    def loadFileTexture(self, name):
        if name in self.loadedTextures:
            return self.loadedTextures[name]

        modelDirectory = rapi.getDirForFilePath( rapi.getLastCheckedName() )
        filename = modelDirectory + name

        if not os.path.isfile(filename):
            print('File not found: ' + filename)
            return None

        extension = os.path.splitext(filename)[1][1:].lower()
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
        internalType = PIXELFORMAT_TO_OPENGL_INTERNAL_TYPE[pixelType]

        return self.loadTextureFromData(texture.name, data, width, height, internalType)

    def loadTextureFromData(self, name, data, width, height, internalType):
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        if internalType == GL_RGB or internalType == GL_RGBA:
            glTexImage2D(GL_TEXTURE_2D, 0, internalType, width, height, 0, internalType, GL_UNSIGNED_BYTE, data)
        else:
            glCompressedTexImage2D(GL_TEXTURE_2D, 0, internalType, width, height, 0, data)

        self.loadedTextures[name] = textureId
        return textureId
