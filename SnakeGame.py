import pygame
from pygame.locals import *

from Snake import Snake
from NeuralString import Neural

from random import randint

class Colors:
	BLACK = pygame.Color(0, 0, 0)
	WHITE = pygame.Color(255, 255, 255)
	RED = pygame.Color(255, 0, 0)
	GREEN = pygame.Color(0, 255, 0)
	BLUE = pygame.Color(0, 0, 255)

class Game:
	def __init__(self, snakes):
		self.snakes = snakes
		self.width = 15
		self.height = 15
		self.clear_board()
		self.food = [8, 8]
		self.alive_snakes = len(snakes)

	def print_board(self):
		for row in self.board:
			for value in row:
				print("0" if value is None else value[0], end=" ")
			print()

	def clear_board(self):
		self.board = [[None for _ in range(self.width)] for _ in range(self.height)]

	def kill_snake(self, snake):
		self.alive_snakes -= 1
		snake.score -= 25
		snake.dead = True

	def reset_food(self):
		self.food = [randint(1, self.width-1), randint(1, self.height-1)]

	def over(self):
		return self.alive_snakes == 0

	def update(self):
		# rensa boarden
		# uppdatera ormarna
		# rita ut ormarna
		# rita ut maten


		self.clear_board()

		for snake in self.snakes:
			if snake.dead:
				continue

			snake.take_a_step()
			# snake.score -= 1

			for part in snake.body[1:]:
				self.board[part[1]][part[0]] = "SNAKE"

			# self.print_board()

			head = snake.body[0]
			if self.is_coord_wall(head) or snake.hunger == snake.hunger_threshold:
				self.kill_snake(snake)
				snake.score -= 50
				continue

			if list(head) == self.food:
				b = snake.score
				snake.score += 15
				# print("before: ", b,", after: ", snake.score)
				snake.food += 1
				snake.hunger = 0
				snake.growing = True
				self.reset_food()

			snake.hunger += 1

			self.board[head[1]][head[0]] = "SNAKE"

		for snake in self.snakes:
			snake.make_decision(self.is_wall_left_of_snake(snake),
								self.is_snake_facing_wall(snake),
								self.is_wall_right_of_snake(snake),
								self.is_food_left_of_snake(snake, self.food),
								self.is_snake_facing_food(snake, self.food),
								self.is_food_right_of_snake(snake, self.food))
								#self.get_distance_head_food(snake, self.food))

		self.board[self.food[1]][self.food[0]] = "FOOD"

	def is_coord_wall(self, coord):
		return (coord[1] < 0 or coord[1] >= self.width or
				coord[0] < 0 or coord[0] >= self.height or
				self.board[coord[1]][coord[0]] == "SNAKE")

	def get_distance_head_food(self, snake, food):
		return abs(abs(snake.body[0][0]) - abs(food[0]))  +abs(abs(snake.body[0][1]) - abs(food[1]))

	def is_wall_left_of_snake(self, snake):
		return self.is_coord_wall(snake.get_coord_left())

	def is_wall_right_of_snake(self, snake):
		return self.is_coord_wall(snake.get_coord_right())

	def is_snake_facing_wall(self, snake):
		return self.is_coord_wall(snake.get_coord_facing())

	def is_food_left_of_snake(self, snake, food):
		return self.is_food_in_direction(snake, food, snake.get_direction_of_left())

	def is_food_right_of_snake(self, snake, food):
		return self.is_food_in_direction(snake, food, snake.get_direction_of_right())

	def is_snake_facing_food(self, snake, food):
		return self.is_food_in_direction(snake, food, snake.facing)

	def is_food_in_direction(self, snake, food, direction):
		head_at = snake.body[0]
		sign = lambda a: a>0
		if head_at[1] == food[1]:
			if direction[0] > 0:
				return food[0] > head_at[0]
			elif direction[0] < 0:
				return food[0] < head_at[0]
		if head_at[0] == food[0]:
			if direction[1] > 0:
				return food[1] > head_at[1]
			elif direction[1] < 0:
				return food[1] < head_at[1]
		return False

	def draw(self, window, x_offset, y_offset):
		for y, row in enumerate(self.board):
			for x, column in enumerate(row):
				elem = self.board[y][x]
				rect = (x_offset + 10*x, y_offset + 10*y, 8, 8)
				if elem == None:
					pygame.draw.rect(window, Colors.WHITE, rect)
				elif elem == "SNAKE":
					pygame.draw.rect(window, Colors.BLUE, rect)
				elif elem == "FOOD":
					pygame.draw.rect(window, Colors.RED, rect)
				# else:
				# 	pygame.draw.rect(window, Colors.GREEN, rect)


if __name__ == "__main__":
	pygame.init()
	clock = pygame.time.Clock()
	window = pygame.display.set_mode((640, 480))

	neural = Neural()
	snake = Snake(5, 5, neural)
	game = Game([snake])
	step_max = 150
	while True:
		window.fill(Colors.BLACK)
		if game.over():
			break
		game.update()
		game.draw(window, 0, 0)
		pygame.display.update()
		clock.tick(5)

	print("DONE")