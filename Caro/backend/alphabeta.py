def alphabeta(board, depth, remaining_depth, alpha, beta, is_maximizing, ai_player, nodes_evaluated):
    nodes_evaluated[0] += 1

    winner, _ = board.check_winner()
    human_player = 'O' if ai_player == 'X' else 'X'

    if winner == ai_player:
        return 10 - depth
    elif winner == human_player:
        return -10 + depth
    elif winner == 'Draw':
        return 0

    if remaining_depth == 0:
        return board.evaluate_heuristic(ai_player)

    if is_maximizing:
        val = -float('inf')
        for r, c in board.get_empty_cells():
            board.make_move(r, c, ai_player)
            val = max(val, alphabeta(board, depth + 1, remaining_depth - 1, alpha, beta, False, ai_player, nodes_evaluated))
            board.undo_move(r, c)
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return val
    else:
        val = float('inf')
        for r, c in board.get_empty_cells():
            board.make_move(r, c, human_player)
            val = min(val, alphabeta(board, depth + 1, remaining_depth - 1, alpha, beta, True, ai_player, nodes_evaluated))
            board.undo_move(r, c)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return val
