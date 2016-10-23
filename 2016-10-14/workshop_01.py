from pyplasm import *

beamsWeight = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
pilarsHeight = [4.0, 4.0, 3.0]
bx=1
bz=1
px=1
py=1
beamDepth = [15.0, 5.0, 3.0, 5.0]
pilar1 = CUBOID([0,0,0])
totalArc = STRUCT([pilar1])
totPilarHeight=0
t = STRUCT([CUBOID([])])

for j,pilar in enumerate(pilarsHeight):
	firstPilar = CUBOID([px,py,pilar])
	totBeamWeight=0
	if j!=0:
			parzBeam = STRUCT([T(3)(totPilarHeight+1), firstPilar])
			totalArc = STRUCT([totalArc,parzBeam])
	else:
			totalArc = STRUCT([totalArc,firstPilar])
	
	totPilarHeight= totPilarHeight + pilar

	for i,beam in enumerate(beamsWeight):
		parzPilar = CUBOID([bx,beam,bz])
		if i==0:
			if(j==0):
				nextBeam = STRUCT([T(2)(0.5),T(3)(totPilarHeight), parzPilar])
			else:
				nextBeam = STRUCT([T(2)(0.5),T(3)(totPilarHeight+1), parzPilar])
		else:
			if(j==0):
				nextBeam = STRUCT([T(2)(totBeamWeight+0.5),T(3)(totPilarHeight), parzPilar])
			else:
				nextBeam = STRUCT([T(2)(totBeamWeight+0.5),T(3)(totPilarHeight+1), parzPilar])
		totBeamWeight = totBeamWeight + beam
		nextPilar = CUBOID([px,py,pilar])
		if(j==0):
			firstPilar = STRUCT([T(2)(totBeamWeight), nextPilar])
		else:
			firstPilar = STRUCT([T(2)(totBeamWeight),T(3)(totPilarHeight-pilar+1), nextPilar])
		arc = STRUCT([firstPilar,nextBeam])
		totalArc = STRUCT([totalArc,arc])
for x,depth in enumerate(beamDepth):
	t = STRUCT([totalArc, T(1)(depth), t])
VIEW(t)
