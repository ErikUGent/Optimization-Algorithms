# Solution for Travelling Salesman Problem using SPHERE based Sphere Algorithm

from operator import attrgetter
import random, sys, time, copy
import numpy as np

class Graph:

	def __init__(self, amount_vertices):
		self.edges = {} 
		self.vertices = set() 
		self.amount_vertices = amount_vertices 

	def addEdge(self, src, dest, cost = 0):
		# check the edge already exists
		if not self.existsEdge(src, dest):
			self.edges[(src, dest)] = cost
			self.vertices.add(src)
			self.vertices.add(dest)

	# checks if exists a edge linking "src" in "dest"
	def existsEdge(self, src, dest):
		return (True if (src, dest) in self.edges else False)

	def showGraph(self):
		print('Showing the graph:\n')
		for edge in self.edges:
			print('%d linked in %d with cost %d' % (edge[0], edge[1], self.edges[edge]))

	# returns total cost of the path
	def getCostPath(self, path):
		
		total_cost = 0
		for i in range(self.amount_vertices - 1):
			total_cost += self.edges[(path[i], path[i+1])]

		# add cost of the last edge
		total_cost += self.edges[(path[self.amount_vertices - 1], path[0])]
		return total_cost

	def getRandomPaths(self, max_size):

		random_paths, list_vertices = [], list(self.vertices)

		initial_vertice = random.choice(list_vertices)
		if initial_vertice not in list_vertices:
			print('Error: initial vertice %d not exists!' % initial_vertice)
			sys.exit(1)

		list_vertices.remove(initial_vertice)
		list_vertices.insert(0, initial_vertice)

		for i in range(max_size):
			list_temp = list_vertices[1:]
			random.shuffle(list_temp)
			list_temp.insert(0, initial_vertice)

			if list_temp not in random_paths:
				random_paths.append(list_temp)

		return random_paths

class CompleteGraph(Graph):

	def generates(self):
		for i in range(self.amount_vertices):
			for j in range(self.amount_vertices):
				if i != j:
					weight = random.randint(1, 10)
					self.addEdge(i, j, weight)

class Particle:

	def __init__(self, solution, cost):

		# current solution
		self.solution = solution

		# best solution (fitness) it has achieved so far
		self.pbest = solution

		# set costs
		self.cost_current_solution = cost
		self.cost_pbest_solution = cost

		self.velocity = []

	# set pbest
	def setPBest(self, new_pbest):
		self.pbest = new_pbest

	# returns the pbest
	def getPBest(self):
		return self.pbest

	# set the new velocity (sequence of swap operators)
	def setVelocity(self, new_velocity):
		self.velocity = new_velocity

	# returns the velocity (sequence of swap operators)
	def getVelocity(self):
		return self.velocity

	# set solution
	def setCurrentSolution(self, solution):
		self.solution = solution

	# gets solution
	def getCurrentSolution(self):
		return self.solution

	# set cost pbest solution
	def setCostPBest(self, cost):
		self.cost_pbest_solution = cost

	# gets cost pbest solution
	def getCostPBest(self):
		return self.cost_pbest_solution

	# set cost current solution
	def setCostCurrentSolution(self, cost):
		self.cost_current_solution = cost

	# gets cost current solution
	def getCostCurrentSolution(self):
		return self.cost_current_solution

	# removes all elements of the list velocity
	def clearVelocity(self):
		del self.velocity[:]

# Sphere algorithm
class SPHERE:

	def __init__(self, graph, iterations, size_population, r2=6, r1=2):
		self.graph = graph 
		self.iterations = iterations 
		self.size_population = size_population 
		self.particles = [] 
		self.beta = (2*np.pi*r1)/60 # the probability that all swap operators in swap sequence (gbest - x(t-1))
		self.alfa = (2*np.pi*r2)/60 # the probability that all swap operators in swap sequence (pbest - x(t-1))

		# initialized with a group of random particles (solutions)
		solutions = self.graph.getRandomPaths(self.size_population)

		# checks if exists any solution
		if not solutions:
			print('Initial population empty! Try run the algorithm again...')
			sys.exit(1)

		# creates the particles and initialization of swap sequences in all the particles
		for solution in solutions:
			# creates a new particle
			particle = Particle(solution=solution, cost=graph.getCostPath(solution))
			# add the particle
			self.particles.append(particle)

		# updates "size_population"
		self.size_population = len(self.particles)


	# set gbest (best particle of the population)
	def setGBest(self, new_gbest):
		self.gbest = new_gbest

	# returns gbest (best particle of the population)
	def getGBest(self):
		return self.gbest

	def run(self):
		def breed(parent1, parent2, crossoverRate):
			child = []
			childP1 = []
			childP2 = []

			geneA = int(random.random()*len(parent1))
			geneB = int(random.random()*len(parent1))
		
			startGene = min(geneA, geneB)
			endGene = max(geneA, geneB)

			for i in range(startGene, endGene):
				crossover_prob=np.random.rand()
				if crossoverRate>=crossover_prob:
					childP1.append(parent1[i])

			childP2 = [item for item in parent2 if item not in childP1]
			child = childP1 + childP2	
			return child
		
		# for each time step (iteration)
		for t in range(self.iterations):

			# updates gbest (best particle of the population)
			self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

			# for each particle in the swarm
			for particle in self.particles:

#				particle.clearVelocity() # cleans the speed of the particle
				solution_gbest = copy.copy(self.gbest.getPBest()) # gets solution of the gbest
				solution_pbest = particle.getPBest()[:] # copy of the pbest solution
				solution_particle = particle.getCurrentSolution()[:] # gets copy of the current solution of the particle

				for i in range(self.graph.amount_vertices):
					if random.random() <= self.alfa:
						# makes the swap
						solution_particle = breed(solution_particle, solution_pbest, self.alfa)						
						aux = solution_particle 
				
				for i in range(self.graph.amount_vertices):
					if random.random() <= self.beta:
						# makes the swap
						solution_particle = breed(solution_particle, solution_gbest, self.beta)						
						aux = solution_particle 
				
				# updates the current solution
				particle.setCurrentSolution(solution_particle)
				# gets cost of the current solution
				cost_current_solution = self.graph.getCostPath(solution_particle)
				# updates the cost of the current solution
				particle.setCostCurrentSolution(cost_current_solution)

				# checks if current solution is pbest solution
				if cost_current_solution < particle.getCostPBest():
					particle.setPBest(solution_particle)
					particle.setCostPBest(cost_current_solution)
		

if __name__ == "__main__":
	
	# creates the Graph instance
	graph = Graph(amount_vertices=10)

	# This graph is in the folder "images" of the repository.
	graph.addEdge(0, 1, 5)
	graph.addEdge(1, 0, 5)
	graph.addEdge(0, 2, 6)
	graph.addEdge(2, 0, 6)
	graph.addEdge(0, 3, 4)
	graph.addEdge(3, 0, 4)
	graph.addEdge(0, 4, 2)
	graph.addEdge(4, 0, 2)
	graph.addEdge(0, 5, 9)
	graph.addEdge(5, 0, 9)
	graph.addEdge(0, 6, 3)
	graph.addEdge(6, 0, 3)
	graph.addEdge(0, 7, 6)
	graph.addEdge(7, 0, 6)
	graph.addEdge(0, 8, 2)
	graph.addEdge(8, 0, 2)
	graph.addEdge(0, 9, 3)
	graph.addEdge(9, 0, 3)
	graph.addEdge(1, 2, 1)
	graph.addEdge(2, 1, 1)
	graph.addEdge(1, 3, 4)
	graph.addEdge(3, 1, 4)
	graph.addEdge(1, 4, 6)
	graph.addEdge(4, 1, 6)
	graph.addEdge(1, 5, 3)
	graph.addEdge(5, 1, 3)	
	graph.addEdge(1, 6, 4)
	graph.addEdge(6, 1, 4)
	graph.addEdge(1, 7, 2)
	graph.addEdge(7, 1, 2)	
	graph.addEdge(1, 8, 4)
	graph.addEdge(8, 1, 4)
	graph.addEdge(1, 9, 3)
	graph.addEdge(9, 1, 3)		
	graph.addEdge(2, 3, 5)
	graph.addEdge(3, 2, 5)
	graph.addEdge(2, 4, 4)
	graph.addEdge(4, 2, 4)
	graph.addEdge(2, 5, 2)
	graph.addEdge(5, 2, 2)
	graph.addEdge(2, 6, 5)
	graph.addEdge(6, 2, 5)
	graph.addEdge(2, 7, 2)
	graph.addEdge(7, 2, 2)
	graph.addEdge(2, 8, 3)
	graph.addEdge(8, 2, 3)
	graph.addEdge(2, 9, 5)
	graph.addEdge(9, 2, 5)
	graph.addEdge(3, 4, 3)
	graph.addEdge(4, 3, 3)
	graph.addEdge(3, 5, 8)
	graph.addEdge(5, 3, 8)
	graph.addEdge(3, 6, 7)
	graph.addEdge(6, 3, 7)
	graph.addEdge(3, 7, 2)
	graph.addEdge(7, 3, 2)
	graph.addEdge(3, 8, 7)
	graph.addEdge(8, 3, 7)
	graph.addEdge(3, 9, 4)
	graph.addEdge(9, 3, 4)
	graph.addEdge(4, 5, 10)
	graph.addEdge(5, 4, 10)
	graph.addEdge(4, 6, 9)
	graph.addEdge(6, 4, 9)
	graph.addEdge(4, 7, 5)
	graph.addEdge(7, 4, 5)
	graph.addEdge(4, 8, 6)
	graph.addEdge(8, 4, 6)
	graph.addEdge(4, 9, 6)
	graph.addEdge(9, 4, 6)
	graph.addEdge(5, 6, 1)
	graph.addEdge(6, 5, 1)
	graph.addEdge(5, 7, 12)
	graph.addEdge(7, 5, 12)
	graph.addEdge(5, 8, 10)
	graph.addEdge(8, 5, 10)
	graph.addEdge(5, 9, 2)
	graph.addEdge(9, 5, 2)
	graph.addEdge(6, 7, 1)
	graph.addEdge(7, 6, 1)
	graph.addEdge(6, 8, 8)
	graph.addEdge(8, 6, 8)
	graph.addEdge(6, 9, 9)
	graph.addEdge(9, 6, 9)
	graph.addEdge(7, 8, 2)
	graph.addEdge(8, 7, 2)
	graph.addEdge(7, 9, 3)
	graph.addEdge(9, 7, 3)
	graph.addEdge(8, 9, 7)
	graph.addEdge(9, 8, 7)

	# creates a SPHERE instance
	start_time = time.time()
	sphere = SPHERE(graph, iterations=500, size_population=50, r2=10, r1=5)
	sphere.run() # runs the Sphere algorithm

	# shows the global best particle
	print('gbest: %s | cost: %d\n' % (sphere.getGBest().getPBest(), sphere.getGBest().getCostPBest()))
	print('the elapsed time:%s'% (round(time.time() - start_time, 4)))
