import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        
        # Create 9x9 grid of Entry widgets
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_board()
        
        # Solve and Reset Buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=9, column=0, columnspan=9)

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_sudoku)
        solve_button.pack(side=tk.LEFT, padx=5)

        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_board)
        reset_button.pack(side=tk.LEFT, padx=5)

    def create_board(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, justify='center', font=('Arial', 18))
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry
    
    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val == '':
                    current_row.append('.')
                else:
                    try:
                        val = int(val)
                        if val < 1 or val > 9:  # Check if input is within 1-9
                            messagebox.showerror("Error", f"Invalid number at row {row+1}, col {col+1}: {val}. Only numbers between 1 and 9 are allowed.")
                            return None
                        current_row.append(val)
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid input at row {row+1}, col {col+1}. Only numbers between 1 and 9 are allowed.")
                        return None
            board.append(current_row)
        return board
    
    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] != '.':
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(board[row][col]))
    
    def reset_board(self):
        # Clear all entries
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def solve_sudoku(self):
        board = self.get_board()
        if board is None:  # Invalid board, stop execution
            return
        
        # Check if the initial board is valid
        if not self.is_valid_initial_board(board):
            messagebox.showerror("Error", "Invalid board configuration.")
            return
        
        if self.solve(board):
            self.set_board(board)
            messagebox.showinfo("Success", "Sudoku Solved!")
        else:
            messagebox.showerror("Error", "No solution exists.")
    
    def is_valid_initial_board(self, board):
        """Checks if the current board configuration is valid."""
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != '.':
                    # Temporarily set the cell to empty to validate the number
                    board[row][col] = '.'
                    if not self.valid(board, num, (row, col)):
                        return False
                    board[row][col] = num
        return True

    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find
        
        for i in range(1, 10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i
                if self.solve(board):
                    return True
                board[row][col] = '.'
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    return (i, j)
        return None
    
    def valid(self, board, num, pos):
        # Check row
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        
        # Check column
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        
        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
