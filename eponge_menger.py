# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 15:23:37 2021

@authors: Valentin CASTELLON - Stephane IOVLEFF - Antoine BENIS
"""

from opengl_fcts import *
from math import *
from random import *


class Cube(Object3D):
    # Détails des arguments
    # taille_cube : Taille du cube que l'on souhaite créer
    # x,y,z : Position de ce meme cube dans l'espace
    # couleur : Couleur de ce meme cube
    
    def __init__(self,taille_cube,x,y,z,couleur):
        super().__init__()
        
        t_c=taille_cube
        
        #Ajout des sommets dans l'espace
        vertices = [                # Sommet situé par rapport au cube en position ...
            x,y,z,                  # Top Arriere Gauche
            x+t_c,y,z,              # Top Arriere Droit
            x+t_c,y+t_c,z,          # Bottom Arriere Droit
            x,y+t_c,z,              # Bottom Arriere Gauche
            x,y,z+t_c,              # Top Avant Gauche
            x+t_c,y,z+t_c,          # Top Avant Droit
            x+t_c,y+t_c,z+t_c,      # Bottom Avant Droit
            x,y+t_c,z+t_c           # Bottom Avant Gauche
            ]                       # quand la caméra est situé en position x=0,y=0,z=30
        
                                    # Phase de ...
        tab_indices = [0,2,1,0,2,3, # derrière,
                       0,7,3,0,7,4, # gauche,
                       1,6,2,1,6,5, # droite,
                       0,5,1,0,5,4, # dessus,
                       3,6,2,3,6,7, # dessous,
                       4,6,7,4,6,5  # avant...
                       ]            # quand la caméra est situé en position x=0,y=0,z=30
        
        # Construction du cube à l'aide de la table des vertices
        # de la table des indices et de la primitives graphique
        # openGL : GL_TRIANGLES
        primitives = [(GL_TRIANGLES,tab_indices)]
        self.Shader=PositionShader(vertices,primitives,color=(couleur,couleur,couleur))
        
    # Détails des arguments
    # taille_cube : taille du cube de génération 0 (le plus gros de la structure finale)
    # m : numéro de la génération à construire (m=1 correspondra aux cubes de génération 1)
    # n : nombre total de génération souhaitée
    # L : Liste vide qui va contenir les futurs cubes crées
    # x,y,z : Position du cube de génération 0 (premier cube construit) dans l'espace
    # flag : flag permettant de ne pas constuire de cube derriere une face d'un cube de génération
    #        précédente (exemple : https://imgur.com/a/BfJnfIO )
    
    # Resultat de la fonction :
    # Une liste L contenant l'ensemble des cubes crées
    
    def fractale_eponge_menger_remix(self,taille_cube,m,n,L,x,y,z,flag):
        if m==n:     # Quand on arrive au numéro de la génération souhaité, la fonction s'arrete
                     # Comme la création commence à la génération 0, on souhaite alors crée m-1 générations
                     # La fonction est donc finie
            return L #La fonction renvoit la liste des objets crées
        
        elif m==0:
            # Cas de la premiere génération
            cube=Cube(taille_cube,x,y,z,(m+1.0)/n)  #On constuit le cube de génération 0
            L.append(cube)                          #On l'ajoute à la liste des objets que la fonction renverra
            #On appelle de nouveau la fonction de manière récursive de génération 1 (car m=0 dans cette partie du code)
            Cube(taille_cube,x,y,z,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,x,y,z,0)
        else:
            # Cas de la génération située entre 2 inclus et m-1
            taille_cube=taille_cube/3 # La taille du cube de gén m est trois plus petite que celle de gen m-1
            # On va créer ensuite 5 ou 6 cubes suplémentaires que l'on va ensuite placer dans l'espace
            # On va crée 6 cubes pour la génération 1 car les 6 cubes de la génération 1 seront visible à partir d'un certain angle de vue
            # Cependant, à partir de la génération 2, il faut crée uniquement 5 cubes supplémentaires sur chaque cube crée à la génération précédente
            # cf. "flag" dans la partie "Détails des arguments"
            if flag!=2:
                #Coordonnée du nouveau cube
                xa=x+taille_cube
                ya=y+taille_cube
                za=z-taille_cube
                cube1=Cube(taille_cube,xa,ya,za,(m+1.0)/n)  # On crée le nouveau cube
                L.append(cube1)                             # On l'ajoute à la liste des objets quye la fonction renverra
                #On appelle de nouveau la fonction de manière récursive de génération m+1
                Cube(taille_cube,xa,ya,za,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xa,ya,za,1)
            
            if flag!=1:
                xb=x+taille_cube
                yb=y+taille_cube
                zb=z+(3.0*taille_cube)
                cube2=Cube(taille_cube,xb,yb,zb,(m+1.0)/n)
                L.append(cube2)
                Cube(taille_cube,xb,yb,zb,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xb,yb,zb,2)
            
            if flag!=4:
                #Gauche
                xc=x-taille_cube
                yc=y+taille_cube
                zc=z+taille_cube
                cube3=Cube(taille_cube,xc,yc,zc,(m+1.0)/n)
                L.append(cube3)
                Cube(taille_cube,xc,yc,zc,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xc,yc,zc,3)
            
            if flag!=3:
                #Droite
                xd=x+(3.0*taille_cube)
                yd=y+taille_cube
                zd=z+taille_cube
                cube4=Cube(taille_cube,xd,yd,zd,(m+1.0)/n)
                L.append(cube4)
                Cube(taille_cube,xd,yd,zd,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xd,yd,zd,4)
            
            if flag!=6:
                #Dessus
                xe=x+taille_cube
                ye=y+(3.0*taille_cube)
                ze=z+taille_cube
                cube5=Cube(taille_cube,xe,ye,ze,(m+1.0)/n)
                L.append(cube5)
                Cube(taille_cube,xe,ye,ze,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xe,ye,ze,5)
            
            if flag!=5:
                #Dessous
                xf=x+taille_cube
                yf=y-taille_cube
                zf=z+taille_cube
                cube6=Cube(taille_cube,xf,yf,zf,(m+1.0)/n)
                L.append(cube6)
                Cube(taille_cube,xf,yf,zf,(m+1.0)/n).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xf,yf,zf,6)
            
    """
    #Rotation de l'objet 3D
    def updateTRSMatrices(self):
        time=glfw.get_time()
        rot_x = pyrr.Matrix44.from_x_rotation(0.6 * time)
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * time)
        self.R=np.matmul(rot_x,rot_y)
    """


def main():
    
    #Taille et titre de la fenetre
    window=Window(800,600,"Projet IN55 - Fractale Cube")
    if not window.Window:
        return
    
    #Angle de vue (angle de la "caméra") (x,y,z)
    #x_cam=0
    #y_cam=0
    #z_cam=20
    #window.initViewMatrix(eye=[x_cam,y_cam,z_cam])
    window.initViewMatrix()
    
    #Parametres de la fractale
    taille_cube = 6
    nombre_generation = 3  #Eviter d'aller au dessus de 5
    #Position du cube de génération 0
    x=-3
    y=-3
    z=0
    
    objects=[]
    Cube(taille_cube,x,y,z,(0.0+1.0)/1.0).fractale_eponge_menger_remix(taille_cube,0,nombre_generation+1,objects,x,y,z,0)

    #Rendu visuel de la liste d'objet
    
    window.render(objects)
    
    
if __name__ == "__main__":
    main()