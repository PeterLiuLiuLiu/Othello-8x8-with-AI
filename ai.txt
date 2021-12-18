1a. Did you attempt to make your computer player very smart -- i.e., 
	do something more clever than just pick a random legal move?
1b. If so, were you able to accomplish this? Is your computer player as smart as you would like?

	My original intent was to make a very smart robot AI that can determine the optimal move that and can calculate all the way to game ending to guarantee a win on the computer. 
	However reading online resources indicates that even even though 4x4 and 6x6 board is strongly solved, 8x8 board if solved this way requires too much computation resources to calculate than realistically possible[1].
	Therefore, a lookup from any game board state and dig out all possible moves are not possible for this final project. Apart from making it random, I choose two main strategies upon building the AI rather then to make random moves.

	I read through a blog by a writter called Marcin[2], and he basically divides the strategy of winning in Othello into 5 parts,
	Part 1 lists out most of the important details: About how to not lose the corners and keep mobility,
	Part 2 stresses the importance of quiet moves over loud moves and reiterated the use of imagination to project the game,
	Part 3 lists out the preferred opening strategy of keeping to the middle 4x4 board, 
	Part 4 lists out the importance of edge and strategy in general for different formations of pieces on board
	Part 5 finally talks about how to secure a win given the effort to not lose from part 1 to 4.

	My computer opponent is designed to mimic some part from part 1 to 4 aiming to:
	- Upon start of game, try staying at center 4x4 rather than  connect out via weak link
	- Try to keep as much mobility throughout the start to middle part of the game so there are maximum amount of choice in subsequent moves, not aim to make the loudest move, but the move that strategically lead to more mobability and advantageous position down the game
	- Throughout the game, try to capture other strategic locations like corners, edges, and stay at the centre
	- Try to make less mistakes and do not go for tiles surrounding corners since it increases the likeihood be corner tile captured by oponent
	- At start to middle of game, it tries to place white pieces on strategically benefitial locations, and when there are only 2X empty tiles left, 
		the computer will turn to finding the moves that flips the move opponent tile and based on the benefiticial location constructed before

	Overall, I think I can roughly achieve what I have aim for using the method that will be described in Q2, but I failed to incorporate all the knowledge from the blog due to time limitation, but the essence is there.
	Given some manually set game state, the computer AI is able to play the move that is deemed more suitable strategically in several occasions by "looking ahead" and use imagination. It is as smart as I like since I fail to beat it in general, and have not notice some random wrong moves made by it.
	More on the algorithm on Q2.
#
#
2. How did you determine which piece to play next?  Tell us about your “pick next move” algorithm.

The AI is divided into two parts

FIRST PART
--- The following happens at the start to middle of the game --- 
	The reason that the computer knows which position is strategically advantageous to place is because I have assigned a score-based valuation system to evaluate each move's value based on all possible moves by white based on current game state.
	For every game state that is white's turn, it will look into what moves possible, and it will build a tree based on each move to check what possible score the AI can get if exploring down. 
	For instance, assume that at current game state, the possible moves for white is [18, 20, 34]. The scoreboard will be set to 0 for all moves, and assume the computer will go down with depth = 2 in mind. 
	Here is the summary moves that will be done by computer calculation on move 18 alone with depth of tree = 2:



	Assign constsants (positive = rewards for white, negative = punishment for white) on:
		corners, edges not immediately next to corner, middle 4x4 (SWEET 16), move that wins the game for white -- positive
		immediate 3 tiles next to corners, move that loses the game for white

	Out of [18, 20, 34] choose 18 by white to start with...

	copy game_board and make move 18 -- __BY WHITE__ -- __AT DEPTH 2 (WHITE)__

		based on the move, get possible move for updated game_board, i.e. move [19, 21, 30] available for black
		copy game_board and move 19 -- __BY BLACK__, assign score cumulatively (multiple suitable contsants if move is special) to move 18 based on move 19 of black -- __ AT DEPTH 2 (BLACK)__

			based on the move, get possibel moves for updated game_board, i.e. move [20, 22, 25, 30] available for white
			copy game_board move 20 -- __ BY WHITE__, assign score cumulatively(multiple suitable contsants if move is special) to move 18 based on the move 20 by white -- __REACH DEPTH 1 (WHITE)__
			
				based on the move, get possibel moves for updated game_board, i.e. move [21, 24, 25, 26, 39] available for black
				copy game_board move 21 -- __ BY BLACK__, assign score cumulatively(multiple suitable contsants if move is special) to move 18 based on the move 21 by black-- __AT DEPTH 1 (BLACK)__
					

					based on the move, get possibel moves for updated game_board, i.e. move [12, 22, 24, 30, 35, 40] available for white
					copy game_board move 12 -- __ BY WHITE__, assign score cumulatively(multiple suitable contsants if move is special) to move 18 based on the move 12 by white -- __REACH DEPTH 0 (WHITE)__
				
					... CONTINUE for move by white [22, 24, 30, 35, 40]
					When finished all, go up back to black with depth 1 black

				... CONTINUE for move by black[24, 25, 26, 39]
				When finished all, go up back to black with depth 1 white

			add counter for number_of_immediate_child, number of possible black move by move 18 at depth 2 white, used to average the value
          	      For instance, Each of the 3 moves will have a value and calculate back to the move 18, which then needs to average out by 3 at depth 2 black since move 21 may have 10 moves at depth 2 black, 
			... CONTINUE for move by white [22, 25, 30]
			When finished all, go up back to black with depth 2 black

		... CONTINUE for move by white [21, 30]
		When finished all, go up back to black with depth 2 white

	... CONTINUE for move by white [20, 34]
	When return the total move_score_dict and choose the one with max. value determined after adding all the moves down the tree with rewards and punishment of advantageous and disadvantageous moves

	It loops recursive from depth 2 white to depth 0 white then traverse back to other sister nodes at various depth until all possible moves by white at current game state is explored, choose argmax value of move.

SECOND PART
--- The following happens at the near end of the game ---  

	Base on the strategic moves by the tree search before, the computer should have established beneficial position on the board, so from the later part of the game, the computer can choose moves that inflicts the max cpture and flipping of opponent, and feast on its effort before
	AI chances tactics from placing strategic moves for later benefits to placing move that captures move opponent pieces, after the empty tile on board is less than HARD_AI_CHANGE_TACTICS, a contant.
#
#
3. How often did your computer program beat you, or your friends, or whoever tested it out for you?

I am not a good player myself thus I have not beat the computer after I have finalized all the parameters, It will often seem to look at few steps ahead (which is not surprising since I build it) and determine the move that surprises me and strategically more valuable.
I have given my wife a chance to play it, noticed two things, it runs a lot faster on mac M1 chip, I guess since the recursion is expensive and M1 handles it better, and my wife is a worse player than me so she has not beat the computer once too. I will continue playing it until I beat it once, observe how it was beaten and probablty fine tune the parameters to optimize.
That also brings to the things to improve.

I remember the closest thing for me to beat it is to wait till the computer to make mistake. When the computer notice there are less tile than the constant, it changes tactics to play the maximum tile flipping move, I tried to wait and not make bad moves until the max. flipping turned on, and honestly I tried and sucessfully occupied FOUR corners and trapped the white in the center, but i still lose the game 31 to 33... =.=
The constant HARD_AI_CHANGE_TACTICS is set to 26 for precisely this reason, even tho optimalization has not been done, it is going to switch on max. flipping mode later after half of the game is made since switching it too early will cause the AI to make bad moves while not building enough good stragetically stronghold, while switching it too late makes the actual implementation of flipping delayed. 
Ultimately, one has to occupy tiles to win and the change mode did precisely capture as much flips as possible based on the good move the AI has done at the start to over half of the game.
#
#
4. How would you improve it in the future? 

First and foremost, Recursion is almost never the solution to a full scale problem like this since it is computationally expensive in terms of procesing speed and memory to search down the tree, even with a depth of 2 and actual traversal of a height 4 (W --> B --> W --> B --> W)
I may use iterations instead and try to score some game state to reuse in the future so that the computer need not compute the game state everytime with project move if it has been calculated before.

Secondly, the hard-code constant makes optimalization manual, and we might never get an optimal constant for rewards and punishment, so in the future after simplying the recursive structure, it is possible to set the constants into variable, feed it into a reinforcement learning algorithm and fine tune its value so that the optimal reward and punishment can make the score-based system more efective in determining the most valuable move

Finally, of course, the knowledge of Othello is endless, and I cannot simply include every detail of advantageous strategy in there, probably one source of improvement comes from the game that I also take into account the snapshot of game state and reward or punish the computer based on all pattern Wedge, Pair, Anchor...., with that score-algorithm of the overall game state not only on the move itself, the score can be more comprehensive in judging, thus lead to a AI



[1]: "Computer Othello -- Solving Othello" from Wikipedia: https://en.wikipedia.org/wiki/Computer_Othello
[2]: How to win at Othello?" by Marcin, Jan 4, 2017: https://bonaludo.com/2017/01/04/how-to-win-at-othello-part-1-strategy-basics-stable-discs-and-mobility/