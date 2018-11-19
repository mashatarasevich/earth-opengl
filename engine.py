from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = 933120000

from matrix import perspective

class Engine:
    def __init__(self, wnd, program, model, cam):
        print('GL version:', str(glGetString(GL_VERSION)))
        print('GLSL version:', str(glGetString(GL_SHADING_LANGUAGE_VERSION)))
        print('Max texture size:', glGetIntegerv(GL_MAX_TEXTURE_SIZE)) 
        self.wnd = wnd
        self.setup_timer()
        self.mouse_button_pressed = [False] * 16
        self.mouse_button_pressed_xy = [(None, None)] * 16
        self.proj = np.eye(4)
        self.model = model
        self.cam = cam
        self.program = program
        self.dist = 0
        self.wireframe = False
        self.update_wireframe()
        self.adaptive_tess = True
        self.grid = True
        self.normals = False
        self.bump = False
        hires = False

        self.vao = glGenVertexArrays(1)
        self.vbo, self.ebo = glGenBuffers(2)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, model.vertices.nbytes, model.vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, model.triangles.nbytes, model.triangles, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)

        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        self.load_height_texture(hires)
        self.load_surface_texture(hires)

        glClearColor(0.1, 0.1, 0.1, 1.0);

    def load_surface_texture(self, hires=False):
        image = Image.open('topo_21600x10800.png' if hires else 'topo_10800x5400.png')
        width, height = image.size

        west = image.crop((0, 0, width // 2, height))
        east = image.crop((width // 2, 0, width, height))

        west_bytes = west.tobytes("raw", "RGB", 0, -1)
        east_bytes = east.tobytes("raw", "RGB", 0, -1)

        surfeast, surfwest = glGenTextures(2)
        self.surfwest = surfwest
        self.surfeast = surfeast

        for tex, data in zip((surfwest, surfeast), (west_bytes, east_bytes)):
            glBindTexture(GL_TEXTURE_2D, tex)
            print('glTexImage2D(surface)')
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width//2, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
            glGenerateMipmap(GL_TEXTURE_2D);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        del west_bytes
        del east_bytes
        del image
        glBindTexture(GL_TEXTURE_2D, 0)
        print('load_surface_texture done')

    def load_height_texture(self, hires=False):
        image = Image.open('elev_21600x10800.png' if hires else 'elev_10800x5400.png')
        width, height = image.size

        west = image.crop((0, 0, width // 2, height))
        east = image.crop((width // 2, 0, width, height))

        west_bytes = west.tobytes("raw", "L", 0, -1)
        east_bytes = east.tobytes("raw", "L", 0, -1)

        westtex, easttex = glGenTextures(2)
        self.westtex = westtex
        self.easttex = easttex

        for tex, data in zip((westtex, easttex), (west_bytes, east_bytes)):
            glBindTexture(GL_TEXTURE_2D, tex)
            print('glTexImage2D(height)')
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, width//2, height, 0, GL_RED, GL_UNSIGNED_BYTE, data)
            glGenerateMipmap(GL_TEXTURE_2D);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        del west_bytes
        del east_bytes
        del image
        glBindTexture(GL_TEXTURE_2D, 0)
        print('load_height_texture done')

    def update_wireframe(self):
        if self.wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def setup_timer(self):
        self.frames = 0
        glutTimerFunc(1000, self.timer, 1000)  # every sec

    def timer(self, interval_ms):
        fps = self.frames / (interval_ms * 1e-3)
        glutSetWindowTitle('Frames per second: ' + str(fps))
        self.setup_timer()

    def distance(self):
        h = 1.0 + np.exp(self.dist / 10)
        return h

    def display(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.program.get())

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.surfwest)
            self.program.set_uniform_int("surfwest", 0);

            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.surfeast)
            self.program.set_uniform_int("surfeast", 1);

            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, self.westtex)
            self.program.set_uniform_int("westtex", 2);

            glActiveTexture(GL_TEXTURE3)
            glBindTexture(GL_TEXTURE_2D, self.easttex)
            self.program.set_uniform_int("easttex", 3);
            
            self.program.set_uniform_mat("proj", self.proj)
            self.program.set_uniform_vec("trans", np.array([0, 0, self.distance(), 0], dtype=np.float32))
            self.program.set_uniform_mat("modelrot", self.model.total_rotation())
            self.program.set_uniform_mat("viewrot", self.cam.total_rotation())

            self.program.set_uniform_int("adaptive_tess", 1 if self.adaptive_tess else 0)
            self.program.set_uniform_int("grid", 1 if self.grid else 0)
            self.program.set_uniform_int("normals", 1 if self.normals else 0)
            self.program.set_uniform_int("bump", 1 if self.bump else 0)

            glBindVertexArray(self.vao)
            glPatchParameteri(GL_PATCH_VERTICES, 3)
            glDrawElements(GL_PATCHES, self.model.triangles.size, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
            glBindTexture(GL_TEXTURE_2D, 0)
            self.frames += 1
            glutSwapBuffers()
        except KeyboardInterrupt:
            glutDestroyWindow(self.wnd)

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        self.proj = perspective(fovy=45, aspect=w / h, z_near=0.05, z_far=30) 

    def keyDown(self, key, *args):
        pass

    def keyUp(self, key, *args):
        if key == b'\x1b' or key == b'q':
            glutDestroyWindow(self.wnd)
        if key == b'w':
            self.wireframe = not self.wireframe
            self.update_wireframe()
        if key == b'c':
            self.cam.reset()
        if key == b'r':
            self.model.reset()
        if key == b't':
            self.adaptive_tess = not self.adaptive_tess
        if key == b'g':
            self.grid = not self.grid
        if key == b'n':
            self.normals = not self.normals
        if key == b'b':
            self.bump = not self.bump

    def update_delta(self, button, dx, dy):
        # Called on mouse move with button pressed
        if button == GLUT_LEFT_BUTTON:
            self.model.set_add_rotation(dx, dy)
        if button == GLUT_RIGHT_BUTTON:
            self.cam.set_add_rotation(dx, dy)
        if button == GLUT_MIDDLE_BUTTON:
            self.cam.set_add_rotation_roll(dx, dy)

    def commit_delta(self, button, dx, dy):
        # Called on mouse move after button is released
        if button == GLUT_LEFT_BUTTON:
            self.model.commit_rotation(dx, dy)
        if button == GLUT_RIGHT_BUTTON:
            self.cam.commit_rotation(dx, dy)
        if button == GLUT_MIDDLE_BUTTON:
            self.cam.commit_rotation_roll(dx, dy)

    def mouse(self, button, state, x, y):
        if state == 0:  # pressed
            self.mouse_button_pressed[button] = True
            self.mouse_button_pressed_xy[button] = (x, y)
            # Handle wheel
            if button == 3 and self.dist > -50:
                self.dist -= 1
            if button == 4 and self.dist < 10:
                self.dist += 1
        else:  # released
            self.mouse_button_pressed[button] = False
            x0, y0 = self.mouse_button_pressed_xy[button]
            self.commit_delta(button, x - x0, y - y0)

    def motion(self, x, y):
        for button, ispress in enumerate(self.mouse_button_pressed):
            if ispress:
                x0, y0 = self.mouse_button_pressed_xy[button]
                self.update_delta(button, x - x0, y - y0)
