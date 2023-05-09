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
        #Change game status back to in progress
        self.gameStatus.setText("In Progress")
        #Make the new game
        self.model.newGame()

    def buttonClicked(self):
        #Retrieves which button was clicked
        clicked = self.sender()
        row = clicked.property("myRow")
        col = clicked.property("myCol")
        #Testing purposes
        print(f"Button {row}x{col} was pressed")
        #Disables that button
        clicked.setEnabled(False)
        #Send the information to the model and get back a number determining what to do
        #Return type 0 means no bombs surrounding it
        #Return type anything else means thats the num of bombs around that square
        result = self.model.clickedSquare(row, col)
        if(result == -1):
            clicked.setText(chr(0x25cf))
        elif(result == 0):
            #Do nothing
            pass
        else:
            clicked.setText(str(result))
        #Adds the button to the list
        self.buttons.append(clicked)
        #Check game status
        if(self.model.gameState() == 1):
            self.gameStatus.setText("Game Won!")
        elif(self.model.gameState() == -1):
            self.gameStatus.setText("Game Lost!")