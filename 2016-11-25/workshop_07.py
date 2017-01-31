""" workshop 07 """

from pyplasm import *
""" xArray e' l'array corrispondende all'asse x
 	 yArray e' l'array corrispondende all'asse yArray
 	 occupancy e' l'array di array che stabilisce quale celle sono di vetro e quali di legno """
#window1
#xArray = [0.0,0.1,0.5,0.6,1.0,1.1]
#yArray = [0.0,0.1,1.0,1.1,1.3,1.4]
#occupancy = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1]]
glassTexture = "texture/glass.jpg"
woodTexture = "texture/wood.png"
wood1Texture = "texture/wood1.jpg"
#window2
#xArray = [0.0,0.1,0.5,0.6,1.0,1.1]
#yArray = [0.0,0.1,0.6,0.7,1.2,1.3]
#occupancy = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

#puerta
#xArray = [0.0,0.2,0.5,0.7]
#yArray = [0.0,0.2,0.4,0.5,1.6,1.8]
#occupancy = [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]]

#porta
xArray = [0.0,0.2,0.4,0.6,0.8,1.0]
yArray = [0.0,0.2,0.8,1.0,1.6,1.8]
occupancy = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

""" struttura iniziale"""
zero = QUOTE([.0,.0])
initStruct = STRUCT([zero])
""" funzione che crea la finestra: i vetri sono blu i legni sono bianchi """
def window(i, j, partStruct):
	if j != len(yArray)-1:
		if  i != len(xArray)-1:
			if occupancy[j][i]==0:
				x = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
  				x = MATERIAL([0,1.36,2.55,0.5,  0,1,0,0.5, 0,0,1,0, 0,0,0,0.5, 100])(x)
  
				#x = COLOR(BLUE)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
				struct = STRUCT([T([1,2,3])([xArray[i],yArray[j],0.1/3]), x])
			else:
				#x = COLOR(WHITE)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))
				x = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))

				struct = STRUCT([T([1,2])([xArray[i],yArray[j]]), x])
			partStruct = STRUCT([partStruct,struct])
			return window(i+1, j, partStruct)
		else:
			return window(0, j+1, partStruct)
	else:
		VIEW(partStruct)

""" funzione che crea la porta """

def door(i, j, partStruct):
	if j != len(yArray)-1:
		if  i != len(xArray)-1:
			if occupancy[j][i]==0:
				#x = TEXTURE([wood1Texture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
				x = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
  				x = MATERIAL([0,1.36,2.55,0.5,  0,1,0,0.5, 0,0,1,0, 0,0,0,0.5, 100])(x)
  
				#x = COLOR(WHITE)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
				struct = STRUCT([T([1,2,3])([xArray[i],yArray[j],0.1/3]), x])
			else:
				x = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))

				#x = COLOR(BROWN)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))
				struct = STRUCT([T([1,2])([xArray[i],yArray[j]]), x])
			partStruct = STRUCT([partStruct,struct])
			return door(i+1, j, partStruct)
		else:
			return door(0, j+1, partStruct)
	else:
		VIEW(partStruct)


#window(0, 0, initStruct)
door(0, 0, initStruct)