import sys
from PyQt5.QtWidgets import *

from main.python.PyQt5.PhonebookWindow import PhonebookWindow


class Phonebook(QMainWindow):
    def __init__(self):
        super(Phonebook, self).__init__()
        self.ui = PhonebookWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        self.ui.db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    phonebook = Phonebook()
    phonebook.show()
    sys.exit(app.exec_())