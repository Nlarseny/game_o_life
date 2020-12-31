import tkinter as tk
import time

window = tk.Tk()
matrix = []
ROW_CONST = 25
COL_CONST = 50


class Cell:
    def __init__(self, pos_i, pos_j, alive, updated, change):
        self.pos_i = pos_i
        self.pos_j = pos_j
        self.alive = alive
        self.updated = updated
        self.change = change

        local_button = tk.Button(master=window, bg="black", command=self.clicked)
        local_button.grid(row=self.pos_i, column=self.pos_j, sticky="nsew")
        self.button = local_button

    def get_state(self):
        return self.alive

    def set_state(self, state):
        self.alive = state

    def get_cords(self):
        return self.pos_i, self.pos_j

    def update(self):
        self.updated = True

    def clicked(self):
        if not matrix[self.pos_i][self.pos_j].alive:
            matrix[self.pos_i][self.pos_j].alive = True
            self.button.configure(bg="green")
        else:
            matrix[self.pos_i][self.pos_j].alive = False
            self.button.configure(bg="black")

    def die(self):
        if not self.updated:
            self.alive = False
            self.updated = True
            self.button.configure(bg="black")

    def live(self):
        if not self.updated:
            self.alive = True
            self.updated = True
            self.button.configure(bg="green")

    def count_neighbors(self):
        count = 0

        # bottom row
        if self.pos_i - 1 > 0 and matrix[self.pos_i - 1][self.pos_j].alive:
            count += 1
        if self.pos_i - 1 > 0 and self.pos_j - 1 > 0 and matrix[self.pos_i - 1][self.pos_j - 1].alive:
            count += 1
        if self.pos_i - 1 > 0 and self.pos_j + 1 < COL_CONST and matrix[self.pos_i - 1][self.pos_j + 1].alive:
            count += 1

        # sides
        if self.pos_j - 1 > 0 and matrix[self.pos_i][self.pos_j - 1].alive:
            count += 1
        if self.pos_j + 1 < COL_CONST and matrix[self.pos_i][self.pos_j + 1].alive:
            count += 1

        # top row
        if self.pos_i + 1 < ROW_CONST and matrix[self.pos_i + 1][self.pos_j].alive:
            count += 1
        if self.pos_i + 1 < ROW_CONST and self.pos_j - 1 > 0 and matrix[self.pos_i + 1][self.pos_j - 1].alive:
            count += 1
        if self.pos_i + 1 < ROW_CONST and self.pos_j + 1 < COL_CONST and matrix[self.pos_i + 1][self.pos_j + 1].alive:
            count += 1

        return count
    

def begin_life():
    for x in range(ROW_CONST):
        for y in range(COL_CONST):
            cur_cell = matrix[x][y]
            neighbors = cur_cell.count_neighbors()

            if neighbors < 2 and cur_cell.alive:
                cur_cell.change = True
            if neighbors > 3 and cur_cell.alive:
                cur_cell.change = True
            if not cur_cell.alive and neighbors == 3:
                cur_cell.change = True

    for x in range(ROW_CONST):
        for y in range(COL_CONST):
            cur_cell = matrix[x][y]
            if cur_cell.change:
                if cur_cell.alive:
                    cur_cell.die()
                else:
                    cur_cell.live()
            cur_cell.updated = False
            cur_cell.change = False


if __name__ == '__main__':

    # matrix = []
    for i in range(ROW_CONST):
        row = []
        for j in range(COL_CONST):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j)
            label = tk.Label(master=frame, text="    ")
            label.pack()

            cell = Cell(i, j, False, False, False)
            row.append(cell)
        matrix.append(row)


    def start():
        while True:
            begin_life()
            window.update()
            time.sleep(.08)


    button = tk.Button(master=window, text="START", fg="green", command=start)
    button.grid(row=0, column=COL_CONST + 2, sticky="nsew")

    window.mainloop()
