import sys

import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QAction, QCursor
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, \
    QGridLayout, QVBoxLayout, QToolTip, QHBoxLayout, QMessageBox
from pathlib import Path
from Generator import Generator

INIT_SIZE_TILE = 60
NUMBER = 9
FIRST_WINDOW_SIZE = 700
BOTTOM_NUMBER_SIZE = 45
NORMAL_BUTTON_STYLE = """
                QPushButton {
                background-color: #eaebff;
                color: black;
                padding: 10px 10px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            """
HIGHLIGHT_BUTTON_STYLE = """ 
        QPushButton {
                background-color: #ffcc77;
                color: black;
                padding: 10px 20px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover { 
                background-color: #ffcc00;
            }
            """

SELECTED_BUTTON_STYLE = """
        QPushButton {
                background-color: #999999;
                color: black;
                padding: 10px 20px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover { 
                background-color: #ffcc00;
            }
            """
FILL_BUTTON_STYLE = """
        QPushButton {
                background-color: #aaaaaa;
                color: black;
                padding: 10px 20px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover { 
                background-color: #ffcc00;
            }
            """
difficulties = {
    'easy': (35, 0),
    'medium': (81, 5),
    'hard': (81, 10),
    'extreme': (81, 15)
}


class Game:
    def __init__(self, level: str):
        self.level = level
        self.difficulty = difficulties[level]
        self.gen = Generator("../base.txt")
        self.gen.randomize(100)
        self.size_of_table = 9
        self.time = 0
        self.solved = self.gen.board.copy()  # a copy of table (solved)
        self.gen.reduce_via_logical(self.difficulty[0])
        self.has_problem = False
        if self.difficulty[1] != 0:
            self.gen.reduce_via_logical(self.difficulty[1])
        self.final_table = self.gen.board.copy()
        self.first_having_number = np.zeros((self.size_of_table, self.size_of_table), dtype='int32')
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j].value != 0:
                    self.first_having_number[i][j] = 1

    def is_solve(self) -> bool:
        if self.has_problem:
            return False
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j] != self.solved.rows[i][j]:
                    return False
        return True

    def add_number(self, a: int, b: int, number: int):
        if self.first_having_number[a][b] == 1:
            return 2
        if self.final_table.rows[a][b].value == 0 and self.solved.rows[a][b].value == number:
            self.final_table.rows[a][b].value = number
            return 0  # valid move
        if self.final_table.rows[a][b].value == 0:
            self.final_table.rows[a][b].value = number
            if self.check_possible(a, b, number):
                self.has_problem = True
                return 1  # valid move at the moment
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

    def check_complete(self):
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j] == 0:
                    return False
        return True

    def __str__(self):
        return f"Game: {self.level}, Time: {self.time}"



class MyWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.the_widget = None
        self.game = None
        self.setWindowTitle("Sudoku")
        self.setMinimumSize(FIRST_WINDOW_SIZE, FIRST_WINDOW_SIZE)
        self.init_topBar()
        self.initUI()
        self.init_board()
        self.init_game()
        self.add_number_buttons()
        self.show()
        self.table_map = np.zeros((NUMBER, NUMBER), dtype='int32')
        for i in range(NUMBER):
            for j in range(NUMBER):
                if self.game.final_table.rows[i][j].value != 0:
                    self.table_map[i][j] = 0
                else:
                    self.table_map[i][j] = 1
        print(self.game.final_table)
        self.selected_x = -1
        self.selected_y = -1
        self.haveSelected = False
        self.hasProblem = False

    def init_topBar(self):
        self.timer_label = QLabel('Timer: 0', self)
        self.timer_label.setFont(QFont('Arial', 15))
        self.timer_label.move(0, 0)
        self.timer_label.adjustSize()
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        setting_action = QAction('setting')
        setting_action.setShortcut('Ctrl+D')
        save_action.triggered.connect(self.my_save)
        exit_action.triggered.connect(self.close)
        easy = QAction('easy', self)
        medium = QAction('medium', self)
        hard = QAction('hard', self)
        extreme = QAction('extreme', self)
        about = QAction('about', self)
        self.my_menubar = self.menuBar()
        self.file_menu = self.my_menubar.addMenu('File')
        self.new_game_menu = self.my_menubar.addMenu('New')
        self.about = self.my_menubar.addMenu('About')
        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(setting_action)
        easy.triggered.connect(lambda: self.new_game('easy'))
        medium.triggered.connect(lambda: self.new_game('medium'))
        hard.triggered.connect(lambda: self.new_game('hard'))
        extreme.triggered.connect(lambda: self.new_game('extreme'))
        about.triggered.connect(self.about_clicked)
        self.new_game_menu.addAction(easy)
        self.new_game_menu.addAction(medium)
        self.new_game_menu.addAction(hard)
        self.new_game_menu.addAction(extreme)
        self.about.addAction(about)


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
        self.game = Game(level)
        self.table_map = np.zeros((NUMBER, NUMBER), dtype='int32')
        for i in range(NUMBER):
            for j in range(NUMBER):
                if self.game.final_table.rows[i][j] != -1:
                    self.table_map[i][j] = 0
                else:
                    self.table_map[i][j] = -1
        self.change_board()
        self.hasProblem = False
        self.selected_x = -1
        self.selected_y = -1
        self.haveSelected = False


    def initUI(self):
        # self.add_timer()
        ...

    def init_game(self):
        my_file = Path("save.txt")
        if my_file.exists() and my_file.is_file():
            msg = QMessageBox()
            msg.setWindowTitle("Load game")
            msg.setText("Do you want to load the previous game?")
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = msg.exec()
            if result == QMessageBox.StandardButton.Yes:
                self.my_load()
            else:
                self.game = Game('medium')
        else:
            self.game = Game('medium')
        self.change_board()

    def add_number_buttons(self):
        self.bottom_numbers = [[None] * 9 for _ in range(9)]
        self.my_layout = QHBoxLayout()
        for i in range(NUMBER):
            btn = QPushButton(str(i + 1))
            btn.setFixedSize(BOTTOM_NUMBER_SIZE, BOTTOM_NUMBER_SIZE)
            btn.clicked.connect(lambda _, a=i: self.bottom_button_clicked(a + 1))
            self.my_layout.addWidget(btn)
            btn.setStyleSheet(NORMAL_BUTTON_STYLE)
            self.bottom_numbers[i] = btn
        self.my_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.the_widget = QWidget(self)
        self.the_widget.setFixedSize(NUMBER * (BOTTOM_NUMBER_SIZE + 5), (BOTTOM_NUMBER_SIZE + 10))
        self.the_widget.setLayout(self.my_layout)
        self.the_widget.move((self.width() - self.the_widget.width()) // 2,
                             self.height() - self.the_widget.height() - 20)
        self.the_widget.show()

    def bottom_button_clicked(self, number: int):
        if not self.haveSelected:
            return
        if self.haveSelected:
            result = self.game.add_number(self.selected_x, self.selected_y, number)
            if result == 0:
                self.buttons[self.selected_x][self.selected_y].setText(str(number))
                self.check_game_complete()
            elif result == 1:
                self.buttons[self.selected_x][self.selected_y].setText(str(number))
                self.hasProblem = True
                self.check_game_complete()
            else:
                alert = QMessageBox()
                alert.setWindowTitle("Invalid move")
                alert.setText("Invalid move")
                alert.setIcon(QMessageBox.Icon.Warning)
                alert.setStandardButtons(QMessageBox.StandardButton.Ok)
                alert.exec()
            self.haveSelected = False

    def init_board(self):
        layout = QGridLayout()
        self.buttons = [[None] * 9 for _ in range(9)]
        for i in range(3):
            for j in range(3):
                mimi_container = QGridLayout()
                mini_widget = QWidget(self)
                for k in range(3):
                    for z in range(3):
                        button = QPushButton('1')
                        button.setFixedSize(INIT_SIZE_TILE, INIT_SIZE_TILE)  # Set the fixed size of the button
                        button.clicked.connect(lambda _, a=i * 3 + k, b=3 * j + z: self.click_button(a, b))
                        button.setStyleSheet(NORMAL_BUTTON_STYLE)
                        self.buttons[i * 3 + k][3 * j + z] = button
                        mimi_container.addWidget(button, k, z)
                mini_widget.setLayout(mimi_container)
                mini_widget.setStyleSheet('#mini_widget {border: 2px solid black}')
                mini_widget.setFixedSize(3 * INIT_SIZE_TILE + 3, 3 * INIT_SIZE_TILE + 3)
                layout.addWidget(mini_widget, i, j)
        container = QWidget(self)
        container.setMinimumSize(9 * INIT_SIZE_TILE + 4, 9 * INIT_SIZE_TILE + 4)
        container.move((self.width() - container.width()) // 2, (self.height() - container.height()) // 2)
        container.setLayout(layout)
        container.setStyleSheet('#container {border: 1px solid black}')
        container.show()

    def change_board(self):
        for i in range(NUMBER):
            for j in range(NUMBER):
                if str(self.game.final_table.rows[i][j])[7] != '0':
                    self.buttons[i][j].setText(str(self.game.final_table.rows[i][j])[7])
                    self.buttons[i][j].setStyleSheet(FILL_BUTTON_STYLE)
                else:
                    self.buttons[i][j].setText('')
                    self.buttons[i][j].setStyleSheet(NORMAL_BUTTON_STYLE)

    def click_button(self, a: int, b: int):
        self.haveSelected = False
        for i in range(NUMBER):
            for j in range(NUMBER):
                if self.table_map[i][j] == 1:
                    self.buttons[i][j].setStyleSheet(NORMAL_BUTTON_STYLE)
                else:
                    self.buttons[i][j].setStyleSheet(FILL_BUTTON_STYLE)
        if self.game.first_having_number[a][b] == 0:
            # self.show_number_buttons()
            for i in range(NUMBER):
                self.buttons[i][b].setStyleSheet(HIGHLIGHT_BUTTON_STYLE)
                self.buttons[a][i].setStyleSheet(HIGHLIGHT_BUTTON_STYLE)
            starting_a = (a // 3) * 3
            starting_b = (b // 3) * 3
            for i in range(starting_b, starting_b + 3, 1):
                for j in range(starting_a, starting_a + 3, 1):
                    self.buttons[j][i].setStyleSheet(HIGHLIGHT_BUTTON_STYLE)
            self.buttons[a][b].setStyleSheet(SELECTED_BUTTON_STYLE)
            self.selected_x = a
            self.selected_y = b
            self.haveSelected = True

    def about_clicked(self):
        alert = QMessageBox()
        alert.setWindowTitle("about")
        alert.setText("this is a sudoku game for more information go https://github.com/motrnam/PyQt6Sodoko")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.exec()

    def my_save(self):
        print("save")
        table = self.game.final_table
        result = ""
        temp = ""
        solved = ""
        for i in range(9):
            for j in range(9):
                result += str((table.rows[i][j].value))
                temp += str(self.game.first_having_number[i][j])
                solved += str(self.game.solved.rows[i][j].value)
        result += '\n'
        result += temp
        result += '\n'
        result += str(self.game.time)
        result += '\n'
        result += self.game.level
        result += '\n'
        result += solved
        result += '\n'
        temp_string = ""
        for i in range(NUMBER):
            for j in range(NUMBER):
                temp_string += str(self.table_map[i][j])
            temp_string += '\n'
        with open("save.txt", "w") as f:
            f.write(result)

    def my_load(self):  # not tested
        try:
            with open("save.txt", "r") as f:
                table = f.readline().strip('\n')
                initial_zero = f.readline().strip('\n')
                time = f.readline().strip('\n')
                level = f.readline().strip('\n')
                solved = f.readline().strip('\n')
            self.game = Game(level.strip('\n'))
            self.game.time = int(time)
            self.game.first_having_number = np.zeros((NUMBER, NUMBER), dtype='int32')
            for i in range(NUMBER):
                for j in range(NUMBER):
                    self.game.final_table.rows[i][j].value = int(table[i * NUMBER + j])
                    self.game.first_having_number[i][j] = int(initial_zero[i * NUMBER + j])
                    self.game.solved.rows[i][j].value = int(solved[i * NUMBER + j])
            self.table_map = np.zeros((NUMBER, NUMBER), dtype='int32')
            for i in range(NUMBER):
                for j in range(NUMBER):
                    if self.game.final_table.rows[i][j].value != 0:
                        self.table_map[i][j] = 0
                    else:
                        self.table_map[i][j] = 1
        except:
            raise Exception('Error in loading file')  # TODO instead of this make random table

    def check_game_complete(self):
        if self.game.check_complete() and self.game.is_solve():
            alert = QMessageBox()
            alert.setWindowTitle("Congratulations")
            alert.setText("you solved the sudoku")
            alert.setIcon(QMessageBox.Icon.Information)
            alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            alert.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindows()
    app.exec()
