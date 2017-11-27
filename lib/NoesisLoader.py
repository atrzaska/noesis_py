import os
import pygame
from OpenGL.GL import *
import rapi

SHAPE_TO_GL_OBJECT = {
    'RPGEO_TRIANGLE': GL_TRIANGLES,
    'RPGEO_TRIANGLE_STRIP': GL_TRIANGLE_STRIP
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
        self.loadTextures = False

    def render(self):
        self.gl_list = glGenLists(1)

        glNewList(self.gl_list, GL_COMPILE)

        if self.blending:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for i in range(len(self.rpgContext.faceBuffers)):
            vertexBufferLength = len(self.rpgContext.vertexBuffers)
            if vertexBufferLength == 1:
                vertices = self.rpgContext.vertexBuffers[0]
                normals = self.rpgContext.normalBuffers[0]
                uvs = self.rpgContext.uvBuffers[0]
                faceInfo = self.rpgContext.faceBuffers[i]
            else:
                vertices = self.rpgContext.vertexBuffers[i]
                normals = self.rpgContext.normalBuffers[i]
                uvs = self.rpgContext.uvBuffers[i]
                faceInfo = self.rpgContext.faceBuffers[i]

            materialName = faceInfo.material
            noeMaterials = self.rpgContext.models[-1].materials
            materials = noeMaterials.matList
            material = next(x for x in materials if x.name == materialName)
            textures = noeMaterials.texList
            textureName = material.texName
            texture = next(x for x in textures if x.name == textureName)

            if self.loadTextures and texture != None:
                glBindTexture(GL_TEXTURE_2D, self.loadTexture(texture))

            glBegin(SHAPE_TO_GL_OBJECT[faceInfo.shape])
            for face in faceInfo.buff:
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

    def loadMaterial(self, material):
        texture = material.texture

        if texture in self.loadedTextures:
            return self.loadedTextures[texture]

        directory = os.getcwd()
        filename = directory + '/data/' + texture
        surf = pygame.image.load(filename)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size

        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        self.loadedTextures[texture] = textureId
        return textureId

    def loadTexture(self, texture):
        if texture.name in self.loadedTextures:
            return self.loadedTextures[texture.name]

        width = texture.width
        height = texture.height
        data = texture.pixelData

        return self.loadTextureFromData(texture.name, data, width, height)

    def loadTextureFromData(self, name, data, width, height):
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        self.loadedTextures[name] = textureId
        return textureId
