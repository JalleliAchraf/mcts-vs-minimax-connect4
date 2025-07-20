#!/usr/bin/env python3
"""
Comprehensive MCTS Testing Suite
Tests individual components and overall algorithm performance
"""

import time
import random
from connect4 import Connect4
from mcts import MCTSPlayer, Node
from minimax import MinimaxPlayer

def test_node_basics():
    """Test Node class fundamental operations"""
    print("=== Testing Node Basics ===")
    
    game = Connect4()
    node = Node(game)
    
    # Test initial state
    assert node.visits == 0, "Initial visits should be 0"
    assert node.wins == 0, "Initial wins should be 0"
    assert len(node.children) == 0, "Initial children should be empty"
    assert len(node.untried_moves) == 7, "Should have 7 untried moves initially"
    
    # Test player logic
    assert node.get_next_player() == 1, "First player should be 1"
    
    # Test terminal detection
    assert not node.is_terminal(), "Empty board should not be terminal"
    assert not node.is_fully_expanded(), "Empty node should not be fully expanded"
    
    print("✓ Node basics passed!")

def test_node_expansion():
    """Test node expansion mechanics"""
    print("=== Testing Node Expansion ===")
    
    game = Connect4()
    root = Node(game)
    
    # Test first expansion
    child1 = root.expand_node()
    assert child1 is not None, "First expansion should create child"
    assert len(root.children) == 1, "Root should have 1 child"
    assert len(root.untried_moves) == 6, "Root should have 6 untried moves left"
    assert child1.parent == root, "Child should point to parent"
    assert child1.move in [0,1,2,3,4,5,6], "Child move should be valid column"
    
    # Test multiple expansions
    for i in range(6):  # Expand remaining moves
        child = root.expand_node()
        assert child is not None, f"Expansion {i+2} should succeed"
    
    assert len(root.children) == 7, "Root should have 7 children"
    assert root.is_fully_expanded(), "Root should be fully expanded"
    
    # Test over-expansion
    child_extra = root.expand_node()
    assert child_extra is None, "Over-expansion should return None"
    
    print("✓ Node expansion passed!")

def test_ucb1_calculation():
    """Test UCB1 scoring mechanism"""
    print("=== Testing UCB1 Calculation ===")
    
    game = Connect4()
    root = Node(game)
    
    # Create children and simulate visits
    child1 = root.expand_node()
    child2 = root.expand_node()
    
    # Unvisited nodes should have infinite UCB1
    assert child1.ucb1_score() == float('inf'), "Unvisited node should have inf UCB1"
    
    # Simulate some statistics
    root.visits = 10
    child1.visits = 5
    child1.wins = 3
    child2.visits = 3
    child2.wins = 1
    
    ucb1_1 = child1.ucb1_score()
    ucb1_2 = child2.ucb1_score()
    
    assert isinstance(ucb1_1, float), "UCB1 should return float"
    assert isinstance(ucb1_2, float), "UCB1 should return float"
    assert ucb1_1 > 0, "UCB1 should be positive"
    assert ucb1_2 > 0, "UCB1 should be positive"
    
    print(f"  Child1 UCB1: {ucb1_1:.3f}")
    print(f"  Child2 UCB1: {ucb1_2:.3f}")
    print("✓ UCB1 calculation passed!")

def test_simulation_consistency():
    """Test that simulation produces valid results"""
    print("=== Testing Simulation Consistency ===")
    
    game = Connect4()
    node = Node(game)
    
    results = []
    for _ in range(50):  # Run many simulations
        result = node.simulate()
        results.append(result)
        assert result in [0, 1, 2, 3], f"Invalid simulation result: {result}"
    
    # Check we get variety in results
    unique_results = set(results)
    print(f"  Simulation results seen: {sorted(unique_results)}")
    assert len(unique_results) >= 2, "Should see multiple different outcomes"
    
    print("✓ Simulation consistency passed!")

def test_backpropagation():
    """Test backpropagation mechanics"""
    print("=== Testing Backpropagation ===")
    
    game = Connect4()
    root = Node(game)
    child = root.expand_node()
    grandchild = child.expand_node()
    
    # Test backpropagation from grandchild
    initial_visits = [root.visits, child.visits, grandchild.visits]
    
    grandchild.backpropagate(1)  # Player 1 wins
    
    final_visits = [root.visits, child.visits, grandchild.visits]
    
    # All nodes should have increased visits
    for i in range(3):
        assert final_visits[i] == initial_visits[i] + 1, f"Node {i} visits not updated correctly"
    
    # Check win attribution
    if grandchild.player_who_moved == 1:
        assert grandchild.wins == 1, "Grandchild should get win if they're player 1"
    
    print("✓ Backpropagation passed!")

print("Running MCTS Unit Tests...")
test_node_basics()
test_node_expansion()
test_ucb1_calculation()
test_simulation_consistency()
test_backpropagation()
print("\n🎉 All unit tests passed!")
