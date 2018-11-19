from OpenGL.GL import *

def link(shaders):
    program = glCreateProgram()
    if program == 0:
        raise ValueError('Could not glCreateProgram')

    for shader in shaders:
        glAttachShader(program, shader)

    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS, None) == GL_FALSE:
        info_log = glGetProgramInfoLog(program)
        print(info_log)
        glDeleteProgram(program)
        raise ValueError('glLinkProgram failed')

    return program

def load_shader(kind, filename):
    print('Loading', filename)
    shader = glCreateShader(kind)
    if shader == 0:
        raise ValueError('glCreateShader failed')

    with open(filename, 'r') as f:
        source = f.read()

    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS, None) == GL_FALSE:
        info_log = glGetShaderInfoLog(shader)
        print(info_log)
        glDeleteProgram(shader)
        raise ValueError('Shader compilation failed')

    return shader


class Program:
    def __init__(self, **kwargs):
        known_types = {
                'vertex': GL_VERTEX_SHADER,
                'tess_control': GL_TESS_CONTROL_SHADER,
                'tess_eval': GL_TESS_EVALUATION_SHADER,
                'geometry': GL_GEOMETRY_SHADER,
                'fragment': GL_FRAGMENT_SHADER,
            }
        shaders = []
        for key, filename in kwargs.items():
            shaders.append(load_shader(known_types[key], filename))
        self.program = link(shaders)

    def set_uniform_mat(self, key, value):
        var = glGetUniformLocation(self.program, key)
        glUniformMatrix4fv(var, 1, GL_FALSE, value.flatten())

    def set_uniform_vec(self, key, value):
        var = glGetUniformLocation(self.program, key)
        glUniform4fv(var, 1, value.flatten())

    def set_uniform_int(self, key, value):
        var = glGetUniformLocation(self.program, key)
        glUniform1i(var, value)

    def get(self):
        return self.program
