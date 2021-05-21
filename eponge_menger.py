# -*- coding: utf-8 -*-
"""
Created on Wed May 19 05:23:37 2021

@author: Antoine-fusee
"""

from opengl_fcts import *
from math import *


class Cube(Object3D):
    def __init__(self,taille_cube,x,y,z):
        super().__init__()
        
        t_c=taille_cube
        
        """
        vertices = [
            x,y,z,
            x+t_c,y,z,
            x+t_c,y+t_c,z,
            x,y+t_c,z,
            x,y,z+t_c,
            x+t_c,y,z+t_c,
            x+t_c,y+t_c,z+t_c,
            x,y+t_c,z+t_c
            ]

                                   #Phase de ...
        tab_indices = [0,2,1,0,2,3, #derrière
                       0,7,3,0,7,4, #gauche
                       1,6,2,1,6,5, #droite
                       0,5,1,0,5,4, #dessus
                       3,6,2,3,6,7, #dessous
                       4,6,7,4,6,5  #avant
                       ]
        """
        #Gestion des couleurs
        
        p0=(x,y,z) 
        p1=(x+t_c,y,z)
        p2=(x+t_c,y+t_c,z)
        p3=(x,y+t_c,z)
        p4=(x,y,z+t_c)
        p5=(x+t_c,y,z+t_c)
        p6=(x+t_c,y+t_c,z+t_c)
        p7=(x,y+t_c,z+t_c)
       
        vertices = []
        
        red=(2*t_c,0.0,0.0)
        blue=(0.0,0.0,2*t_c)
        green=(0.0,2*t_c,0.0)
        
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
        
        addVertex(vertices,p0,green)
        addVertex(vertices,p1,green)
        addVertex(vertices,p2,green)
        addVertex(vertices,p3,green)
        addVertex(vertices,p4,green)
        addVertex(vertices,p5,green)
        addVertex(vertices,p6,green)
        addVertex(vertices,p7,green)
        
        
        tab_indices = [0,2,1,0,2,3, #arriere
                       4,6,7,4,6,5  #avant
                      ]
        """
        tab2_indices=[0,5,1,0,5,4, #dessous
                      3,6,2,3,6,7, #dessus
                      ] 
        
        tab3_indices=[1,6,2,1,6,5, #droite
                      0,7,3,0,7,4, #gauche
                      ]
        
        tab1_indices=np.array([0,2,1,0,2,3, #avant
                              4,6,7,4,6,5  #arriere
                              ])
        """
        tab2_indices=np.array([0,5,1,0,5,4, #dessus
                               3,6,2,3,6,7, #dessous
                               ])
        
        tab3_indices=np.array([1,6,2,1,6,5, #droite
                               0,7,3,0,7,4, #gauche
                               ])
        
       
        #tab_indices.extend(tab1_indices+4)
        tab_indices.extend(tab2_indices+4)
        tab_indices.extend(tab3_indices+4)
        
        
        primitives = [(GL_TRIANGLES,tab_indices)]
        
        self.Shader=ColorPositionShader(vertices, primitives)
        #self.Shader=PositionShader(vertices,primitives,color=(1.0,1.0,1.0))
        
    """
    def avant(self,taille_cube,x,y,z):
        (self.x,self.y,self.z).translate((x+t/3,y+t/3,z-t/3))
        return x,y,z

    def arriere(self,x,y,z,t):
        self.x=x+t/3
        self.y=y+t/3
        self.z=z+t
        return x,y,z

    def gauche(self,taille_cube,x,y,z):
        (self.x,self.y,self.z).translate((x-t/3,y+t/3,z+t/3))
        print(x)
        print(y)
        print(z)
        return x,y,z

    def droite(self,x,y,z,t):
        self.x=x+t
        self.y=y+t/3
        self.z=z+t/3
        return x,y,z
    
    def dessous(self,x,y,z,t):
        self.x=x+t/3
        self.y=y-t/3
        self.z=z+t/3
        return x,y,z
    
    def dessus(self,x,y,z,t):
        self.x=x+t/3
        self.y=y+t
        self.z=z+t/3
        return x,y,z
    """
    
    def fractale_eponge_menger_remix(self,taille_cube,m,n,L,x,y,z):
        if m==n:
            return L
        elif m==0:
            cube=Cube(taille_cube,x,y,z)
            L.append(cube)
            Cube(taille_cube,x,y,z).fractale_eponge_menger_remix(taille_cube,m+1,n,L,x,y,z)
        else:
            taille_cube=taille_cube/3
            
            #Avant? OK
            xa=x+taille_cube
            ya=y+taille_cube
            za=z-taille_cube
            cube1=Cube(taille_cube,xa,ya,za)
            L.append(cube1)
            Cube(taille_cube,xa,ya,za).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xa,ya,za)
            
            #Arriere? OK
            xb=x+taille_cube
            yb=y+taille_cube
            zb=z+(3.0*taille_cube)
            cube2=Cube(taille_cube,xb,yb,zb)
            L.append(cube2)
            Cube(taille_cube,xb,yb,zb).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xb,yb,zb)
            
            #Gauche? FAIS BUGUER
            xc=x-taille_cube
            yc=y+taille_cube
            zc=z+taille_cube
            cube3=Cube(taille_cube,xc,yc,zc)
            L.append(cube3)
            Cube(taille_cube,xc,yc,zc).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xc,yc,zc)
            
            #Droite? FAIS BUGUER
            xd=x+(3.0*taille_cube)
            yd=y+taille_cube
            zd=z+taille_cube
            cube4=Cube(taille_cube,xd,yd,zd)
            L.append(cube4)
            Cube(taille_cube,xd,yd,zd).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xd,yd,zd)
            
            #Dessus? FAIS BUGUER
            xe=x+taille_cube
            ye=y+(3.0*taille_cube)
            ze=z+taille_cube
            cube5=Cube(taille_cube,xe,ye,ze)
            L.append(cube5)
            Cube(taille_cube,xe,ye,ze).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xe,ye,ze)
            
            #Dessous? FAIS BUGUER
            xf=x+taille_cube
            yf=y-taille_cube
            zf=z+taille_cube
            cube6=Cube(taille_cube,xf,yf,zf)
            L.append(cube6)
            Cube(taille_cube,xf,yf,zf).fractale_eponge_menger_remix(taille_cube,m+1,n,L,xf,yf,zf)
            
    
    def updateTRSMatrices(self):
        time=glfw.get_time()
        rot_x = pyrr.Matrix44.from_x_rotation(0.6 * time)
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * time) 

        self.R=np.matmul(rot_x,rot_y)
    

def main():
    
    #Taille et titre de la fenetre
    window=Window(1900,1080,"Projet - Eponge de Menger remix")
    if not window.Window:
        return
    
    #Angle de vue (angle de la "caméra") (x,y,z)
    window.initViewMatrix(eye=[0,0,20])
    
    #Parametre
    taille_cube = 8
    nombre_generation = 3
    x=8
    y=0
    z=0
    #Liste d'objet qu'on veut afficher
    objects=[]
    Cube(taille_cube,x,y,z).fractale_eponge_menger_remix(taille_cube,0,nombre_generation+1,objects,x,y,z)

    #Rendu visuel de la liste d'objet
    window.render(objects)
    
if __name__ == "__main__":
    main()