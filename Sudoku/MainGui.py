from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QDialog, QVBoxLayout, QLabel
import sys
from Generator import Generator

difficulties = {
    'easy': (35, 0),
    'medium': (81, 5),
    'hard': (81, 10),
    'extreme': (81, 15)
}


class Game:
    def __init__(self, level: str):
        self.difficulty = difficulties[level]
        self.gen = Generator(self.difficulty)
        self.gen.randomize(100)
        self.size_of_table = 9
        self.solved = self.gen.board.copy()  # a copy of table (solved)
        self.gen.reduce_via_logical(self.difficulty[0])
        if self.difficulty[1] != 0:
            self.gen.reduce_via_logical(self.difficulty[1])
        self.final_table = self.gen.board.copy()

    def is_solve(self) -> bool:
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table[i][j] != self.solved[i][j]:
                    return False
        return True

    def add_number(self, a: int, b: int, number: int):
        if self.final_table[a][b] == 0 and self.solved[a][b] == number:
            self.final_table[a][b] = number
            return 0
        if self.final_table[a][b] == 0:
            if self.check_possible(a, b, number):
                return 1
        return 2

    def check_possible(self, a: int, b: int, number: int) -> bool:
        for i in range(self.size_of_table):
            if self.final_table[i][b] == self.final_table[a][b] or self.final_table[a][i] == self.final_table[a][b]:
                return False
        starting_a = (a // 3) * 3
        starting_b = (b // 3) * 3
        for i in range(starting_b, starting_b + 3, 1):
            for j in range(starting_a, starting_a + 3, 1):
                if self.final_table[i][j] == self.final_table[a][b]:
                    return False
        return True


class MyWindows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.game = Game('extreme')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindows()
    app.exec()
