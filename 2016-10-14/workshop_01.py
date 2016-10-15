from larlib import *

beamsWeight = [4.0, 8.5, 6.0, 4.0, 8.0]
pilarsHeight = [4.0, 2.5, 5.0]
pilar_space_tot=0

pilar1 = CUBOID([0,0,0])
totalArc = STRUCT([pilar1])
totPilarHeight=0

for j,pilar in enumerate(pilarsHeight):
	firstPilar = CUBOID([1,1,pilar])
	totBeamWeight=0
	if j!=0:
			parzBeam = STRUCT([T(3)(totPilarHeight+1), firstPilar])
			totalArc = STRUCT([totalArc,parzBeam])
	else:
			totalArc = STRUCT([totalArc,firstPilar])
	
	totPilarHeight= totPilarHeight + pilar

	for i,beam in enumerate(beamsWeight):
		parzPilar = CUBOID([1,beam,1])
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
		nextPilar = CUBOID([1,1,pilar])
		if(j==0):
			firstPilar = STRUCT([T(2)(totBeamWeight), nextPilar])
		else:
			firstPilar = STRUCT([T(2)(totBeamWeight),T(3)(totPilarHeight-pilar+1), nextPilar])
		arc = STRUCT([firstPilar,nextBeam])
		totalArc = STRUCT([totalArc,arc])


VIEW(totalArc)
