""" workshop 10 """

from pyplasm import *
import numpy as np

""" texture del muro esterno """
wallTexture = "/texture/glass.jpg"
doorTexture = "/texture/wood.jpg"
metalTexture = "texture/metal.jpg"
""" struttura vuota da cui iniziare """
init = CUBOID([.0,.0,.0])
initStruct = STRUCT([init])

def readFromLineFile(l):
	file = open("liness/"+str(l)+".lines","r")
	data = file.read()
	file.close()
	return data.splitlines()

level1 = readFromLineFile("porte1") #livello contenente solo le porte del piano terra
level2 = readFromLineFile("finestre1") #livello contenente solo le finestre del piano terra
level3 = readFromLineFile("porte2") #livello contenente solo le porte del primo piano
level4 = readFromLineFile("finestre2") #livello contenente solo le finestre del primo piano
level0 = readFromLineFile("niente") #livello contenente niente (serve per creare lo spazio tra la finestra e il soffitto)


#levels = [level1,level2,level0,level3,level4,level0]
doorsLevel = [level1,level0,level0,level3,level0,level0] #porte al piano terra, spazio, spazio, porte del primo piano, spazio, spazio
windowsLevel = [level0, level2, level0, level0, level4, level0] #spazio, finestre piano terra, spazio, spazio, finestre primo piano, spazio
heights = [60.0,30.0,30.0,60.0,30.0,30.0] #porta alta 60, finestra alta 30, da finestra a soffitto ancora 30

def buildDoors(l,i,h,building):
	if l <= len(doorsLevel)-1:
		if i < len(doorsLevel[l])-1:
			coords = doorsLevel[l][i]
			arrayCoords = coords.split(",")
			elem = np.array(arrayCoords, dtype=float)
			
			build = MKPOL([[[elem[0],elem[1],0.0],[elem[0],elem[3],0.0],[elem[2],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2,3,4]],[1]])
			buildOffset = OFFSET([1.5, 1.5, heights[l]])(build)
			buildTexture = TEXTURE([doorTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
			buildTraslated = STRUCT([T(3)(h), buildTexture])
			finalStruct = STRUCT([buildTraslated, building])
			#maniglia cuboidale
			handle_1 = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([5,5,5]))
			handle_1 = STRUCT([T([1,2,3])([1.5,1.5,h+30.0]), handle_1])
			handle_tras = STRUCT([handle_1])
			handle_tras = STRUCT([T([1,2,3])([elem[0],elem[1],0.0]), handle_tras])
			finalStruct = STRUCT([finalStruct,handle_tras])
			return buildDoors(l,i+1,h,finalStruct)
		else:
			if heights[l] >= 60: 
				h = h + heights[l] #se e' una porta tiro su di 60
			else:
				h = h + heights[l]/2 #se e' una finestra tiro su di 30
			return buildDoors(l+1,0,h,building)
	else:
		buildWindows(0,0,0.0,building)

def buildWindows(l,i,h,building):
	if l <= len(windowsLevel)-1:
		if i < len(windowsLevel[l])-1:
			coords = windowsLevel[l][i]
			arrayCoords = coords.split(",")
			elem = np.array(arrayCoords, dtype=float)
			build = MKPOL([[[elem[0],elem[1],0.0],[elem[0],elem[3],0.0],[elem[2],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2,3,4]],[1]])
			buildOffset = OFFSET([1.5, 1.5, heights[l]])(build)
			buildTexture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
			buildTraslated = STRUCT([T(3)(h), buildTexture])
			finalStruct = STRUCT([buildTraslated, building])
			return buildWindows(l,i+1,h,finalStruct)
		else:
			if heights[l]<60:
				h = h + heights[l]
			else:
				h = h + heights[l]/2
			return buildWindows(l+1,0,h,building)
	else:
		VIEW(building)

buildDoors(0,0,0.0,initStruct)