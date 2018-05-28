import random


class Dice(object):

    def __init__(self):
        self.val = 0

    def throw_dice(self):
        out = random.randint(2, 12)
        return out