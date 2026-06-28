import random
import time
from .minimax import minimax
from .alphabeta import alphabeta
from .expectimax import expectimax

class CaroAI:
    @staticmethod
    def minimax(board, depth, is_maximizing, ai_player, max_depth, nodes_evaluated):
        return minimax(board, depth, is_maximizing, ai_player, max_depth, nodes_evaluated)

    @staticmethod
    def alphabeta(board, depth, remaining_depth, alpha, beta, is_maximizing, ai_player, nodes_evaluated):
        return alphabeta(board, depth, remaining_depth, alpha, beta, is_maximizing, ai_player, nodes_evaluated)

    @staticmethod
    def expectimax(board, depth, remaining_depth, is_maximizing, ai_player, nodes_evaluated):
        return expectimax(board, depth, remaining_depth, is_maximizing, ai_player, nodes_evaluated)

    @staticmethod
    def get_best_move(board, algorithm, max_depth, ai_player):
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            return None, 0, 0.0

        start_time = time.perf_counter()
        nodes_evaluated = [0]
        best_val = -float('inf')
        tied_moves = []

        if algorithm == "Minimax":
            for r, c in empty_cells:
                board.make_move(r, c, ai_player)
                val = minimax(board, 1, False, ai_player, max_depth, nodes_evaluated)
                board.undo_move(r, c)
                
                if val > best_val:
                    best_val = val
                    tied_moves = [(r, c)]
                elif val == best_val:
                    tied_moves.append((r, c))

        elif algorithm == "Alpha-Beta Pruning":
            alpha = -float('inf')
            beta = float('inf')
            for r, c in empty_cells:
                board.make_move(r, c, ai_player)
                val = alphabeta(board, 1, max_depth - 1, alpha, beta, False, ai_player, nodes_evaluated)
                board.undo_move(r, c)
                
                if val > best_val:
                    best_val = val
                    tied_moves = [(r, c)]
                elif val == best_val:
                    tied_moves.append((r, c))
                alpha = max(alpha, best_val)

        elif algorithm == "Expectimax":
            for r, c in empty_cells:
                board.make_move(r, c, ai_player)
                val = expectimax(board, 1, max_depth - 1, False, ai_player, nodes_evaluated)
                board.undo_move(r, c)
                
                if val > best_val:
                    best_val = val
                    tied_moves = [(r, c)]
                elif val == best_val:
                    tied_moves.append((r, c))

        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000.0
        best_move = random.choice(tied_moves) if tied_moves else None
        return best_move, nodes_evaluated[0], elapsed_time_ms
