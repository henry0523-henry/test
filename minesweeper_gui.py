import tkinter as tk
import random
from tkinter import messagebox

class MinesweeperGUI:
    def __init__(self, master, rows=9, cols=9, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.flags = set()
        self.game_over = False
        self._place_mines()
        self._calculate_numbers()
        self._create_widgets()

    def _place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.mine_positions.add((r, c))

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mine_positions:
                    self.board[r][c] = 'M'
                else:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if (nr, nc) in self.mine_positions:
                                    count += 1
                    self.board[r][c] = str(count) if count > 0 else ' '

    def _create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.master, width=2, height=1, font=('Arial', 14),
                                command=lambda r=r, c=c: self.open_cell(r, c))
                btn.bind('<Button-3>', lambda e, r=r, c=c: self.toggle_flag(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def open_cell(self, r, c):
        if self.game_over or self.visible[r][c] or (r, c) in self.flags:
            return
        self.visible[r][c] = True
        btn = self.buttons[r][c]
        if (r, c) in self.mine_positions:
            btn.config(text='💣', bg='red')
            self.game_over = True
            self.reveal_all()
            messagebox.showinfo('게임 오버', '지뢰를 밟았습니다!')
            return
        btn.config(text=self.board[r][c], relief=tk.SUNKEN, state=tk.DISABLED, bg='lightgrey')
        if self.board[r][c] == ' ':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if not self.visible[nr][nc]:
                            self.open_cell(nr, nc)
        if self.check_win():
            self.game_over = True
            self.reveal_all()
            messagebox.showinfo('승리', '축하합니다! 모두 찾았습니다!')

    def toggle_flag(self, r, c):
        if self.game_over or self.visible[r][c]:
            return
        btn = self.buttons[r][c]
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text='')
        else:
            self.flags.add((r, c))
            btn.config(text='🚩')

    def reveal_all(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                if (r, c) in self.mine_positions:
                    btn.config(text='💣', bg='red')
                elif self.board[r][c] != ' ':
                    btn.config(text=self.board[r][c], bg='lightgrey')
                btn.config(state=tk.DISABLED)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_positions and not self.visible[r][c]:
                    return False
        return True

def main():
    root = tk.Tk()
    root.title('지뢰찾기')
    MinesweeperGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
