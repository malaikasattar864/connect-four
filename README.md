Introduction: 

The game we chose is Connect Four. Connect Four is a two-player, abstract strategy game that is played on a grid. The game's objective is to be the first player to connect four of their own discs in a row, either horizontally, vertically, or diagonally, within the grid. Attached with the report are four codes:  

MCTS Implementation – Human Vs AI  

MCTS Implementation – AI Vs AI  

Alpha Beta Pruning – Human Vs AI  

Alpha Beta Pruning – AI Vs AI  

Alpha-Beta Pruning is a classic adversarial search algorithm, while MCTS is a probabilistic search algorithm Following is the comparative analysis of the above-mentioned code according to their efficiency and accuracy: 

 

Comparative Analysis:  

To compare both the code i.e., Monte-Carlo Tree Search and Alpha Beta Pruning, we will analyze efficiency in terms of the number of nodes explored and accuracy in terms of the quality of moves chosen by each algorithm.   

 

Efficiency - Number of Nodes Explored:  

In the MCTS code, the number of nodes explored is calculated by counting the number of times “select_uct” is called, as this is where the algorithm decides which child node to explore. The “node.N” attribute represents the number of times a node has been visited. In our code it all depends on the parameter t which is the time in seconds in which the algorithm has to make a decision. So, the algorithm tries to visit as many nodes as it can in that allocated time.  

In the Alpha-Beta Pruning code, the number of nodes explored is not explicitly counted, but it is calculated by adding a counter within the “minimax” function to track the number of nodes visited during the search.  

   

Accuracy - Quality of Moves:  

The quality of moves is assessed by the outcome of the game (win, lose, or tie) after a move is made. Further accuracy of the codes is calculated by running each multiple times and seeing the results.   

When the MCTS was run multiple times, it always won the game in Human Vs AI code. The MCTS is designed in such a way that it never lets the human player win. We tried multiple times to play but always lost. In the AI Vs AI, the AI’s won alternatively depending upon who did the first move? The first move is randomly selected using the random library in python. So sometimes AI X wins and sometimes AI O wins the game.  

In the case of Alpha-Beta Pruning, AI always won against the AI but It was noticed that it’s moves a little less genius than the MCTS. But in the case of an AI Vs AI, one AI always won the game.   

Insights:  

In an ideal AI Vs AI game, none of the AI should be able to win the game because both are equally intelligent. This happens in games like tic-tac-toe where the game space is very small, and chances of tie are higher. But in the case of our game the game pieces are placed in stacks so eventually there comes an instant when one of the AI has to win the game. Our board game is bigger than most usual games, it’s 6 x 7. 

 

 
