from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QDialog, QVBoxLayout, QLabel

from Sudoku.Generator import Generator

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
        self.solved = self.gen.board.copy()  # a copy of table (solved)
        self.gen.reduce_via_logical(self.difficulty[0])
        if self.difficulty[1] != 0:
            self.gen.reduce_via_logical(self.difficulty[1])
        self.final_table = self.gen.board.copy()

    def is_solve(self) -> bool:
        return False

    def add_number(self, a: int, b: int, number: int):
        pass

    def check_possible(self, a: int, b: int, number: int) -> bool:
        ...


class MyWindows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
