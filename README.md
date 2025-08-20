# Connect 4: MCTS vs Minimax Algorithm Comparison

## Overview

This project compares Monte Carlo Tree Search (MCTS) and Minimax with alpha-beta pruning in Connect 4. Spoiler alert: MCTS gets thoroughly outclassed, but that's actually the interesting part. This experiment demonstrates why algorithm choice matters more than parameter tuning.

## What I Found

### Alpha-Beta Pruning Performance (Expected but Impressive)
- **2-10x runtime speedup** over basic minimax across all depths
- Pruning effectiveness increases with search depth
- Essential for any practical minimax implementation

### MCTS vs Minimax (MCTS Clearly Outclassed)
- **MCTS win rates**: 2-19% across simulation counts (50-500)
- **Minimax-4 dominance**: 60-80% win rates consistently
- Even 10x more simulations don't help MCTS much

### Why MCTS Fails in Connect Four
1. **Wrong domain**: Connect Four is deterministic with low branching factor - perfect for Minimax
2. **Random rollouts are weak**: MCTS relies on random play evaluation, which leads to draws
3. **Convergence issues**: MCTS learns "not to lose" but struggles to find winning tactics

## Key Insight
**Don't force MCTS into domains where Minimax excels.** Save MCTS for games with imperfect information, huge state spaces, or weak evaluation functions (like Go).

## Implementation

### Monte Carlo Tree Search (MCTS)
- Random game simulations with UCB1 selection policy
- Scales linearly with simulation count
- Best for uncertain/complex game domains

### Minimax with Alpha-Beta Pruning  
- Systematic tree search with heuristic evaluation
- Exponential scaling with depth (but pruning helps)
- Perfect for tactical, perfect-information games

## Experimental Setup

### Prerequisites
```bash
pip install numpy pygame matplotlib pandas seaborn scipy jupyter
```

### Running the Analysis
```bash
# Main analysis notebook (recommended starting point)
jupyter notebook connect4_algorithm_analysis.ipynb

# Interactive game
python game.py

# Quick performance test
python benchmark.py

# Full test suite
python run_all_tests.py
```

### Configuration
Edit `game.py` to modify player types:
```python
# Game supports these player configurations:
# 1 - Human vs Human
# 2 - Human vs Minimax  
# 3 - Human vs MCTS
# 4 - Minimax vs MCTS
# 5 - MCTS vs Minimax
```

## Experimental Results

### Statistical Methodology
- 3 independent runs with 100 games each (300 total per comparison)
- Controlled randomization with explicit seeding
- 95% confidence intervals for all performance metrics
- Multiple simulation counts tested (50, 100, 200, 500)

### Runtime Performance
- **MCTS**: Linear scaling (0.8s to 4.2s for 50-500 simulations)
- **Minimax**: Exponential scaling with depth
- **Alpha-beta pruning**: Makes deeper search practical

## What I Learned

This experiment confirmed what game theory suggests: **choose algorithms that fit the domain**. 

**For Connect Four specifically:**
- Minimax excels because it's a tactical, perfect-information game
- MCTS struggles because random rollouts don't capture tactical patterns
- Alpha-beta pruning is essential, not optional

**General lesson:**
Don't try to force trendy algorithms (MCTS) into domains where classical approaches (Minimax) are optimal.

## Project Structure

```
mcts-connect4-recovered/
├── connect4.py                       # Core game logic and Connect4 class
├── mcts.py                          # MCTS implementation  
├── minimax.py                       # Minimax with alpha-beta pruning
├── game.py                          # Interactive pygame interface
├── connect4_algorithm_analysis.ipynb # Main experimental analysis
├── benchmark.py                     # Performance testing utilities
├── test_*.py                       # Test files for validation
├── run_all_tests.py                # Master test runner
└── README.md                       # This file
```

## Files to Focus On

1. **`connect4_algorithm_analysis.ipynb`** - Main experimental notebook with all analysis
2. **`minimax.py`** - See alpha-beta pruning implementation
3. **`mcts.py`** - MCTS implementation 
4. **`game.py`** - Play interactively to get intuition for the algorithms

## Technical Notes

### Statistical Validation
- Confidence intervals quantify uncertainty in win rates
- Multiple independent runs eliminate systematic bias  
- Large sample sizes (300+ games) provide reliable statistics
- Explicit seed management ensures reproducibility

### Why This Matters
Perfect example of **algorithm selection** being more important than parameter optimization. Even with 10x more simulations, MCTS can't overcome its fundamental mismatch with Connect Four's domain characteristics.

## Game Features

### Interactive Interface
- **Mouse hover effect**: Piece follows your mouse for smooth gameplay
- **Multiple game modes**: Human vs Human, Human vs AI, AI vs AI
- **Real-time gameplay**: Watch AI algorithms think and play
- **Clean interface**: Simple but effective pygame visualization

### AI Configuration
- **MCTS simulations**: Adjustable from 50 to 1000+ (more = stronger but slower)
- **Minimax depth**: Adjustable from 3 to 6+ (deeper = stronger but exponentially slower)
- **Alpha-beta pruning**: Always enabled for practical performance

### Testing Suite
- **Unit tests**: Individual component validation
- **Integration tests**: Algorithm behavior verification
- **Tournament analysis**: Head-to-head performance comparison (in Jupyter notebook)
- **Master test runner**: Run everything with `python run_all_tests.py`

## Research Applications

This project demonstrates key concepts for computer science research:

### Algorithm Analysis
- **Empirical comparison** of different AI approaches
- **Statistical significance** testing with proper sample sizes
- **Performance vs accuracy** trade-offs in real systems

### Domain Characteristics
- **Perfect vs imperfect information** game differences
- **Branching factor** effects on algorithm choice
- **Evaluation function** importance in tree search

### Experimental Methodology
- **Reproducible results** with controlled randomization
- **Confidence intervals** for uncertainty quantification
- **Multiple independent runs** for validation

---
