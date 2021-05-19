# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:24:18 2020

@author: LAURI
"""


import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
import math


nb_vert_infos_size=6


class Window:
    def __init__(self,width,height,title):
        self.Window=None

        if not glfw.init():
            return

        self.Window = glfw.create_window(width, height, title, None, None)

        if not self.Window:
            glfw.terminate()
            return

        glfw.make_context_current(self.Window)

        self.updateProjectionMatrix(width,height)


    def updateProjectionMatrix(self,width,height):
        fov = 60
        aspect_ratio = width / height
        near_clip = 0.1
        far_clip = 100

        #create a perspective matrix
        self.ProjectionMatrix = pyrr.matrix44.create_perspective_projection(
                fov,
                aspect_ratio,
                near_clip,
                far_clip
                )

        glViewport(0, 0, width, height)


    def initViewMatrix(self,eye=[0,0,2]):
        eye=np.array(eye)
        target=np.array([0,0,0])
        up=np.array([0,1,0])
        self.ViewMatrix = pyrr.matrix44.create_look_at(eye,target,up)


    def render(self,objects):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        v=self.ViewMatrix
        p=self.ProjectionMatrix
        vp=np.matmul(v,p)

        while not glfw.window_should_close(self.Window):
            glfw.poll_events()
     
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            w, h = glfw.get_framebuffer_size(self.Window)
            self.updateProjectionMatrix(w,h)

            for o in objects:
                o.updateTRSMatrices()
                o.updateModelMatrix()
                mvp=np.matmul(o.ModelMatrix,vp)
                o.Shader.draw(mvp)

            glfw.swap_buffers(self.Window)

        self.CloseWindow()


    def CloseWindow(self):
        glfw.terminate()


class Object3D:
    def __init__(self):
        self.translate((0,0,0))
        self.scale((1,1,1))
        self.R=pyrr.matrix44.create_identity()

    def translate(self,vec):
        self.T = pyrr.matrix44.create_from_translation(vec)
        
    def scale(self,fac):
        self.S = pyrr.matrix44.create_from_scale(fac)

    def updateModelMatrix(self):
        self.ModelMatrix=np.matmul(np.matmul(self.S,self.R),self.T)

    def updateTRSMatrices(self):
        pass


def CreateShader(name):
    vs_file=open(name+'.vs.txt','r')
    VERTEX_SHADER = vs_file.read()
    vs_file.close()

    fs_file=open(name+'.fs.txt','r')
    FRAGMENT_SHADER = fs_file.read()
    fs_file.close()

    # Compile The Program and shaders
    return OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                            OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))


class PositionShader:
    def __init__(self,vertices,primitives,color=(1.0,1.0,1.0)):
        self.Vertices=vertices
        self.Primitives=primitives
        self.Shader=CreateShader('position')
        self.Color=color
        self.createBuffers()

    def createBuffers(self):
        vertices=np.array(self.Vertices, dtype=np.float32)

        self.NbVertices=int(len(vertices)/nb_vert_infos_size)

        # Create Buffer object in gpu
        self.VBO = glGenBuffers(1)
        # Bind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.NbVertices*nb_vert_infos_size*4, vertices, GL_STATIC_DRAW)

    def use(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        positionLoc = glGetAttribLocation(self.Shader, 'position')
        glVertexAttribPointer(positionLoc, 3, GL_FLOAT, GL_FALSE, 3*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(positionLoc)
     
        glUseProgram(self.Shader)

    def draw(self,mvp):
        self.use()
        transformLoc = glGetUniformLocation(self.Shader, "mvp")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, mvp)
        colorLoc = glGetUniformLocation(self.Shader, "Color")
        glUniform3fv(colorLoc, 1, self.Color)
        for p in self.Primitives:
            nb_indices=len(p[1])
            glDrawElements(p[0], nb_indices, GL_UNSIGNED_INT, p[1])


class ColorPositionShader:
    def __init__(self,vertices,primitives):
        self.Vertices=vertices
        self.Primitives=primitives
        self.Shader=CreateShader('default')
        self.createBuffers()

    def createBuffers(self):
        vertices=np.array(self.Vertices, dtype=np.float32)

        self.NbVertices=int(len(vertices)/nb_vert_infos_size)

        # Create Buffer object in gpu
        self.VBO = glGenBuffers(1)
        # Bind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.NbVertices*nb_vert_infos_size*4, vertices, GL_STATIC_DRAW)

    def use(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        position = glGetAttribLocation(self.Shader, 'position')
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, nb_vert_infos_size*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(self.Shader, 'color')
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, nb_vert_infos_size*4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)
     
        glUseProgram(self.Shader)

    def draw(self,mvp):
        self.use()
        transformLoc = glGetUniformLocation(self.Shader, "mvp")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, mvp)
        for p in self.Primitives:
            nb_indices=len(p[1])
            glDrawElements(p[0], nb_indices, GL_UNSIGNED_INT, p[1])


def addVertex(tab,p,c):
    tab.extend(p)
    tab.extend(c)
