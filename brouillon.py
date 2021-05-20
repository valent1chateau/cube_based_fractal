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