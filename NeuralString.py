from random import randint, random
import numpy as np

class bcolors:
	""" Class with static color strings. Prepend any text with a color to change it. Make sure to always append ENDC afterwards. """
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	ENDC = '\033[0m'

class Neural:
	""" A string representation of a Neural Network. """
	
	def __init__(self, n_in=6, n_hidden=4, n_out=3, bits_per_axon=8, snake=""):
		""" Creates a Neural instance. If 'snake' is given it will just be snake, otherwise
			a bitstring of length n_in*n_hidden*n_out*bits_per_axon will be generated.' """
		self.n_in = n_in
		self.n_hidden = n_hidden
		self.n_out = n_out
		self.bits_per_axon = bits_per_axon

		if snake == "":
			self.a_in = [str(randint(0,1)) for _ in range(bits_per_axon*(n_in * n_hidden))]
			self.a_out = [str(randint(0,1)) for _ in range(bits_per_axon*(n_hidden * n_out))]
			self.snake = self.a_in + self.a_out
		else:
			self.a_in = snake[:bits_per_axon*(n_in*n_hidden)]
			self.a_out = snake[bits_per_axon*(n_in*n_hidden):]
			self.snake = snake

		self.length = len(self.snake)

		self.w1 = self.get_weight_matrix(self.a_in)
		self.w2 = self.get_weight_matrix(self.a_out)

	def mata_data(self, *data):
		""" Passing the input data through the neural network. """
		f = np.matmul([*data], self.w1)
		s = np.matmul(f, np.transpose(self.w2))
		# res = np.matmul(np.matmul([*data], self.w1), np.transpose(self.w2))
		res = s
		# print(*data)
		return res

	def mutate(s1):
		""" 
			Currently unused: see overcross.
			Mutations are introduced by flipping bits at random throughout the 'snake'.
		"""
		s2 = "".join([b if random()<0.1 else str(1-int(b)) for b in s1.neural.snake])
		return Neural(snake=s2)

	def overcross(s1, s2, mutate=False):
		"""
			Creates a new 'snake' from two given 'snakes' by splitting at the same index and concatting.

			If mutate is set, the result 'snake' will be affected by mutation.

			More info: https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
		"""
		cut_off = randint(0,len(s1.neural.snake))
		s3 = s1.neural.snake[:cut_off] + s2.neural.snake[cut_off:]

		if mutate:
			s3 = [b if random() < 0.01 else str(1-int(b)) for b in s3]
		return Neural(snake=s3)

	def procreate(s1, s2):
		""" Creates a new Neural using two parent Neural. """
		if s1.neural.length != s2.neural.length:
			raise Error("Snakes are not the same size!?")

		s3 = []
		step = s1.neural.bits_per_axon
		for ni in range(0, s1.neural.length, step):
			child = s1.neural.snake[ni:ni+step] if randint(0, 1) else s2.neural.snake[ni:ni+step]
			child = "".join([b if random()<0.2 else str(1-int(b)) for b in child])
			s3 += child

		return Neural(s1.neural.n_in, s1.neural.n_hidden, s1.neural.n_out, s1.neural.bits_per_axon, snake="".join(s3))

	def get_weight_matrix(self, part):
		""" Generate a weight matrix using the necessary part of the Neural. """
		step = self.bits_per_axon * self.n_hidden
		inner_step = self.bits_per_axon

		w = []

		for ni in range(0, len(part), step):
			string_weights = part[ni:ni+step]
			list_weights = []
			for wi in range(0, len(string_weights), inner_step):
				axon = string_weights[wi:wi+inner_step]
				weight = int("".join(axon), 2) / float(2**self.bits_per_axon-1)
				list_weights.append(weight)
			w.append(list_weights)

		return w

	def __str__(self):
		return """{blue}{axons_in}{green}{axons_out}{endc}""".format(axons_in="".join(self.a_in),
			 axons_out="".join(self.a_out),
			 blue=bcolors.BLUE,
			 green=bcolors.GREEN,
			 endc=bcolors.ENDC)

if __name__ == "__main__":

	a = Neural(1, 1, 1, 8)
	b = Neural(1, 1, 1, 8)
	Neural.overcross(a, b, mutate=True)

	# b = Neural(3, 2, 3, 8, snake=a.snake)
	# print(b)

	# c = Neural.procreate(a, b)
	# print(c)