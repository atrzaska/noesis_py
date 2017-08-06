import os
import pygame
from OpenGL.GL import *
import rapi

SHAPE_TO_GL_OBJECT = {
    'RPGEO_TRIANGLE': GL_TRIANGLES,
    'RPGEO_TRIANGLE_STRIP': GL_TRIANGLE_STRIP
}

class NoesisLoader:
    def __init__(self, rpg):
        self.vertexBuffers = rpg.vertexBuffers
        self.normalBuffers = rpg.normalBuffers
        self.uvBuffers = rpg.uvBuffers
        self.faceBuffers = rpg.faceBuffers
        self.loadedTextures = {}

    def render(self):
        self.gl_list = glGenLists(1)

        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for i in range(len(self.faceBuffers)):
            vertexBufferLength = len(self.vertexBuffers)
            if vertexBufferLength == 1:
                vertices = self.vertexBuffers[0]
                normals = self.normalBuffers[0]
                uvs = self.uvBuffers[0]
                faceInfo = self.faceBuffers[i]
            else:
                vertices = self.vertexBuffers[i]
                normals = self.normalBuffers[i]
                uvs = self.uvBuffers[i]
                faceInfo = self.faceBuffers[i]

            texture = faceInfo.texture
            if texture:
                glBindTexture(GL_TEXTURE_2D, self.loadTexture(texture))

            glBegin(SHAPE_TO_GL_OBJECT[faceInfo.shape])
            for face in faceInfo.buff:
                glNormal3fv(normals[face])
                glTexCoord2fv(uvs[face])
                glVertex3fv(vertices[face])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
        return self

    def loadTexture(self, texture):
        if texture in self.loadedTextures:
            return self.loadedTextures[texture]

        directory = os.getcwd()
        print(texture)
        filename = directory + '/data/' + texture
        surf = pygame.image.load(filename)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size

        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        self.loadedTextures[texture] = textureId
        return textureId
