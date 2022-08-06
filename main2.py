import cv2 as cv
import numpy as np
import random
import heapq
import time

def addLine(image, start, end, color, thickness, alpha):
	overlay = image.copy()

	line = cv.line(overlay, start, end, color, thickness)

	image_new = cv.addWeighted(overlay, alpha, image, 1 - alpha, 0)

	return(image_new)

def getRandomLine(image):
	h, w, _ = image.shape
	start = (random.randrange(0, w), random.randrange(0, h))
	end = (random.randrange(0, w), random.randrange(0, h))
	color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
	thickness = random.randrange(1, max(w, h))
	alpha = random.random()

	return (start, end, color, thickness, alpha)

def addRandomLine(image):
	return addLine(*((image,) + getRandomLine(image, i)))

def getScore(image1, image2):
	image1 = image1 - image2

	avg_color_per_row = np.sum(image1, axis=0)
	avg_color = np.sum(avg_color_per_row, axis=0)

	return sum(avg_color)

def getBest(heap, count):
	return heapq.nsmallest(count, heap)

def mutateLine(line, min_multiplier, max_multiplier):
	start, end, color, thickness, alpha = line

	def randomize(value, cast=int):
		return cast(value * random.uniform(min_multiplier, max_multiplier))
	def randomize_tuple(tpl, cast=int):
		return tuple(randomize(v, cast) for v in tpl)

	#line     = randomize(line, float)
	start = randomize_tuple(start)
	end = randomize_tuple(end)
	color = randomize_tuple(color)
	thickness = max(randomize(thickness), 1)
	alpha = randomize(alpha, float)

	return start, end, color, thickness, alpha


def getNextGen(heap, original_image, blank_image):

	for i in range(len(heap)):
		mutated_line = mutateLine(heap[i][1], 0.7, 1.3)
		score = getScore(original_image, addLine(blank_image, *mutated_line))
		heapq.heappush(heap, (score, mutated_line))

	return heap


original_image = cv.imread("mona.jpg")
h, w, _ = original_image.shape
blank_image = np.zeros((h, w, 3), np.uint8)

avg_color_per_row = np.sum(cv.bitwise_not(original_image), axis=0)
avg_color = np.sum(avg_color_per_row, axis=0)

stop = time.time() + 60 * 30

for j in range(100000):
	heap = []
	for i in range(100):
		random_line = getRandomLine(blank_image)
		score = getScore(original_image, addLine(blank_image, *random_line))
		heapq.heappush(heap, (score, random_line))

	for i in range(10):
		heap = heapq.nsmallest(50, heap)
		heap = getNextGen(heap, original_image, blank_image)

		if i%10==0:
			cv.imwrite(f'evo/GENERATION-{str(j).zfill(4)}{str(i).zfill(4)}.jpg', addLine(blank_image, *heap[0][1]))

		if time.time() >= stop:
			print(heap[0][0])
			#cv.imwrite(f'evo/{heap[0][0]}.jpg', blank_image)
			exit()
			

		print(i, j, 100-( 100 * heap[0][0]/sum(avg_color)))

	final_image = addLine(blank_image, *heap[0][1])
	blank_image = final_image

	if j%10000 == 0:
		cv.imwrite(f'evo/GENERATION-{str(j).zfill(4)}.jpg', final_image)
"""
	if j%1==0:

		
"""



"""
for j in range(1000):
	lines = []
	scores = []
	for i in range(500):
		# makes arguments for a random line
		random_line = getRandomLine(blank_image)
		# adds the line to a black image and gets its score
		score = getScore(original_image, addLine(blank_image, *random_line))
		# append line and score to list
		lines.append(random_line)
		scores.append(score)

	for i in range(50):
		# remove 50 worst lines
		lines = getBest(lines, scores, len(lines)//2)
		# add 50 mutated lines
		lines = getNextGen(lines)
		scores = []

		for line in lines:
			# gets scores for each new line
			score = getScore(original_image, addLine(blank_image, *line))
			scores.append(score)

		print(i, j, min(scores))

	# adds the best line to the blank image
	final_image = addLine(*((blank_image,) + getBest(lines, scores, 1)[0]))
	# final image becomes black image for tne next line
	blank_image = final_image

	if j%5==0:

		cv.imshow('window', final_image)

		cv.waitKey(0)
		cv.destroyAllWindows()
"""