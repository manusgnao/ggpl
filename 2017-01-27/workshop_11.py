""" workshop 11 """
from pyplasm import *
import numpy as np
import sys, os

sys.path.append("house")
import house

#sys.setrecursionlimit(1500)

grassTexture = "texture/grass4.jpg"
asphaltTexture = "texture/asphalt.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]
"""funzione che conta quanti file ci sono in una cartella"""
def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith("."):
        i = i + 1
  return i
"""funzione che legge il contenuto del file lines ottenuto da un file SVG"""
def readSvg(l,reading_level,path):
  file = open("elements/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = countFileDirectory("elements/"+path+"/lines/")
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l!=n-1:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelStreet = readSvg(0,[],"street")
levelHouse = readSvg(0,[],"house")

"""funzione che legge le linee di un file lines"""
def parseLines(l,i, params):
  string_line = params[l][i]
  split_line = string_line.split(",")
  array_line = np.array(split_line, dtype=float)
  return array_line
"""funzione che crea il piano contenente il prato su cui verranno costruite strade e case"""
def createGarden(i,s1):
  if i < len(levelBase[0]):
    params = parseLines(0,i,levelBase)
    a_pol = MKPOL([[[params[0],params[1],0.0],[params[1],params[2],0.0],[params[2],params[3],0.0],[params[3],params[0],0.0]],[[1,2,3,4]],[1]])
    s2 = STRUCT([a_pol, s1])
    return createGarden(i+1,s2)
  else:
    s1 = TEXTURE([grassTexture, TRUE, FALSE, 1, 1, 0, 3, 1])(s1)
    return s1
"""funzione che costruisce le strade a partire da 3 svg"""
def buildStreet(l,i,s1):
	if l <= len(levelStreet)-1:
		if i < len(levelStreet[l]):
			params = parseLines(l,i,levelStreet)
			a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
			a_off = OFFSET([0.0, 0.0, 0.0])(a_pol)
			s2 = STRUCT([a_off, s1])
			return buildStreet(l,i+1,s2)
		else:
			s1 = SOLIDIFY(SKEL_2(s1))
			s1=STRUCT([T(3)(5.0),s1])
			s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 10, 10])(s1)
			return buildStreet(l+1,0,s1)
	else:
		return s1
"""funzione che costruisce una casa in corrispondenza del perimetro a essa assegnato"""
def buildHouse(i,s1):
  if i < len(levelHouse[0]):
    params = parseLines(0,i,levelHouse)
    h2 = house.createMoreHouse(0,initStruct,0.0)
    
    if(i==3 or i==7):
      h2 = ROTATE([1,2])(PI/2)(h2)
      h2 = STRUCT([T([1,2,3])([params[0]+940.00,params[1]+3150.0,2.0]),h2])

    else:
      h2 = ROTATE([1,2])(-PI/2)(h2)
      h2 = STRUCT([T([1,2,3])([params[0]-290.00,params[1]+3910.0,2.0]),h2])

    s1 = STRUCT([h2, s1])
    return buildHouse(i+4,s1)
  else:
    return s1


"""funzione che costruisce un isolato di un quartiere utilizzando le funzioni precedentemente illustrate"""
def buildBlock():
  garden_level = createGarden(0,initStruct)
  street_level = buildStreet(0,0,initStruct)
  house_level2 = buildHouse(3,initStruct)
  house=STRUCT([initStruct,T(3)(0.0),garden_level])
  house=STRUCT([house,T(3)(2.0),street_level])
  house=STRUCT([house,T(3)(2.0),house_level2])
  return house

"""funzione che costruisce un quartiere residenziale richiamando la funzione che costruisce isolati"""
def suburban_neighborhood(i,s1,d):
  if i < 3:
    h1 = buildBlock()
    h1=STRUCT([T(1)(d),h1])
    s1= STRUCT([h1, s1])
    return suburban_neighborhood(i+1,s1,d+3600.0)
  else:
    VIEW(s1)

suburban_neighborhood(0,initStruct,0.0)


