clear()
import Drone

def harv_weird():
	use_item(Items.Weird_Substance)
	x, y = get_pos_x(), get_pos_y()
	l = [[North], (South, West), (East, South), (North, East), [West]]
	for m in l:
		for i in m:
			move(i)
		if can_harvest():
			harvest()

Drone.moveTo((1, 1))

while True:

	if spawn_drone(harv_weird):
		move(East)
		move(East)
		move(North)