def dist(coord1, coord2):
	x1, y1 = coord1
	x2, y2 = coord2
	return (x1-x2)**2 + (y1-y2)**2
	
def calcHeuristic(x, y):
	return dist((x, y), measure())

def inverseDirection(m):
	l = {North:South, East:West, South:North, West:East}
	return l[m]

def coordAfterMove(x, y, m):
	l = {North: (0, 1), West:(-1, 0), South:(0,-1), East:(1,0)}
	return (x+l[m][0])%get_world_size(), (y+l[m][1])%get_world_size()

