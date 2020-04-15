import re
import os
from State import State
from decimal import Decimal

def create_grid(file_name):
    currentPath = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(currentPath, file_name)
    cnt = 0
    states=[]
    size = 0
    discount_factor = 0
    noises = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if line.startswith('#') or line.startswith(' ') or line.startswith('\n'):
                continue
            else:
                if cnt >= 3:
                    temp = re.split(r'[#]', line)[0].strip()
                    temp1 = re.split(r'[\,\s\n]', temp)
                    # states[cnt - 3] = temp1
                    row_index = cnt - 3
                    for col_index, val in enumerate(temp1):
                        if val == 'X':
                            state = State(0.0, False, row_index, col_index)
                            state.set_initial_policy(noises)
                            states[row_index][col_index] = state

                        else:
                            init_val = float(val)
                            state = State(init_val, True, row_index, col_index)
                            state.has_value = True
                            states[row_index][col_index] = state
                    cnt = cnt + 1
                if cnt == 0:  # get self.size
                    temp = re.split(r'[#]', line)[0]
                    size = int(re.split(r'[\s\n]', temp)[0])
                    states = [[0] * size for i in range(size)]
                    cnt = cnt + 1
                elif cnt == 1:  # get self.disCountFactor
                    discount_factor = float(re.split(r'[\s\n]', line)[0])
                    cnt = cnt + 1
                elif cnt == 2:  # get self.noises
                    temp = re.split(r'[#]', line)[0].strip()
                    noises = re.split(r'[\,\s,\n]+', temp)
                    for index, val in enumerate(noises):
                        noises[index] = float(val)
                    if len(noises) == 3:
                        noises.append(0)
                    cnt = cnt + 1
    return [size, discount_factor, noises, states]

def out_of_range(x, y, size):
    if x>=0 and x<size and y>=0 and y<size:
        return False
    return True

def get_longest_length(states, grid_size):
    max_length = 0
    for value in states:
        for state in value:
            temp_str = str(Decimal(state.val).quantize(Decimal('0.00')))
            max_length = max(max_length, len(temp_str))
    return max_length

def print_states(states, grid_size):
    #get_longest_length(states, grid_size)
    longest_length = get_longest_length(states, grid_size)
    for index_row, row_val in enumerate(states):
        for index_col, state in enumerate(row_val):
            temp_str = str(Decimal(state.val).quantize(Decimal('0.00')))
            if index_col<grid_size-1:
                print(temp_str.ljust(longest_length+3), end='')
            else:
                print(temp_str.ljust(longest_length))

def print_direction(states, grid_size):
    for index_row, value_row in enumerate(states):
        for index_col, state in enumerate(value_row):
            if index_col<grid_size-1:
                print(state.dir+' ', end='')
            else:
                print(state.dir)


