#!/usr/bin/env python3

import sys
fa_file = open(sys.argv[1])
contents = fa_file.readlines()
new_list = []
for i in range(1, len(contents), 2):
    new_list.append(contents[i].strip())
x,y = new_list
print(x)
counter = 0
for char in x:
	if char == y[counter]:
		print("|", end = "")
	else:
		print(" ", end = "")
	counter += 1
print()
print(y)
fa_file.close()