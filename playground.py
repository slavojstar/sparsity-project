# Idea is to make an orchestra-like matrix of instruments that abide by the
# following rules:
# 1) If the instrument next to you is playing, do not play.
# 2) Otherwise play at random.
# 'When the guy next to you is playing, don't play.'
# https://www.youtube.com/watch?v=cIsewG2g-1g

# Ambiguity to the rules:
# CASE 1: Is it the case that an instrument can start playing
# forcing the instruments next to it to stop?
# CASE 2: Or is it the case that an instrument should never start
# to play if the instruments next to it are playing (suspect this
# is the easier scenario to program)
# (subcase: if an instrument stops playing, what should the adjacent
# instruments do? Should they necessarily start? Wouldn't this just create
# waves throughout the orchestra? Is that good or bad?)

# 'As your note dies away look at the person sitting next to you
# and let them swell in' - Hans Zimmer (a bit ambiguous)

# GOALS:
# 1) Create an orchestra matrix which plays to the above rules
# 2) Make it so you can hear the orchestra
# 3) Make it so you can See the orchestra (in real time)
# 4) Make it sound good

import random
import time
from multiprocessing.dummy import Pool as ThreadPool
import os
import threading
import numpy as np

def SimplePlay(M, pos):
	''' Takes a (0, 1)-array M and a position in that array and oscillates
	it randomly between 0 and 1'''

	while True:
		print(M)
		time.sleep(random.uniform(0.1, 0.2))
		if M[pos] == 1:
			M[pos] = 0
		else:
			M[pos] = 1

def AvoidantPlay(M, pos):
	''' Takes a 0-array M and a position in that array. 
	BinaryPlay then applies the following rules to the element at
	position pos: change to 1 for a random amount of time after a
	random amount of time, unless the adjacent element is 1 in which
	case wait another random amount of time and check again '''

	while True:
		print(M)
		time.sleep(random.uniform(0.1, 3))
		if M[(pos - 1) % len(M)] == 1 or M[(pos + 1) % len(M)] == 1:
			continue
		else:
			M[pos] = 1
			print(M)
			time.sleep(random.uniform(0.1, 3))
			M[pos] = 0

def AvoidantPlay2(M, pos, zeroStart, zeroEnd, oneStart, oneEnd):
	''' Takes a 0-array M and a position in that array. 
	BinaryPlay then applies the following rules to the element at
	position pos: change to 1 for a random amount of time after a
	random amount of time, unless the adjacent element is 1 in which
	case wait another random amount of time and check again. The final
	four args set the boundaries for the amount of time the element can
	be zero or one.'''

	while True:
		print(M)
		time.sleep(random.uniform(zeroStart, zeroEnd))
		if M[(pos - 1) % len(M)] == 1 or M[(pos + 1) % len(M)] == 1:
			continue
		else:
			M[pos] = 1
			print(M)
			time.sleep(random.uniform(oneStart, oneEnd))
			M[pos] = 0

# M = [0, 0]
# M = [0] * 8
# M = [1, 1, 1]
# M = [1, 0, 1]
# M = [0, 0, 1, 0]
# inArray = [(M, x) for x in range(len(M))]

# pool = ThreadPool(len(M))
# results = pool.starmap(AvoidantPlay, inArray)
# results = pool.starmap(SimplePlay, inArray)

# Now lets move to 2D

def AvoidantPlay3(M, pos, n, zeroStart, zeroEnd, oneStart, oneEnd):
	i = pos[0]
	j = pos[1]
	while True:
		PrintMatrix(M)
		time.sleep(random.uniform(zeroStart, zeroEnd))
		if neighbours(M, pos) > n - 1:
			continue
		else:
			M[i][j] = 1
			PrintMatrix(M)
			time.sleep(random.uniform(oneStart, oneEnd))
			M[i][j] = 0

def AvoidantPlayWrapped(M, pos, n, zeroStart, zeroEnd, oneStart, oneEnd):
	i = pos[0]
	j = pos[1]
	while True:
		PrintMatrix(M)
		time.sleep(random.uniform(zeroStart, zeroEnd))
		if wrappedNeighbours(M, pos) > n - 1:
			continue
		else:
			M[i][j] = 1
			PrintMatrix(M)
			time.sleep(random.uniform(oneStart, oneEnd))
			M[i][j] = 0

def InversePlay(M, pos, n, zeroStart, zeroEnd, oneStart, oneEnd):
	i = pos[0]
	j = pos[1]
	while True:
		print(M)
		time.sleep(random.uniform(oneStart, oneEnd))
		if neighbours2(M, pos) < 8:
			continue
		else:
			M[i][j] = 0
			print(M)
			time.sleep(random.uniform(zeroStart, zeroEnd))
			M[i][j] = 1

def neighbours(M, pos):
	''' Takes a square (0, 1)-matrix and a position of an element within it
	and returns the number of neighbours to that position which contain 1 not
	0 '''

	# Check whether the input is a matrix
	if not type(M) is np.ndarray:
		print("Warning: Can only take matrices as input, {0} is not \
			a matrix.".format(M))
		return

	# Check whether the position is a tuple
	if not type(pos) is tuple:
		print("Warning: Position must be a tuple. {0} is not \
			a tuple.".format(pos))
		return

	# Check whether the input is a (0, 1)-matrix
	for row in M:
		for element in row:
			if not element == 0 and not element == 1:
				print("Warning: Input must be a (0, 1) matrix. {0} is not \
					a (0, 1)-matrix".format(M))
				return

	# Check whether input is not a jagged array
	checkLength = len(M[0])
	for row in M:
		if len(row) != checkLength:
			print("Warning: Array input must be non-jagged.")
			return

	neighbourSum = 0

	newM = np.zeros(M.shape, dtype=int)
	np.copyto(newM, M)

	row = pos[0] + 1
	col = pos[1] + 1

	newM = np.insert(newM, 0, 0, axis=1)
	newM = np.insert(newM, newM.shape[1], 0, axis=1)

	zeros = np.zeros((1, newM.shape[1]), dtype=int)

	newM = np.concatenate((zeros, newM))
	newM = np.concatenate((newM, zeros))

	m = newM[row - 1:row + 2, col - 1:col + 2]

	m[1][1] = 0

	for ro in m:
		for ele in ro:
			neighbourSum += ele

	return neighbourSum

def neighbours2(M, pos):
	''' Takes a square (0, 1)-matrix and a position of an element within it
	and returns the number of neighbours to that position which contain 1 not
	0 (edges are counted as neighbours)'''

	# Check whether the input is a matrix
	if not type(M) is np.ndarray:
		print("Warning: Can only take matrices as input, {0} is not \
			a matrix.".format(M))
		return

	# Check whether the position is a tuple
	if not type(pos) is tuple:
		print("Warning: Position must be a tuple. {0} is not \
			a tuple.".format(pos))
		return

	# Check whether the input is a (0, 1)-matrix
	for row in M:
		for element in row:
			if not element == 0 and not element == 1:
				print("Warning: Input must be a (0, 1) matrix. {0} is not \
					a (0, 1)-matrix".format(M))
				return

	# Check whether input is not a jagged array
	checkLength = len(M[0])
	for row in M:
		if len(row) != checkLength:
			print("Warning: Array input must be non-jagged.")
			return

	neighbourSum = 0

	newM = np.zeros(M.shape, dtype=int)
	np.copyto(newM, M)

	row = pos[0] + 1
	col = pos[1] + 1

	newM = np.insert(newM, 0, 1, axis=1)
	newM = np.insert(newM, newM.shape[1], 1, axis=1)

	ones = np.ones((1, newM.shape[1]), dtype=int)

	newM = np.concatenate((ones, newM))
	newM = np.concatenate((newM, ones))

	m = newM[row - 1:row + 2, col - 1:col + 2]

	m[1][1] = 0

	for ro in m:
		for ele in ro:
			neighbourSum += ele

	return neighbourSum

def wrappedNeighbours(M, pos):
	''' Takes a square (0, 1)-matrix and a position of an element within it
	and returns the number of neighbours to that position which contain 1 not
	0. The matrix is wrapped on all sides.'''

	# Check whether the input is a matrix
	if not type(M) is np.ndarray:
		print("Warning: Can only take matrices as input, {0} is not \
			a matrix.".format(M))
		return

	# Check whether the position is a tuple
	if not type(pos) is tuple:
		print("Warning: Position must be a tuple. {0} is not \
			a tuple.".format(pos))
		return

	# Check whether the input is a (0, 1)-matrix
	for row in M:
		for element in row:
			if not element == 0 and not element == 1:
				print("Warning: Input must be a (0, 1) matrix. {0} is not \
					a (0, 1)-matrix".format(M))
				return

	# Check whether input is not a jagged array
	checkLength = len(M[0])
	for row in M:
		if len(row) != checkLength:
			print("Warning: Array input must be non-jagged.")
			return

	neighbourSum = 0

	newM = np.zeros(M.shape, dtype=int)
	np.copyto(newM, M)

	row = pos[0] + 1
	col = pos[1] + 1

	# attach the leftmost column to the right of the array,
	# and vice versa.
	newM = np.insert(newM, 0, M[:, -1], axis=1)
	newM = np.insert(newM, newM.shape[1], M[:, 0], axis=1)

	#zeros = np.zeros((1, newM.shape[1]), dtype=int)

	# attach the bottom row to the top and vice versa, (Note:
	# opposite corners touch when the array is wrapped)
	top = M[0, :]
	bottom = M[-1, :]

	# put the corners in
	tLast = top[-1]
	tFirst = top[0]
	top = np.insert(top, 0, tLast)
	top = np.insert(top, len(top), tFirst)
	top = np.reshape(top, (1, top.shape[0]))

	# and for the bottom
	bLast = bottom[-1]
	bFirst = bottom[0]
	bottom = np.insert(bottom, 0, bLast)
	bottom = np.insert(bottom, len(bottom), bFirst)
	bottom = np.reshape(bottom, (1, bottom.shape[0]))
	
	newM = np.concatenate((bottom, newM))
	newM = np.concatenate((newM, top))

	# take a slice of the position and its neighbours
	m = newM[row - 1:row + 2, col - 1:col + 2]

	# don't count the position itself in the sum
	m[1][1] = 0

	for ro in m:
		for ele in ro:
			neighbourSum += ele

	return neighbourSum

def PrintWrap(M):
	''' Takes an array M and prints 3 M's by 3 M's
	to imply wrapping '''

	threeM = ""

	for l in range(3):
		for i in range(M.shape[0]):
			for s in range(3):
				for j in range(M.shape[1]):
					threeM += str(M[i][j])
				if s != 2:
					threeM += "|"
			threeM += "\n"
		if l != 2:
			threeM += "-" * M.shape[1] * 3
			threeM += "--"
			threeM += "\n"

	print(threeM)

def PrintMatrix(M):
	''' Takes an array M and prints it '''

	m_string = ""

	for i in range(M.shape[0]):
		for j in range(M.shape[1]):
			m_string += str(M[i][j])
			m_string += " "
		m_string += "\n"

	print(m_string)

# M = np.array([[0, 0], [0, 0]])
M = np.zeros((10, 10), dtype=int)
# M = np.ones((5, 5), dtype=int)
n = 1
zeroStart = oneStart = 0.1
zeroEnd = oneEnd = 5

inArray = [(M, (i, j), n, zeroStart, zeroEnd, oneStart, oneEnd) for i in range(len(M))\
for j in range(len(M[0]))]

pool = ThreadPool(100)
results = pool.starmap(AvoidantPlay3, inArray)

def deprecated(fun):
	def wrapped_fun(*args, **kwargs):
		print("Warning: function %s is deprecated." %fun)
		return fun(*args, **kwargs)
	return wrapped_fun








































