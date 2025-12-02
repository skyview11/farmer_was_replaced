from mapper import initMapInfo, MapInfo
import Drone
def Init(debug=False):
	## init map
	
	clear()
	initMapInfo()
	Drone.initPumpkinStatus()
	Drone.initCactusStatus()
	Drone.initSunflowerStatus()
	## init drone position
	Drone.addMoveToQueue(0, 0)

	initialPlant(debug)

def initialPlant(Debug=False):
	if Debug:
		__initialPlantDebug()
	else:
		__initialPlant()

def __initialPlantDebug():
	for y in range(1):
		for x in range(get_world_size()):
			for w in Drone.Plant(x, y, MapInfo[x][y]):
				Drone.WorkQueue.append(w)

def __initialPlant():
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			for w in Drone.Plant(x, y, MapInfo[x][y]):
				Drone.WorkQueue.append(w)		

def collectRemain():
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			Drone.moveTo((x, y))
			harvest()
			
if __name__=="__main__":
	collectRemain()
	