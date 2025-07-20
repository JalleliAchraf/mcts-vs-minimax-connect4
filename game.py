#!/usr/bin/env python3
"""
Simple Connect4 Game Interface
Uses existing MCTS and Minimax implementations
"""

import pygame as pg
import sys
import math
from connect4 import Connect4
from mcts import MCTSPlayer
from minimax import MinimaxPlayer

# Initialize Pygame
pg.init()

# Constants
ROWS = 6
COLS = 7
SQUARE_SIZE = 100
WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class GameInterface:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Connect4 - MCTS vs Minimax")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 75)
        
        # Game state
        self.game = Connect4()
        self.game_over = False
        self.turn = 0
        
        # Player setup
        self.player1 = None
        self.player2 = None
        self.player1_name = ""
        self.player2_name = ""
        
        # Mouse tracking
        self.mouse_x = 0
        
        # Game mode selection
        self.in_menu = True

    def draw_board(self):
        """Draw the game board"""
        for c in range(COLS):
            for r in range(ROWS):
                pg.draw.rect(self.screen, BLUE, 
                           (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, 
                            SQUARE_SIZE, SQUARE_SIZE))
                pg.draw.circle(self.screen, BLACK, 
                             (int(c * SQUARE_SIZE + SQUARE_SIZE/2), 
                              int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), 
                             int(SQUARE_SIZE/2 - 5))

        # Draw pieces
        for c in range(COLS):
            for r in range(ROWS):
                if self.game.board[r][c] == 1:
                    pg.draw.circle(self.screen, RED, 
                                 (int(c * SQUARE_SIZE + SQUARE_SIZE/2), 
                                  int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), 
                                 int(SQUARE_SIZE/2 - 5))
                elif self.game.board[r][c] == 2:
                    pg.draw.circle(self.screen, YELLOW, 
                                 (int(c * SQUARE_SIZE + SQUARE_SIZE/2), 
                                  int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), 
                                 int(SQUARE_SIZE/2 - 5))

    def draw_hover_piece(self):
        """Draw the hovering piece that follows mouse"""
        if not self.game_over and self.is_human_turn():
            col = int(self.mouse_x // SQUARE_SIZE)
            if 0 <= col < COLS:
                color = RED if self.game.current_player == 1 else YELLOW
                pg.draw.circle(self.screen, color, 
                             (int(col * SQUARE_SIZE + SQUARE_SIZE/2), 
                              int(SQUARE_SIZE/2)), 
                             int(SQUARE_SIZE/2 - 5))

    def draw_menu(self):
        """Draw game mode selection menu"""
        self.screen.fill(WHITE)
        
        title = self.font.render("Connect4", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        font = pg.font.SysFont("Arial", 30)
        options = [
            "1 - Human vs Human",
            "2 - Human vs Minimax",
            "3 - Human vs MCTS", 
            "4 - Minimax vs MCTS",
            "5 - MCTS vs Minimax",
            "ESC - Exit"
        ]
        
        for i, option in enumerate(options):
            text = font.render(option, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH//2, 200 + i * 50))
            self.screen.blit(text, text_rect)

    def setup_players(self, mode):
        """Setup players based on mode selection"""
        self.in_menu = False
        self.game = Connect4()
        self.game_over = False
        self.turn = 0
        
        if mode == 1:  # Human vs Human
            self.player1 = "human"
            self.player2 = "human"
            self.player1_name = "Player 1"
            self.player2_name = "Player 2"
        elif mode == 2:  # Human vs Minimax
            self.player1 = "human"
            self.player2 = MinimaxPlayer(depth=5)
            self.player1_name = "Human"
            self.player2_name = "Minimax"
        elif mode == 3:  # Human vs MCTS
            self.player1 = "human"
            self.player2 = MCTSPlayer(simulations=1000)
            self.player1_name = "Human"
            self.player2_name = "MCTS"
        elif mode == 4:  # Minimax vs MCTS
            self.player1 = MinimaxPlayer(depth=4)
            self.player2 = MCTSPlayer(simulations=800)
            self.player1_name = "Minimax"
            self.player2_name = "MCTS"
        elif mode == 5:  # MCTS vs Minimax
            self.player1 = MCTSPlayer(simulations=800)
            self.player2 = MinimaxPlayer(depth=4)
            self.player1_name = "MCTS"
            self.player2_name = "Minimax"

    def is_human_turn(self):
        """Check if current player is human"""
        current_player = self.player1 if self.game.current_player == 1 else self.player2
        return current_player == "human"

    def make_move(self, col):
        """Make a move in the specified column"""
        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col)
            
            # Check for win
            if self.game.is_winning_move(row, col):
                self.game_over = True
            elif len(self.game.get_valid_moves()) == 0:
                self.game_over = True
            else:
                self.game.switch_player()
                self.turn += 1

    def ai_move(self):
        """Handle AI player move"""
        current_player_obj = self.player1 if self.game.current_player == 1 else self.player2
        
        if hasattr(current_player_obj, 'get_move'):
            col = current_player_obj.get_move(self.game, self.game.current_player)
        elif hasattr(current_player_obj, 'get_best_move'):
            col = current_player_obj.get_best_move(self.game, self.game.current_player)
        else:
            # Fallback to random
            import random
            col = random.choice(self.game.get_valid_moves())
        
        if col is not None:
            self.make_move(col)

    def draw_status(self):
        """Draw game status"""
        if self.game_over:
            winner = self.game.get_game_state()
            if winner == 1:
                text = f"{self.player1_name} Wins!"
                color = RED
            elif winner == 2:
                text = f"{self.player2_name} Wins!"
                color = YELLOW
            else:
                text = "Draw!"
                color = WHITE
        else:
            current_name = self.player1_name if self.game.current_player == 1 else self.player2_name
            text = f"{current_name}'s Turn"
            color = RED if self.game.current_player == 1 else YELLOW
        
        font = pg.font.SysFont("Arial", 40)
        label = font.render(text, True, color)
        self.screen.blit(label, (40, 10))
        
        # Instructions
        if self.game_over:
            inst_text = "Press R to restart, ESC for menu"
        else:
            inst_text = "Click to drop piece, R to restart, ESC for menu"
        
        inst_font = pg.font.SysFont("Arial", 20)
        inst_label = inst_font.render(inst_text, True, WHITE)
        self.screen.blit(inst_label, (10, HEIGHT - 25))

    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                
                elif event.type == pg.KEYDOWN:
                    if self.in_menu:
                        if event.key == pg.K_1:
                            self.setup_players(1)
                        elif event.key == pg.K_2:
                            self.setup_players(2)
                        elif event.key == pg.K_3:
                            self.setup_players(3)
                        elif event.key == pg.K_4:
                            self.setup_players(4)
                        elif event.key == pg.K_5:
                            self.setup_players(5)
                        elif event.key == pg.K_ESCAPE:
                            running = False
                    else:
                        if event.key == pg.K_r:
                            self.setup_players(1)  # Restart with same mode
                        elif event.key == pg.K_ESCAPE:
                            self.in_menu = True
                
                elif event.type == pg.MOUSEMOTION:
                    self.mouse_x = event.pos[0]
                
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not self.in_menu and not self.game_over and self.is_human_turn():
                        col = int(event.pos[0] // SQUARE_SIZE)
                        self.make_move(col)
            
            # AI moves
            if not self.in_menu and not self.game_over and not self.is_human_turn():
                self.ai_move()
            
            # Drawing
            if self.in_menu:
                self.draw_menu()
            else:
                self.screen.fill(BLACK)
                self.draw_board()
                self.draw_hover_piece()
                self.draw_status()
            
            pg.display.flip()
            self.clock.tick(60)
        
        pg.quit()
        sys.exit()

def main():
    """Run the game"""
    game = GameInterface()
    game.run()

if __name__ == "__main__":
    main()

    def get_current_player(self):
        """Get the current player object"""
        return self.player1 if self.game.current_player == 1 else self.player2

    def handle_human_move(self, col: int) -> bool:
        """Handle a human player's move"""
        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col)
            
            if self.game.is_winning_move(row, col):
                self.game_over = True
                self.winner = self.game.current_player
            elif self.game.get_game_state() == 3:
                self.game_over = True
                self.winner = None
            else:
                self.game.switch_player()
            
            return True
        return False

    def handle_ai_move(self):
        """Handle an AI player's move"""
        current_player_obj = self.get_current_player()
        col = current_player_obj.get_move(self.game, self.game.current_player)
        
        if col is not None and self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col)
            
            if self.game.is_winning_move(row, col):
                self.game_over = True
                self.winner = self.game.current_player
            elif self.game.get_game_state() == 3:
                self.game_over = True
                self.winner = None
            else:
                self.game.switch_player()

    def restart_game(self):
        """Restart the current game"""
        self.game = Connect4()
        self.game_over = False
        self.winner = None

    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                
                elif event.type == pg.KEYDOWN:
                    if self.in_menu:
                        if event.key == pg.K_1:
                            self.setup_game_mode(1)
                        elif event.key == pg.K_2:
                            self.setup_game_mode(2)
                        elif event.key == pg.K_3:
                            self.setup_game_mode(3)
                        elif event.key == pg.K_4:
                            self.setup_game_mode(4)
                        elif event.key == pg.K_5:
                            running = False
                    else:
                        if event.key == pg.K_r:
                            self.restart_game()
                        elif event.key == pg.K_ESCAPE:
                            self.in_menu = True
                
                elif event.type == pg.MOUSEMOTION and not self.in_menu:
                    self.hover_col = event.pos[0] // SQUARE_SIZE
                
                elif event.type == pg.MOUSEBUTTONDOWN and not self.in_menu:
                    if not self.game_over and isinstance(self.get_current_player(), HumanPlayer):
                        col = event.pos[0] // SQUARE_SIZE
                        self.handle_human_move(col)
            
            # Handle AI moves
            if not self.in_menu and not self.game_over and not isinstance(self.get_current_player(), HumanPlayer):
                self.handle_ai_move()
            
            # Draw everything
            if self.in_menu:
                self.draw_menu()
            else:
                self.draw_board()
                self.draw_ui()
            
            pg.display.flip()
            self.clock.tick(60)
        
        pg.quit()
        sys.exit()


def main():
    """Main function to run the game"""
    game = GameInterface()
    game.run()


if __name__ == "__main__":
    main()