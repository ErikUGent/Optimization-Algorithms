# Solution for Travelling Salesman Problem using SPHERE based Sphere Algorithm

from operator import attrgetter
import random, sys, time, copy
import numpy as np
import Distance_40

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

		cost=graph.getCostPath(list_temp)
		print(cost)
		return random_paths

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

	def __init__(self, graph, iterations, size_population, r2, r1):
		self.graph = graph 
		self.iterations = iterations 
		self.size_population = size_population 
		self.particles = [] 
		self.beta = (2*np.pi*r1)/60 # the probability that all swap operators in swap sequence (gbest - x(t-1))
		self.alfa = (2*np.pi*r2)/60 # the probability that all swap operators in swap sequence (pbest - x(t-1))

		solutions = self.graph.getRandomPaths(self.size_population)

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
		
		for t in range(self.iterations):

			# updates gbest (best particle of the population)
			self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

			# for each particle in the swarm
			for particle in self.particles:

#				particle.clearVelocity() # cleans the speed of the particle
				solution_gbest = copy.copy(self.gbest.getPBest()) # gets solution of the gbest
				solution_pbest = particle.getPBest()[:] # copy of the pbest solution
				solution_particle = particle.getCurrentSolution()[:] # gets copy of the current solution of the particle
				
				# generates new solution for particle
				if random.random() <= self.alfa:
						# makes the swap
					solution_particle = breed(solution_particle, solution_pbest, self.alfa)						
							
				if random.random() <= self.beta:
						# makes the swap
					solution_particle = breed(solution_particle, solution_gbest, self.beta)						
				
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
	
	graph = Graph(amount_vertices=42)
	x = Distance_40.main()
	num_cust = 42
	matr = num_cust*num_cust

	for i in range(0, matr):
		vert = x[i]
		start = vert[0]
		end = vert[1]
		dista = vert[2]
		graph.addEdge(start, end, dista)

	start_time = time.time()
	
	for j in range(0, 10):
		sphere = SPHERE(graph, iterations=1000, size_population=750, r2=20, r1=10)
		sphere.run() # runs the Sphere algorithm

		# shows the global best particle
		print('gbest: %s | cost: %d\n' % (sphere.getGBest().getPBest(), sphere.getGBest().getCostPBest()))
	
	print('the elapsed time:%s'% (round(time.time() - start_time, 4)))