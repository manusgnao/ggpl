""" workshop 05 """
from pyplasm import *

""" Riproduzione di una Lavagna
boardX --> lunghezza del piano della lavagna (asse X)
boardY --> spessore del piano della lavagna (asse Y)
boardZ --> altezza del piano della lavagna (asse Z)
legX --> asse X del sostegno della lavagna
legY --> asse Y del sostegno della lavagna
legZ --> altezza del sostegno della lavagna
"""

def makeLavagna(boardX,boardY,boardZ,legX,legY,legZ):
	lavagna = COLOR(BLACK)(CUBOID([boardX,boardY,boardZ]))
	leg = CUBOID([legX,legY,legZ])
	couple = STRUCT([leg,T(1)(boardX-legX),leg])
	totalLavagna = STRUCT([couple, T(3)(legZ), lavagna])
	VIEW(totalLavagna)

""" Riproduzione di un Banco
planX --> lunghezza del piano del banco (asse X)
planY --> spessore del piano del banco (asse Y)
planZ --> altezza del piano del banco (asse Z)
legX --> asse X della gamba del banco
legY --> asse Y della gamba del banco
legZ --> altezza della gamba del banco
"""

def makeDesk(planX,planY,planZ,legX,legY,legZ):
	tableLeg = CUBOID([legX,legY,legZ])

	couple = STRUCT([tableLeg, T(2)(legZ), tableLeg])

	legs = STRUCT([couple, T(1)(planX), couple])

	plan = COLOR(GREEN)(CUBOID([planX+legX,planY+legY,planZ]))

	desk = STRUCT([legs, T(3)(legZ), plan])
	VIEW(desk)

""" Riproduzione di una Sedia
seatX --> lunghezza del sedile della sedia (asse X)
seatY --> spessore del sedile della sedia (asse Y)
seatZ --> altezza del sedile della sedia (asse Z)
legX --> asse X della gamba della sedia
legY --> asse Y della gamba della sedia
legZ --> altezza della gamba della sedia
"""

def makeChair(legX,legY,legZ,seatX,seatY,seatZ):
	chairLeg = CUBOID([legX,legY,legZ])
	couple = STRUCT([chairLeg, T(2)(seatY), chairLeg])
	legs = STRUCT([couple, T(1)(seatX), couple]) 
	seat = COLOR(RED)(CUBOID([seatX+legX,seatY+legY,seatZ]))
	parzChair = STRUCT([legs, T(3)(legZ-seatZ), seat, T(3)(seatZ), couple])
	back = COLOR(RED)(CUBOID([legX,seatY-legY,seatZ*2]))
	chair = STRUCT([parzChair, T([2,3])([0.05,0.65]), back])
	VIEW(chair)
	

#makeLavagna(3.0,0.1,1.5,0.1,0.1,0.6)
#makeDesk(0.8,0.5,0.05,0.05,0.05,0.5)
#makeChair(0.05,0.05,0.4,0.3,0.3,0.05)