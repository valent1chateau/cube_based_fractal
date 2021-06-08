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
from camera import Camera

nb_vert_infos_size=6
cam = Camera()
first_mouse = True
lastX, lastY = 400, 300
left, right, forward, backward = False, False, False, False

class Window:
    def __init__(self,width,height,title):
        self.Window=None

        if not glfw.init():
            return

        self.Window = glfw.create_window(width, height, title, None, None)

        if not self.Window:
            glfw.terminate()
            return

        def key_input_clb(self, key, scancode, action, mode):
            global left, right, forward, backward
            if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
                glfw.set_window_should_close(self, True)
        
            if key == glfw.KEY_W and action == glfw.PRESS:
                forward = True
            elif key == glfw.KEY_W and action == glfw.RELEASE:
                forward = False
            if key == glfw.KEY_S and action == glfw.PRESS:
                backward = True
            elif key == glfw.KEY_S and action == glfw.RELEASE:
                backward = False
            if key == glfw.KEY_A and action == glfw.PRESS:
                left = True
            elif key == glfw.KEY_A and action == glfw.RELEASE:
                left = False
            if key == glfw.KEY_D and action == glfw.PRESS:
                right = True
            elif key == glfw.KEY_D and action == glfw.RELEASE:
                right = False
            if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
                left, right, forward, backward = False, False, False, False


        def mouse_enter_clb(self,entered):
            global first_mouse
    
            if entered:
                first_mouse = False
            else:
                first_mouse = True
        
        def mouse_look_clb(self,xpos,ypos):
            global lastX, lastY
            if first_mouse:
                lastX = xpos
                lastY = ypos
            xoffset = xpos - lastX
            yoffset = lastY - ypos
            lastX = xpos
            lastY = ypos
            cam.process_mouse_movement(xoffset, yoffset)

          
        glfw.set_window_pos(self.Window, 200, 200) 
        glfw.set_cursor_pos_callback(self.Window, mouse_look_clb)
        glfw.set_cursor_enter_callback(self.Window, mouse_enter_clb)
        glfw.set_key_callback(self.Window, key_input_clb)
        
        glfw.make_context_current(self.Window)
        self.updateProjectionMatrix(width,height)
       

    def do_movement(self):
        if left:
            cam.process_keyboard("LEFT", 0.05)
        if right:
            cam.process_keyboard("RIGHT", 0.05)
        if forward:
            cam.process_keyboard("FORWARD", 0.05)
        if backward:
            cam.process_keyboard("BACKWARD", 0.05)  

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

    
    def initViewMatrix(self):
        self.ViewMatrix = cam.get_view_matrix()
        

    def render(self,objects):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        while not glfw.window_should_close(self.Window):
            v=self.ViewMatrix
            p=self.ProjectionMatrix
            vp=np.matmul(v,p)
            glfw.poll_events()
            self.do_movement()
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            w, h = glfw.get_framebuffer_size(self.Window)
            self.updateProjectionMatrix(w,h)
            self.initViewMatrix()
            
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
