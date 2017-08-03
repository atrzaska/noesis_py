import os
import pygame
from OpenGL.GL import *

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
                faces = self.faceBuffers[i]
            else:
                vertices = self.vertexBuffers[i]
                normals = self.normalBuffers[i]
                uvs = self.uvBuffers[i]
                faces = self.faceBuffers[i]

            # glBindTexture(GL_TEXTURE_2D, self.loadedTextures[self.currentTexture])

            glBegin(SHAPE_TO_GL_OBJECT[faces.shape])
            for face in faces.buff:
                glNormal3fv(normals[face])
                glTexCoord2fv(uvs[face])
                glVertex3fv(vertices[face])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
        return self

    def renderTexture(self, texture):
        filename = directory + '/' + texture
        directory = os.path.dirname(filename)
        surf = pygame.image.load(directory + '/' + texture)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size

        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        self.loadedTextures[texture] = textureId
        return textureId
