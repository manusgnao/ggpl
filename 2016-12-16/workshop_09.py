""" WORKSHOP 09 """
from pyplasm import *

textureRoof = "texture/textureRoof.jpg"
textureGround = "texture/textureGround.jpg"

spessore = 0.2
"""coordinate X del teto"""
x = [
  1.0,  #0
  3.0,  #1
  7.0,  #2
  8.0,  #3
  10.0, #4
  12.0, #5
  14.0, #6
  16.0, #7
  17.0, #8
  21.0, #9
  23.0  #10
]
"""coordinate Y del teto"""
y = [
  1.0,  #0
  3.0,  #1
  5.0,  #2
  7.0,  #3
  8.0,  #4
  10.0, #5
  11.0, #6
  12.0  #7
]

z = [
  0.0,  #0
  2.0   #1
]
"""vertici che creeranno il tetto"""
vertex = [
  [x[0],y[0],z[0]], #1 ---> vertici esterni
  [x[0],y[3],z[0]], #2
  [x[3],y[7],z[0]], #3
  [x[7],y[7],z[0]], #4
  [x[10],y[3],z[0]],#5
  [x[10],y[0],z[0]],#6
  [x[7],y[0],z[0]], #7
  [x[5],y[2],z[0]], #8
  [x[3],y[0],z[0]], #9
  [x[1],y[1],z[1]], #10 ---> vertici interni (terrazzo)
  [x[1],y[2],z[1]], #11
  [x[4],y[5],z[1]], #12
  [x[6],y[5],z[1]], #13
  [x[9],y[2],z[1]], #14
  [x[9],y[1],z[1]], #15
  [x[8],y[1],z[1]], #16
  [x[5],y[4],z[1]], #17
  [x[2],y[1],z[1]]  #18

]
"""unendo i vertici si creano le celle"""
cells = [
  [1,2,11,10],
  [2,3,12,11],
  [3,4,13,12],
  [4,5,14,13],
  [5,6,15,14],
  [6,7,16,15],
  [7,8,17,16],
  [8,9,18,17],
  [9,10,1,18]
]



"""creazione del tetto"""
roof = MKPOL([vertex, cells,[1]])
roof = TEXTURE([textureRoof, TRUE, FALSE, 1, 1, 0, 6, 6])(OFFSET([spessore, spessore, spessore])(SKEL_2(roof)))
"""creazione del terrazzo"""
ground = MKPOL([vertex, [[10,11,12,17,18],[12,13,17],[13,14,15,16,17]],[1]])
ground = TEXTURE([textureGround, TRUE, FALSE, 1, 1, 0, 6, 6])(OFFSET([spessore, spessore, spessore])(SKEL_2(ground)))
"""unione di tetto e terrazzo"""
completeRoof = STRUCT([roof, ground])

VIEW(completeRoof)

