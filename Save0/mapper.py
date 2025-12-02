import const
import args

MAP_X = get_world_size()
MAP_Y = get_world_size()

def isTree(x, y):
	cond1 = (x+y)%2==0
	cond2 = not (isPumpkin(x, y) or isSunFlower(x, y) or isCarrot(x, y) or isCactus(x, y))
	return cond1 and cond2

def isSunFlower(x, y):
	cond1 = (x >= 6) and (x < 10) 
	cond2 = (y >= 1) and (y < 7)
	return cond1 and cond2


def isGrass(x, y):
	cond1 = (x+y)%2 == 1
	cond2 = not (isPumpkin(x, y) or isSunFlower(x, y) or isCarrot(x, y) or isCactus(x, y))
	return cond1 and cond2

def isCarrot(x, y):
	
	return (x >= MAP_X//2) and (y >= MAP_X//2)

def isPump1(x, y):
	cond1 = x < 6
	cond2 = y >= 1 and y < 7
	return cond1 and cond2

def isPump2(x, y):
	cond1 = (x >= 10) and (x < 16) 
	cond2 = y >= 1 and y < 7
	return cond1 and cond2
def isPumpkin(x, y):
	return isPump1(x, y) or isPump2(x, y)

def isCactus1(x, y):
	return y==0
def isCactus2(x, y):
	return y==7

def isCactus(x, y):
	return isCactus1(x, y) or isCactus2(x, y)

# mapInfo
MapInfo = list()

def initMapInfo():
	for x in range(get_world_size()):
		MapInfo.append(list())
		for y in range(get_world_size()):
			if isTree(x, y):
				MapInfo[x].append(Entities.Tree)
			elif isCarrot(x, y):
				MapInfo[x].append(Entities.Carrot)
			elif isPumpkin(x, y):
				MapInfo[x].append(Entities.Pumpkin)
			elif isSunFlower(x, y):
				MapInfo[x].append(Entities.Sunflower)
			elif isCactus(x, y):
				MapInfo[x].append(Entities.Cactus)
			else:
				MapInfo[x].append(Entities.Grass)