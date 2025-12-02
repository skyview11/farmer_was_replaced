def makeList(shape, value):
	l = list()
	n = shape[0]
	if len(shape)==1:
		for _ in range(n):
			l.append(value)
		return l
	for _ in range(n):
		l.append(makeList(shape[1:], value))
	
	return l
	
if __name__ == "__main__":
	l = makeList([4, 4, 4], 1)
	quick_print(l)