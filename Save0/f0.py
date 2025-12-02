def get_entity_type_in_direction(dir):
	move(dir)
	return get_entity_type()

def zero_arg_wrapper():
	return get_entity_type_in_direction(North)
drone = spawn_drone(zero_arg_wrapper)
print(wait_for(drone))