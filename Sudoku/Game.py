from .Generator import Generator
from .Cell import FILLING_STATE

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
        self.final_table = None
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
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j].value != 0:
                    self.final_table.rows[i][j].state = FILLING_STATE.FILLED_BY_GAME

    def is_solve(self) -> bool:
        if self.has_problem:
            return False
        for i in range(self.size_of_table):
            for j in range(self.size_of_table):
                if self.final_table.rows[i][j] != self.solved.rows[i][j]:
                    return False
        return True

    def add_number(self, a: int, b: int, number: int):
        if self.final_table.rows[a][b].state == FILLING_STATE.FILLED_BY_GAME:
            raise Exception("This cell is filled by game")
        if self.check_possible(a, b, number):
            self.final_table.rows[a][b].value = number
            self.final_table.rows[a][b].state = FILLING_STATE.FILLED_BY_USER

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

    def get_final_table(self):
        return self.final_table

    def get_cell(self, a: int, b: int):
        return self.final_table.rows[a][b].value, self.final_table.rows[a][b].state
