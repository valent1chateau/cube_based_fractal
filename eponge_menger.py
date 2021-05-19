# -*- coding: utf-8 -*-
"""
Created on Wed May 19 05:23:37 2021

@author: Antoine-fusee
"""

from opengl_fcts import *
from math import *


class Cube(Object3D):
    def __init__(self,taille_cube):
        super().__init__()
        
        t_c=taille_cube
        
        
        p0=(0.0,0.0,0.0)
        p1=(t_c,0.0,0.0)
        p2=(t_c,t_c,0.0)
        p3=(0.0,t_c,0.0)
        p4=(0.0,0.0,t_c)
        p5=(t_c,0.0,t_c)
        p6=(t_c,t_c,t_c)
        p7=(0.0,t_c,t_c)
        
        red=(2*t_c,0.0,0.0)
        blue=(0.0,0.0,2*t_c)
            
        vertices = []
        """
        for i in range(8):
            addVertex(vertices,pi,red)
        
        for j in range(8):
            addVertex(vertices, pj, blue)
        """
        """
                                    #Phase de ...
        tab_indices = [0,2,1,0,2,3, #devant
                       0,7,3,0,7,4, #gauche
                       1,6,2,1,6,5, #droite
                       0,5,1,0,5,4, #dessous
                       3,6,2,3,6,7, #dessus
                       4,6,7,4,6,5  #arriere
                       ]
        """
        addVertex(vertices,p0,red)
        addVertex(vertices,p1,red)
        addVertex(vertices,p2,red)
        addVertex(vertices,p3,red)
        addVertex(vertices,p4,red)
        addVertex(vertices,p5,red)
        addVertex(vertices,p6,red)
        addVertex(vertices,p7,red)
        
        addVertex(vertices,p0,blue)
        addVertex(vertices,p1,blue)
        addVertex(vertices,p2,blue)
        addVertex(vertices,p3,blue)
        addVertex(vertices,p4,blue)
        addVertex(vertices,p5,blue)
        addVertex(vertices,p6,blue)
        addVertex(vertices,p7,blue)
        
        tab_indices = [0, 1, 2, 2, 3, 0,
                   4, 5, 6, 6, 7, 4]

        tab2_indices=np.array([4, 5, 1, 1, 0, 4,
                   6, 7, 3, 3, 2, 6,
                   5, 6, 2, 2, 1, 5,
                   7, 4, 0, 0, 3, 7])

        tab_indices.extend(tab2_indices+8)
        
        primitives = [(GL_TRIANGLES,tab_indices)]
        
        self.Shader=ColorPositionShader(vertices, primitives)
    
    
    """def updateTRSMatrices(self):
        time=glfw.get_time()
        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * time)
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * time)

        self.R=np.matmul(rot_x,rot_y)
    """
    



def main():
    
    #Taille et titre de la fenetre
    window=Window(800,600,"Projet - Eponge de Menger")

    if not window.Window:
        return
    
    #Angle de vue (angle de la "caméra") (x,y,z)
    window.initViewMatrix(eye=[15,12,30])
    
    taille_cube = 3
    
    #Liste d'objet qu'on veut afficher
    objects=[]
    for k in range(taille_cube):
        for j in range(taille_cube):
            for i in range(taille_cube):
                #if (i==j or i==k or j==k) and i!=0 and i!=taille_cube-1 and k!=0:
                if ((i!=0 and i !=taille_cube-1) and (i==j or i==k)) or ((j!=0 and j!=taille_cube-1) and j==k):
                    print('cube non dessiné à la position: ',(i,j,k))
                else:
                    cube_i_j_k=Cube(taille_cube)
                    cube_i_j_k.translate((taille_cube*i,taille_cube*j,taille_cube*k))
                    objects.append(cube_i_j_k)

        
    #cube.translate((-8,0,0)) #Modification de l'emplacement
                                       #de l'objet dans la fenetre

    #Rendu visuel de la liste d'objet
    window.render(objects)

if __name__ == "__main__":
    main()