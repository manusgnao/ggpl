""" workshop 08 """

from pyplasm import *
import numpy as np

""" texture del muro esterno """
wallTexture = "/texture/wall.jpg"

""" struttura vuota da cui iniziare """
init = CUBOID([.0,.0,.0])
initStruct = STRUCT([init])

""" da file level-X.lines estraggo i punti """
def readFromLineFile(l):
	file = open("lines/level-"+str(l)+".lines","r")
	data = file.read()
	file.close()
	return data.splitlines()

""" perimetro dell'edificio """
level1 = readFromLineFile(1)
""" piantina dell'edificio con porte """
level2 = readFromLineFile(2)
""" piantina dell'edificio con porte e finestre"""
level3 = readFromLineFile(3)
""" piantina dell'edificio con porte chiuse per stipiti delle porte """
level4 = readFromLineFile(4)

""" array da scorrere per costruire un piano sull'altro"""
levels = [level1,level2,level3,level4,level1]

""" altezza di ogni piano """
heights = [0.0,30.0,30.0,20.0,0.0]		

""" leggo i punti e costruisco i livelli dell'edificio """
def buildHome(l,i,h,building):
	""" ciclo i livelli """
	if l <= len(levels)-1:
		"""ciclo i punti di ongni muro di un piano"""
		if i < len(levels[l])-1:
			"""prendo i punti di un muro"""
			coords = levels[l][i]
			"""li inserisco in un array"""
			arrayCoords = coords.split(",")
			"""trasformo ogni elemento dell'array da string a float"""
			elem = np.array(arrayCoords, dtype=float)
			""" creo il muro(1D) unendo i punti estratti dal lines nella sua posizione
			elem[0] --> x1
			elem[1] --> y1
			elem[2] --> x2
			elem[3] --> y2
			[elem[0],elem[1]] --> x1,y1
			[elem[0],elem[3]] --> x1,y2
			[elem[2],elem[1]] --> x2,y1
			[elem[2],elem[3]] --> x2,y1
			"""
			build = MKPOL([[[elem[0],elem[1],0.0],[elem[0],elem[3],0.0],[elem[2],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2,3,4]],[1]])
			"""do al muro l'altezza riferita al piano che sto creando"""
			buildOffset = OFFSET([1.5, 1.5, heights[l]])(build)
			"""applico la texture al muro"""
			buildTexture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
			"""traslo il piano per farlo posizionare sopra il piano precedente tramite h"""
			buildTraslated = STRUCT([T(3)(h), buildTexture])
			finalStruct = STRUCT([buildTraslated, building])
			"""rieseguo la funzione per creare un nuovo muro"""
			return buildHome(l,i+1,h,finalStruct)
		else:
			"""calcolo l'altezza complessiva per posizionare il nuovo piano"""
			h = h + heights[l]
			"""rieseguo la funzione per creare un nuovo piano"""
			return buildHome(l+1,0,h,building)
	else:
		VIEW(building)

buildHome(0,0,0.0,initStruct)