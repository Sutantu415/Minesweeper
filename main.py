from PyQt5.QtWidgets import QApplication
from minesweeperWindow import *

app = QApplication([])
window = minesweeperWindow()
window.show()
app.exec_()