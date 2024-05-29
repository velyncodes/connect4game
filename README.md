
# Connect Four Game
A game where the PLAYER and BOT take turns dropping chips into a grid, aiming to connect four chips of the same color in a row, either vertically, horizontally, or diagonally.

## How it works - Connect Four game with AI
- The Minimax Algorithm models a game as a *decision tree.*
- Each possible move in the game is represented by a tree. Each node in this tree corresponds to a game state, and each branch from a node represents a possible move.
- The algorithm operates recursively, exploring all potential moves until it reaches terminal positions. At each step:
    - If it is the Maximizer's turn, the algorithm selects the move that maximizes the value.
    - If it is the Minimizer's turn, the algorithm selects the move that minimizes the value.

## How to run this
Open your terminal and enter:  ```python connect4ai.py``` (to play with BOT) or ```python connect4.py``` (to play with your friend).


## Conclusion

The **Minimax Algorithm** is designed to teach a player the optimal moves to win a game. This algorithm aims to maximize the player's advantage while minimizing the opponent's advantage.

By using the Minimax algorithm, a player can thoroughly evaluate each potential move, enabling them to make the most advantageous decisions by anticipating the opponent's best possible responses.
