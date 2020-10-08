from random import randint as randint, choices as choices, random as random
from sys import byteorder
from copy import deepcopy

class BitManip:
    def __init__(self):
       pass

    def binStrToInt(self, binStr, bin_len):
        val = int(binStr, 2)
        b = val.to_bytes(int(bin_len / 8), byteorder=byteorder, signed=False)                                                          
        return int.from_bytes(b, byteorder=byteorder, signed=True)

    def intToBinStr(self, num, bin_len):
        return format(num if num >= 0 else (1 << bin_len) + num, '0' + str(bin_len) + 'b')


class QuadraticGA:
    def __init__(self, quad_result, pop_sz, chrom_len=8, crossover_prob=0.7, mutation_prob=0.1):
        self.bit = BitManip()
        self.population = []
        self.avg_fitness = 0
        self.fitness_ratio = []
        self.quad_result = quad_result
        self.pop_sz = pop_sz
        self.generation = 1
        self.chrom_len = chrom_len
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.solutions = []
        self.populate()

    def fetch(self, index):
        return self.population[index]

    def populate(self):
        bound = 2 ** self.chrom_len
        for i in range(self.pop_sz):
            num = randint(-bound, bound)
            chromosome = self.bit.intToBinStr(num, self.chrom_len)
            self.population.append({
                'id': i, 'chromosome': chromosome, 'fitness': 0
            })

    # Testing x^2 = 64
    def fitness(self, chromosome):
        decoded_val = self.bit.binStrToInt(chromosome, self.chrom_len) 
        return 1000 - (decoded_val ** 2 - self.quad_result)
    
    def get_fitness_ratio(self):
        self.fitness_ratio = []
        total = sum(indiv['fitness'] for indiv in self.population)
        self.avg_fitness = total / self.pop_sz

        for indiv in self.population:
            self.fitness_ratio.append(indiv['fitness'] / total)

    def crossover(self, indiv1, indiv2):
        if random() > self.crossover_prob:
            return
        break_gene = randint(1, self.chrom_len - 1)
        child1 = indiv1['chromosome'][:break_gene] + indiv2['chromosome'][break_gene:]
        child2 = indiv2['chromosome'][:break_gene] + indiv1['chromosome'][break_gene:]
        indiv1['chromosome'], indiv2['chromosome'] = child1, child2

    def mutate(self, indiv):
        if random() > self.mutation_prob:
            pass
        mutate_point = randint(0, self.chrom_len - 1)
        indiv['chromosome'] = list(indiv['chromosome'])
        indiv['chromosome'][mutate_point] = str(int(not bool(indiv['chromosome'][mutate_point])))
        indiv['chromosome'] = ''.join(indiv['chromosome'])
        
    def roulette(self):
        return choices(self.population, self.fitness_ratio, k=1)

    def select(self):
        select1 = self.roulette()[0]
        select2 = None
        while select2 == None or select1['id'] == select2['id']:
            print('shit')
            select2 = self.roulette()[0]

        return select1, select2

    def status(self):
        print('Generation: {}, fitness: {}'.format(self.generation, self.avg_fitness))

    def decodeSolution(self):
        for solution in self.solutions:
            print('X = ' + str(self.bit.binStrToInt(solution['chromosome'], self.chrom_len)))

    def assignId(self, population):
        for i in range(len(population)):
            population[i]['id'] = i

    def evolve(self):
        while True:
            new_population = []
            size = 0
            fittest = self.population[0]
            # compute fitness
            for indiv in self.population:
                indiv['fitness'] = self.fitness(indiv['chromosome'])
                if indiv['fitness'] >= fittest['fitness']:
                    fittest = indiv
            
            self.get_fitness_ratio()

            # solved?
            if fittest['fitness'] == 1000:
                self.solutions.append(fittest)
            if len(self.solutions) == 2:
                self.decodeSolution()
                break

            while size < self.pop_sz:
                print(self.population)
                self.status()

                # select
                indiv1, indiv2 = self.select()
                self.assignId(new_population)

                # crossover
                self.crossover(indiv, indiv2)
                
                # mutate
                self.mutate(indiv1)
                self.mutate(indiv2)

                new_population.append(indiv1)
                new_population.append(indiv2)

                size += 2
            
            self.population = deepcopy(new_population)
            self.generation += 1


quad = QuadraticGA(64, 20, 8)
quad.evolve()

# x = [3,2,1]

# def test(arr):
#     for i in range(3):
#         arr[i] = i

# test(x)
# print(x)
