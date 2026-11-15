import pygame
import sys
import os
import math
import numpy as np
import rapi
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from NoesisLoader import *

SCALE = int(os.getenv('SCALE', '1'))
WIDTH = 1280 * SCALE
HEIGHT = 720 * SCALE

HELP = """Controls:
  left mouse drag  rotate        right mouse drag  pan        wheel  zoom
  space            play/pause    left/right        step frame (shift: 10)
  up/down or n/p   next/previous animation         r      toggle bind pose
  l                toggle fixed-function lighting
  esc              quit"""


class NoesisViewer:
    def __init__(self, models):
        self.models = models
        self.toon = False  # True = unlit (flat colour)
        self.loaders = []

    def applyLighting(self):
        if self.toon:
            glDisable(GL_LIGHTING)
        else:
            glEnable(GL_LIGHTING)

    def frameModels(self):
        """Initial camera: look at the centre of all models' bind-pose bounds."""
        pts = [buf.positions * loader.scale for loader in self.loaders for buf in loader.buffers if len(buf.positions)]
        if not pts:
            return (0.0, 0.0), 5.0
        pts = np.concatenate(pts)
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        center = (lo + hi) / 2
        width, height, depth = (float(x) for x in hi - lo)
        # distance at which the bounds fit the 60 degree vertical field of view, with a margin
        tanHalf = math.tan(math.radians(30.0))
        fit = max(height / 2 / tanHalf, width / 2 / (tanHalf * WIDTH / float(HEIGHT)))
        return (center[0], center[1]), max(1.0, fit * 1.1 + depth / 2)

    def caption(self):
        parts = []
        for loader in self.loaders:
            a = loader.animator
            if a.anim:
                parts.append('%s %d/%d%s' % (a.anim.name, int(a.frame), a.anim.numFrames,
                                             '' if a.playing else ' (paused)'))
        pygame.display.set_caption('Noesis-Py' + (' - ' + ', '.join(parts) if parts else ''))

    def call(self):
        pygame.init()
        viewport = (WIDTH, HEIGHT)
        srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        self.applyLighting()

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.2, 0.2, 0.2, 0.2)

        for model in self.models:
            loader = NoesisLoader(model)
            loader.render()
            self.loaders.append(loader)
        print(HELP)

        clock = pygame.time.Clock()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(60.0, width/float(height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

        (cx, cy), zpos = self.frameModels()
        rx, ry = (0,0)
        tx, ty = (0,0)
        rotate = move = False
        while 1:
            seconds = clock.tick(60) / 1000.0
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN:
                    shift = pygame.key.get_mods() & KMOD_SHIFT
                    if e.key == K_ESCAPE:
                        sys.exit()
                    if e.key == K_l:
                        self.toon = not self.toon
                        self.applyLighting()
                    for loader in self.loaders:
                        a = loader.animator
                        if e.key == K_SPACE:
                            a.playing = not a.playing
                        elif e.key == K_RIGHT:
                            a.playing = False
                            a.step(10 if shift else 1)
                        elif e.key == K_LEFT:
                            a.playing = False
                            a.step(-10 if shift else -1)
                        elif e.key in (K_UP, K_n):
                            a.next(1)
                        elif e.key in (K_DOWN, K_p):
                            a.next(-1)
                        elif e.key == K_r:
                            a.bindPose = not a.bindPose
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4: zpos = max(0.2, zpos * 0.9)
                    elif e.button == 5: zpos *= 1.1
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

            for loader in self.loaders:
                loader.update(seconds)
            self.caption()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(60.0, width/float(height), 0.1, 1000.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            pan = zpos / 400.0
            glTranslate(tx * pan, ty * pan, -zpos)
            glRotate(ry, 1, 0, 0)
            glRotate(-rx, 0, 1, 0)
            glTranslate(-cx, -cy, 0)
            for loader in self.loaders:
                loader.draw()
            pygame.display.flip()
