""" WORKSHOP 04 """
from pyplasm import *

depth = 0.2
roofTexture = "texture/roof.jpg"

"""le 3 dimensioni del tetto"""
x = [1.0,7.0,11.0,15.0,21.0]
y = [2.0,7.0,12.0,17.0]
z = [0.0, 5.0]

"""vertici e celle rappresentati sul piano cartesiano"""
verts = [[x[1],y[0],z[0]],[x[2],y[0],z[1]],[x[3],y[0],z[0]],[x[3],y[1],z[0]],[x[4],y[1],z[0]],[x[4],y[2],z[1]],[x[4],y[3],z[0]],[x[0],y[3],z[0]],[x[0],y[2],z[1]],[x[0],y[1],z[0]],[x[1],y[1],z[0]],[x[2],y[2],z[1]],[x[4],y[2],z[0]],[x[0],y[2],z[0]],[x[2],y[2],z[0]],[x[2],y[3],z[0]],[x[2],y[0],z[0]]]
cells = [[8,7,9,6],[9,10,11,12],[12,4,5,6],[12,11,1,2],[12,2,3,4],[10,8],[7,5],[14,9],[13,6],[1,3],[12,15],[12,16],[13,14],[2,17]]

"""replica semplificata del modello da ricreare"""
simpleStruct = MKPOL([verts, cells,[1]])

"""creazione del telaio del tetto"""
structRoof = OFFSET([depth, depth, depth])(SKEL_1(simpleStruct))

"""creazione delle celle che dovranno essere poggiate sull'impalcatura del tetto"""
translatedRoof = STRUCT([T([3])([depth*2])(simpleStruct)])

"""estrazione dei punti che serviranno a coprire precisamente il telaio"""
points = UKPOL(translatedRoof)
newVerts = points[0]
newCells = points[1]

"""copertura del telaio"""
newVerts = [[x[0],y[2],z[1]+depth*2],[x[4],y[3]+depth,z[0]+depth],[x[4],y[2],z[1]+depth*2],[x[0],y[3]+depth,z[0]+depth],[x[0],y[1]-depth,z[0]+depth],[x[2],y[2],z[1]+depth*2],[x[1]-depth,y[1]-depth,z[0]+depth],[x[0],y[2],z[1]+depth*2],[x[4],y[1]-depth,z[0]+depth],[x[2],y[2],z[1]+depth*2],[x[3]+depth,y[1]-depth,z[0]+depth],[x[4],y[2],z[1]+depth*2],[x[2],y[0],z[1]+depth*2],[x[1]-depth,y[1]-depth,z[0]+depth],[x[1]-depth,y[0],z[0]+depth],[x[2],y[2],z[1]+depth*2],[x[2],y[2],z[1]+depth*2],[x[3]+depth,y[0],z[0]+depth],[x[3]+depth,y[1]-depth,z[0]+depth],[x[2],y[0],z[1]+depth*2],[x[0],y[3]+depth,z[0]+depth],[x[0],y[1]-depth,z[0]+depth],[x[4],y[3]+depth,z[0]+depth],[x[4],y[1]-depth,z[0]+depth],[x[0],y[2],z[1]+depth*2],[x[0],y[2],z[0]+depth],[x[4],y[2],z[1]+depth*2],[x[4],y[2],z[0]+depth],[x[3]+depth,y[0],z[0]+depth],[x[1]-depth,y[0],z[0]+depth],[x[2],y[2],z[1]+depth*2],[x[2],y[2],z[0]+depth],[x[2],y[3]+depth,z[0]+depth],[x[2],y[2],z[1]+depth*2],[x[4],y[2],z[0]+depth],[x[0],y[2],z[0]+depth],[x[2],y[0],z[1]+depth*2],[x[2],y[0],z[0]+depth]]

"""creo la copertura adattata al telaio in modo che lo ricopra completamente"""
panel = MKPOL([newVerts, newCells,[1]])
#panel = COLOR(RED)(OFFSET([depth, depth, depth])(SKEL_2(panel)))
panel = TEXTURE([roofTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(OFFSET([depth, depth, depth])(SKEL_2(panel)))

"""creazione del tetto: le celle sono poggiate sopra il telaio"""
roof = STRUCT([structRoof, panel])

VIEW(roof)

