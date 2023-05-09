import random

class minesweeperModel:
    def __init__(self):
        self.newGame()

    def newGame(self):
        self.stateOfGame = 0
        self.squaresClicked = 0
        #10 Random Bomb Locations
        self.bombLocations = []
        #This is to make sure that every bomb is on a unique square
        while len(self.bombLocations) != 10:
            temp = [random.randint(1,10), random.randint(1,10)]
            for loc in self.bombLocations:
                if loc == temp:
                    break
            else:
                self.bombLocations.append(temp)

    def clickedSquare(self, row, col):
        self.squaresClicked += 1
        count = 0
        temp = [row, col]
        #If the square is a bomb set the gamestate to -1 to show you lost
        for bomb in self.bombLocations:
            if temp == bomb:
                self.stateOfGame = -1
                return -1
            
        #If the square doesn't have any bombs surrounding it, return 0
        surroundingSquares = [[row-1, col-1],[row-1,col], [row-1, col+1], [row, col-1], [row, col+1], [row+1, col-1], [row+1, col], [row+1, col+1]]
        for i in range(10):
            for surSqrs in surroundingSquares:
                if self.bombLocations[i] == surSqrs:
                    count+=1
        return count
    
    def gameState(self):
        # -1 means you lost the game
        # 0 means game is in progress
        # 1 means the game has been won
        if(self.squaresClicked >= 90 and self.stateOfGame != -1):
            return 1
        elif(self.stateOfGame == -1 and self.squaresClicked < 90):
            return -1
        else:
            return 0