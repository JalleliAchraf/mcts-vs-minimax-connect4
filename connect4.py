import numpy as np
import pygame as pg
THREE_IN_ROW = 100    
TWO_IN_ROW = 10       
CENTER_BONUS = 3
class Connect4:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1
    def drop_piece(self,row,col):
        self.board[row][col] = self.current_player

    def switch_player(self):
        self.current_player = 3 - self.current_player
    def is_valid_location(self, col):
        return self.board[0][col] == 0  
    def get_next_open_row(self, col):
        for r in range(self.rows-1, -1, -1):  
            if self.board[r][col] == 0:
                return r
        return None

    def is_winning_move(self, row, col):
        # check horizontal
        for c in range(max(0, col-3), min(self.cols-3, col+1)):
            if all(self.board[row][c+i] == self.current_player for i in range(4)):
                return True
        # check vertical
        for r in range(max(0, row-3), min(self.rows-3, row+1)):
            if all(self.board[r+i][col] == self.current_player for i in range(4)):
                return True
        # check positive diagonal
        for r, c in zip(range(max(0, row-3), min(self.rows-3, row+1)),
                        range(max(0, col-3), min(self.cols-3, col+1))):
            if all(self.board[r+i][c+i] == self.current_player for i in range(4)):
                return True
        # check negative diagonal
        for r, c in zip(range(max(0, row-3), min(self.rows-3, row+1)),
                        range(min(self.cols-1, col+3), max(-1, col-4), -1)):
            if all(self.board[r+i][c-i] == self.current_player for i in range(4)):
                return True
        return False
    def get_game_state(self):
        """
        Returns:
        0 = game ongoing
        1 = player 1 wins  
        2 = player 2 wins
        3 = draw
        """
        # Check for wins by scanning the entire board
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:  
                    player = self.board[row][col]
                    
                    # Check horizontal (right)
                    if col <= self.cols - 4:
                        if all(self.board[row][col + i] == player for i in range(4)):
                            return player
                    
                    # Check vertical (down)
                    if row <= self.rows - 4:
                        if all(self.board[row + i][col] == player for i in range(4)):
                            return player
                    
                    # Check positive diagonal (down-right)
                    if row <= self.rows - 4 and col <= self.cols - 4:
                        if all(self.board[row + i][col + i] == player for i in range(4)):
                            return player
                    
                    # Check negative diagonal (down-left)
                    if row <= self.rows - 4 and col >= 3:
                        if all(self.board[row + i][col - i] == player for i in range(4)):
                            return player
        
        # Check for draw (top row full)
        if all(self.board[0][col] != 0 for col in range(self.cols)):
            return 3
        
        # Game is still ongoing
        return 0
    def evaluate_position(self, player):
        """
        Evaluate the current board position for the given player.
        Returns: int/float (higher = better for player)
        """
        game_state=self.get_game_state()
        if game_state==player:
            return 1000
        elif game_state==3-player:
            return -1000
        elif game_state==3:
            return 0
        else :
            score = 0
            for row in range(self.rows-3):
                for col in range(self.cols-3):
                        window = [self.board[row][col + i] for i in range(4)]
                        score+=self.evaluate_window(window,player)
            for col in range(self.cols):
                for row in range(self.rows - 3):  
                        window = [self.board[row + i][col] for i in range(4)]
                        score+=self.evaluate_window(window,player)
            for row in range(self.rows - 3):
                for col in range(self.cols - 3):
                        window = [self.board[row + i][col + i] for i in range(4)]
                        score+=self.evaluate_window(window,player)
            for row in range(3, self.rows):  
                for col in range(self.cols - 3):
                        window = [self.board[row - i][col + i] for i in range(4)]
                        score+=self.evaluate_window(window,player)
            #add central position bonus
            bonus=0
            center_col= self.cols//2
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board[row][col]==player:
                        distance_from_center=abs(col-center_col)
                        bonus+=max(0,CENTER_BONUS-distance_from_center)
            return score+bonus
 
        
    def evaluate_window(self, window, player):
        opponent = 3 - player
        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(0)
        score = 0
        if player_count == 3 and empty_count == 1:
            score += THREE_IN_ROW
        elif player_count == 2 and empty_count == 2:
            score += TWO_IN_ROW
        if opponent_count == 3 and empty_count == 1:
            score -= THREE_IN_ROW
        elif opponent_count == 2 and empty_count == 2:
            score -= TWO_IN_ROW
        return score

    def get_valid_moves(self):
        """Return list of valid column numbers where pieces can be dropped"""
        return [col for col in range(self.cols) if self.is_valid_location(col)]
    
    def copy_game(self):
        """Create a deep copy of the game state"""
        new_game = Connect4(self.rows, self.cols)
        new_game.board = np.copy(self.board)
        new_game.current_player = self.current_player
        return new_game
        
    def simulate_move(self, col, player):
        """Make a move and return undo information. Assumes col is valid."""
        row = self.get_next_open_row(col)
        self.board[row][col] = player
        return (row, col)  
    
    def undo_move(self, undo_info):
        """Undo a move using the undo information"""
        row, col = undo_info
        self.board[row][col] = 0

    def draw_board(self, screen, square_size):
        blue = (0, 0, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        radius = int(square_size / 2 - 5)
        for c in range(self.cols):
            for r in range(self.rows):
                pg.draw.rect(screen, blue, (c * square_size, r * square_size + square_size, square_size, square_size))
                if self.board[r][c] == 0:
                    pg.draw.circle(screen, black, (int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), radius)
                elif self.board[r][c] == 1:
                    pg.draw.circle(screen, red, (int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), radius)
                else:
                    pg.draw.circle(screen, yellow, (int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), radius)

    def print_board(self):
        """Print the board in a human-readable format"""
        print("  " + " ".join(str(i) for i in range(self.cols)))
        print("  " + "-" * (self.cols * 2 - 1))  
        for row in range(self.rows):
            row_str = "| "
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    row_str += ". "  
                elif self.board[row][col] == 1:
                    row_str += "1 "  
                else:
                    row_str += "2 "  
            row_str += "|"
            print(row_str)
        
        print("  " + "-" * (self.cols * 2 - 1)) 

