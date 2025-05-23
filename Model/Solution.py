from abc import ABC, abstractmethod
import numpy as np

class Solution(ABC):
    def __init__(self, repr=None):
        if repr is None:
            repr = self.random_initial_representation()
        self.repr = repr

    def __repr__(self):
        return str(self.repr)

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def random_initial_representation(self):
        pass


class SportsLeagueSolution(Solution):
    def __init__(self, repr=None, players_df=None):
        if players_df is None:
            raise ValueError("players_df must be provided")
        self.players_df = players_df
        super().__init__(repr=repr)

    def random_initial_representation(self):
        self.repr = generate_league(self.players_df)
        self.players_df["team"] = -1
        for team_idx, team in enumerate(self.repr):
            self.players_df.loc[team, "team"] = team_idx
        return self.repr

    def fitness(self):
        team_avg_skills = []
        self.players_df["team"] = -1
        for team_idx, team in enumerate(self.repr):
            self.players_df.loc[team, "team"] = team_idx
            team_df = self.players_df.loc[team]
            total_salary = team_df["salary"].sum()
            if total_salary > 750:
                return 1e9
            avg_skill = team_df["skill"].mean()
            team_avg_skills.append(avg_skill)
        return float(np.std(team_avg_skills))
