from pyplasm import *
import numpy as np
import sys, os

sys.setrecursionlimit(1500)

pavTexture = "texture/pav2.png"
wallTexture = "texture/wall1.jpg"
wallStone = "texture/wall4.jpg"
doorTexture = "texture/white_wood.jpg"
metalTexture = "texture/metal.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

def readSvg(l,reading_level,path):
  file = open("all/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = len([name for name in os.listdir("all/"+path+"/lines/")])-2
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l<n:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelEst = readSvg(0,[],"esterno")
levelInt = readSvg(0,[],"interno")
levelPorte = readSvg(0,[],"porte")

def createBase(i,s1):
  if i < len(levelBase[0]):
    a = levelBase[0][i]
    a_split = a.split(",")
    a_number = np.array(a_split, dtype=float)
    a_pol = POLYLINE([[a_number[0],a_number[1]],[a_number[2],a_number[3]]])
    a_off = OFFSET([4.0, 0.0, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return createBase(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

def createEst(l,i,h,s1):
  if l <= len(levelEst)-1:
    if i < len(levelEst[l]):
      a = levelEst[l][i]
      a_split = a.split(",")
      a_number = np.array(a_split, dtype=float)
      a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([3.0, 3.0, level_height[l]])(a_pol)
      if l==0:
        a_texture = TEXTURE([wallStone, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
      else:
        if l==3:
          a_texture = TEXTURE([wallStone, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
        else:
          a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createEst(l,i+1,h,s2)
    else:
      h = h + level_height[l]
      return createEst(l+1,0,h,s1)
  else:
    return s1

def createInt(l,i,h,s1):
  if l <= len(levelInt)-1:
    if i < len(levelInt[l]):
      a = levelInt[l][i]
      a_split = a.split(",")
      a_number = np.array(a_split, dtype=float)
      a_pol = MKPOL([[[a_number[0],a_number[1],0.0],[a_number[0],a_number[3],0.0],[a_number[2],a_number[1],0.0],[a_number[2],a_number[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([1.0, 1.0, level_height[l]])(a_pol)
      a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createInt(l,i+1,h,s2)
    else:
      h = h + level_height[l]
      return createInt(l+1,0,h,s1)
  else:
    return s1

def buildDoors(l,i,h,s1):
  if l <= len(levelPorte)-1:
    if i < len(levelPorte[l]):
      coords = levelPorte[l][i]
      arrayCoords = coords.split(",")
      elem = np.array(arrayCoords, dtype=float)
      build = MKPOL([[[elem[0],elem[1],0.0],[elem[0],elem[3],0.0],[elem[2],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2,3,4]],[1]])
      buildOffset = OFFSET([1.5, 1.5, heights[l]])(build)
      buildTexture = TEXTURE([doorTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
      buildTraslated = STRUCT([T(3)(h), buildTexture])
      finalStruct = STRUCT([buildTraslated, s1])
      #maniglia cuboidale
      handle_1 = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(CUBOID([5,5,5]))
      handle_1 = STRUCT([T([1,2,3])([1.5,1.5,h+30.0]), handle_1])
      handle_tras = STRUCT([handle_1])
      handle_tras = STRUCT([T([1,2,3])([elem[0],elem[1],0.0]), handle_tras])
      finalStruct = STRUCT([finalStruct,handle_tras])
      return buildDoors(l,i+1,h,finalStruct)
    else:
      h = h + heights[l] #se e' una porta tiro su di 60
      return buildDoors(l+1,0,h,s1)
  else:
    return s1

def createHouse():
  a = createBase(0,initStruct)
  b = createEst(0,0,0.0,initStruct)
  c = createInt(0,0,0.0,initStruct)
  d = buildDoors(0,0,0.0,initStruct)
  house=STRUCT([a,T(3)(3.0),b])
  house=STRUCT([house,T(3)(3.5),c])
  house=STRUCT([house,T(3)(83.0),a])
  house=STRUCT([house,T(3)(163.0),a])
  house=STRUCT([house,T(3)(3.5),d])
  #house = SKEL_3(house)
  VIEW(house)

createHouse()