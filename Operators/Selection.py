import random
from copy import deepcopy


def tournament_selection(population, maximization = False):

    tournament_size = 4  # for now, it's just a fixed size of 5

    # Randomly sample individuals from population
    sample_population = random.sample(population, tournament_size)
    # Sort by fitness (lowest for minimization)
    sample_population.sort(key=lambda x: x.fitness(), reverse=maximization)

    return sample_population[0]


def ranking_selection(population, maximization=False):
    """
    Ranking selection based on linear rank probabilities.
    
    Args:
        population (list): A list of individuals in the population
    
    Returns:
        list or individual: The selected individual
    """
    sorted_population = sorted(population, key=lambda x: x.fitness(), reverse=True)
    n = len(population)
    ranks = list(range(1, n + 1))  # linear rank

    selected = random.choices(sorted_population, weights=ranks, k=1)
    return deepcopy(selected[0])