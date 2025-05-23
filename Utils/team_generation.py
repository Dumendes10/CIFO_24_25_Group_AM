import random
from collections import defaultdict

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