class CaroBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def make_move(self, r, c, player):
        if self.board[r][c] == ' ':
            self.board[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        self.board[r][c] = ' '

    def get_empty_cells(self):
        cells = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == ' ':
                    cells.append((r, c))
        return cells

    def is_full(self):
        return len(self.get_empty_cells()) == 0

    def check_winner(self):
        for r in range(3):
            if self.board[r][0] == self.board[r][1] == self.board[r][2] != ' ':
                return self.board[r][0], [(r, 0), (r, 1), (r, 2)]

        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] != ' ':
                return self.board[0][c], [(0, c), (1, c), (2, c)]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0], [(0, 0), (1, 1), (2, 2)]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2], [(0, 2), (1, 1), (2, 0)]

        if self.is_full():
            return 'Draw', []

        return None, []

    def get_all_lines(self):
        lines = []
        for r in range(3):
            lines.append((self.board[r][0], self.board[r][1], self.board[r][2]))
        for c in range(3):
            lines.append((self.board[0][c], self.board[1][c], self.board[2][c]))
        lines.append((self.board[0][0], self.board[1][1], self.board[2][2]))
        lines.append((self.board[0][2], self.board[1][1], self.board[2][0]))
        return lines

    def evaluate_heuristic(self, ai_player):
        human_player = 'O' if ai_player == 'X' else 'X'
        score = 0
        lines = self.get_all_lines()

        for line in lines:
            ai_count = line.count(ai_player)
            human_count = line.count(human_player)
            empty_count = line.count(' ')

            if ai_count == 3:
                score += 100
            elif human_count == 3:
                score -= 100
            elif ai_count == 2 and empty_count == 1:
                score += 10
            elif ai_count == 1 and empty_count == 2:
                score += 1
            elif human_count == 2 and empty_count == 1:
                score -= 10
            elif human_count == 1 and empty_count == 2:
                score -= 1

        return score
