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
        
        unit=taille_cube
        
        vertices = [
            0.0,0.0,0.0,
            unit,0.0,0.0,
            unit,0.0,unit,
            0.0,0.0,unit,
            0.0,unit,0.0,
            0.0,unit,unit,
            unit,unit,0.0,
            unit,unit,unit
            ]
                                    #Phase de ...
        tab_indices = [0,1,4,4,6,1, #devant
                       0,4,5,0,5,3, #gauche
                       4,5,6,5,7,6, #dessus
                       0,3,2,0,2,1, #dessous
                       6,7,1,7,1,2, #droite
                       5,7,2,5,2,3  #derriere
                       ]
        
        primitives = [(GL_TRIANGLES,tab_indices)]
        
        self.Shader=PositionShader(
            vertices, primitives,color=(1.0,1.0,1.0)
            )
    
    def updateTRSMatrices(self):
        time=glfw.get_time()
        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * time)
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * time)

        self.R=np.matmul(rot_x,rot_y)
        
def main():
    
    #Taille et titre de la fenetre
    window=Window(1024,768,"Projet - Eponge de Menger")

    if not window.Window:
        return
    
    #Angle de vue (angle de la "caméra") (x,y,z)
    window.initViewMatrix(eye=[0,0,20])
    
    
    cube=Cube(3) #Appel de la fonction de création de l'objet
    #cube.scale((3.0,3.0,3.0)) #Modification de la taille de l'objet
    #cube.translate((-8,0,0)) #Modification de l'emplacement
                                       #de l'objet dans la fenetre
    
    #Liste d'objet qu'on veut afficher
    objects=[cube]
    #Rendu visuel de la liste d'objet
    window.render(objects)

if __name__ == "__main__":
    main()