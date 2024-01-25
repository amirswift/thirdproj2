class Cell:
    def __init__(self, value, x, y):
        self.possible_values = []
        self.cages_involved = []
        self.value = value
        self.x = x
        self.y = y

    def set_cages_involved(self, cage):
        self.cages_involved.append(cage)

    def set_possible_values(self, sudoku_table, sudoku_cages):
        if self.value != 0:
            self.possible_values = set([self.value])
        else:
            self.possible_values = get_possible_values(sudoku_table, sudoku_cages, self)
            if len(self.possible_values) == 1:
                self.value = self.possible_values.pop()
                self.set_possible_values(sudoku_table, sudoku_cages)

    def __str__(self) -> str:
        return str(self.value)


class Cage:
    def __init__(self, value, cells):
        self.value = value
        self.cells = cells

    def __str__(self):
        return f"Cage {self.value}: {', '.join(str(cell) for cell in self.cells)}"


def add_cage(cage_str, sudoku_table):
    cage_parts = cage_str.split(">")
    value = int(cage_parts[1][1:])
    cords = cage_parts[0].split()
    cage_cells = []
    for cord in cords:
        x = int(cord[0])
        y = int(cord[1])
        cage_cells.append(sudoku_table[x - 1][y - 1])
        sudoku_table[x - 1][y - 1].set_cages_involved(cage_cells[-1])
    return Cage(value, cage_cells)


def possible_values_in_cage(sudoku_cages, cell):
    min_max_possible_value = float("inf")
    sum_cells_in_cage = 0
    zero_cells_in_cage = -1
    for sudoku_cage in sudoku_cages:
        if cell in sudoku_cage.cells:
            for c in sudoku_cage.cells:
                sum_cells_in_cage = sum_cells_in_cage + c.value
                if c.value == 0:
                    zero_cells_in_cage = zero_cells_in_cage + 1

            if zero_cells_in_cage == 0:
                return set([sudoku_cage.value - sum_cells_in_cage])
            else:
                tmp = int(
                    sudoku_cage.value
                    - sum_cells_in_cage
                    - int((zero_cells_in_cage * (zero_cells_in_cage + 1)) / 2)
                )
            if tmp < min_max_possible_value:
                min_max_possible_value = tmp
            sum_cells_in_cage = 0
            zero_cells_in_cage = 0

    print(f"sudoku_cage.value: {sudoku_cage.value}")
    print(f"Sum of cells in cage: {sum_cells_in_cage}")
    print(f"Zero cells in cage: {zero_cells_in_cage}")
    print(f"Value of cage: {sudoku_cage.value}")
    print(f"Possible values in cage: {min_max_possible_value}")
    possible_values = []
    while min_max_possible_value > 0:
        if min_max_possible_value < 10:
            possible_values.append(min_max_possible_value)
        min_max_possible_value -= 1
    return set(possible_values)


def get_block_values(sudoku_table, cell):
    block_values = set()
    block_x = (cell.x // 3) * 3
    block_y = (cell.y // 3) * 3
    for i in range(block_x, block_x + 3):
        for j in range(block_y, block_y + 3):
            block_values.add(sudoku_table[i][j].value)
    return block_values


def get_possible_values(sudoku_table, sudoku_cages, cell):
    print(cell.x, cell.y)
    row_values = set(table[cell.x])
    # print(f"Row values: {row_values}")
    column_values = set(row[cell.y] for row in table)
    # print(f"Column values: {column_values}")
    block_values = get_block_values(sudoku_table, cell)
    cage_values = possible_values_in_cage(sudoku_cages, cell)
    if "int" in str(type(cage_values)):
        possible_values = cage_values
    else:
        possible_values = cage_values - row_values - column_values - block_values
    print(f"Possible values: {possible_values}")
    print("- - - - - - - - - - -")
    return possible_values


sudoku_table = []
table = []
for i in range(9):
    # tmp = input(f"Enter row {i + 1} (9 digits, use 0 for empty cells): ").split()
    # tmp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    tmp = input().split()
    row = [Cell(int(tmp[v]), i, v) for v in range(len(tmp))]
    sudoku_table.append(row)
    table.append([int(v) for v in (tmp)])

n = int(input())
sudoku_cages = []
for i in range(n):
    cage = input()
    sudoku_cages.append(add_cage(cage, sudoku_table))

for row in sudoku_table:
    for cell in row:
        cell.set_possible_values(sudoku_table, sudoku_cages)

print("Sudoku table:")
for row in sudoku_table:
    print(" ".join(map(str, row)))

print("Sudoku cages:")
for cage in sudoku_cages:
     print(cage)

