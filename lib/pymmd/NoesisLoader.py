import os
import pygame
from OpenGL.GL import *

SHAPE_TO_GL_OBJECT = {
    'RPGEO_TRIANGLE': GL_TRIANGLES,
    'RPGEO_TRIANGLE_STRIP': GL_TRIANGLE_STRIP
}

class NoesisLoader:
    def __init__(self, rpg):
        self.vertices = rpg.vertices
        self.normals = rpg.normals
        self.uvs = rpg.uvs
        self.faceBuffers = rpg.faceBuffers
        self.gl_list = glGenLists(1)

        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        print({ 'vertices_len': len(self.vertices) })
        # TODO not working array of faces should be 3 vertices instead
        for face in self.faceBuffers:
            print({ 'shapeLen': len(face['buff']) })
            glBegin(SHAPE_TO_GL_OBJECT[face['shape']])
            for face in face['buff']:
                glVertex3fv(self.vertices[face])
                glNormal3fv(self.normals[face])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
