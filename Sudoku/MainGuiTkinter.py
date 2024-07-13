import tkinter as tk

TABLE_SIZE = 9
TABLE_WIDTH = 20


class MainGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main GUI")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        self.table_layout = tk.Frame(self)
        self.table_layout.pack()

    def createTable(self, table_in_string: str):
        for i in range(TABLE_SIZE):
            for j in range(TABLE_SIZE):
                cell = tk.Label(self.table_layout, text=table_in_string[i * TABLE_SIZE + j], width=TABLE_WIDTH)
                cell.grid(row=i, column=j)


if __name__ == "__main__":
    app = MainGui()
    app.createTable("123456789" * 9)
    app.mainloop()
