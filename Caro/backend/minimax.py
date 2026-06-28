def minimax(board, depth, is_maximizing, ai_player, max_depth, nodes_evaluated):
    nodes_evaluated[0] += 1

    winner, _ = board.check_winner()
    human_player = 'O' if ai_player == 'X' else 'X'

    if winner == ai_player:
        return 10 - depth
    elif winner == human_player:
        return -10 + depth
    elif winner == 'Draw':
        return 0

    if depth >= max_depth:
        return board.evaluate_heuristic(ai_player)

    if is_maximizing:
        best_val = -float('inf')
        for r, c in board.get_empty_cells():
            board.make_move(r, c, ai_player)
            val = minimax(board, depth + 1, False, ai_player, max_depth, nodes_evaluated)
            board.undo_move(r, c)
            best_val = max(best_val, val)
        return best_val
    else:
        best_val = float('inf')
        for r, c in board.get_empty_cells():
            board.make_move(r, c, human_player)
            val = minimax(board, depth + 1, True, ai_player, max_depth, nodes_evaluated)
            board.undo_move(r, c)
            best_val = min(best_val, val)
        return best_val
