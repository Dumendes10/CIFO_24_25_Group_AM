import random
from collections import defaultdict, Counter

def get_position_map(players_df):
    
    """
    Creates a mapping from player ID to their position.

    This function takes a DataFrame of players with at least two columns:
    'id' (unique player identifier) and 'position' (e.g., GK, DEF, MID, FWD),
    and returns a dictionary that maps each player ID to their respective position.

    Args:
        players_df (pd.DataFrame): A DataFrame containing player information,
                                   with 'id' and 'position' columns.

    Returns:
        dict: A dictionary mapping each player ID (int) to their position (str).
              Example: {0: 'GK', 1: 'DEF', 2: 'MID', ...}
    """
    return dict(zip(players_df['id'], players_df['position']))

def standard_crossover_with_position_repair(parent1, parent2, players_df, verbose=False):
    crossover_point=random.randint(1, len(parent1) - 1)
    if verbose:
        print(f"[Crossover] Crossover point at team index {crossover_point}")

    position_map = get_position_map(players_df) # creates a mapping from player ID to their position
    all_players = set(players_df['id']) # creates a set of all players

    # Crossover on team level by the crossover point defined on the arguments
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

    # Position slots by index inside each team
    # we want to always keep the [GK, DEF, DEF, MID, MID, FWD, FWD] formatation
    position_slots = ["GK", "DEF", "DEF", "MID", "MID", "FWD", "FWD"] # players are assumed to always appear in this fixed order

    def repair_offspring(offspring):

        """
        Repairs an offspring by removing duplicate players and replacing 
        them with valid players that were missing from the solution.

        This function ensures:
            - Each player appears only once across all teams.
            - Players are only replaced by others who play the same position.
            - All players from the original player pool are used exactly once.

        The function relies on two external variables:
            - `all_players`: A set of all player IDs expected to be used in the solution.
            - `position_map`: A dictionary mapping player IDs to their positions (e.g., 'GK', 'DEF').
            - `position_slots`: A list defining the position expected at each slot in a team.

        Parameters:
            offspring (list of list of int): A candidate solution represented as a list of teams, 
                                            where each team is a list of player IDs.

        Returns:
            list of list of int: A repaired version of the offspring, where:
                                - All players are unique.
                                - Each player is placed in a slot matching their position.
                                - Missing players are added in valid positions.

        Notes:
            The function modifies teams independently, attempting to replace invalid entries
            (duplicates or misplaced players) with players not yet used but suitable for
            the expected position.
        """
        
        # receives an offspring, thelist of teams and it returns a "repaired" version where:
            # * All players are unique, so no duplicates across teams, that is a problem with the standard crossover
            # * Players are replaced only with others of the same position
            # * Any missing players are added back.


        # Flatten all players used
        flat = [p for team in offspring for p in team] # Flattens the list of teams into a single list of all player IDs
        counts = Counter(flat) # Count occurrences of each player ID ( how many times each player appears in the flattened offspring)

        # Find duplicates and missing players
        duplicates = {p for p, c in counts.items() if c > 1} # get the players that appear more than once
        used = set(flat) # get the players that are used in the offspring
        missing = list(all_players - used) # get the players that are missing in the offspring but should be there (all players come from above code)
        
        if verbose:
            print("[Repair] Starting repair process")
            print(f"  Duplicates found: {sorted(duplicates)}")
            print(f"  Missing players: {sorted(missing)}\n")
        
        # Build available players by position for replacements

        available_by_pos = defaultdict(list)  # create a dict where the key is a position  and the value is a shuffled list of player IDs that are available for that position
        for pid in missing: # for each player ID in the missing list
            pos = position_map[pid] # get the position of the player
            available_by_pos[pos].append(pid) # append the player ID to the list of available players for that position
        for pos in available_by_pos: # for each position in the available players
            random.shuffle(available_by_pos[pos]) # shuffle the list of available players for that position

        # Track used players to avoid duplicates
        used_players = set() #  tracks player IDs that have already been added to teams to prevent further duplicates during the repair process
        repaired_offspring = [] 
        for team_idx, team in enumerate(offspring): # for each team in the offspring
            new_team = [] # create a new team
            for idx, pid in enumerate(team): # for each player ID in the team
                pos = position_slots[idx] # get the position of the player based on the index

                # If player is duplicated or already used, replace
                if pid in used_players or pid in duplicates: # if the player ID is already used or is a duplicate
                    if available_by_pos[pos]: # if there are available players for that position
                        replacement = available_by_pos[pos].pop() # get a replacement player ID from the available players for that position
                        if verbose:
                            print(f"  Team {team_idx}: Replacing player {pid} (pos {pos}) → {replacement}")
                        new_team.append(replacement) # add the replacement player ID to the new team
                        used_players.add(replacement) # add the replacement player ID to the used players
                    else:
                        if verbose:
                            print(f"  Team {team_idx}: No replacement available for player {pid} in position {pos}, keeping original")
                        # If no available players left in that position (should not happen), keep original
                        new_team.append(pid) # add the original player ID to the new team
                        used_players.add(pid) # add the original player ID to the used players
                else: # if the player ID is not a duplicate and not already used
                    new_team.append(pid) # add the original player ID to the new team
                    used_players.add(pid) # add the original player ID to the used players

            repaired_offspring.append(new_team) # add the new team to the repaired offspring
        return repaired_offspring

    return repair_offspring(offspring1), repair_offspring(offspring2)


def validate_league(league, players_df, position_slots = ["GK", "DEF", "DEF", "MID", "MID", "FWD", "FWD"]):
    """
    Validates a league composed of multiple teams.

    Requirements checked:
        - Each player appears exactly once across all teams (no duplicates or missing).
        - Players are placed in the correct position slot according to position_slots.
        - Each team has the correct number of players.

    Parameters:
        league (list of list of int): The league to validate, as a list of teams (each a list of player IDs).
        players_df (pd.DataFrame): DataFrame with at least 'id' and 'position' columns.
        position_slots (list of str): Expected position at each index of a team, e.g., 
                                      ["GK", "DEF", "DEF", "MID", "MID", "FWD", "FWD"]

    Returns:
        bool: True if the league is valid. Otherwise, prints detailed issues and returns False.
    """

    all_player_ids = set(players_df['id'])
    expected_team_size = len(position_slots)

    # 1. Check total number of players
    flat_players = [p for team in league for p in team]
    player_counts = Counter(flat_players)

    # Check if every player is used exactly once
    if set(flat_players) != all_player_ids:
        missing = all_player_ids - set(flat_players)
        extra = set(flat_players) - all_player_ids
        if missing:
            print(f"Missing players: {missing}")
        if extra:
            print(f"Unknown players found: {extra}")
        return False

    duplicates = {p for p, c in player_counts.items() if c > 1}
    if duplicates:
        print(f"Duplicated players: {duplicates}")
        return False

    # 2. Check team structure and position integrity
    position_map = dict(zip(players_df['id'], players_df['position']))
    for i, team in enumerate(league):
        if len(team) != expected_team_size:
            print(f"Team {i} has invalid size {len(team)}. Expected {expected_team_size}.")
            return False
        for idx, pid in enumerate(team):
            expected_pos = position_slots[idx]
            actual_pos = position_map.get(pid)
            if actual_pos != expected_pos:
                print(f"Team {i}, player {pid} in slot {idx} expected {expected_pos}, got {actual_pos}.")
                return False

    print("League is valid!")
    return True


def crossover_by_position_dual_any(parent1, parent2, players_df, keep_positions=None, verbose=False):
    """
    Dual crossover with random position selection:
    - Randomly selects 2 positions if none specified
    - Preserves selected positions from each parent
    - Fills remaining slots from other parent
    - Ensures no duplicate players per team
    """
    position_map = dict(zip(players_df['id'], players_df['position']))
    position_slots = ["GK", "DEF", "DEF", "MID", "MID", "FWD", "FWD"]
    unique_positions = list(set(position_slots))  # ['GK', 'DEF', 'MID', 'FWD']
    
    # Set random positions 
    if keep_positions is None:
        keep_positions = random.sample(unique_positions, 2)
        
    if verbose:
        print(f"[Crossover] Keeping positions from primary parent: {keep_positions}\n")

    def make_offspring(primary, secondary):
        offspring = []
        
        for team_idx in range(5):
            # Track used players PER TEAM
            used_players = set()
            new_team = [None] * 7
            
            
            # 1. Preserve selected positions from primary parent
            for i, slot in enumerate(position_slots):
                if slot in keep_positions:
                    player_id = primary[team_idx][i]
                    if player_id not in used_players:
                        new_team[i] = player_id
                        used_players.add(player_id)

            # 2. Fill remaining slots from secondary parent
            for i, slot in enumerate(position_slots):
                if new_team[i] is not None:
                    continue
                
                # Find first available player in secondary team with correct position
                for player_id in secondary[team_idx]:
                    if (position_map[player_id] == slot and 
                        player_id not in used_players and 
                        slot not in keep_positions):
                        new_team[i] = player_id
                        used_players.add(player_id)
                        break

            # 3. Fallback: fill from global pool if needed
            for i, slot in enumerate(position_slots):
                if new_team[i] is None:
                    available = players_df[
                        (players_df["position"] == slot) & 
                        (~players_df["id"].isin(used_players))
                    ].id.values
                    if len(available) > 0:
                        new_team[i] = available[0]
                        used_players.add(new_team[i])

            offspring.append(new_team)
            
        return offspring

    return (
        make_offspring(parent1, parent2),
        make_offspring(parent2, parent1)
    )
