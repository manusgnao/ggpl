"""workshop_02"""
from pyplasm import *
import csv
import numpy as np
"""
weightBeams ---> lunghezza delle travi tra i pilastri dell'edificio
heightPilars ---> lunghezza dei pilastri dell'edificio
floorDepth ---> distanza tra un piano e l'altro all'interno dell'edificio
pilarWeight ---> larghezza di un pilastro
beamWeight ---> larghezza delle travi, sempre la meta' dei pilastri in modo 
				 che una trave possa sempre poggiare su un pilastro
"""
#weightBeams = [5.0, 2.5, 5.0]
#heightPilars = [4.0, 3.5, 2.0]
#floorDepth = [2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 5.0]
#pilarWeight = 0.5
#beamWeight = pilarWeight/2.0

with open('frame_data_435861.csv', 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect, delimiter=';')
    for i,row in enumerate(reader):
    	if i == 0:
    		weightBeams = row
    		weightBeams = filter(None, weightBeams)
    		weightBeams = np.array(weightBeams, dtype=float)
    		print weightBeams
    	if i == 1:
    		heightPilars = row
    		heightPilars = filter(None, heightPilars)
    		heightPilars = np.array(heightPilars, dtype=float)
    		print heightPilars
    	if i == 2:
    		floorDepth = row
    		floorDepth = filter(None, floorDepth)
    		floorDepth = np.array(floorDepth, dtype=float)
    		print floorDepth
    	if i == 3:
    		pilarWeight = row[0]
    		pilarWeight = float(pilarWeight)
    	if i == 4:
    		beamWeight = row[0]
    		beamWeight = float(beamWeight)


"""
inizializzo una struttura vuota in cui verra' costruito il telaio
"""
pilar0 = CUBOID([0,0,0])
start = STRUCT([pilar0])

"""
funzione ricorsiva che crea l'intera struttura andando a creare un piano sull'altro
"""
def ggpl_bone_structure(heightPilarTot, beamWeightTot, floorDepthTot, x, z, y, totalStruct):
	if  z < len(heightPilars):
		pilar1 = CUBOID([pilarWeight,pilarWeight,heightPilars[z]])
		pilarBeam1 = STRUCT([T(1)(floorDepthTot),T(2)(beamWeightTot),T(3)(heightPilarTot), pilar1])
		beam1 = CUBOID([beamWeight,weightBeams[y],beamWeight])
		beam1Next = STRUCT([T([1,2,3])([beamWeight/2.0+floorDepthTot, (3.0*pilarWeight/4.0)+beamWeightTot, heightPilarTot+heightPilars[z]]), beam1])
		if  x < len(floorDepth):
			totalStruct = STRUCT([totalStruct,pilarBeam1,beam1Next])
			beam2 = CUBOID([floorDepth[x],beamWeight,beamWeight])
			beam2Next = STRUCT([T([1,2,3])([beamWeight/2.0+floorDepthTot, (pilarWeight/4.0)+beamWeightTot, heightPilarTot+heightPilars[z]]), beam2])
			beamWeightTot=beamWeightTot+weightBeams[y]+(pilarWeight/2.0)
			if y < len(weightBeams) - 1:
				y=y+1
				totalStruct = STRUCT([totalStruct,beam2Next])
				return ggpl_bone_structure(heightPilarTot, beamWeightTot, floorDepthTot, x, z, y, totalStruct)
			else:
				pilar1Next = STRUCT([T(1)(floorDepthTot),T(2)(beamWeightTot),T(3)(heightPilarTot), pilar1])
				beam2Next = STRUCT([T([1,2,3])([beamWeight/2.0+floorDepthTot, (pilarWeight/4.0)+beamWeightTot,heightPilarTot+heightPilars[z]]), beam2])
				totalStruct = STRUCT([totalStruct,beam2Next,pilar1Next,beam2Next])
				floorDepthTot = floorDepthTot + floorDepth[x]
				x=x+1
				return ggpl_bone_structure(heightPilarTot, 0, floorDepthTot, x, z, 0, totalStruct)
		else:
			heightPilarTot = heightPilarTot + heightPilars[z] + beamWeight
			z=z+1
			return ggpl_bone_structure(heightPilarTot, 0, 0, 0, z, 0, totalStruct)
	else:
		distance = 0
		for p in floorDepth:
			distance = distance + p
		return createLastFrame(distance, 0, 0, 0, 0, totalStruct)

"""
funzione ricorsiva che crea il telaio di chiusura della struttura
"""
def createLastFrame(distance, heightPilarTot, beamWeightTot, i, y, totalStruct):
	pilar1 = CUBOID([pilarWeight,pilarWeight,heightPilars[y]])
	pilarBeam1 = STRUCT([T(1)(distance),T(2)(beamWeightTot),T(3)(heightPilarTot), pilar1])
	beam1 = CUBOID([beamWeight,weightBeams[i],beamWeight])
	beam1Next = STRUCT([T([1,2,3])([beamWeight/2.0+distance, (3.0*pilarWeight/4.0)+beamWeightTot,heightPilarTot+heightPilars[y]]), beam1])
	beamWeightTot=beamWeightTot+weightBeams[i]+(pilarWeight/2.0)
	if i == len(weightBeams) - 1:
		pilar1Next = STRUCT([T(1)(distance),T(2)(beamWeightTot),T(3)(heightPilarTot), pilar1])
		heightPilarTot = heightPilarTot + heightPilars[y] + beamWeight
		totalStruct = STRUCT([totalStruct,pilarBeam1,beam1Next,pilar1Next])
		if y != len(heightPilars) - 1:
			y=y+1
			return createLastFrame(distance, heightPilarTot, 0, 0, y, totalStruct)
		else:
			VIEW(totalStruct)
	else:
		i=i+1
		totalStruct = STRUCT([totalStruct,pilarBeam1,beam1Next])
		return createLastFrame(distance, heightPilarTot, beamWeightTot, i, y, totalStruct)

ggpl_bone_structure(0, 0, 0, 0, 0, 0, start)