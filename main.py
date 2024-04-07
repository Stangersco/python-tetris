from abc import abstractmethod
from os import system
from random import choice, randint
from time import sleep, time

import keyboard


COUNT_COLS_X = 6
COUNT_ROWS_Y = 18

GRAFIKA = "0"
COUNT_UP_SPEED = 15
MAX_SPEED = 0.6
START_SPEED = 1
SPEED_UP = 0.05

KEY_DOWN = "s"
KEY_LEFT = "a"
KEY_RIGHT = "d"
KEY_ROTATE = "r"


class Block:
    def __init__(self):
        self.pos_1 = [0, 0]
        self.pos_2 = [0, 0]
        self.pos_3 = [0, 0]
        self.pos_4 = [0, 0]
        self.rotate_now = 0
        self.max_rotate = 0

    def get(self):
        return self.pos_1, self.pos_2, self.pos_3, self.pos_4

    def move_right(self):
        self.pos_1[1] += 1
        self.pos_2[1] += 1
        self.pos_3[1] += 1
        self.pos_4[1] += 1

    def move_left(self):
        self.pos_1[1] -= 1
        self.pos_2[1] -= 1
        self.pos_3[1] -= 1
        self.pos_4[1] -= 1

    def move_down(self):
        self.pos_1[0] += 1
        self.pos_2[0] += 1
        self.pos_3[0] += 1
        self.pos_4[0] += 1

    def rotate(self):
        self.pos_1, self.pos_2, self.pos_3, self.pos_4 = self.get_rotate()
        self.rotate_now = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0

    @abstractmethod
    def get_rotate(self):
        pass


class Square(Block):
    """
    [.][1][1]
    [.][1][1]
    [.][.][.]
    """
    max_range = 2

    def __init__(self, pos):
        super().__init__()

        self.pos_1 = [0, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [1, pos]
        self.pos_4 = [1, pos + 1]

        self.rotate_now = 0

    def get_rotate(self):
        return self.pos_1, self.pos_2, self.pos_3, self.pos_4

    def rotate(self):
        pass


class BlockOne(Block):
    """
    [.][.][1]
    [.][1][1]
    [.][.][1]
    """
    max_range = 2

    def __init__(self, pos):
        super().__init__()
        self.pos_1 = [1, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [1, pos + 1]
        self.pos_4 = [2, pos + 1]

        self.rotate_now = 0
        self.max_rotate = 3

    def get_rotate(self):
        rotate = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0
        res = self.get()

        if rotate == 1:
            y4, x4 = self.pos_4
            res = self.pos_1, self.pos_2, self.pos_3, [y4 - 1, x4 + 1]
        elif rotate == 2:
            y1, x1 = self.pos_1
            res = [y1 + 1, x1 + 1], self.pos_2, self.pos_3, self.pos_4
        elif rotate == 3:
            y2, x2 = self.pos_2
            res = self.pos_1, [y2 + 1, x2 - 1], self.pos_3, self.pos_4
        elif rotate == 0:
            y, x = self.pos_3
            res = [y, x - 1], [y - 1, x], self.pos_3, [y + 1, x]

        return res


class BlockTwo(Block):
    """
    [.][1][1]
    [.][.][1]
    [.][.][1]
    """

    max_range = 2

    def __init__(self, pos):
        super().__init__()

        self.pos_1 = [0, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [1, pos + 1]
        self.pos_4 = [2, pos + 1]

        self.rotate_now = 0
        self.max_rotate = 3

    def get_rotate(self):
        rotate = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0
        y3, x3 = self.pos_3

        res = []

        if rotate == 1:
            res = [y3, x3 - 1], [y3, x3 + 1], self.pos_3, [y3 - 1, x3 + 1]
        elif rotate == 2:
            res = [y3 + 1, x3], [y3 - 1, x3], self.pos_3, [y3 + 1, x3 + 1]
        elif rotate == 3:
            res = [y3, x3 - 1], [y3, x3 + 1], self.pos_3, [y3 + 1, x3 - 1]
        elif rotate == 0:
            res = [y3-1, x3 - 1], [y3 - 1, x3], self.pos_3, [y3 + 1, x3]

        return res


class Line(Block):
    """
    [1][1][1][1]
    """
    max_range = 4

    def __init__(self, pos):
        super().__init__()

        self.pos_1 = [0, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [0, pos + 2]
        self.pos_4 = [0, pos + 3]

        self.rotate_now = 0
        self.max_rotate = 1

    def get_rotate(self):
        rotate = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0
        res = []

        y2, x2 = self.pos_2

        if rotate == 1:
            res = [y2 - 1, x2], self.pos_2, [y2 + 1, x2], [y2 + 2, x2]
        if rotate == 0:
            res = [y2, x2 - 1], self.pos_2, [y2, x2 + 1], [y2, x2 + 2]

        return res


class Tetris:
    matrix_place = list()
    speed = START_SPEED
    block = None
    count = 0

    def __init__(self):
        self.matrix_place = [['.' for _ in range(COUNT_COLS_X)] for _ in range(COUNT_ROWS_Y)]
        self.full_len = [GRAFIKA for _ in range(COUNT_COLS_X)]

        self.score = 0

    def play(self):
        time_now = time()
        while time() - time_now < self.speed:
            sleep(0.1)
            if keyboard.is_pressed(KEY_DOWN):
                break
            elif keyboard.is_pressed(KEY_LEFT) and self.check_left():
                self.remove()
                self.block.move_left()
                self.place()
                self.print()
            elif keyboard.is_pressed(KEY_RIGHT) and self.check_right():
                self.remove()
                self.block.move_right()
                self.place()
                self.print()
            elif keyboard.is_pressed(KEY_ROTATE) and self.check_rotate():
                self.remove()
                self.block.rotate()
                self.place()
                self.print()

        if self.check_down():
            self.remove()
            self.block.move_down()
            self.place()
        else:
            self.count += 1
            if self.count >= COUNT_UP_SPEED:
                self.speed -= SPEED_UP
                self.speed = max((self.speed, MAX_SPEED))
                self.count = 0

            self.check_full()
            self.check_end()
            self.create_block()

        self.print()

    def print(self):
        system("cls")
        print(self.matrix_place[0], f"score = {self.score}")
        for i in self.matrix_place[1:]:
            print(i)

    def place(self):
        """
        Place block in matrix_place
        """
        for y, x in self.block.get():
            self.matrix_place[y][x] = GRAFIKA

    def remove(self):
        """
        Remove block in matrix_place
        """
        for y, x in self.block.get():
            self.matrix_place[y][x] = '.'

    def check_rotate(self):
        res = True
        for y, x in self.block.get_rotate():
            if y >= COUNT_ROWS_Y or x >= COUNT_COLS_X or x < 0 or (
                    self.matrix_place[y][x] == GRAFIKA and [y, x] not in self.block.get()):
                res = False
                break
        return res

    def check_down(self):
        res = True
        pos = self.block.get()
        for y, x in pos:
            if y + 1 >= COUNT_ROWS_Y or self.matrix_place[y + 1][x] == GRAFIKA and [y + 1, x] not in pos:
                res = False
                break
        return res

    def check_left(self):
        res = True
        pos = self.block.get()
        for y, x in pos:
            if x - 1 < 0 or self.matrix_place[y][x - 1] == GRAFIKA and [y, x - 1] not in pos:
                res = False
                break
        return res

    def check_right(self):
        res = True
        pos = self.block.get()
        for y, x in pos:
            if x + 1 >= COUNT_COLS_X or self.matrix_place[y][x + 1] == GRAFIKA and [y, x + 1] not in pos:
                res = False
                break
        return res

    def check_end(self):
        pos = self.block.get()
        for y, x in pos:
            if y == 0:
                print("end")
                sleep(3)
                self.clear()
                break

    def check_full(self):
        """
        Check if matrix_place has full row and remove it, then add score
        """
        while self.full_len in self.matrix_place:
            self.matrix_place.remove(self.full_len)
            self.matrix_place.insert(0, ['.' for _ in range(COUNT_COLS_X)])
            self.score += int(100 * (1-self.speed + 1))

    def create_block(self):
        """
        Create random block in random range
        """
        block = choice((Square, Line, BlockOne, BlockTwo))
        self.block = block(randint(0, COUNT_COLS_X - block.max_range))
        self.place()

    def clear(self):
        self.matrix_place = [['.' for _ in range(COUNT_COLS_X)] for _ in range(COUNT_ROWS_Y)]
        self.speed = START_SPEED


if __name__ == "__main__":
    game = Tetris()
    game.create_block()
    while True:
        game.play()
