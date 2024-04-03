import keyboard
from time import sleep, time
from os import system
from random import choice, randint


class Block:
    pos_1 = pos_2 = pos_3 = pos_4 = None

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


class Square(Block):
    """
    [.][1][1]
    [.][1][1]
    [.][.][.]
    """
    max_range = 2
    max_rotate = 0

    def __init__(self, pos):
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
    max_rotate = 3

    def __init__(self, pos):
        self.pos_1 = [1, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [1, pos + 1]
        self.pos_4 = [2, pos + 1]

        self.rotate_now = 0

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

    def rotate(self):
        self.pos_1, self.pos_2, self.pos_3, self.pos_4 = self.get_rotate()
        self.rotate_now = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0


class BlockTwo(Block):
    """
    [.][1][1]
    [.][.][1]
    [.][.][1]
    """

    max_range = 2
    max_rotate = 3

    def __init__(self, pos):
        self.pos_1 = [0, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [1, pos + 1]
        self.pos_4 = [2, pos + 1]

        self.rotate_now = 0

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

    def rotate(self):
        self.pos_1, self.pos_2, self.pos_3, self.pos_4 = self.get_rotate()
        self.rotate_now = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0


class Line(Block):
    """
    [1][1][1][1]
    """
    max_rotate = 1
    max_range = 4

    def __init__(self, pos):
        self.pos_1 = [0, pos]
        self.pos_2 = [0, pos + 1]
        self.pos_3 = [0, pos + 2]
        self.pos_4 = [0, pos + 3]

        self.rotate_now = 0

    def get_rotate(self):
        rotate = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0
        res = []

        y2, x2 = self.pos_2

        if rotate == 1:
            res = [y2 - 1, x2], self.pos_2, [y2 + 1, x2], [y2 + 2, x2]
        if rotate == 0:
            res = [y2, x2 - 1], self.pos_2, [y2, x2 + 1], [y2, x2 + 2]

        return res

    def rotate(self):
        self.pos_1, self.pos_2, self.pos_3, self.pos_4 = self.get_rotate()
        self.rotate_now = self.rotate_now + 1 if self.rotate_now + 1 <= self.max_rotate else 0


class Tetris:
    matrix_place = list()
    speed = 1
    block = None
    count = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.matrix_place = [['.' for _ in range(self.x)] for _ in range(self.y)]
        self.full_len = ['1' for _ in range(self.x)]
        self.create_block()

    def play(self):
        time_now = time()
        while time() - time_now < self.speed:
            sleep(0.1)
            if keyboard.is_pressed("s"):
                break
            elif keyboard.is_pressed("a") and self.check_left():
                self.remove()
                self.block.move_left()
                self.place()
                self.print()
            elif keyboard.is_pressed("d") and self.check_right():
                self.remove()
                self.block.move_right()
                self.place()
                self.print()
            elif keyboard.is_pressed("r") and self.check_rotate():
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
            if self.count >= 10:
                self.speed -= 0.05

            self.check_full()
            self.check_end()
            self.create_block()

        self.print()

    def print(self):
        system("cls")
        for i in self.matrix_place:
            print(i)

    def place(self):
        for y, x in self.block.get():
            self.matrix_place[y][x] = '1'

    def remove(self):
        for y, x in self.block.get():
            self.matrix_place[y][x] = '.'

    def check_rotate(self):
        res = True
        for y, x in self.block.get_rotate():
            if y >= self.y or x >= self.x or x < 0 or (
                    self.matrix_place[y][x] == '1' and [y, x] not in self.block.get()):
                res = False
                break
        return res

    def check_down(self):
        res = True
        pos = self.block.get()
        for y, x in pos:
            if y + 1 >= self.y or self.matrix_place[y + 1][x] == '1' and [y + 1, x] not in pos:
                res = False

        return res

    def check_left(self):
        res = True
        pos = self.block.get()
        for y, x in pos:
            if x - 1 < 0 or self.matrix_place[y][x - 1] == '1' and [y, x - 1] not in pos:
                res = False
        return res

    def check_right(self):
        res = True
        pos = self.block.get()
        for y, x in pos:
            if x + 1 >= self.x or self.matrix_place[y][x + 1] == '1' and [y, x + 1] not in pos:
                res = False
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
        while self.full_len in self.matrix_place:
            self.matrix_place.remove(self.full_len)
            self.matrix_place.insert(0, ['.' for _ in range(self.x)])

    def create_block(self):
        block = choice((Square, Line, BlockOne, BlockTwo))
        self.block = block(randint(0, self.x - block.max_range))
        self.place()

    def clear(self):
        self.matrix_place = [['.' for _ in range(self.x)] for _ in range(self.y)]
        self.speed = 1


if __name__ == "__main__":
    game = Tetris(6, 18)
    while True:
        game.play()
