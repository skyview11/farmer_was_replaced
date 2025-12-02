import Drone
from mazeUtil import calcHeuristic, inverseDirection, coordAfterMove, dist
import mazeScanner

def generate_maze(size=5, pos=(0, 0)):
	clear()
	Drone.moveTo(pos)

	plant(Entities.Bush)
	substance = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	

# ================ {A-star] ===========================
OpenList = dict() # key: F value, value: coord
ClosedList = list() # size x size matrix. 0 if not closed, 1 if cloesd
RollbackLog = list()

def regenMaze(size=5):
	substance = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def init(size=5, gen_maze=False, pos=(0, 0)):
	global OpenList
	global ClosedList
	
	
	
	OpenList = dict()
	ClosedList = list()
	
	if gen_maze:
		mazeScanner.init()
		generate_maze(size, pos)
		mazeScanner.scanMaze(size)
	for x in range(get_world_size()):
		ClosedList.append(list())
		for y in range(get_world_size()):
			ClosedList[x].append(0)
	
	return
	
def search():
	need_rollback = False # 길 막혔을 떄 되돌아와야 하는지를 기록
	while True: ## todo: change to arrive cond
	
		x, y = get_pos_x(), get_pos_y()
		if (x, y) == measure():
			break
		## find movable coordinates
		info = dict()
		for m in [North, West, South, East]:
			next_x, next_y = coordAfterMove(x, y, m)
			if can_move(m) and ClosedList[next_x][next_y] == 0:
				h = calcHeuristic(next_x, next_y)
				if h in info:
					info[h].append(m)
				else:
					info[h] = [m]
		
		ClosedList[x][y] = 1
		
		if len(info) > 0:
			OpenList[(x, y)] = info
		
		## rollback if no more path
		if len(info) == 0:
			while True:
				m = RollbackLog.pop(-1)
				move(m)
				if (get_pos_x(), get_pos_y()) in OpenList:
					break
		
		## explore next node
		x, y = get_pos_x(), get_pos_y()
		min_h = min(OpenList[(x, y)])
		m = OpenList[(x, y)][min_h].pop(0)
		if len(OpenList[(x, y)][min_h]) == 0:
			OpenList[(x, y)].pop(min_h)
		if len(OpenList[(x, y)]) == 0:
			OpenList.pop((x, y))
		move(m)
		RollbackLog.append(inverseDirection(m))
	return

def run(size=5, pos=(0, 0), gen_maze=False):
	init(size, gen_maze, pos)
	x, y = measure()
	path = mazeScanner.movePlanner(x, y)
	for m in path:
		move(m)
		mazeScanner.updateMap(get_pos_x(), get_pos_y())
	regenMaze(size)
	
if __name__=="__main__":
	
	
	
	size=16
	run(size, (5, 5), True)
	for _ in range(299):
		run(size, (5, 5), False)
	
		
		
		
		
		
	