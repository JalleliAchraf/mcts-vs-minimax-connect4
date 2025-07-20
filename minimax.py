from connect4 import Connect4
from math import inf


class MinimaxPlayer:
    def __init__(self, depth=6, use_alpha_beta=True):
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta

    def get_best_move(self, game, player):
        if self.use_alpha_beta:
            return self.minimax_ab(game, self.depth, -inf, inf, True, player)[1]
        else:
            return self.minimax_basic(game, self.depth, True, player)[1]
    def minimax_basic(self, game, depth, maximizing_player, player):
        if depth == 0 or game.get_game_state() != 0:
            return game.evaluate_position(player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:  
            return game.evaluate_position(player), None
            
        if maximizing_player:
            best_score = -inf
            best_col = valid_moves[0] 
            for col in valid_moves:
                undo_info = game.simulate_move(col, player)
                score, _ = self.minimax_basic(game, depth-1, False, player)
                game.undo_move(undo_info)
                if score > best_score:
                    best_score = score
                    best_col = col
            return best_score, best_col
        else:
            best_score = inf  
            best_col = valid_moves[0]  
            for col in valid_moves:
                undo_info = game.simulate_move(col, 3-player)
                score, _ = self.minimax_basic(game, depth-1, True, player)
                game.undo_move(undo_info)
                if score < best_score:
                    best_score = score
                    best_col = col
            return best_score, best_col
    def minimax_ab(self, game, depth, alpha, beta, maximizing_player, player):
        if depth == 0 or game.get_game_state() != 0:
            return game.evaluate_position(player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:  
            return game.evaluate_position(player), None
        if maximizing_player:
            best_score = -inf
            best_col = valid_moves[0] 
            for col in valid_moves:
                undo_info = game.simulate_move(col, player)
                score, _ = self.minimax_ab(game, depth-1, alpha, beta, False, player)
                game.undo_move(undo_info)  
                
                if score > best_score: 
                    best_score = score
                    best_col = col
                
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break 
            return best_score, best_col 
        else:
            best_score = inf
            best_col = valid_moves[0]
            for col in valid_moves:
                undo_info = game.simulate_move(col, 3-player)  
                score, _ = self.minimax_ab(game, depth-1, alpha, beta, True, player)
                game.undo_move(undo_info)
                if score < best_score:
                    best_score = score
                    best_col = col
                beta = min(beta, best_score)
                if beta <= alpha:
                    break 
            return best_score, best_col 
            








