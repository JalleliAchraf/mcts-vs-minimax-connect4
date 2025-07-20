import math
import random
from connect4 import Connect4

class Node:
    def __init__(self, game_state, move=None, parent=None, player_who_moved=None):
        """
        MCTS Node representing a game state
        
        Args:
            game_state: Connect4 game at this state
            move: The move that led to this state (column number)
            parent: Parent node in the tree
            player_who_moved: Player who made the move to reach this state
        """
        self.game_state = game_state.copy_game()  
        self.move = move              
        self.parent = parent         
        self.player_who_moved = player_who_moved  
        
        # MCTS statistics
        self.visits = 0               
        self.wins = 0                 
        self.children = []            
        self.untried_moves = self.game_state.get_valid_moves() 
    def get_next_player(self):
        """Get the player whose turn it is at this node"""
        if self.player_who_moved is None: 
            return 1  
        return 3 - self.player_who_moved 
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    def is_terminal(self):
        return self.game_state.get_game_state() != 0
    def ucb1_score(self, C=math.sqrt(2)):
        """Calculate UCB1 score for node selection"""
        if self.visits==0:
            return float('inf')
        else:
            return (self.wins/self.visits) + C * math.sqrt(math.log(self.parent.visits) / self.visits)
    def select_best_child(self):
        """Select child with highest UCB1 score"""
        if not self.children:  
            return None
        best_score = max(child.ucb1_score() for child in self.children)
        best_children = [child for child in self.children if child.ucb1_score() == best_score]
        return random.choice(best_children)  
    def expand_node(self):
        if not self.is_fully_expanded():
            move_to_try=self.untried_moves.pop()
            player=self.get_next_player()
            current_state=self.game_state.copy_game()
            current_state.simulate_move(move_to_try,player)
            child=Node(current_state,move_to_try,self,player)
            self.children.append(child)  
            return child
        else:
            return None
    def simulate(self):
        """Run a random simulation from this node to a terminal state"""
        current_state=self.game_state.copy_game()
        player=self.get_next_player()
        while current_state.get_game_state() == 0 and len(current_state.get_valid_moves()) > 0:
            valid_moves = current_state.get_valid_moves()
            move_to_make=random.choice(valid_moves)
            current_state.simulate_move(move_to_make,player)
            player=3-player
        return current_state.get_game_state()  
    def backpropagate(self, result):
        """Update statistics back up the tree"""
        self.visits += 1
        if result == self.player_who_moved:
            self.wins += 1
        elif result == 3:  
            self.wins += 0.5
        if self.parent:
            self.parent.backpropagate(result)
class MCTSPlayer:
        def __init__(self, simulations=1000):
            """MCTS-based Connect 4 player"""
            self.simulations = simulations
        def _select(self, node):
            """Phase 1: Selection - Navigate down the tree using UCB1"""
            while not node.is_terminal() and node.is_fully_expanded():
                best_child = node.select_best_child()
                if best_child is None:  
                    break
                node = best_child
            return node
             
        def get_move(self, game, player):
            """Get the best move using MCTS"""
            root = Node(game, parent=None, player_who_moved=3 - player) 
            for i in range(self.simulations):
                node = self._select(root)
                if not node.is_terminal():
                    expanded_node = node.expand_node()
                    if expanded_node:  
                        node = expanded_node
                result = node.simulate()
                node.backpropagate(result)
            
            # Safety check: if no children were created, fall back to random valid move
            if not root.children:
                valid_moves = root.game_state.get_valid_moves()
                if valid_moves:
                    return random.choice(valid_moves)
                else:
                    return 0  
            
            best_child = max(root.children, key=lambda child: child.visits)
            return best_child.move

                




 
        
        
   