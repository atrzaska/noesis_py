import pygame
import sys
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from NoesisLoader import *

class NoesisViewer:
    def __init__(self, rpg):
        self.rpg = rpg
        self.toon = True

    @classmethod
    def call(self, rpg):
        return NoesisViewer(rpg).call()

    def call(self):
        noesisLoader = NoesisLoader(self.rpg)

        pygame.init()
        viewport = (1280,720)
        srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

        if not self.toon:
            glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
            glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHTING)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        model = noesisLoader.render()

        clock = pygame.time.Clock()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(90.0, width/float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

        rx, ry = (0,0)
        tx, ty = (0,0)
        zpos = 5
        rotate = move = False
        while 1:
            clock.tick(30)
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4: zpos = max(1, zpos-1)
                    elif e.button == 5: zpos += 1
                    elif e.button == 1: rotate = True
                    elif e.button == 3: move = True
                elif e.type == MOUSEBUTTONUP:
                    if e.button == 1: rotate = False
                    elif e.button == 3: move = False
                elif e.type == MOUSEMOTION:
                    i, j = e.rel
                    if rotate:
                        rx += i
                        ry += j
                    if move:
                        tx += i
                        ty -= j

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslate(tx/20., ty/20., - zpos)
            glRotate(ry, 1, 0, 0)
            glRotate(-rx, 0, 1, 0)
            glCallList(model.gl_list)
            pygame.display.flip()
