import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 8
PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    '.': ''
}

START_BOARD = [
    list('rnbqkbnr'),
    list('pppppppp'),
    list('........'),
    list('........'),
    list('........'),
    list('........'),
    list('PPPPPPPP'),
    list('RNBQKBNR'),
]

class ChessGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('체스')
        self.board = [row[:] for row in START_BOARD]
        self.turn = 'white'  # white goes first
        self.selected = None
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.status = tk.Label(master, text='White 차례', font=('Arial', 16))
        self.status.grid(row=0, column=0, columnspan=8)
        self.create_board()

    def create_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.master, text=PIECES[self.board[r][c]], font=('Arial', 32), width=2, height=1,
                                bg=self.get_color(r, c), command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r+1, column=c)
                self.buttons[r][c] = btn

    def get_color(self, r, c):
        return '#f0d9b5' if (r + c) % 2 == 0 else '#b58863'

    def on_click(self, r, c):
        piece = self.board[r][c]
        if self.selected:
            sr, sc = self.selected
            if (sr, sc) == (r, c):
                self.selected = None
                self.update_board()
                return
            if self.is_valid_move(sr, sc, r, c):
                self.move_piece(sr, sc, r, c)
                self.selected = None
                self.turn = 'black' if self.turn == 'white' else 'white'
                self.status.config(text=f"{'White' if self.turn == 'white' else 'Black'} 차례")
            else:
                self.selected = None
            self.update_board()
        else:
            if (self.turn == 'white' and piece.isupper()) or (self.turn == 'black' and piece.islower()):
                self.selected = (r, c)
                self.update_board()

    def is_valid_move(self, sr, sc, r, c):
        # 매우 단순한 이동 규칙만 적용 (기본 이동, 잡기, 자기 말 위 금지)
        piece = self.board[sr][sc]
        target = self.board[r][c]
        if (self.turn == 'white' and target.isupper()) or (self.turn == 'black' and target.islower()):
            return False
        dr, dc = r - sr, c - sc
        if piece.lower() == 'p':  # Pawn
            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1
            if dc == 0 and target == '.' and ((dr == direction) or (sr == start_row and dr == 2*direction and self.board[sr+direction][sc] == '.' and self.board[r][c] == '.')):
                return True
            if abs(dc) == 1 and dr == direction and target != '.' and ((piece.isupper() and target.islower()) or (piece.islower() and target.isupper())):
                return True
            return False
        elif piece.lower() == 'r':  # Rook
            if dr == 0 or dc == 0:
                return self.clear_path(sr, sc, r, c)
        elif piece.lower() == 'n':  # Knight
            return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]
        elif piece.lower() == 'b':  # Bishop
            if abs(dr) == abs(dc):
                return self.clear_path(sr, sc, r, c)
        elif piece.lower() == 'q':  # Queen
            if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                return self.clear_path(sr, sc, r, c)
        elif piece.lower() == 'k':  # King
            return max(abs(dr), abs(dc)) == 1
        return False

    def clear_path(self, sr, sc, r, c):
        dr = (r - sr) and ((r - sr)//abs(r - sr))
        dc = (c - sc) and ((c - sc)//abs(c - sc))
        cr, cc = sr + dr, sc + dc
        while (cr, cc) != (r, c):
            if self.board[cr][cc] != '.':
                return False
            cr += dr
            cc += dc
        return True

    def move_piece(self, sr, sc, r, c):
        self.board[r][c] = self.board[sr][sc]
        self.board[sr][sc] = '.'
        # 승리 조건(킹 잡힘) 체크
        kings = sum(row.count('K') for row in self.board), sum(row.count('k') for row in self.board)
        if kings[0] == 0:
            messagebox.showinfo('게임 종료', 'Black 승리!')
            self.master.destroy()
        elif kings[1] == 0:
            messagebox.showinfo('게임 종료', 'White 승리!')
            self.master.destroy()

    def update_board(self):
        # 기본 보드 색상 및 말 표시
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = self.buttons[r][c]
                btn.config(text=PIECES[self.board[r][c]], bg=self.get_color(r, c))
        # 선택된 말과 이동 가능 경로 하이라이트
        if self.selected:
            sr, sc = self.selected
            self.buttons[sr][sc].config(bg='#f7ec6f')  # 선택된 말
            # 이동 가능한 경로 표시
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if (sr, sc) != (r, c) and self.is_valid_move(sr, sc, r, c):
                        self.buttons[r][c].config(bg='#ffe066')

def main():
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
