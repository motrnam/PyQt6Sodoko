import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, cairo

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

class SudokuGrid(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()

        self.set_size_request(540, 540)

        self.connect("draw", self.on_draw)

    def on_draw(self, widget, cr):
        allocation = self.get_allocation()
        width = allocation.width
        height = allocation.height

        # Draw grid lines
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(2)

        for i in range(10):
            if i % 3 == 0:
                cr.set_line_width(4)
            else:
                cr.set_line_width(2)

            cr.move_to(0, i * (height / 9))
            cr.line_to(width, i * (height / 9))
            cr.stroke()

            cr.move_to(i * (width / 9), 0)
            cr.line_to(i * (width / 9), height)
            cr.stroke()

        # Draw puzzle numbers
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(20)

        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    cr.move_to(j * (width / 9) + 0.35 * (width / 9), i * (height / 9) + 0.65 * (height / 9))
                    cr.show_text(str(puzzle[i][j]))

def main():
    win = Gtk.Window()
    win.set_default_size(540, 600)
    win.connect("destroy", Gtk.main_quit)

    grid = SudokuGrid()
    win.add(grid)

    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
