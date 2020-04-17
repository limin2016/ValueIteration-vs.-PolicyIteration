import copy
class State(object):
    def __init__(self, val, is_terminal, row_index, col_index):
        self.val = val
        self.is_terminal = is_terminal
        self.row_index = row_index
        self.col_index = col_index
        self.noises = [0,0,0,0]
        self.dir = '-'

    def set_initial_policy(self, noises):
        self.noises[0] = noises[0]
        self.noises[1] = noises[1]
        self.noises[2] = noises[3]
        self.noises[3] = noises[2]

