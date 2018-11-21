
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
		res = list(self.neural.mata_data(*args))
		choice = res.index(max(res))


		# # print("res: {}, choice: {}".format(res, choice))
		# if res[0] < 1/3: self.turn_left()
		# if res[0] > 2/3: self.turn_right()
		if choice == 1: self.turn_left()	
		if choice == 2: self.turn_right()

	def buff(self):
		self.growing = 1

	def get_direction_of_left(self, facing=None):
		if facing is None: 
			facing = self.facing
		# --> [1, 0]
		# ^ [0, -1]
		# <-- [-1, 0]
		# v [0, 1]

		### moving in X direction
		if facing[0] != 0:
			return [0, facing[0] * -1]


		### moving in Y direction
		else:
			return [facing[1], 0]

	def get_direction_of_right(self):
		return self.get_direction_of_left(facing=self.get_direction_of_left(facing=self.get_direction_of_left()))

	def turn_left(self):
		self.facing = self.get_direction_of_left()

	def turn_right(self):
		for _ in range(3): self.turn_left()
	
	def get_coord_facing(self):
		return [self.body[0][0] + self.facing[0], self.body[0][1] + self.facing[1]]

	def get_coord_left(self):
		left = self.get_direction_of_left()
		return [self.body[0][0] + left[0], self.body[0][1] + left[1]]

	def get_coord_right(self):
		right = self.get_direction_of_right()
		return [self.body[0][0] + right[0], self.body[0][1] + right[1]]

	def take_a_step(self):
		self.body = [(self.get_coord_facing()[0], self.get_coord_facing()[1])] + \
			(self.body if self.growing else self.body[:-1])
		self.growing = False