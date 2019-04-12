
class Snake():
	INITIAL_LENGTH = 5

	def __init__(self, x, y, neural):
		self.facing = [1, 0]
		self.body = [[x-self.facing[0]*i, y-self.facing[1]*i] for i in range(Snake.INITIAL_LENGTH)]
		self.score = 0
		self.ranking = -1
		self.neural = neural
		self.dead = False
		self.growing = False
		self.hunger = 0
		self.hunger_threshold = 50
		self.food = 0

	def make_decision(self, *args):
		""" Use current 'state'/'situation' to make a decision using this snakes innate neural network """
		res = list(self.neural.mata_data(*args))
		choice = res.index(max(res))

		if choice == 1: self.turn_left()	
		if choice == 2: self.turn_right()

	def buff(self):
		""" Make the snake grow once """
		self.growing = 1

	def get_direction_of_left(self, facing=None):
		""" Returns the direction 'left' of currently faced direction """
		# --> [1, 0]
		# ^ [0, -1]
		# <-- [-1, 0]
		# v [0, 1]

		if facing is None: 
			facing = self.facing

		### moving in X direction
		if facing[0] != 0:
			return [0, facing[0] * -1]

		### moving in Y direction
		else:
			return [facing[1], 0]

	def get_direction_of_right(self):
		""" Returns the direction 'right' of currently faced direction """
		return self.get_direction_of_left(facing=self.get_direction_of_left(facing=self.get_direction_of_left()))

	def turn_left(self):
		""" Turns the snake 'left' """
		self.facing = self.get_direction_of_left()

	def turn_right(self):
		""" Turns the snake 'right' """
		for _ in range(3): self.turn_left()
	
	def get_coord_facing(self):
		""" Returns the coordinates of the tile directily infront of the snake """
		return [self.body[0][0] + self.facing[0], self.body[0][1] + self.facing[1]]

	def get_coord_left(self):
		""" Returns the coordinates of the tile directly to the left of the snake """
		left = self.get_direction_of_left()
		return [self.body[0][0] + left[0], self.body[0][1] + left[1]]

	def get_coord_right(self):
		""" Returns the coordinates of the tile directly to the right of the snake """
		right = self.get_direction_of_right()
		return [self.body[0][0] + right[0], self.body[0][1] + right[1]]

	def take_a_step(self):
		""" Makes the snake go forward one tile in the direction it is facing """
		self.body = [(self.get_coord_facing()[0], self.get_coord_facing()[1])] + \
			(self.body if self.growing else self.body[:-1])
		self.growing = False