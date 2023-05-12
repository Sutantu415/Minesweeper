import random

class minesweeperModel:
    def __init__(self):
        self.newGame()

    def newGame(self):
        self.stateOfGame = 0
        self.squaresClicked = 0
        self.bombLocations = []

    def clickedSquare(self, row, col):
        self.squaresClicked += 1
        count = 0
        #Sets the bombs if the square is the first square clicked to initialize the game
        #makes it so the first square and surrounding squares will never be bombs
        if(self.squaresClicked == 1):
            self.makeBombs(row, col)
            return count
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
    
    def gameState(self, listOfButtons):
        # -1 means you lost the game
        # 0 means game is in progress
        # 1 means the game has been won
        if(len(listOfButtons) >= 90 and self.stateOfGame != -1):
            return 1
        elif(self.stateOfGame == -1 and len(listOfButtons) < 90):
            return -1
        else:
            return 0
        
    def makeBombs(self, row, col):
        #10 Random Bomb Locations
        #This is to make sure that every bomb is on a unique square after the first square has been clicked
        #Also makes it so that it has no bombs surrounding that starting square
        nonAvailableSquares = [[row, col], [row-1, col-1],[row-1,col], [row-1, col+1], [row, col-1], [row, col+1], [row+1, col-1], [row+1, col], [row+1, col+1]]
        while len(self.bombLocations) != 10:
            temp = [random.randint(1,10), random.randint(1,10)]
            for invalid in nonAvailableSquares:
                if invalid == temp:
                    break
            else:
                for loc in self.bombLocations:
                    if loc == temp:
                        break
                else:
                    self.bombLocations.append(temp)