__UID__ = 0

def GetUID():
	global __UID__
	__UID__ += 1
	return __UID__

# drone command ENUM
CMD_MOVE = GetUID()
CMD_HARV = GetUID()
CMD_PLANT = GetUID()
CMD_CK_PUMP_STAT = GetUID()
CMD_USE_WATER = GetUID()
CMD_CK_SF_STAT = GetUID()
CMD_HARV_BEST_SF = GetUID()
CMD_CK_CACTUS_STATUS = GetUID()

# pumpkin status enum
PUMP_EMPTY = GetUID()
PUMP_DEAD = GetUID()
PUMP_GROWN = GetUID()
