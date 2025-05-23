from abc import ABC, abstractmethod
from random import randint, shuffle, choice
from copy import deepcopy

class MutationOperator(ABC):
    @abstractmethod
    def mutate(self, solution):
        pass
    

def player_swap_mutation(solution, verbose=False):
    """
    Applies player swap mutation to a SportsLeagueSolution representation.

    This mutation swaps players in the same position index between two different teams,
    preserving the positional structure of the team.

    Args:
        solution (object): A solution object of SportsLeagueSolution
        verbose (bool): Whether to print debug information.

    Returns:
        object: A mutated copy of the solution.
    """

    new_repr = deepcopy(solution.repr)

    # Choose the id within the team of the player that will be swapped
    player_to_swap = randint(0, 6)

    # Choose the teams where the players will be swapped. Make sure they are different
    team_to_swap_1 = randint(0, 4)
    team_to_swap_2 = randint(0, 4)
    while team_to_swap_1 == team_to_swap_2:
        team_to_swap_2 = randint(0, 4)

    # Extract player IDs before swap for accurate logging
    pid1 = new_repr[team_to_swap_1][player_to_swap]
    pid2 = new_repr[team_to_swap_2][player_to_swap]
    if verbose:
        print(f"Swapping player {pid1} from team {team_to_swap_1} "
            f"with player {pid2} from team {team_to_swap_2}")

    # Swap players at the chosen index
    new_repr[team_to_swap_1][player_to_swap], new_repr[team_to_swap_2][player_to_swap] = pid2, pid1

    mutated = deepcopy(solution)
    mutated.repr = new_repr
    return mutated


def role_shuffle_mutation(solution, verbose=False):
    """
    Shuffles all players of the same role (e.g. all defenders) across teams.

    Args:
        solution (object): A solution object with a `.repr` attribute.
        verbose (bool): Whether to print debug info.

    Returns:
        object: A mutated copy of the solution.
    """
    new_repr = deepcopy(solution.repr)

    # Choose the role that will be affected
    # Remembering that the player IDs withing the team correspond to {"GK": 0, "DEF": [1, 2], "MID": [3, 4], "FWD": [5, 6]}
    i = randint(0, 6)
    if i in [1, 2]:
        i = [1, 2]
    elif i in [3, 4]:
        i = [3, 4]
    elif i in [5, 6]:
        i = [5, 6]
    else:
        i = [0]

    # If verbose, print the role and indexes being shuffled
    if verbose:
        role_map = {
            "GK": [0],
            "DEF": [1, 2],
            "MID": [3, 4],
            "FWD": [5, 6]
        }
        inv_map = {tuple(v): k for k, v in role_map.items()}
        role_name = inv_map[tuple(i)]
        print(f"Shuffling players in role {role_name}, corresponding to indexes {i}")

    # Remove all the players from the selected role and shuffle them
    bag_of_players = []
    for team in new_repr:
        bag_of_players += [team[i] for i in i]
        
    shuffle(bag_of_players)

    # Once shuffled, put them back in the teams
    index = 0
    for team in new_repr:
        for j in i:
            team[j] = bag_of_players[index]
            index += 1

    mutated = deepcopy(solution)
    mutated.repr = new_repr
    return mutated


def player_role_left_shift_mutation(solution, verbose=False):
    """
    Shifts all players of the same role (e.g., all defenders) leftward across teams.

    Args:
        solution (object): A solution object with a `.repr` attribute.
        verbose (bool): Whether to print debug info.

    Returns:
        object: A mutated copy of the solution.

    """
    new_repr = deepcopy(solution.repr)
    # Choose the role that will be affected
    # Remembering that the player IDs withing the team correspond to {"GK": 0, "DEF": [1, 2], "MID": [3, 4], "FWD": [5, 6]}
    i = randint(0, 6)
    if i in [1, 2]:
        i = [1, 2]
    elif i in [3, 4]:
        i = [3, 4]
    elif i in [5, 6]:
        i = [5, 6]
    else:
        i = [0]
    
    # Get all the players from the selected role
    role_players = []
    for team in new_repr:
        for idx in i:
            role_players.append(team[idx])

    # Shift left 
    shift_amount = randint(1, len(new_repr) - 1)
    role_players = role_players[shift_amount:] + role_players[:shift_amount]
    
    # If verbose, print the role and indexes being shifted
    if verbose:
        role_map = {
            "GK": [0],
            "DEF": [1, 2],
            "MID": [3, 4],
            "FWD": [5, 6]
        }
        inv_map = {tuple(v): k for k, v in role_map.items()}
        role_name = inv_map[tuple(i)]
        print(f"Shifting role group {role_name}, corresponding to indexes {i}, by {shift_amount} positions")

    # Reassign to teams
    index = 0
    for team in new_repr:
        for idx in i:
            team[idx] = role_players[index]
            index += 1


    mutated = deepcopy(solution)
    mutated.repr = new_repr
    return mutated