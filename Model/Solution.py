import numpy as np
import random
from collections import defaultdict
from abc import ABC, abstractmethod

def generate_league(df):    
    num_teams=5
    available_ids = df.index.tolist()
    random.shuffle(available_ids)

    league = []

    for _ in range(num_teams):
        pos_map = defaultdict(list)

        # Build position map using current available players
        for i in available_ids:
            pos = df.loc[i, "position"]
            pos_map[pos].append(i)

        # Check we have enough players left per role
        if (len(pos_map["GK"]) < 1 or
            len(pos_map["DEF"]) < 2 or
            len(pos_map["MID"]) < 2 or
            len(pos_map["FWD"]) < 2):
            raise ValueError("Not enough players left to form a full team")

        # Select players for the team
        team = []
        team += random.sample(pos_map["GK"], 1)
        team += random.sample(pos_map["DEF"], 2)
        team += random.sample(pos_map["MID"], 2)
        team += random.sample(pos_map["FWD"], 2)

        # Remove them from pool
        for idx in team:
            available_ids.remove(idx)

        league.append(team)

    return league


class Solution(ABC):
    def __init__(self, repr=None):
        # To initialize a solution we need to know it's representation.
        # If no representation is given, a representation is randomly initialized.
        if repr == None:
            repr = self.random_initial_representation()
        # Attributes
        self.repr = repr

    # Method that is called when we run print(object of the class)
    def __repr__(self):
        return str(self.repr)

    # Other methods that must be implemented in subclasses
    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def random_initial_representation():
        pass




class SportsLeagueSolution(Solution):
    def __init__(self, repr=None, players_df=None):
        self.players_df = players_df
        super().__init__(repr=repr)

    
    def random_initial_representation(self):
        self.repr = generate_league(self.players_df)

        # Reset the 'team' column
        self.players_df["team"] = -1

        # Assign team number to each player
        for team_idx, team in enumerate(self.repr):
            self.players_df.loc[team, "team"] = team_idx

        return self.repr

    def fitness(self):
        team_avg_skills = []

        # Reset team column (optional safety)
        self.players_df["team"] = -1

        for team_idx, team in enumerate(self.repr):
            self.players_df.loc[team, "team"] = team_idx
            team_df = self.players_df.loc[team]

            total_salary = team_df["salary"].sum()
            if total_salary > 750:
                return 1e9  # Penalize invalid solution

            avg_skill = team_df["skill"].mean()
            team_avg_skills.append(avg_skill)

        # Minimize std deviation of team avg skills → balanced league
        return float(np.std(team_avg_skills))
