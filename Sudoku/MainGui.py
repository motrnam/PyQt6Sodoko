import sys

import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, \
    QGridLayout

from Generator import Generator

INIT_SIZE_TILE = 40
difficulties = {
    'easy': (35, 0),
    'medium': (81, 5),
    'hard': (81, 10),
    'extreme': (81, 15)
}


class Game:
    def __init__(self, level: str):
        self.difficulty = difficulties[level]
        self.gen = Generator("../base.txt")
        self.gen.randomize(100)
        self.size_of_table = 9
        self.time = 0
        self.solved = self.gen.board.copy()  # a copy of table (solved)
        self.gen.reduce_via_logical(self.difficulty[0])
        if self.difficulty[1] != 0:
            self.gen.reduce_via_logical(self.difficulty[1])
        self.final_table = self.gen.board.copy()
        self.first_having_number = np.zeros((self.size_of_table, self.size_of_table))
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j] != 0:
                    self.first_having_number[i][j] = 1

    def is_solve(self) -> bool:
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j] != self.solved[i][j]:
                    return False
        return True

    def add_number(self, a: int, b: int, number: int):
        if self.final_table.rows[a][b] == 0 and self.solved[a][b] == number:
            self.final_table.rows[a][b] = number
            return 0
        if self.final_table.rows[a][b] == 0:
            if self.check_possible(a, b, number):
                return 1
        return 2

    def check_possible(self, a: int, b: int, number: int) -> bool:
        for i in range(self.size_of_table):
            if (self.final_table.rows[i][b] == self.final_table.rows[a][b] or self.final_table.rows[a][i] ==
                    self.final_table.rows[a][b]):
                return False
        starting_a = (a // 3) * 3
        starting_b = (b // 3) * 3
        for i in range(starting_b, starting_b + 3, 1):
            for j in range(starting_a, starting_a + 3, 1):
                if self.final_table[i][j] == number:
                    return False
        return True


class MyWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setFixedSize(500, 500)
        self.init_topBar()
        self.initUI()
        self.init_board()
        self.show()

    def init_topBar(self):
        self.timer_label = QLabel('Timer: 0', self)
        self.timer_label.setFont(QFont('Arial', 15))
        self.timer_label.move(0, 0)
        self.timer_label.adjustSize()
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.my_save)
        exit_action.triggered.connect(self.close)
        easy = QAction('easy', self)
        medium = QAction('medium', self)
        hard = QAction('hard', self)
        extreme = QAction('extreme', self)
        self.my_menubar = self.menuBar()
        self.file_menu = self.my_menubar.addMenu('File')
        self.new_game_menu = self.my_menubar.addMenu('New')
        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(save_action)
        easy.triggered.connect(lambda: self.new_game('easy'))
        medium.triggered.connect(lambda: self.new_game('medium'))
        hard.triggered.connect(lambda: self.new_game('hard'))
        extreme.triggered.connect(lambda: self.new_game('extreme'))
        self.new_game_menu.addAction(easy)
        self.new_game_menu.addAction(medium)
        self.new_game_menu.addAction(hard)
        self.new_game_menu.addAction(extreme)

    def add_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        # Update the timer label every second
        current_time = int(self.timer_label.text().split(':')[-1])
        current_time += 1
        self.timer_label.setText(f'Timer: {current_time}')

    def new_game(self, level: str):
        print(level)
        self.game = Game('easy')
        # self.initUI()

    def initUI(self):
        # self.add_timer()
        ...

    def init_board(self):
        layout = QGridLayout()
        self.all_button = list()
        for i in range(9):
            for j in range(9):
                button = QPushButton('1')
                button.setFixedSize(INIT_SIZE_TILE, INIT_SIZE_TILE)  # Set the fixed size of the button
                self.all_button.append(button)
                layout.addWidget(button, i, j)
                button.clicked.connect(lambda _, a=i, b=j: self.click_button(a, b))
                button.setStyleSheet(
                    'QPushButton {'
                    '    background-color: #E0E0E0;'
                    '    border: 1px solid #909090;'
                    '    border-radius: 5px;'
                    '}'
                    'QPushButton:hover {'
                    '    background-color: #C0C0C0;'
                    '}'
                )

        container = QWidget(self)
        container.setFixedSize(9 * INIT_SIZE_TILE, 9 * INIT_SIZE_TILE)
        container.move((self.width() - container.width()) // 2, (self.height() - container.height()) // 2)
        container.setLayout(layout)
        container.show()

    def change_board(self):
        ...

    def click_button(self, a: int, b: int):
        print(f'click {a} {b}')

    def my_save(self):
        print("save")
        table = self.game.final_table
        result = ""
        temp = ""
        for i in range(9):
            for j in range(9):
                result += str(table[i][j])
                temp += str(self.game.first_having_number[i][j])
        result += '\n'
        result += temp
        result += '\n'
        result += self.game.time
        with open("save.txt", "w") as f:
            f.write(result)

    def my_load(self):  # not tested
        with open("save.txt", "r") as f:
            table = f.readline()
            time = f.readline()
        table = table.split('\n')[0]
        time = time.split('\n')[0]
        table = [int(x) for x in table]
        self.game.final_table = table
        self.game.time = time
        self.change_board()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindows()
    app.exec()
