import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget
from PyQt6.QtGui import QColor, QPen, QFont

# Define the puzzle (0 represents empty cells)
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

class SudokuGrid(QGraphicsView):
    def __init__(self):
        super().__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.cell_size = 60
        self.grid_size = self.cell_size * 9
        self.font = QFont("Arial", 20)

        # Draw grid lines
        pen = QPen(QColor(0, 0, 0))
        for i in range(10):
            scene.addLine(0, i * self.cell_size, self.grid_size, i * self.cell_size, pen)
            scene.addLine(i * self.cell_size, 0, i * self.cell_size, self.grid_size, pen)

        # Make certain lines thicker to form subgrid boundaries
        pen.setWidth(3)
        for i in range(0, 10, 3):
            scene.addLine(0, i * self.cell_size, self.grid_size, i * self.cell_size, pen)
            scene.addLine(i * self.cell_size, 0, i * self.cell_size, self.grid_size, pen)

        # Draw puzzle numbers
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    text_item = scene.addText(str(puzzle[i][j]), self.font)
                    text_item.setPos(j * self.cell_size + self.cell_size / 3, i * self.cell_size + self.cell_size / 3)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        sudoku_grid = SudokuGrid()
        layout.addWidget(sudoku_grid)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(540, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
