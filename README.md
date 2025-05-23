# Fantasy Sports League Optimization with Genetic Algorithms

The coolest CIFO Group.

**Group AM** for Computational Intelligence for Optimization 2025.


##  To-Do List

1. **Problem Definition**  
   Clearly outline the optimization challenge and project goals.

2. **Class Design**  
   - Implement classes for `Player`, `Team`, and `League`.

3. **Solution Representation**  
   - Define how solutions (leagues/teams) are encoded for the algorithm.

4. **Genetic Algorithm Components**  
   - **Selection Algorithms:** Implement and test different selectors.
   - **Crossover Operators:** Develop and integrate crossover methods.
   - **Mutation Operators:** Add mutation strategies.
   - **GA Framework:** Assemble the complete genetic algorithm workflow.

5. **Results Analysis**  
   - Evaluate and visualize the algorithm’s performance.

6. **Documentation & Reporting**  
   - Write clear documentation and prepare the final project report.


## Overview

This project uses a Genetic Algorithm (GA) to automatically build balanced and competitive fantasy sports leagues. The algorithm considers real-world constraints like salary cap, position requirements, and player exclusivity.

## Problem & Approach

- Objective: Build teams so that the difference in average skill between teams is minimized.
- Constraints: Salary cap (€750M per team), fixed team roles (1 GK, 2 DEF, 2 MID, 2 FWD per team), and no duplicate players.
- Encoding: Each solution is a league of five teams, each represented as a list of player IDs.

## Genetic Algorithm Design

- Mutation Operators: Player Swap, Role Shuffle, Player Role Left Shift.
- Crossover Operators: Standard Crossover with Position Repair, Crossover by Position Dual Any.
- Selection Methods: Ranking Selection and Tournament Selection (best results with tournament size k=4).
- Fitness Function: Standard deviation of team average skills (lower is better), with penalties for salary cap violations.
- Elitism: Used to preserve the best solutions each generation.

## Key Findings

- Mutation rate has the biggest impact on performance; higher rates led to better and more consistent results.
- Crossover probability had little effect on final fitness.
- Elitism improved stability and convergence.
- The best configuration produced leagues with very small differences in team skill averages.

## Results

- The GA reliably created leagues where all constraints were met and teams were well balanced.
- The approach is robust and can be adapted to other sports or league formats.

## Future Work

- Test more selection methods and larger populations.
- Run for more generations to see if further improvements are possible.
- Add diversity-preserving techniques to avoid premature convergence.

---

**Conclusion:**  
A well-designed Genetic Algorithm can automate the creation of fair, balanced fantasy sports leagues, even with complex real-world constraints.

---

See the full report, code, and result visualizations in this repository!



