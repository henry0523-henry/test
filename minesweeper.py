import random

class Minesweeper:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self._place_mines()
        self._calculate_numbers()
        self.game_over = False
        self.win = False

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

    def print_board(self, reveal=False):
        print('   ' + ' '.join([str(i) for i in range(self.cols)]))
        print('  +' + '--' * self.cols + '+')
        for r in range(self.rows):
            row = [self.board[r][c] if (self.visible[r][c] or reveal) else '.' for c in range(self.cols)]
            print(f'{r:2}|', ' '.join(row), '|')
        print('  +' + '--' * self.cols + '+')

    def open_cell(self, r, c):
        if self.visible[r][c]:
            return
        self.visible[r][c] = True
        if (r, c) in self.mine_positions:
            self.game_over = True
            return
        if self.board[r][c] == ' ':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if not self.visible[nr][nc]:
                            self.open_cell(nr, nc)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_positions and not self.visible[r][c]:
                    return False
        self.win = True
        return True

def main():
    game = Minesweeper()
    while not game.game_over and not game.win:
        game.print_board()
        try:
            move = input('열 칸을 "행 열"로 입력 (예: 0 1): ')
            r, c = map(int, move.strip().split())
            if not (0 <= r < game.rows and 0 <= c < game.cols):
                print('범위 오류!')
                continue
            game.open_cell(r, c)
            if game.game_over:
                print('지뢰를 밟았습니다! 게임 오버!')
                game.print_board(reveal=True)
                break
            if game.check_win():
                print('축하합니다! 모두 찾았습니다!')
                game.print_board(reveal=True)
                break
        except Exception as e:
            print('입력이 잘못되었습니다.', e)

if __name__ == '__main__':
    main()
