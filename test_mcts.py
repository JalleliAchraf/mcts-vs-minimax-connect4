#!/usr/bin/env python3

from connect4 import Connect4
from mcts import MCTSPlayer
from minimax import MinimaxPlayer

def test_mcts_basic():
    """Test basic MCTS functionality"""
    print("Testing MCTS Player...")
    
    game = Connect4()
    mcts_player = MCTSPlayer(simulations=100)  # Use fewer simulations for quick test
    
    # Test that MCTS can make a move
    move = mcts_player.get_move(game, 1)
    print(f"MCTS chose move: {move}")
    assert move in game.get_valid_moves(), "MCTS chose invalid move!"
    
    # Make the move and test again
    game.drop_piece(move, 1)
    move2 = mcts_player.get_move(game, 2)
    print(f"MCTS chose second move: {move2}")
    assert move2 in game.get_valid_moves(), "MCTS chose invalid second move!"
    
    print("✓ Basic MCTS test passed!")

def test_mcts_vs_minimax():
    """Quick test of MCTS vs Minimax"""
    print("\nTesting MCTS vs Minimax...")
    
    game = Connect4()
    mcts_player = MCTSPlayer(simulations=200)
    minimax_player = MinimaxPlayer(depth=4)
    
    # Play a few moves
    for turn in range(6):  # Play 6 moves total
        current_player = (turn % 2) + 1
        
        if current_player == 1:
            move = mcts_player.get_move(game, current_player)
            print(f"Turn {turn+1}: MCTS (Player {current_player}) plays column {move}")
        else:
            move = minimax_player.get_best_move(game, current_player)
            print(f"Turn {turn+1}: Minimax (Player {current_player}) plays column {move}")
            
        game.simulate_move(move, current_player)
        game.print_board()
        print()
        
        # Check for winner
        game_state = game.get_game_state()
        if game_state != 0:
            if game_state == 3:
                print("Game over! Draw!")
            else:
                print(f"Game over! Winner: Player {game_state}")
            break
    
    print("✓ MCTS vs Minimax test completed!")

if __name__ == "__main__":
    test_mcts_basic()
    test_mcts_vs_minimax()
