import random
from copy import deepcopy
from typing import Callable
from Model.Solution import SportsLeagueSolution
from Model.Solution import Solution



def get_best_ind(population: list[Solution], maximization: bool):
    fitness_list = [ind.fitness() for ind in population]
    if maximization:
        return population[fitness_list.index(max(fitness_list))]
    else:
        return population[fitness_list.index(min(fitness_list))]

def genetic_algorithm(
    initial_population: list[Solution],
    max_gen: int,
    selection_algorithm: Callable,
    maximization: bool = False,
    xo_prob: float = 0.9,
    mut_prob: float = 0.2,
    elitism: bool = True,
    verbose: bool = False,
):
    """
    Executes a genetic algorithm to optimize a population of solutions.

    Args:
        initial_population (list[Solution]): The starting population of solutions.
        max_gen (int): The maximum number of generations to evolve.
        selection_algorithm (Callable): Function used for selecting individuals.
        maximization (bool, optional): If True, maximizes the fitness function; otherwise, minimizes. Defaults to False.
        xo_prob (float, optional): Probability of applying crossover. Defaults to 0.9.
        mut_prob (float, optional): Probability of applying mutation. Defaults to 0.2.
        elitism (bool, optional): If True, carries the best individual to the next generation. Defaults to True.
        verbose (bool, optional): If True, prints detailed logs for debugging. Defaults to False.

    Returns:
        Solution: The best solution found on the last population after evolving for max_gen generations.
        list[float]: The fitness of the best individual over the generations
    """
    best_fitness_over_gens = []

    # 1. Initialize a population with N individuals
    population = initial_population

    # 2. Repeat until termination condition
    for gen in range(1, max_gen + 1):
        if verbose:
            print(f'-------------- Generation: {gen} --------------')

        # 2.1. Create an empty population P'
        new_population = []

        # 2.2. If using elitism, insert best individual from P into P'
        if elitism:
            new_population.append(deepcopy(get_best_ind(population, maximization)))
        
        # 2.3. Repeat until P' contains N individuals
        while len(new_population) < len(population):
            # 2.3.1. Choose 2 individuals from P using a selection algorithm
            first_ind = selection_algorithm(population, maximization)
            second_ind = selection_algorithm(population, maximization)

            if verbose:
                print(f'Selected individuals:\n{first_ind}\n{second_ind}')

            # 2.3.2. Choose an operator between crossover and replication
            # 2.3.3. Apply the operator to generate the offspring
            if random.random() < xo_prob:
                offspring1, offspring2 = first_ind.crossover(second_ind)
                if verbose:
                    print(f'Applied crossover')
            else:
                offspring1, offspring2 = deepcopy(first_ind), deepcopy(second_ind)
                if verbose:
                    print(f'Applied replication')
            
            if verbose:
                print(f'Offspring:\n{offspring1}\n{offspring2}')
            
            # 2.3.4. Apply mutation to the offspring
            first_new_ind = offspring1.mutation(mut_prob)
            # 2.3.5. Insert the mutated individuals into P'
            new_population.append(first_new_ind)

            if verbose:
                print(f'First mutated individual: {first_new_ind}')
            
            if len(new_population) < len(population):
                second_new_ind = offspring2.mutation(mut_prob)
                new_population.append(second_new_ind)
                if verbose:
                    print(f'Second mutated individual: {second_new_ind}')
        
        # 2.4. Replace P with P'
        population = new_population

        if verbose:
            print(f'Final best individual in generation: {get_best_ind(population, maximization).fitness()}')
        
        best_ind = get_best_ind(population, maximization)
        best_fitness_over_gens.append(best_ind.fitness())

    # 3. Return the best individual in P + the best individual fitness over generations
    return get_best_ind(population, maximization), best_fitness_over_gens



class SportsLeagueGASolution(SportsLeagueSolution):

    def __init__(self, mutation_function, crossover_function, players_df, repr = None): # mutation_function: Callable, crossover_function: Callable
        super().__init__(players_df=players_df, repr=repr)
        self.players_df = players_df 

        # Save as attributes for access in methods
        self.mutation_function = mutation_function
        self.crossover_function = crossover_function


    # crossover
    def crossover(self, other_solution):
        # Apply crossover function to self representation and other solution representation
        offspring1_repr, offspring2_repr = self.crossover_function(self.repr, other_solution.repr, self.players_df)

        return (
            SportsLeagueGASolution(repr=offspring1_repr,
                                   mutation_function=self.mutation_function,
                                   crossover_function=self.crossover_function,
                                   players_df=self.players_df),
            SportsLeagueGASolution(repr=offspring2_repr,
                                   mutation_function=self.mutation_function,
                                   crossover_function=self.crossover_function,
                                   players_df=self.players_df)
        )


    # mutation
    def mutation(self, mut_prob):
        if random.random() < mut_prob:
             # Perform some actual mutation on self.repr
             mutated_repr = self.mutation_function(self)
             return SportsLeagueGASolution(repr=mutated_repr.repr,
                                          mutation_function=self.mutation_function,
                                          crossover_function=self.crossover_function,
                                          players_df=self.players_df)
        else:
             return deepcopy(self)
        
