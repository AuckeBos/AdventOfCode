import heapq
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
import numpy as np
from numpy import ndarray
from typing import List, Tuple

from adventofcode.helpers.base_matrix import BaseMatrix

class Map(BaseMatrix):
    # For each node in map, set distance to start
    distances: ndarray
    # At each cell indicate the cost of entering that cell
    costs: ndarray
    # Boolean array. Value is true if cell is visited
    visited: ndarray
    # Current active node
    active_node: Tuple[int, int]
    # Min distance to current active node
    current_distance: int
    history: List[Tuple[int, int]]
    parents: ndarray
    
    def reset(self):
        self.costs = self.data.copy().astype(int)
        self.distances = np.full(
            self.costs.shape, fill_value=np.iinfo(int).max, dtype=int
        )
        self.visited = np.full(self.costs.shape, fill_value=False, dtype=bool)
        self.history = []
        self.distances[0, 0] = 0
        self.active_node = 0, 0
        self.parents = np.full(self.costs.shape, fill_value=None, dtype=object)

    @property
    def end(self) -> Tuple[int, int]:
        return self.distances.shape[0] - 1, self.distances.shape[1] - 1
    
    def is_valid_history(self, history: List[Tuple[int, int]]) -> bool:
        # Check if the history does not contain three consecutive moves in the same direction
        if len(history) < 4:
            return True
        else:
            return not np.all(np.diff(history[-4:]) == 0)

    def next(self, neighbours: List[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Return the neighbor to visit next. It's the one with the lowest distance, if it is not visited yet and the history would still be valid if we visit it
        """
        for r, c in neighbours:
            if not self.visited[r, c] and self.is_valid_history(self.history + [(r, c)]):
                return r, c
        raise ValueError(f"No valid neighbour found for {self.active_node}")
    
    
    def done(self) -> bool:
        """
        Done if destination is visited
        :return: bool
        """
        return self.visited[self.end]

    def get_neighbours(self) -> List[Tuple[int, int]]:
        result = self.adjacent_fields(*self.active_node, as_values=False)
        # Prevent going back
        result = [(r, c) for r, c in result if (r, c) != self.history[-1]]
        # Remove out of bounds
        result = [(r, c) for r, c in result if 0 <= r < self.data.shape[0] and 0 <= c < self.data.shape[1]]
        # Remove visited
        result = [(r, c) for r, c in result if not self.visited[r, c]]
        return result
    
    def get_path(self) -> List[Tuple[int, int]]:
        result = np.full(self.costs.shape, fill_value=".")
        path = []
        node = self.end
        while node != (0, 0):
            result[node] = "#"
            path.append(node)
            node = self.parents[node]
        path.append((0, 0))
        print("\n".join(["".join(row) for row in result]))
        return result
    

    def dijkstra(self, min_straight_steps: int = None, max_straight_steps: int = None) -> int:
        """
        Dijksta's with the constraints that:
        - If min_straight_steps is given, any direction must be taken at least min_straight_steps times in a row, before turning
        - If max_straight_steps is given, any direction must be taken at most max_straight_steps times in a row, before turning
        """
        # queue is a list of (distance, amount_steps_straight, last_direction, (r, c))
        all_possible_directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
        distances = np.full(self.costs.shape, fill_value=np.iinfo(int).max, dtype=int)
        parents = np.full(self.costs.shape, fill_value=None, dtype=object)
        queue: List[Tuple[int, int, Tuple[int, int], Tuple[int, int]]] = []
        visited: set[Tuple[Tuple[int, int], int, Tuple[int, int]]] = set()

        costs = self.costs.copy()
        heapq.heappush(queue, (0, 0, (0, 0), (0, 0)))
        while queue:
            distance, amount_steps_straight, last_direction, node = heapq.heappop(queue)
            state = (node, amount_steps_straight, last_direction)
            if state in visited:
                continue
            visited.add(state)
            possible_directions = all_possible_directions - {(last_direction[0] * -1, last_direction[1] * -1)}
            for direction in possible_directions:
                if direction == last_direction:
                    new_amount_steps_straight = amount_steps_straight + 1
                    if max_straight_steps is not None and new_amount_steps_straight > max_straight_steps:
                        continue
                else: 
                    if (amount_steps_straight != 0) and (min_straight_steps is not None and amount_steps_straight < min_straight_steps):
                        continue
                    new_amount_steps_straight = 1
                if max_straight_steps is not None and new_amount_steps_straight > max_straight_steps:
                    continue                
                r, c = node[0] + direction[0], node[1] + direction[1]
                if 0 <= r < costs.shape[0] and 0 <= c < costs.shape[1]:
                    new_distance = distance + costs[r, c]
                    if new_distance < distances[r, c]:
                        distances[r, c] = new_distance
                        parents[r, c] = node
                    heapq.heappush(queue, (new_distance, new_amount_steps_straight, direction, (r, c)))
        # Create a matrix of the path. Each cell has '.', excpet for the one in the shortest path, which has '#'. Use parents to find the path
        self.print_parents(distances, parents)
        print(distances[distances.shape[0] - 1, distances.shape[1] - 1])
        return distances[distances.shape[0] - 1, distances.shape[1] - 1]
    
    def print_parents(self, distances: ndarray, parents: ndarray):
        result = np.full(self.costs.shape, fill_value=".")
        node = (distances.shape[0] - 1, distances.shape[1] - 1)
        while node != (0, 0):
            if parents[node] is None:
                break
            result[node[0], node[1]] = "#"
            node = parents[node]
        result[0, 0] = "#"
        print("\n".join(["".join(row) for row in result]))        



class Puzzle17(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 17
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

    @property
    def test_input_alternative(self) -> str:
        return """111111111111
999999999991
999999999991
999999999991
999999999991"""

    @property
    def test_answer_a(self):
        return 102

    @property
    def test_answer_b(self):
        return 71

    def parse_input(self, input_: str) -> Map:
        map = Map()
        map.parse_input(input_, None)
        map.reset()
        return map

    def a(self, map: Map):
        return map.dijkstra(max_straight_steps=3)

    def b(self, map: Map):
        return map.dijkstra(min_straight_steps=4, max_straight_steps=10)


puzzle = Puzzle17()
puzzle.solve()
