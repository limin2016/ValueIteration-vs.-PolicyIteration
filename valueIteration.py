import copy
from utils import out_of_range, printStates
import time

def value_iteration(discount_factor, noises, states, grid_size):
    max_difference = 0
    acceptable_difference = 0.00001
    for row_val in states:
        for index,state in enumerate(row_val):
            if state.is_terminal:
                continue
            next_states = [copy.copy(state), copy.copy(state), copy.copy(state), copy.copy(state)]
            update_value(next_states[0], noises[0], noises[1], noises[2], noises[3], discount_factor, states, grid_size)
            update_value(next_states[1], noises[3], noises[0], noises[1], noises[2], discount_factor, states, grid_size)
            update_value(next_states[2], noises[2], noises[3], noises[0], noises[1], discount_factor, states, grid_size)
            update_value(next_states[3], noises[1], noises[2], noises[3], noises[0], discount_factor, states, grid_size)
            max_state = next_states[0]
            for next_state in next_states:
                if max_state.val < next_state.val:
                    max_state = next_state
            states[state.row_index][state.col_index] = copy.deepcopy(max_state)
            max_difference = max(max_difference, abs(max_state.val-state.val))
            del next_state
    if max_difference < acceptable_difference:
        return True
    else:
        return False




def update_value(state, left_noise, up_noise, right_noise, down_noise, discount_factor, states, grid_size):
    # left point
    row_index_left = state.row_index
    col_index_left = state.col_index - 1
    # up point
    row_index_up = state.row_index - 1
    col_index_up = state.col_index
    # right point
    row_index_right = state.row_index
    col_index_right = state.col_index + 1
    # down point
    row_index_down = state.row_index + 1
    col_index_down = state.col_index


    # calculate values in four directions
    final_value = 0
    if not out_of_range(row_index_left, col_index_left, grid_size):
        final_value += left_noise * states[row_index_left][col_index_left].val * discount_factor
    else:
        final_value += state.val * left_noise * discount_factor

    if not out_of_range(row_index_up, col_index_up, grid_size):
        final_value += up_noise * states[row_index_up][col_index_up].val * discount_factor
    else:
        final_value += state.val * up_noise * discount_factor

    if not out_of_range(row_index_right, col_index_right, grid_size):
        final_value += right_noise * states[row_index_right][col_index_right].val * discount_factor
    else:
        final_value += state.val * right_noise * discount_factor

    if not out_of_range(row_index_down, col_index_down, grid_size):
        final_value += down_noise * states[row_index_down][col_index_down].val * discount_factor
    else:
        final_value += state.val * down_noise * discount_factor
    state.val = final_value



def do_several_value_iterations(discount_factor, noises, states, grid_size):
    time_start = time.time()
    if_converge = False
    while not if_converge:
        if_converge = value_iteration(discount_factor, noises, states, grid_size)
    time_end = time.time()
    print('\n')
    print('Value iteration run ',time_end-time_start, ' s')
    printStates(states, grid_size)