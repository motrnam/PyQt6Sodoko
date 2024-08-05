import pickle
import sys
from pathlib import Path

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, \
    QGridLayout, QHBoxLayout, QMessageBox

from Sudoku.Game import Game
from Sudoku.Cell import FILLING_STATE
from Configs import *


class MyWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.bottom_numbers = None
        self.new_game_menu = None
        self.file_menu = None
        self.the_widget = None
        self.game = None
        self.setWindowTitle("Sudoku")
        self.setMinimumSize(FIRST_WINDOW_SIZE, FIRST_WINDOW_SIZE)
        self.init_topBar()
        self.init_board()
        self.init_game()
        self.add_number_buttons()
        self.show()
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

    def new_game(self, level: str):
        self.game = Game(level)

        self.change_board()
        self.hasProblem = False
        self.selected_x = -1
        self.selected_y = -1
        self.haveSelected = False

    def init_game(self):
        my_file = Path("../Sudoku/Game.pickle")
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
        print("change board")
        for i in range(NUMBER):
            for j in range(NUMBER):
                pass

    def click_button(self, a: int, b: int):
        for i in range(NUMBER):
            for j in range(NUMBER):
                pass

    def about_clicked(self):
        alert = QMessageBox()
        alert.setWindowTitle("about")
        alert.setText("this is a sudoku game for more information go https://github.com/motrnam/PyQt6Sodoko")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.exec()

    def my_save(self):
        print("save")
        with open("../Sudoku/Game.pickle", "wb") as file:
            pickle.dump(self.game, file)

    def my_load(self):  # not tested
        try:
            with open("../Sudoku/Game.pickle", "rb") as file:
                self.game = pickle.load(file)
                self.change_board()
        except:
            alert = QMessageBox()
            alert.setWindowTitle("Error")
            alert.setText("Error in loading file")
            alert.setIcon(QMessageBox.Icon.Warning)
            alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            alert.exec()

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
