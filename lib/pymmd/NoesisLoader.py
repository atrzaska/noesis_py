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
        self.flipV = True
        self.blending = True

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
            materials = noeMaterials.materials
            material = next(x for x in materials if x.name == materialName)
            texture = material.texture
            # texture = noeMaterials.textures[0]

            if texture != None:
                glBindTexture(GL_TEXTURE_2D, self.loadMaterial(material))
                # glBindTexture(GL_TEXTURE_2D, self.loadTexture(texture))

            glBegin(SHAPE_TO_GL_OBJECT[faceInfo.shape])
            for face in faceInfo.buff:
                normal = normals[face]
                vertex = vertices[face]
                uv = uvs[face]

                x = normal[0] * -1 if self.flipX else normal[0]
                y = normal[1]
                z = normal[2]
                glNormal3fv([x, y, z])
                u = uv[0]
                v = 1 - uv[1] if self.flipV else uv[1]
                glTexCoord2fv([u, v])
                x = vertex[0] * -1 if self.flipX else vertex[0]
                y = vertex[1]
                z = vertex[2]
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

        ix = texture.width
        iy = texture.height
        image = texture.data

        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        self.loadedTextures[texture.name] = textureId
        return textureId
