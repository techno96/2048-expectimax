from __future__ import absolute_import, division, print_function
import copy, random
from game import Game
import math
import numpy as np

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 
WT_MATRIX = np.array([[7,6,5,4], [6,5,4,3], [5,4,3,2], [4,3,2,1]])

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

        self.payoff = 0

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def getPayoff():
        return self.payoff

    def setPayoff(self, payoff):
        self.payoff = payoff
        

# AI agent. To be used to determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root
        if depth == self.search_depth: 
            return 

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)

            # NOTE: the following calls may be useful:
            self.simulator.reset(*(node.state))

            
            for direction in range(4):
                self.simulator.reset(*(node.state))

                initial_state = copy.deepcopy(self.simulator.get_state())

                if self.simulator.move(direction) and self.simulator.get_state() != initial_state:
                    child_node = Node(self.simulator.get_state(), CHANCE_PLAYER)
                    node.children.append([direction, child_node])

            self.simulator.reset(*(node.state))


        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
        

            self.simulator.reset(*(node.state))
            open_tiles = self.simulator.get_open_tiles()

            
            for entry in open_tiles:
                self.simulator.reset(*(node.state))
    
                st = copy.deepcopy(self.simulator.get_state())
                st[0][entry[0]][entry[1]] = 2

                child_node = Node(st, MAX_PLAYER)

                node.children.append([None, child_node])
                

            self.simulator.reset(*(node.state))


        # TODO: build a tree for each child of this node

        
        for c in node.children:
            self.build_tree(c[1], depth + 1)

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):

        if node == None:
            node = self.root

        if node.is_terminal():
            # double check this
            return None, node.state[1]

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic

            value = float("-inf")
            direction = None

            for i in range(len(node.children)):
                e = self.expectimax(node.children[i][1])

                if e[1] > value:
                    value = e[1]
                    direction = node.children[i][0]

            return direction, value

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0.0
            for child in node.children:
                value += self.expectimax(child[1])[1] * (1.0/len(node.children))
            
            return None, value


    # Expectimax implementation with improved heuristic
    # Referenced from https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf        
    def expectimax_ec(self, node = None):

        if node == None:
            node = self.root

        if node.is_terminal():
            # double check this
            return None, self.get_wt_score(node.state)

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic

            value = float("-inf")
            direction = None

            for i in range(len(node.children)):
                e = self.expectimax_ec(node.children[i][1])

                if e[1] > value:
                    value = e[1]
                    direction = node.children[i][0]

            return direction, value

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0.0
            for child in node.children:
                value += self.expectimax_ec(child[1])[1] * (1.0/len(node.children))
            
            return None, value

    def get_empty_tiles(self, state):
        count = 0
        for i in range(0, len(state)):
            for j in range(0, len(state)):
                if state[i][j] == 0:
                    count += 1
        return count        

    # Returns a weighted score (heuristic) for Depth 3 tree
    # Also rewards based on the empty tiles since they signify that
    # the game is proceeding in the right direction    
    def get_wt_score(self, state):
        return np.sum(np.multiply(np.array(state[0]), WT_MATRIX)) + 5 * self.get_empty_tiles(state[0])
                

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
       
        direction, _ = self.expectimax(self.root)
        return direction

    # Implement expectimax with customized evaluation function here
    def compute_decision_ec(self):
        self.build_tree()
       
        direction, _ = self.expectimax_ec(self.root)
        return direction
