"""workshop 10"""
from pyplasm import *
import numpy as np
import sys, os

"""elenco di texture che verranno usate"""

woodTexture = "texture/wood.png"
wallTexture = "texture/wall1.jpg"
stoneTexture = "texture/stone.jpg"
metalTexture = "texture/metal.jpg"
glassTexture = "texture/glass.jpg"
roofTexture = "texture/roof.jpg"

"""struttura iniziale vuota che viene usata per costruire ogni pezzo"""

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
levelHeight = [60.0,60.0,40.0,60.0,60.0,40.0]

"""funzione che conta quanti file ha una directory"""

def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith('.'):
        i = i + 1
  return i

""" funzione che legge il file svg"""

def readSvg(l,level,path):
  file = open("elements/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = countFileDirectory("elements/"+path+"/lines/")
  file.close()
  d = data.splitlines()
  level = level + [d]
  if l!=n-1:
    return readSvg(l+1,level,path)
  else:
    return level

"""generazione dei livelli
base      --> perimetro della casa
external  --> livello che contiene le pareti esterne, con i fori per porte e finestre
internal  --> contiene i muri della casa con i fori per le porte
doors     --> contiene le porte, da inserire nei fori dei muri
windows   --> contiene le finestre da inserire nei fori del muro
stair    --> contiene il rettangolo che conterra' la scala
"""

baseLevel = readSvg(0,[],"base")
externalLevel = readSvg(0,[],"external")
internalLevel = readSvg(0,[],"internal")
doorsLevel = readSvg(0,[],"doors")
windowsLevel = readSvg(0,[],"windows")
stairLevel = readSvg(0,[],"stair")

"""funzione che converte i punti di un file .lines in un array"""

def convertLines(l,i, params):
  stringLine = params[l][i]
  splitLine = stringLine.split(",")
  arrayLine = np.array(splitLine, dtype=float)
  return arrayLine

"""funzione che costruisce il piano terra a partire dal file della cartella base"""

def buildFirstFloor(i,structure):
  if i < len(baseLevel[0]):
    params = convertLines(0,i,baseLevel)
    pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    offset = OFFSET([4.0, 0.0, 2.0])(pol)
    struct = STRUCT([offset, structure])
    return buildFirstFloor(i+1,struct)
  else:
    structure = SOLIDIFY(SKEL_2(structure))
    structure = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(structure)
    return structure

""" funzione che costruisce le pareti esterne a partire dai file della cartella external
    al livello terreno viene posta una copertura in pietra e sopra una texture del muro esterno
"""

def buildExternal(l,i,h,structure):
  if l <= len(externalLevel)-1:
    if i < len(externalLevel[l]):
      params = convertLines(l,i,externalLevel)
      pol = MKPOL([[[params[0],params[1],0.0],[params[0],params[3],0.0],[params[2],params[1],0.0],[params[2],params[3],0.0]],[[1,2,3,4]],[1]])
      offset = OFFSET([3.0, 3.0, levelHeight[l]])(pol)
      if l==0:
        texture = TEXTURE([stoneTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(offset)
      else:
        if l==3:
          texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 7, 1])(offset)
        else:
          texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(offset)
      translated = STRUCT([T(3)(h), texture])
      struct = STRUCT([translated, structure])
      return buildExternal(l,i+1,h,struct)
    else:
      h = h + levelHeight[l]
      return buildExternal(l+1,0,h,structure)
  else:
    return structure

"""funzione che crea i muri interni di tutti e due i piani e i fori per le porte 
le prende dal file della cartella internal"""

def buildIntenal(l,i,h,structure):
  if l <= len(internalLevel)-1:
    if i < len(internalLevel[l]):
      params = convertLines(l,i,internalLevel)
      pol = MKPOL([[[params[0],params[1],0.0],[params[0],params[3],0.0],[params[2],params[1],0.0],[params[2],params[3],0.0]],[[1,2,3,4]],[1]])
      offset = OFFSET([1.0, 1.0, levelHeight[l]])(pol)
      texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(offset)
      translated = STRUCT([T(3)(h), texture])
      struct = STRUCT([translated, structure])
      return buildIntenal(l,i+1,h,struct)
    else:
      h = h + levelHeight[l]
      return buildIntenal(l+1,0,h,structure)
  else:
    return structure

"""funzione che costruisce una porta in legno"""

def buildOneDoor(elem, j, h, door):
  if j < 14:
    build = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    buildOffset = OFFSET([3.5, 3.5, 8.5])(build)
    buildTexture = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
    buildTras = STRUCT([T([3])([h]), buildTexture])
    h = h + 8.5
    door = STRUCT([buildTras,door])
    return buildOneDoor(elem, j+1, h, door)
  else:
    return door

"""funzione che costruisce una manglia e la inserise a meta' altezza della porta"""

def createHandle(elem,structure):
  handle = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
  handle0 = OFFSET([8.0, 1.0, 1.0])(handle)
  if (elem[0]-elem[2]<1.0) & (elem[0]-elem[2]>-1.0):
    handle_0 = STRUCT([T([1,2,3])([-2.0,1.0,62.0]), handle0])
    handle_1 = STRUCT([T([1,2,3])([-2.0,3.0,62.0]), handle0])
    handle1 = OFFSET([1.0, 1.5, 1.0])(handle)
    handle_2 = STRUCT([T([1,2,3])([5.0,1.0,62.0]), handle1])
    handle_3 = STRUCT([T([1,2,3])([5.0,6.0,62.0]), handle1])
    handle_01 = DIFF([handle_0,handle_1])
    handle_23 = DIFF([handle_2,handle_3])
    handle_23_2 = STRUCT([T([1])([-8.0]), handle_23])
  else:
    handle = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    handle0 = OFFSET([1.0, 8.0, 1.0])(handle)
    handle_0 = STRUCT([T([1,2,3])([1.0,-2.0,62.0]), handle0])
    handle_1 = STRUCT([T([1,2,3])([3.0,-2.0,62.0]), handle0])
    handle1 = OFFSET([1.0, 1.5, 1.0])(handle)
    handle_2 = STRUCT([T([1,2,3])([1.0,5.0,62.0]), handle1])
    handle_3 = STRUCT([T([1,2,3])([6.0,5.0,62.0]), handle1])
    handle_01 = DIFF([handle_0,handle_1])
    handle_23 = DIFF([handle_2,handle_3])
    handle_23_2 = STRUCT([T([2])([-8.0]), handle_23])
  handle_all = STRUCT([handle_01,handle_23,handle_23_2])
  handle_all = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(handle_all)
  structure = STRUCT([structure,handle_all])
  return structure

""" funzione che grazie alla funzione che costruisce una porta e al file della cartella doors costruisce
    tutte le porte di entrambi i piani"""

def buildAllDoors(l,i,h,structure):
  if l <= len(doorsLevel)-1:
    if i < len(doorsLevel[l]):
      params = convertLines(l,i,doorsLevel)
      d = buildOneDoor(params, 0, h, initStruct)
      hand = createHandle(params,initStruct)
      hand = STRUCT([T([3])([h]), hand])
      finalStruct = STRUCT([d, structure, hand])
      return buildAllDoors(l,i+1,h,finalStruct)
    else:
      h = h + 160.0
      return buildAllDoors(l+1,0,h,structure)
  else:
    return structure

""" funzione che costruisce una finestra di vetro trasparente con una cornice di legno"""

def buildOneWindow(params,h):
  q1 = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0]],[[1,2]],[1]])
  q1 = OFFSET([3.5, 3.5, 50.0])(q1)
  q1 = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q1)
  q1 = MATERIAL([0,1.36,2.55,0.5,  0,1,0,0.5, 0,0,1,0, 0,0,0,0.5, 100])(q1)
  if (params[0]-params[2]<1.0) & (params[0]-params[2]>-1.0):
    if params[1]<params[3]:
      q2 = MKPOL([[[params[0],params[1]-2.0,0.0],[params[2],params[3]+2.0,0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 60.0])(q2)
    else:
      q2 = MKPOL([[[params[0],params[1]+2.0,0.0],[params[2],params[3]-2.0,0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 60.0])(q2)
  if (params[1]-params[3]<1.0) & (params[1]-params[3]>-1.0):
    if params[0]<params[2]:
      q2 = MKPOL([[[params[0]-2.0,params[1],0.0],[params[2]+2.0,params[3],0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 60.0])(q2)
    else:
      q2 = MKPOL([[[params[0]+2.0,params[1],0.0],[params[2]-2.0,params[3],0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 60.0])(q2)
  q2 = STRUCT([T(3)(-3.5), q2])
  q2 = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q2)
  q = DIFFERENCE([q2,q1])
  q = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q)
  allWindow = STRUCT([q,q1])
  allWindow = STRUCT([T(3)(h), allWindow])
  return allWindow

"""funzione che crea tutte le funestre usando la funzione precedente e i file della cartella windows"""

def buildAllWindows(l,i,h,structure):
  if l <= len(windowsLevel)-1:
    if i < len(windowsLevel[l]):
      params = convertLines(l,i,windowsLevel)
      w = buildOneWindow(params,h)
      finalStruct = STRUCT([w, structure])
      return buildAllWindows(l,i+1,h,finalStruct)
    else:
      h = h + 160.0
      return buildAllWindows(l+1,0,h,structure)
  else:
    return structure

""" funzione che costruisce il tetto
    viene creata la prima meta' del tetto e poi ribaltata per creare la seconda parte
"""

def buildRoof(i,structure):
  params = convertLines(0,i,baseLevel)
  if i==0:
    triangle = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0],[(params[2]+params[0])/2,(params[3]+params[1])/2,60.0]],[[1,2,3]],[1]])
    frame = MKPOL([[[params[0],params[1]],[(params[2]+params[0])/2-60.0,(params[3]+params[1])/2]],[[1,2]],[1]])
    triangle = OFFSET([-3.0, 0.0, 0.0])(triangle)
  else:
    triangle = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0],[(params[2]+params[0])/2,(params[3]+params[1])/2,60.0]],[[1,2,3]],[1]])
    frame = MKPOL([[[params[0],params[1]],[(params[2]+params[0])/2-60.0,(params[3]+params[1])/2]],[[1,2]],[1]])
    triangle = OFFSET([3.0, 0.0, 0.0])(triangle)
  triangle = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(triangle)
  height = baseLevel[0][3]
  heightSplit = height.split(",")
  heightNumber = np.array(heightSplit, dtype=float)
  height = heightNumber[2] - heightNumber[0]
  roof = STRUCT([T([1,3])([heightNumber[0]-8,params[0]-1]),(ROTATE([1,3])(-PI/2)(PROD([frame,Q(height+10)])))])
  roof = OFFSET([3.0, 3.0, 3.0])(roof)
  roof = TEXTURE([roofTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(roof)
  struct = STRUCT([triangle, structure])
  struct = STRUCT([roof, struct])
  return struct

def buildSecondFloor(i,base,structure):
  if i < len(stairLevel[0]):
    params = convertLines(0,i,stairLevel)
    pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    offset = OFFSET([4.0, 5.5, 2.0])(pol)
    s2 = STRUCT([offset, structure])
    return buildSecondFloor(i+1,base,s2)
  else:
    structure = SOLIDIFY(SKEL_2(structure))
    structure = DIFF([base,structure])
    structure = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(structure)
    return structure

"""funzione che crea le scale a partire dal file nella cartella stairs"""

def buildStairs(tempLength,tempHeight,structure):
  params = convertLines(0,3,stairLevel)
  params2 = convertLines(0,0,stairLevel)
  height = 160.0
  stepHeight = 10.44
  steps=height/stepHeight
  steps=height/steps
  stepLength = 22.5
  length = (params2[2]-params2[0])
  build = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
  buildOffset = OFFSET([5.0, stepLength, stepHeight])(build)
  traslation=STRUCT([T([1,2,3])([0.5,tempLength+stepLength,tempHeight]),buildOffset])
  tempLength=tempLength + stepLength/2
  tempHeight=tempHeight + stepHeight
  structure=STRUCT([traslation,structure])
  if tempHeight < height:
    return buildStairs(tempLength, tempHeight, structure)
  else:
    structure = TEXTURE([woodTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(structure)
    structure=STRUCT([traslation,structure])
    return structure

"""funzione finale che assembla i risultati di tutte le funzioni precedenti"""

def buildHouse():
  firstFloor = buildFirstFloor(0,initStruct)
  secondFloor = buildSecondFloor(0,firstFloor,initStruct)
  external = buildExternal(0,0,0.0,initStruct)
  internal = buildIntenal(0,0,0.0,initStruct)
  doors = buildAllDoors(0,0,0.0,initStruct)
  windows = buildAllWindows(0,0,30.0,initStruct)
  halfRoof = buildRoof(0,initStruct)
  roof_level_2 = buildRoof(2,initStruct)
  stairs_level = buildStairs(0.0,0.0,initStruct)
  house=STRUCT([firstFloor,T(3)(3.0),external])
  house=STRUCT([house,T(3)(3.5),stairs_level])
  house=STRUCT([house,T(3)(3.5),internal])
  house=STRUCT([house,T(3)(163.0),secondFloor])
  house=STRUCT([house,T(3)(323.0),firstFloor])
  house=STRUCT([house,T(3)(3.0),doors])
  house=STRUCT([house,T(3)(37.0),windows])
  house=STRUCT([house,T(3)(325.0),halfRoof])
  house=STRUCT([house,T(3)(325.0),roof_level_2])
  VIEW(house)

buildHouse()