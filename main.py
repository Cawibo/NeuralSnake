import pygame, sys, random
from pygame.locals import *
from SnakeGame import Game
from Snake import Snake
from NeuralString import Neural
from random import choice
import numpy


def generate_minds(n):
	return [Neural() for _ in range(n)]

def create_snakes(n):
	return [Snake(5, 5, mind) for mind in generate_minds(n)]

def create_games(n, snakes):
	return [Game([snake]) for snake in snakes]

def evaluate_generation(snakes):
	games = create_games(len(snakes), snakes)
	running_count = len(snakes)

	while running_count > 0:
		for game in games:
			game.update()
			if game.over():
				running_count -= 1

	games = sorted(games, key=lambda game:game.snakes[0].score, reverse=True)
	return [snake for snake in [game.snakes[0] for game in games]]

# def test(n, gens, times):

# 	data = [0 for _ in range(gens)]

# 	for t in range(times):
# 		snakes = create_snakes(n)
# 		for gen in range(gens):		
# 			snakes = evaluate_generation(snakes)

# 			food_list = [s.food for s in snakes]
# 			data[gen] += max(food_list)

# 			survivors = snakes[:n//10]		

# 			snakes = survivors +\
# 				[Snake(5, 5, Neural.overcross(choice(survivors), choice(survivors), mutate=True)) for _ in range(n-len(survivors))]

# 		print(t/times*100, "% done")
# 	return [d/times for d in data]

# import matplotlib.pyplot as plt
# import pylab

# data = test(1000, 100, 100)
# for row in data:
# 	print(row)

# fig = plt.figure()
# plt.plot(data)
# plt.show()

if __name__ == "__main__":
	pygame.init()
	clock = pygame.time.Clock()

	data = []

	window = pygame.display.set_mode((640, 480))
	n = 100
	snakes = create_snakes(n)
	counter = 0
	while True and counter <= 10000000:
		counter += 1
		snakes = evaluate_generation(snakes)
		
		best = snakes[0]
		worst = snakes[len(snakes)-1]

		print("max: {}, min: {}".format(
			best.score,
			worst.score))

		for s in snakes[:10]:
			print("score: ", s.score)

		games = [Game([Snake(5, 5, best.neural)]),
				Game([Snake(5, 5, snakes[1].neural)])]#, Game([Snake(5, 5, worst.neural)])
		while True and counter >= 10:
			window.fill(pygame.Color(0, 0, 0))
			alive = 0
			for gi, game in enumerate(games):
				alive += game.alive_snakes
				if game.over():
					continue
				game.update()
				game.draw(window, 10 + 170*gi, 10 )
			pygame.display.update()
			clock.tick(150)
			if not alive:
				break

		food_list = [s.food for s in snakes]
		filtered_list = [s.food for s in snakes if s.food >= 1]

		data.append([
			counter,
			max(snakes, key=lambda s:s.food).food,
			sum(food_list)/10,
			numpy.median(food_list),
			numpy.median(filtered_list)
			])

		# remova all below 0 score
		# rest = list(filter(lambda snake:snake.score > 0, snakes[:n//2]))
		survivors = snakes[:n//10]

		# if not rest:
		# 	rest = create_snakes(n)
		

		snakes = survivors +\
			[Snake(5, 5, Neural.overcross(choice(survivors), choice(survivors), mutate=True)) for _ in range(n-len(survivors))]
		print(len(snakes))
		# snakes = survivors +\
		# 	[Snake(5, 5, Neural.overcross(choice(survivors), choice(survivors), mutate=True)) for _ in range(n-len(survivors))]survivors

	# print(data)
	# with open("data10.out", "a") as f:
	# 	for gen in data:
	# 		print(gen)
	# 		f.write(", ".join(map(str, gen)))
	# 		f.write("\n")