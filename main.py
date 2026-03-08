import tkinter as tk
from tkinter import messagebox
from bfs import bfs
from helpers import GOAL_STATE, states
import random

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")

        self.tiles = []
        self.entries = []
        self.path = []
        self.current_step = 0  # To track step in path

        self.create_controls()
        self.create_input_board()
        self.create_board()

    # Controls: Algorithm dropdown + Solve + Randomize + Next Step
    def create_controls(self):
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(frame, text="Algorithm:").pack(side=tk.LEFT)

        self.algorithm = tk.StringVar(value="BFS")
        options = ["BFS","DFS","IDFS","A* Manhattan","A* Euclidean"]  # can extend to DFS, A*, etc.
        menu = tk.OptionMenu(frame, self.algorithm, *options)
        menu.pack(side=tk.LEFT)

        solve_btn = tk.Button(frame, text="Solve", command=self.solve)
        solve_btn.pack(side=tk.LEFT, padx=5)

        random_btn = tk.Button(frame, text="Randomize Puzzle", command=self.randomize_puzzle)
        random_btn.pack(side=tk.LEFT, padx=5)

        next_btn = tk.Button(frame, text="Next Step", command=self.next_step)
        next_btn.pack(side=tk.LEFT, padx=5)
        self.next_btn = next_btn
        self.next_btn.config(state=tk.DISABLED)  # Disable until solution is computed

    # Input puzzle
    def create_input_board(self):
        tk.Label(self.root, text="Enter Puzzle (0 = blank)").grid(row=1, column=0, columnspan=3)

        for i in range(3):
            row = []
            for j in range(3):
                entry = tk.Entry(self.root, width=3, font=("Helvetica", 18), justify="center")
                entry.grid(row=i+2, column=j)
                row.append(entry)
            self.entries.append(row)

    # Board for animation
    def create_board(self):
        tk.Label(self.root, text="Solution Animation").grid(row=5, column=0, columnspan=3)

        for i in range(3):
            row = []
            for j in range(3):
                tile = tk.Label(
                    self.root,
                    text="",
                    font=("Helvetica", 32),
                    width=4,
                    height=2,
                    borderwidth=2,
                    relief="ridge"
                )
                tile.grid(row=i+6, column=j)
                row.append(tile)
            self.tiles.append(row)

    # Read puzzle from GUI
    def get_input_state(self):
        state = ""
        for i in range(3):
            for j in range(3):
                val = self.entries[i][j].get()
                state += val
        return state

    # Update board
    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                val = state[i*3 + j]
                self.tiles[i][j].config(text="" if val == '0' else val)

    # Solve button
    def solve(self):
        start_state = self.get_input_state()
        algo = self.algorithm.get()
##########################################################################################EDIT HERE####################################33333
        if algo == "BFS":
            self.path, stats = bfs(start_state)
        elif algo == "DFS":
            print("get me a path and stats, and i will literally do everything you wisj")
        elif algo == "IDFS":
            print("get me a path and stats, and i will literally do everything you wisj")
        elif algo == "A* Manhattan":
            print("get me a path and stats, and i will literally do everything you wisj")
        elif algo == "A* Euclidean":
            print("get me a path and stats, and i will literally do everything you wisj")
        else:
            return

        if self.path is None:
            messagebox.showerror("No solution", "Could not find a solution!")
            return

        print("Statistics:", stats)
        print("Path",self.path)
        self.current_step = 0
        self.update_board(self.path[self.current_step])
        self.next_btn.config(state=tk.NORMAL)  # Enable "Next Step" button

    # Next Step button
    def next_step(self):
        if self.path and self.current_step < len(self.path)-1:
            self.current_step += 1
            self.update_board(self.path[self.current_step])
        if self.current_step == len(self.path)-1:
            self.next_btn.config(state=tk.DISABLED)  # Disable at goal

    # Randomize puzzle
    def randomize_puzzle(self):
        puzzle = list("012345678")
        random.shuffle(puzzle)
        state = "".join(puzzle)
        while not self.is_solvable(state):
            random.shuffle(puzzle)
            state = "".join(puzzle)

        for i in range(3):
            for j in range(3):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, state[i*3 + j])

    # Check solvable
    def is_solvable(self, state):
        inv_count = 0
        nums = [int(x) for x in state if x != '0']
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] > nums[j]:
                    inv_count += 1
        return inv_count % 2 == 0


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()