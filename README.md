# 2048-expectimax
Simulating an AI playing 2048 using the Expectimax algorithm

The base game engine uses code from [here](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2). 

The AI player is modeled as a max player, and the computer as a chance player (picking a random open spot to place a 2-tile). The score returned by the game engine is used as the evaluation function value at the leaf nodes of the trees. 

You can play the game manually using the arrow keys. Pressing 'Enter' will let the AI play, and pressing 'Enter' again will stop the AI player. Read the game engine code from 'game.py' and see how it returns the game state and evaluate its score from an arbitrary game state after an arbitrary player move. 

A depth-3 game tree means the tree should have the following levels: 

- root: player
- level 1: computer 
- level 2: player
- level 3: terminal with payoff (note that we say "terminal" to mean the leaf nodes in the shallow game tree, not the termination of the game itself)

This tree represents all the game states of a player-computer-player sequence (the player makes a move, the computer place a tile, and then the player makes another move, and then evaluate the score) from the current state. 

Usage
-----
To run the program:
```
    python main.py
```

Once your program is running, here are a few keyboard options available in-game:
- 'r': restart the game
- 'u': undo a move
- '3'-'7': change board size
- 'g': toggle grayscale
