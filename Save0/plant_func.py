def Grass():
	return get_ground_type()==Grounds.Grassland

def Tree():
	plant(Entities.Tree)
	return True
def Bush():
	return plant(Entities.Bush)
def Carrot():
	if get_ground_type() == Grounds.Grassland:
		till()
	return plant(Entities.Carrot)
def Pumpkin():
	if get_ground_type() == Grounds.Grassland:
		till()
	return plant(Entities.Pumpkin)
def SunFlower():
	if get_ground_type() == Grounds.Grassland:
		till()
	return plant(Entities.Sunflower)

def Cactus():
	if get_ground_type() == Grounds.Grassland:
		till()
	return plant(Entities.Cactus)

plantFuncDict = {Entities.Grass: Grass, 
	Entities.Tree: Tree,
	Entities.Bush: Bush,
	Entities.Carrot: Carrot,
	Entities.Pumpkin: Pumpkin,
	Entities.Sunflower: SunFlower, 
	Entities.Cactus: Cactus
}