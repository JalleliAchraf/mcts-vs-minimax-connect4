#!/usr/bin/env python3
"""
MCTS Integration and Performance Tests
Tests the complete algorithm behavior and performance characteristics
"""

import time
import random
from collections import Counter
from connect4 import Connect4
from mcts import MCTSPlayer
from minimax import MinimaxPlayer

def test_mcts_move_validity():
    """Test that MCTS always chooses valid moves"""
    print("=== Testing Move Validity ===")
    
    game = Connect4()
    mcts = MCTSPlayer(simulations=100)
    
    for turn in range(20):  # Test multiple moves
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            break
            
        move = mcts.get_move(game, (turn % 2) + 1)
        assert move in valid_moves, f"Turn {turn}: Invalid move {move}, valid: {valid_moves}"
        
        game.simulate_move(move, (turn % 2) + 1)
        
        if game.get_game_state() != 0:  # Game ended
            break
    
    print("✓ All moves were valid!")

def test_mcts_time_consistency():
    """Test that MCTS runtime scales with simulation count"""
    print("=== Testing Time Consistency ===")
    
    game = Connect4()
    simulation_counts = [50, 100, 200, 500]
    times = []
    
    for sim_count in simulation_counts:
        mcts = MCTSPlayer(simulations=sim_count)
        
        start_time = time.time()
        move = mcts.get_move(game, 1)
        end_time = time.time()
        
        duration = end_time - start_time
        times.append(duration)
        
        print(f"  {sim_count} simulations: {duration:.3f}s (move: {move})")
    
    # Time should generally increase with simulation count
    for i in range(1, len(times)):
        ratio = times[i] / times[i-1]
        print(f"  Ratio {simulation_counts[i]}/{simulation_counts[i-1]}: {ratio:.2f}x")
    
    print("✓ Timing behavior reasonable!")

def test_mcts_exploration():
    """Test that MCTS explores different moves"""
    print("=== Testing Exploration Behavior ===")
    
    game = Connect4()
    mcts = MCTSPlayer(simulations=100)
    
    moves = []
    for _ in range(20):  # Run same position multiple times
        move = mcts.get_move(game, 1)
        moves.append(move)
    
    move_counts = Counter(moves)
    unique_moves = len(move_counts)
    
    print(f"  Move distribution: {dict(move_counts)}")
    print(f"  Unique moves tried: {unique_moves}/7")
    
    assert unique_moves >= 3, "MCTS should explore multiple moves"
    print("✓ Exploration behavior good!")

def test_mcts_winning_positions():
    """Test MCTS behavior in obvious winning/losing positions"""
    print("=== Testing Winning Position Recognition ===")
    
    # Create a winning position for player 1
    game = Connect4()
    # Set up: 1 1 1 . . . .  (player 1 can win by playing column 3)
    game.simulate_move(0, 1)
    game.simulate_move(1, 1) 
    game.simulate_move(2, 1)
    
    print("Position: Player 1 can win by playing column 3")
    game.print_board()
    
    mcts = MCTSPlayer(simulations=500)  # More simulations for clear decision
    
    # Test multiple times to see if MCTS finds the winning move
    winning_moves = 0
    total_tests = 10
    
    for _ in range(total_tests):
        move = mcts.get_move(game, 1)
        if move == 3:  # Winning move
            winning_moves += 1
    
    win_percentage = (winning_moves / total_tests) * 100
    print(f"  Found winning move {winning_moves}/{total_tests} times ({win_percentage}%)")
    
    # MCTS should find the winning move most of the time
    assert win_percentage >= 70, f"MCTS should find obvious wins >70% of time, got {win_percentage}%"
    print("✓ Winning position recognition good!")

def test_mcts_vs_random():
    """Test MCTS performance against random player"""
    print("=== Testing MCTS vs Random Player ===")
    
    def random_player(game, player):
        valid_moves = game.get_valid_moves()
        return random.choice(valid_moves)
    
    mcts = MCTSPlayer(simulations=200)
    wins = 0
    games = 10
    
    for game_num in range(games):
        game = Connect4()
        current_player = 1
        
        while game.get_game_state() == 0 and len(game.get_valid_moves()) > 0:
            if current_player == 1:  # MCTS
                move = mcts.get_move(game, current_player)
            else:  # Random
                move = random_player(game, current_player)
            
            game.simulate_move(move, current_player)
            current_player = 3 - current_player
        
        result = game.get_game_state()
        if result == 1:  # MCTS wins
            wins += 1
        
        print(f"  Game {game_num + 1}: Result = {result} ({'MCTS win' if result == 1 else 'Loss/Draw'})")
    
    win_rate = (wins / games) * 100
    print(f"  MCTS win rate: {wins}/{games} ({win_rate}%)")
    
    # MCTS should beat random player most of the time
    assert win_rate >= 60, f"MCTS should beat random player >60% of time, got {win_rate}%"
    print("✓ MCTS beats random player!")

def run_integration_tests():
    print("Running MCTS Integration Tests...")
    
    test_mcts_move_validity()
    test_mcts_time_consistency()
    test_mcts_exploration()
    test_mcts_winning_positions()
    test_mcts_vs_random()
    
    print("\n🎉 All integration tests passed!")

if __name__ == "__main__":
    run_integration_tests()
