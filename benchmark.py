#!/usr/bin/env python3
"""
Simple Benchmark Script for MCTS vs Minimax
============================================

Quick performance comparison between MCTS and Minimax algorithms
for Connect 4. Provides runtime and win rate metrics.

Usage:
    python benchmark.py [--games N] [--mcts-sims N] [--minimax-depth N]
"""

import time
import argparse
import sys
import random
from connect4 import Connect4
from mcts import MCTSPlayer  
from minimax import MinimaxPlayer

def benchmark_algorithm(player, opponent, games=20, name="Algorithm"):
    """Benchmark an algorithm against an opponent."""
    
    wins = 0
    draws = 0
    total_time = 0
    move_times = []
    
    print(f"Benchmarking {name} ({games} games)...")
    
    for game_num in range(games):
        game = Connect4()
        game_start_time = time.time()
        
        # Alternate who goes first
        if game_num % 2 == 0:
            # Player goes first
            players = [player, opponent]
            player_names = [name, "Opponent"]
            target_player = 1  # Track wins for player 1
        else:
            # Opponent goes first
            players = [opponent, player] 
            player_names = ["Opponent", name]
            target_player = 2  # Track wins for player 2
            
        current_idx = 0
        
        while game.get_game_state() == 0 and len(game.get_valid_moves()) > 0:
            move_start = time.time()
            
            current_player_obj = players[current_idx]
            
            # Get move from current player
            if hasattr(current_player_obj, 'get_move'):
                move = current_player_obj.get_move(game, game.current_player)
            elif hasattr(current_player_obj, 'get_best_move'):
                move = current_player_obj.get_best_move(game, game.current_player)
            else:
                # Fallback to random
                move = random.choice(game.get_valid_moves())
            
            move_time = time.time() - move_start
            
            # Only track move times for the algorithm being benchmarked
            if (game_num % 2 == 0 and current_idx == 0) or (game_num % 2 == 1 and current_idx == 1):
                move_times.append(move_time)
            
            # Make the move
            if move is not None and game.is_valid_location(move):
                row = game.get_next_open_row(move)
                game.drop_piece(row, move)
                
                # Check for win
                if game.is_winning_move(row, move):
                    winner = game.current_player
                    break
                    
                game.switch_player()
                current_idx = 1 - current_idx
            else:
                # Invalid move - should not happen
                break
        
        # Check result
        game_result = game.get_game_state()
        if game_result == target_player:
            wins += 1
        elif game_result == 0 or game_result == 3:
            draws += 1
            
        total_time += time.time() - game_start_time
        
        # Progress indicator
        if (game_num + 1) % 5 == 0:
            current_rate = wins / (game_num + 1)
            print(f"   Progress: {game_num + 1}/{games} | Win rate: {current_rate:.3f}")
    
    # Calculate statistics
    win_rate = wins / games
    avg_move_time = sum(move_times) / len(move_times) if move_times else 0
    avg_game_time = total_time / games
    
    return {
        'name': name,
        'games': games,
        'wins': wins,
        'draws': draws,
        'losses': games - wins - draws,
        'win_rate': win_rate,
        'avg_move_time': avg_move_time,
        'avg_game_time': avg_game_time,
        'total_moves': len(move_times)
    }

def format_results(results):
    """Format benchmark results for display."""
    
    print(f"\n{results['name']} Results:")
    print("=" * 40)
    print(f"Games Played:     {results['games']}")
    print(f"Wins:             {results['wins']} ({results['win_rate']:.1%})")
    print(f"Draws:            {results['draws']} ({results['draws']/results['games']:.1%})")
    print(f"Losses:           {results['losses']} ({results['losses']/results['games']:.1%})")
    print(f"Avg Move Time:    {results['avg_move_time']:.3f}s")
    print(f"Avg Game Time:    {results['avg_game_time']:.1f}s")
    print(f"Total Moves:      {results['total_moves']}")

def run_quick_benchmark():
    """Run a quick benchmark suite."""
    
    print("Connect 4 Algorithm Benchmark")
    print("=" * 50)
    
    # Create random baseline player
    class RandomPlayer:
        def get_move(self, game, player):
            return random.choice(game.get_valid_moves())
    
    random_player = RandomPlayer()
    
    # Test configurations
    algorithms = [
        ("MCTS-100", MCTSPlayer(simulations=100)),
        ("MCTS-200", MCTSPlayer(simulations=200)), 
        ("MCTS-500", MCTSPlayer(simulations=500)),
        ("Minimax-3", MinimaxPlayer(depth=3)),
        ("Minimax-4", MinimaxPlayer(depth=4)),
        ("Minimax-5", MinimaxPlayer(depth=5))
    ]
    
    results = []
    
    # Benchmark each algorithm against random player
    for name, player in algorithms:
        try:
            result = benchmark_algorithm(player, random_player, games=20, name=name)
            format_results(result)
            results.append(result)
        except KeyboardInterrupt:
            print(f"\n⚠️  Benchmark interrupted during {name}")
            break
        except Exception as e:
            print(f"\n❌ Error benchmarking {name}: {e}")
            continue
            
    # Summary comparison
    if len(results) > 1:
        print("\nPerformance Summary:")
        print("=" * 50)
        print(f"{'Algorithm':<12} {'Win Rate':<10} {'Avg Move':<10} {'Strength'}")
        print("-" * 50)
        
        for result in sorted(results, key=lambda x: x['win_rate'], reverse=True):
            strength = "Strong" if result['win_rate'] > 0.8 else "Medium" if result['win_rate'] > 0.6 else "Weak"
            print(f"{result['name']:<12} {result['win_rate']:<10.1%} {result['avg_move_time']:<10.3f} {strength}")

def main():
    """Main benchmark function with argument parsing."""
    
    parser = argparse.ArgumentParser(description='Benchmark MCTS vs Minimax for Connect 4')
    parser.add_argument('--games', type=int, default=20, help='Number of games per algorithm')
    parser.add_argument('--mcts-sims', type=int, default=200, help='MCTS simulations')
    parser.add_argument('--minimax-depth', type=int, default=4, help='Minimax search depth')
    parser.add_argument('--quick', action='store_true', help='Run quick benchmark suite')
    
    args = parser.parse_args()
    
    if args.quick:
        run_quick_benchmark()
    else:
        # Custom benchmark
        print(f"Custom Benchmark: MCTS-{args.mcts_sims} vs Minimax-{args.minimax_depth}")
        print(f"Games: {args.games}")
        print("=" * 60)
        
        mcts_player = MCTSPlayer(simulations=args.mcts_sims)
        minimax_player = MinimaxPlayer(depth=args.minimax_depth)
        
        # MCTS vs Minimax
        mcts_result = benchmark_algorithm(
            mcts_player, minimax_player, 
            games=args.games, name=f"MCTS-{args.mcts_sims}"
        )
        format_results(mcts_result)
        
        # Minimax vs MCTS
        minimax_result = benchmark_algorithm(
            minimax_player, mcts_player,
            games=args.games, name=f"Minimax-{args.minimax_depth}"
        )
        format_results(minimax_result)
        
        print(f"\nHead-to-Head Summary:")
        print(f"MCTS-{args.mcts_sims}: {mcts_result['win_rate']:.1%} win rate")
        print(f"Minimax-{args.minimax_depth}: {minimax_result['win_rate']:.1%} win rate")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        sys.exit(1)
