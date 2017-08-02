import os
import pygame
from OpenGL.GL import *

SHAPE_TO_GL_OBJECT = {
    'RPGEO_TRIANGLE': GL_TRIANGLES,
    'RPGEO_TRIANGLE_STRIP': GL_TRIANGLE_STRIP
}

class NoesisLoader:
    def __init__(self, rpg):
        self.gl_list = glGenLists(1)

        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for i in range(len(rpg.faceBuffers)):
            vertexBufferLength = len(rpg.vertexBuffers)
            if vertexBufferLength == 1:
                vertices = rpg.vertexBuffers[0]
                normals = rpg.normalBuffers[0]
                uvs = rpg.uvBuffers[0]
                faces = rpg.faceBuffers[i]
            else:
                vertices = rpg.vertexBuffers[i]
                normals = rpg.normalBuffers[i]
                uvs = rpg.uvBuffers[i]
                faces = rpg.faceBuffers[i]

            glBegin(SHAPE_TO_GL_OBJECT[faces['shape']])
            for face in faces['buff']:
                glNormal3fv(normals[face])
                glVertex3fv(vertices[face])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
