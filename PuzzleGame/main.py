import random
from collections import deque

class PuzzleGame:
    def __init__(self):
        # S = SOURCE, D = Destination, W = WALL, C = empty cell
        self.puzzles = self.generate_puzzles()

    def get_random_puzzle(self):
        return random.choice(self.puzzles)
    
    def generate_puzzles(self):
        generated_puzzles = [self.puzzle1(), self.puzzle2(), self.puzzle3()]
        valid_puzzles = []
        for index, puzzle in enumerate(generated_puzzles):
            if self.is_valid_puzzle(puzzle):
                valid_puzzles.append(puzzle)
            else:
                print(f"Puzzle at index {index + 1} is invalid.")
        
        return valid_puzzles
    
    def is_valid_puzzle(self, puzzle):
        no_rows, no_cols = len(puzzle) - 1, len(puzzle[0]) - 1
        srcR, srcC = None, None
        destR, destC = None, None

        for r in range(no_rows):
            for c in range(no_cols):
                if puzzle[r][c] == "S":
                    srcR, srcC = r, c
                elif puzzle[r][c] == "D":
                    destR, destC = r, c

        if srcR is None or destR is None:
            return False
        
        def is_valid_cell(row, col):
            return 0 <= row < no_rows and 0 <= col < no_cols and puzzle[row][col] != "W"

        visited = set()
        queue = deque([(srcR, srcC)])
        visited.add((srcR, srcC))
        
        while len(queue) > 0:
            r, c = queue.popleft()
            if r == destR and c == destC:
                return True
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                newR, newC = r + dr, c + dc
                if is_valid_cell(newR, newC) and (newR, newC) not in visited:
                    queue.append((newR, newC))
                    visited.add((newR, newC))

        return False
        
    def puzzle1(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "C", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "C", "C", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "C", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "C", "C", "C", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "C", "W", "W", "C", "W"],
            ["W", "W", "W", "W", "W", "C", "C", "C", "C", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "D", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]

    def puzzle2(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "C", "C", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "C", "C", "C", "W", "W", "W"],
            ["W", "C", "C", "W", "W", "W", "C", "C", "C", "W"],
            ["W", "W", "C", "W", "C", "W", "W", "W", "C", "W"],
            ["W", "W", "C", "W", "W", "W", "W", "W", "C", "W"],
            ["W", "W", "W", "W", "C", "C", "C", "W", "C", "W"],
            ["W", "W", "W", "W", "W", "C", "W", "C", "C", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "D", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]

    def puzzle3(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "C", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "C", "C", "W", "C", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "C", "C", "W", "C", "W", "W", "W"],
            ["W", "W", "W", "W", "C", "C", "C", "C", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "C", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "C", "C", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "D", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]
    
    def puzzle4(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "C", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "C", "C", "W", "W", "W", "W", "W"],
            ["W", "C", "W", "W", "C", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "W", "C", "W", "W", "C", "W"],
            ["W", "W", "C", "C", "W", "C", "C", "W", "W", "W"],
            ["W", "W", "W", "C", "W", "W", "C", "W", "W", "W"],
            ["W", "W", "W", "C", "C", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "C", "C", "C", "D", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]
    
    def puzzle5(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "W", "C", "C", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "C", "W", "W", "W", "W", "W"],
            ["W", "C", "W", "C", "C", "C", "W", "C", "W", "W"],
            ["W", "C", "C", "W", "W", "W", "W", "C", "W", "W"],
            ["W", "W", "C", "C", "W", "W", "W", "C", "C", "W"],
            ["W", "W", "C", "W", "W", "W", "W", "C", "C", "W"],
            ["W", "C", "C", "C", "W", "W", "W", "W", "D", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]
    
    def puzzle6(slef):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "C", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "W", "C", "C", "C", "W", "W"],
            ["W", "C", "W", "C", "W", "C", "C", "W", "W", "W"],
            ["W", "C", "C", "C", "C", "C", "W", "W", "W", "W"],
            ["W", "C", "C", "W", "C", "C", "C", "C", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "C", "C", "D", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]
    
    def puzzle7(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "W", "W", "W", "C", "W", "W", "W"],
            ["W", "W", "C", "C", "W", "W", "W", "C", "W", "W"],
            ["W", "C", "C", "C", "W", "C", "C", "W", "W", "W"],
            ["W", "C", "W", "C", "W", "C", "W", "W", "C", "W"],
            ["W", "C", "C", "C", "C", "W", "C", "C", "W", "W"],
            ["W", "W", "W", "C", "W", "W", "C", "W", "C", "W"],
            ["W", "W", "C", "C", "W", "W", "C", "C", "D", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]
    
    def puzzle8(self):
        return [
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "S", "C", "C", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "C", "W", "C", "C", "W", "W", "W", "W"],
            ["W", "C", "C", "W", "C", "W", "C", "W", "W", "W"],
            ["W", "C", "W", "C", "W", "W", "W", "W", "C", "W"],
            ["W", "C", "W", "C", "W", "C", "C", "C", "W", "W"],
            ["W", "C", "W", "W", "W", "W", "C", "C", "C", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "C", "D", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ]
    
    def print_puzzle(self, grid):
        for row in grid:
            print(" ".join(row))



game = PuzzleGame()
game.print_puzzle(game.get_random_puzzle())