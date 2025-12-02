arr = [1, 2, 3]
ar = [4]
def extend(a, b):
	for i in b:
		a.append(i)
		
extend(arr, ar)
print(arr)