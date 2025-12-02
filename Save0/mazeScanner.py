from mazeUtil import calcHeuristic, inverseDirection, coordAfterMove, dist
import Drone
import util
from maze import generate_maze

MazeMap = list() # row x col x dir

def initMazeMap():
	global MazeMap
	MazeMap = util.makeList((get_world_size(), get_world_size(), 4), 0)

def scanMaze(size):
	global MazeMap
	nodeToVisit = dict()
	isNodeVisited = util.makeList((get_world_size(), get_world_size()), False)
	n_node = size*size
	n_visited = 0
	rollbackStack = list()
	
	while True:
		x, y = get_pos_x(), get_pos_y()
		isNodeVisited[x][y]=True
		n_visited += 1
		## add not visited node to nodeToVisit
		nodeToVisit[(x, y)] = list()
		i = -1
		for m in [North, West, South, East]:
			i += 1
			next_x, next_y = coordAfterMove(get_pos_x(), get_pos_y(), m)
			if not can_move(m):
				continue
			MazeMap[x][y][i] = 1
			if isNodeVisited[next_x][next_y]==False:
				nodeToVisit[(x, y)].append(m)
				
		if n_visited == n_node:
			break
		## goto next node
	
		if len(nodeToVisit[(x, y)]) == 0: ## goto ancestor node
			nodeToVisit.pop((x, y))
			while True:
				m = rollbackStack.pop(-1)
				move(m)
				if (get_pos_x(), get_pos_y()) in nodeToVisit:
					break
		x, y = get_pos_x(), get_pos_y()
		m = nodeToVisit[(x, y)].pop(0)
		if len(nodeToVisit[(x, y)]) == 0:
			nodeToVisit.pop((x, y))
		move(m)
		rollbackStack.append(inverseDirection(m))
		
				

def movePlanner(target_x, target_y):
	cur_x, cur_y = get_pos_x(), get_pos_y()
	OpenList = dict()
	ClosedList = util.makeList((get_world_size(), get_world_size()), 0)
	parents = dict() # key: child node, value: parent node
	F = 0 + dist((cur_x, cur_y), (target_x, target_y))
	OpenList[F] = [{"coord": (cur_x, cur_y), "G": 0}]
	A = 0
	while True:
		A += 1
		## get unexplored node
		min_f = min(OpenList)
		info = OpenList[min_f].pop(0)
		x, y = info["coord"]
		#print(x, y)
		if len(OpenList[min_f])==0:
			OpenList.pop(min_f)
		if ((x, y)==(target_x, target_y)):
			break
		## add node to ClosedList
		ClosedList[x][y] = 1
		## scan neibhor node and add unexplored node 
		j=-1
		for m in [North, West, South, East]:
			j += 1
			next_x, next_y = coordAfterMove(x, y, m)
			if  MazeMap[x][y][j]==0 or ClosedList[next_x][next_y] == 1:
				continue
			G = info["G"] + 1
			F = G + dist((next_x, next_y), (target_x, target_y))
			if F in OpenList:
				OpenList[F].append({"coord": (next_x, next_y), "G": G})
			else:
				OpenList[F]=[{"coord": (next_x, next_y), "G": G}]
			
			if (next_x, next_y) in parents:
				#print("FUCK!!!!")
				parents[(next_x, next_y)] = {"coord": (x, y), "dir": m}
			else:
				parents[(next_x, next_y)] = {"coord": (x, y), "dir": m}
	## get course
	x_, y_ = target_x, target_y
	path = list()
	while (x_, y_) != (cur_x, cur_y):
		info = parents[(x_, y_)]
		x_, y_ = info["coord"]
		path.insert(0, info["dir"])
	return path
			
def init():
	initMazeMap()
	
def updateMap(x, y):
	global MazeMap
	i=-1
	for m in [North, West, South, East]:
		i+=1
		if can_move(m):
			MazeMap[x][y][i] = 1

if __name__ == "__main__":
	size = (6, 6)
	init()
	generate_maze(size[0])
	scanMaze(size)
	x, y = measure()
	path = movePlanner(x, y)
	quick_print(path)
	

