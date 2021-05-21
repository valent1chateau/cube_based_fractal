# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:06:20 2021

@author: Antoine-fusee
"""

"""
#Etape 0
cube=Cube(taille_cube)
objects.append(cube)

#Etape 1
pas=taille_cube/3
for k in range(-1,4,1):
    for j in range(-1,4,1):
        for i in range(-1,4,1):
            if ((k==-1 or k==3) and i==1 and j==1) or ((i==-1 or i==3) and j==1 and k==1) or ((j==-1 or j==3) and i==1 and k==1):
                print('cube dessiné à la position: ',(i,j,k))
                cube_i_j_k=Cube(pas)
                cube_i_j_k.translate((pas*i,pas*j,pas*k))
                objects.append(cube_i_j_k)

#Etape 1 Eponge de Menger
for k in range(taille_cube):
    for j in range(taille_cube):
        for i in range(taille_cube):
            if ((i!=0 and i !=taille_cube-1) and (i==j or i==k)) or ((j!=0 and j!=taille_cube-1) and j==k):
                print('cube non dessiné à la position: ',(i,j,k))
            else:
                cube_i_j_k=Cube(taille_cube)
                cube_i_j_k.translate((taille_cube*i,taille_cube*j,taille_cube*k))
                objects.append(cube_i_j_k)
"""



"""
taille_cube=taille_cube/3
for k in range(-1,4,1):
    for j in range(-1,4,1):
        for i in range(-1,4,1):
            if ((k==-1 or k==3) and i==1 and j==1) or ((i==-1 or i==3) and j==1 and k==1) or ((j==-1 or j==3) and i==1 and k==1):
                print('cube dessiné à la position: ',(i,j,k))
                cube_m_i_j_k=Cube(taille_cube,x,y,z)
                cube_m_i_j_k.translate((taille_cube*i,taille_cube*j,taille_cube*k))
                L.append(cube_m_i_j_k)
Cube(taille_cube,x,y,z).fractale_eponge_menger_remix(taille_cube,m+1,n,L,x,y,z)
"""

#Gestion des couleurs
"""
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

tab2_indices=[0,5,1,0,5,4, #dessous
              3,6,2,3,6,7, #dessus
              ] 

tab3_indices=[1,6,2,1,6,5, #droite
              0,7,3,0,7,4, #gauche
              ]

tab1_indices=np.array([0,2,1,0,2,3, #avant
                      4,6,7,4,6,5  #arriere
                      ])

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
"""