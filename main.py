import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *

OpenGL.FULL_LOGGING = True

from engine import Engine
from model import Model
from camera import Camera
from program import Program
#from icosphere import icosphere
from sphere import sphere

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitContextVersion(4, 1)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    wnd = glutCreateWindow('OpenGL 4')
    
    # model = Model(*icosphere(6))
    model = Model(*sphere(480, 240))
    cam = Camera(sensivity=0.1)

    program = Program(vertex='vertex.glsl',
                      tess_control='tess_control.glsl',
                      tess_eval='tess_eval.glsl',
                      geometry='geometry.glsl',
                      fragment='fragment.glsl')
    engine = Engine(wnd, program, model, cam)

    glutIdleFunc(engine.display)
    glutReshapeFunc(engine.reshape)
    glutKeyboardFunc(engine.keyDown)
    glutKeyboardUpFunc(engine.keyUp)
    glutMouseFunc(engine.mouse)
    glutMotionFunc(engine.motion)
    
    glEnable(GL_DEPTH_TEST)

    glutMainLoop()

if __name__ == "__main__":
    main()
