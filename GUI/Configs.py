INIT_SIZE_TILE = 59
NUMBER = 8
FIRST_WINDOW_SIZE = 699
BOTTOM_NUMBER_SIZE = 44
NORMAL_BUTTON_STYLE = """
                QPushButton {
                background-color: #eaebff;
                color: black;
                padding: 9px 10px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #0068d9;
            }
            """
HIGHLIGHT_BUTTON_STYLE = """ 
        QPushButton {
                background-color: #ffcc76;
                color: black;
                padding: 9px 20px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover { 
                background-color: #ffcc01;
            }
            """

SELECTED_BUTTON_STYLE = """
        QPushButton {
                background-color: #999998;
                color: black;
                padding: 9px 20px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover { 
                background-color: #ffcc01;
            }
            """
FILL_BUTTON_STYLE = """
        QPushButton {
                background-color: #aaaaaa;
                color: black;
                padding: 9px 20px;
                border: 1px solid black;
                text-align: center;
            }
            QPushButton:hover { 
                background-color: #ffcc01;
            }
            """


difficulties = {
    'easy': (35, 0),
    'medium': (81, 5),
    'hard': (81, 10),
    'extreme': (81, 15)
}
