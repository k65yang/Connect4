import math
import random
import copy

class Player:
    def __init__(self, marker) -> None:
        self.marker = marker
        self.isAI = False

    def getMarker(self) -> str:
        return self.marker
    
    def getMove(self) -> None:
        pass

class HumanPlayer(Player):
    def __init__(self, marker) -> None:
        super().__init__(marker)
    
    def getMove(self, game) -> int:
        val = None
        validMoves = game.getAvailableMoves()

        while val == None:
            col = input(self.marker + "\'s turn. Input move (0-6):")
            try:
                val = int(col)
                if val not in validMoves:
                    val = None
                    raise ValueError
                return val
            except ValueError:
                print("Invalid square, try again")
        
        return val

class AIComputer(Player):
    def __init__(self, marker) -> None:
        super().__init__(marker)
        self.isAI = True

    def getMove(self, game) -> int:
        return self.minimax(game, 10, -math.inf, math.inf, True)[0]
    
    def minimax(self, game, depth, alpha, beta, maxPlayer) -> int:
        availableMoves = game.getAvailableMoves()

        if game.hasWinner() or not game.hasMoves() or depth == 0:
            if game.hasWinner(): # someone won the game
                return (None, math.inf) if maxPlayer else (None, -math.inf)
            elif depth == 0: # reached max depth of search
                return (None, game.scoreBoard(self.marker))
            else: # game is tied, no more moves
                return (None, 0)
        
        if maxPlayer:
            score = -math.inf
            colActual = random.choice(availableMoves)
            for col in availableMoves:
                gameCopy = copy.deepcopy(game)
                gameCopy.makeMove(col, self.marker)
                scoreTemp = self.minimax(gameCopy, depth-1, alpha, beta, False)[1]
                if scoreTemp > score:
                    score = scoreTemp
                    colActual = col
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return colActual, score
        else:
            score = math.inf
            colActual = random.choice(availableMoves)
            for col in availableMoves:
                gameCopy = copy.deepcopy(game)
                gameCopy.makeMove(col, "R" if self.marker == "B" else "B")
                scoreTemp = self.minimax(gameCopy, depth-1, alpha, beta, True)[1]
                if scoreTemp < score:
                    score = scoreTemp
                    colActual = col
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return colActual, score