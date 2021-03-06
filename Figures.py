import random
from constatnts import COLORS


class Figures:
    # game pieces and their rotations
    # the main list contains figure types the the inner list is their rotations
    # the numbers represent the positions in a 4x4 matrix where the figure is solid
    # [1, 5, 9, 13] represents a line.
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # long figure
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # L-shaped clockwise figure
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L-shaped counter clockwise figure
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # cross figure
        [[1, 2, 5, 6]],  # block figure
        [[1, 5, 6, 10], [2, 3, 5, 6, ]],  # S piece
        [[1, 5, 4, 8], [1, 2, 6, 7]]  # Z piece
    ]

    # game pieces and their rotations
    figures_dict = {
        "long": [[1, 5, 9, 13], [4, 5, 6, 7]],
        "L-shaped clockwise": [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        "L-shaped counter clockwise": [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        "cross": [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        "block": [[1, 2, 5, 6]],
        "S": [[1, 5, 6, 10], [2, 3, 5, 6, ]],
        "Z":[[1, 5, 4, 8], [1, 2, 6, 7]]
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def image(self):
        '''
        return the type and rotation of a figure
        '''
        return self.figures[self.type][self.rotation]

    def rotate(self):
        '''
        rotate piece to next rotation
        '''
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
