from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from minesweeperModel import *

class minesweeperWindow(QMainWindow):
    def __init__(self):
        super(minesweeperWindow, self).__init__()

        self.buttons = []

        #Menu setup to play a new game
        self.setWindowTitle("Minesweeper")
        menu = self.menuBar().addMenu("&Game")
        newAct = QAction("&New", self, shortcut=QKeySequence.New, triggered=self.newGame)
        menu.addAction(newAct)

        widget = QWidget()
        self.setCentralWidget(widget)

        #Create QVBoxLayout
        layout = QVBoxLayout()
        widget.setLayout(layout)

        #Create QHBoxLayout with 2 QLabels and add
        #them to the QVBoxLayout
        qhLayout = QHBoxLayout()
        bombcount = QLabel("10 Bombs")
        bombcount.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        bombcount.setAlignment(Qt.AlignCenter)
        qhLayout.addWidget(bombcount)
        self.gameStatus = QLabel("In Progress")
        self.gameStatus.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.gameStatus.setAlignment(Qt.AlignCenter)
        qhLayout.addWidget(self.gameStatus)
        layout.addLayout(qhLayout)

        #Create the grid and add it to the QVBoxLayout
        grid = QGridLayout()
        grid.setSpacing(0)
        for rows in range(10):
            for cols in range(10):
                button = QPushButton()
                button.clicked.connect(self.buttonClicked)
                button.setFixedSize(QSize(40,40))
                button.setProperty("myRow", rows+1)
                button.setProperty("myCol", cols+1)
                button.setObjectName(str(rows+1) + str(cols+1))
                grid.addWidget(button, rows, cols)
        layout.addLayout(grid)

        self.model = minesweeperModel()

        self.newGame()

    def newGame(self):
        #Testing
        print("New Game Started")
        #Reset the buttons
        for button in self.buttons:
            button.setEnabled(True)
            button.setText("")
        #Clear the button list
        self.buttons = []
        #Change game status back to in progress
        self.gameStatus.setText("In Progress")
        #Make the new game
        self.model.newGame()

    def buttonClicked(self):
        #Retrieves which button was clicked
        clicked = self.sender()
        self.reveal(clicked)
        row = clicked.property("myRow")
        col = clicked.property("myCol")
        #Testing purposes
        print(f"Button {row}x{col} was pressed")
        print(f"Name of the button is {clicked.objectName()}")
        #Send the information to the model and get back a number determining what to do
        #Return type 0 means no bombs surrounding it
        #Return type anything else means thats the num of bombs around that square
        result = self.model.clickedSquare(row, col)
        if(result == -1):
            #This is a bomb
            clicked.setText(chr(0x25cf))
        elif(result == 0):
            #Gets the surrounding squares of the square
            surroundingSquares = [[row-1, col-1],[row-1,col], [row-1, col+1], [row, col-1], [row, col+1], [row+1, col-1], [row+1, col], [row+1, col+1]]
            #passes the list of surrounding squares into a method to automatically disable the surrounding buttons
            self.checkSquare(surroundingSquares)
        else:
            #Shows how many bombs surrounding the square
            clicked.setText(str(result))
        #Adds the button to the list
        #Check game status
        if(self.model.gameState(self.buttons) == 1):
            self.gameStatus.setText("Game Won!")
        elif(self.model.gameState(self.buttons) == -1):
            self.gameStatus.setText("Game Lost!")
    
    #Method for when a button needs to be disabled
    def reveal(self, button):
        button.setEnabled(False)
        self.buttons.append(button)
        #Removes duplicates
        self.buttons = list(set(self.buttons))

    #To automatically disable a button
    def checkSquare(self, listOfSurroundingSquares):
        #While the list has values
        while listOfSurroundingSquares:
            #Pop the first value
            temp = listOfSurroundingSquares.pop(0)
            #Test
            print(temp)
            #Make sure the square is in the grid
            if (temp[0] >= 1 and temp[0] <= 10) and (temp[1] >= 1 and temp[1] <= 10):
                #If it is check the square
                result = self.model.clickedSquare(temp[0], temp[1])
                #If it has no bombs surrounding it then add all the surrounding squares to the list
                if result == 0:
                    self.reveal(self.centralWidget().findChild(QPushButton, str(temp[0]) + str(temp[1])))
                #Reveal the square and print how many bombs are near it
                else:
                    self.reveal(self.centralWidget().findChild(QPushButton, str(temp[0]) + str(temp[1])))
                    self.centralWidget().findChild(QPushButton, str(temp[0]) + str(temp[1])).setText(str(result))
        
        #Just in case check if you've won
        #No need to check if you've lost because it won't reveal a square with a bomb on it
        if(self.model.gameState(self.buttons) == 1):
            self.gameStatus.setText("Game Won!")