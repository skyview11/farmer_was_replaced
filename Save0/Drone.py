import const
import plant_func
import mapper
import args
## 드론의 이동과 작업 큐를 관리 및 행동
WorkQueue = list()
## workObject: {"type": UID, "func": function, "arg": arg}

def extend(original, toExtend):
	for l in toExtend:
		original.append(l)
	return original

def moveTo(coord):
	x, y = coord
	cur_x, cur_y = get_pos_x(), get_pos_y()
	
	move_vector = [0, 0]
	if abs(x-cur_x) < 0.5 * get_world_size():
		move_vector[0] = x-cur_x
	else:
		move_vector[0] = (get_world_size() - abs(x - cur_x)) * -(x-cur_x)/abs(x-cur_x)
		
	if abs(y-cur_y) < 0.5 * get_world_size():
		move_vector[1] = y-cur_y
	else:
		move_vector[1] = (get_world_size() - abs(y - cur_y)) * -(y-cur_y)/abs(y-cur_y)

	for _ in range(abs(move_vector[0])):
		move([West, East][move_vector[0]>0])
	for _ in range(abs(move_vector[1])):
		move([South, North][move_vector[1]>0])
	
	

def addMoveToQueue(x, y):
	worksToAdd = list()
	work = {"type": const.CMD_MOVE, 
			"func": moveTo, 
			"args": [(x, y)]
			}
	worksToAdd.append(work)
	return worksToAdd


def Harvest(x, y):
	worksToAdd = list()
	moveTo((x, y))
	# 1. dead pumpkin
	# 2. havest only when pumpkin is full
	if can_harvest() or get_entity_type()==Entities.Dead_Pumpkin:
		harvest()
		worksToAdd = Plant(x, y, mapper.MapInfo[x][y])
	else:
		workInfo = {"type": const.CMD_HARV, 
					"func": Harvest, 
					"args": [x, y]
		}
		worksToAdd.append(workInfo)
	return worksToAdd

def Plant(x, y, entity):
	worksToAdd = list()
	moveTo((x, y))
	
	if entity in plant_func.plantFuncDict:
		is_planted = plant_func.plantFuncDict[entity]()
		if not is_planted:
			workInfo = {"type": const.CMD_PLANT, 
						"func": Plant, 
						"args": [x, y, entity]}
			worksToAdd.append(workInfo)
			return worksToAdd
		elif entity == Entities.Pumpkin:
			workInfo = {"type": const.CMD_CK_PUMP_STAT, 
						"func": CheckPumpkinStatus, 
						"args": [x, y]}
			worksToAdd.append(workInfo)
		elif entity == Entities.Sunflower:
			workInfo = {"type": const.CMD_HARV_BEST_SF, 
						"func": HarvestBestSunflower, 
						"args": []}
			worksToAdd.append(workInfo)
			global SunflowerStatus
			SunflowerStatus[measure()].append(((x, y), get_time()))
		
		elif entity == Entities.Cactus:
			workInfo = {"type": const.CMD_CK_CACTUS_STATUS, 
						"func": CheckCactusStatus, 
						"args": [x, y]}
			worksToAdd.append(workInfo)
		elif entity != Entities.Pumpkin:
			workInfo = {"type": const.CMD_HARV, 
						"func": Harvest, 
						"args": [x, y]}
			worksToAdd.append(workInfo)
	return worksToAdd
	
	# use buff items
	#Watering(x, y)
Pumpkin1Status = {"N_GROWN": 0}
Pumpkin2Status = {"N_GROWN": 0}

def initPumpkinStatus():
	global Pumpkin1Status
	global Pumpkin2Status
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if mapper.isPump1(x, y):
				Pumpkin1Status[(x, y)] = const.PUMP_EMPTY
			elif mapper.isPump2(x, y):
				Pumpkin2Status[(x, y)] = const.PUMP_EMPTY


def CheckPumpkinStatus(x, y):
	# harvest only when all pumpkin group is successfully grown
	
	moveTo((x, y))
	## dead pumpkin elimination
	entity_type = get_entity_type()
	if entity_type == Entities.Dead_Pumpkin:
		harvest()
		worksToAdd = Plant(x, y, Entities.Pumpkin)
		return worksToAdd
	if (x, y) in Pumpkin1Status:
		Pumpkin1Status[(x, y)] = const.PUMP_GROWN
		Pumpkin1Status["N_GROWN"] += 1
	elif (x, y) in Pumpkin2Status:
		Pumpkin2Status[(x, y)] = const.PUMP_GROWN
		Pumpkin2Status["N_GROWN"] += 1
	
	worksToAdd = list()
	if Pumpkin1Status["N_GROWN"] == len(Pumpkin1Status)-1:
		harvest()
		Pumpkin1Status["N_GROWN"] = 0
		for k in Pumpkin1Status:
			if k=="N_GROWN":
				continue
			Pumpkin1Status[k] = const.PUMP_EMPTY
			works = Plant(k[0], k[1], Entities.Pumpkin)
			for w in works:
				worksToAdd.append(w)
	if Pumpkin2Status["N_GROWN"] == len(Pumpkin2Status)-1:
		harvest()
		Pumpkin2Status["N_GROWN"] = 0
		for k in Pumpkin2Status:
			if k=="N_GROWN":
				continue
			Pumpkin2Status[k] = const.PUMP_EMPTY
			works = Plant(k[0], k[1], Entities.Pumpkin)
			for w in works:
				worksToAdd.append(w)
	return worksToAdd
#======================[ Sunflower ]===========================#

SunflowerStatus = {} # key: the number of petal, value: coord
def initSunflowerStatus():
	global SunflowerStatus
	for i in range(7, 16):
		SunflowerStatus[i] = list()

def HarvestBestSunflower(): # harvest sunflower that has biggest number of patel
	## get coordinate of best sunflower
	global SunflowerStatus
	for i in range(15, 6, -1):
		if len(SunflowerStatus[i])==0:
			continue
		coord, plant_time = SunflowerStatus[i][0]
		
		cur_t = get_time()
		SunflowerStatus[i].pop(0)
		break
	## harvest sunflower
	moveTo(coord)
	if can_harvest():	
		harvest()
	else:
		worksToAdd = list()
		SunflowerStatus[i].append((coord, plant_time))
		workInfo = {"type": const.CMD_HARV_BEST_SF, 
						"func": HarvestBestSunflower, 
						"args": []}
		worksToAdd.append(workInfo)
	## plant all sunflowers only if all sunflowers are harvested
	for k in SunflowerStatus:
		if len(SunflowerStatus[k])!=0:
			return
	worksToAdd = list()
	for x in range(args.SunflowerPos[0][0], args.SunflowerPos[1][0]+1):
		for y in range(args.SunflowerPos[0][1], args.SunflowerPos[1][1]+1):
			works = Plant(x, y, Entities.Sunflower)
			extend(worksToAdd, works)
	return worksToAdd 
	


def CheckSunflowerStatus(x, y):
	worksToAdd = list()
	moveTo((x, y))
	n_panel = measure()
	if n_panel >= 1:
		extend(worksToAdd, Harvest(x, y))
	else:
		workInfo = {"type": const.CMD_CK_SF_STAT, 
					"func": CheckSunflowerStatus, 
					"args": [x, y]}
		worksToAdd.append(workInfo)
	return worksToAdd
# ===============[ Cactus ]============================
Cactus1Status = dict()
Cactus2Status = dict()

def initCactusStatus():
	global Cactus1Status
	global Cactus2Status
	Cactus1Status["n_harv"] = 0
	Cactus2Status["n_harv"] = 0
	

def bubbleSort(start_coord, dir, n_elem):
	
	for i in range(n_elem-1, 0, -1):
		moveTo(start_coord)
		for j in range(i):
			# print(measure(), measure(East))
			if measure() > measure(dir):
				swap(dir)
			move(dir)
				


def CheckCactusStatus(x, y):
	worksToAdd = list()
	## sort if cactus is Eastmost or Northmost element
	if x==get_world_size()-1 or y==get_world_size()-1:
		bubbleSort((x+1-get_world_size(), y), East, get_world_size())
	elif mapper.MapInfo[x+1][y] != Entities.Cactus and mapper.MapInfo[x][y+1] != Entities.Cactus:
		bubbleSort(x+1-get_world_size(), East, get_world_size())
	## check the cactus is harvestable
	moveTo((x, y))
	global Cactus1Status
	global Cactus2Status
	if not can_harvest():
		workInfo = {"type": const.CMD_CK_CACTUS_STATUS, 
					"func": CheckCactusStatus, 
					"args": [x, y]}
		worksToAdd.append(workInfo)
		return worksToAdd
	elif mapper.isCactus1(x, y):
		Cactus1Status["n_harv"] += 1
	elif mapper.isCactus2(x, y):
		Cactus2Status["n_harv"] += 1
	
	## harvest if all grown
	
	worksToAdd = list()
	if Cactus1Status["n_harv"] == get_world_size():
		Cactus1Status["n_harv"] = 0
		extend(worksToAdd, Harvest(0, 0))
		for i in range(1, get_world_size()):
			extend(worksToAdd, Plant(i, 0, Entities.Cactus))
	if Cactus2Status["n_harv"] == get_world_size():
		Cactus2Status["n_harv"] = 0
		extend(worksToAdd, Harvest(0, 7))
		for i in range(1, get_world_size()):
			extend(worksToAdd, Plant(i, 7, Entities.Cactus))
			
	return worksToAdd
	
		
	
	
		
	
	

def Watering(x, y):
	worksToAdd = list()
	if get_water() >= 0.5:
		return
	if num_items(Items.Water) == 0:
		global WorkQueue
		workInfo = {"type": const.CMD_USE_WATER, 
					"func": Watering, 
					"args": [x, y]
		}
		worksToAdd.append(workInfo)
		return worksToAdd
	while get_water() < 0.9:
		use_item(Items.Water)

def run():
	global WorkQueue
	while True:
		if len(WorkQueue) > 0:
			work = WorkQueue.pop(0)
			if work["type"]==const.CMD_HARV_BEST_SF:
				worksToAdd = work["func"]()
			elif work["type"]==const.CMD_MOVE:
				worksToAdd = work["func"](work["args"][0])
			elif work["type"]==const.CMD_HARV:
				worksToAdd = work["func"](work["args"][0], work["args"][1])
			elif work["type"]==const.CMD_CK_PUMP_STAT:
				worksToAdd = work["func"](work["args"][0], work["args"][1])
			elif work["type"]==const.CMD_CK_SF_STAT:
				worksToAdd = work["func"](work["args"][0], work["args"][1])
			elif work["type"]==const.CMD_USE_WATER:
				worksToAdd = work["func"](work["args"][0], work["args"][1])
			elif work["type"]==const.CMD_CK_CACTUS_STATUS:
				worksToAdd = work["func"](work["args"][0], work["args"][1])
			elif work["type"]==const.CMD_PLANT:
				worksToAdd = work["func"](work["args"][0], work["args"][1], work["args"][2])
			
			
			else:
				print("UID Error: " + str(work["type"]))
			if worksToAdd ==None:
				continue
			for w in worksToAdd:
				a = w["type"]
				WorkQueue.append(w)
		else:
			print("ERROR! WorkQueue is Empty!")
	
	


			