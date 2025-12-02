import Drone

Drone.moveTo((10, 10))
if get_ground_type()==Grounds.Grassland:
	till()
for dir in [North, East, South, West]:
	def task():
		move(dir)
		do_a_flip()
	spawn_drone(task)