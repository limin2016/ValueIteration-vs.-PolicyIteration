from utils import out_of_range, printStates
import copy
import time

def update_value(state, states, grid_size, discount_factor):
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
        final_value += state.noises[0] * states[row_index_left][col_index_left].val * discount_factor
    else:
        final_value += state.val * state.noises[0] * discount_factor

    if not out_of_range(row_index_up, col_index_up, grid_size):
        final_value += state.noises[1] * states[row_index_up][col_index_up].val * discount_factor
    else:
        final_value += state.val * state.noises[1] * discount_factor

    if not out_of_range(row_index_right, col_index_right, grid_size):
        final_value += state.noises[2] * states[row_index_right][col_index_right].val * discount_factor
    else:
        final_value += state.val * state.noises[2] * discount_factor

    if not out_of_range(row_index_down, col_index_down, grid_size):
        final_value += state.noises[3] * states[row_index_down][col_index_down].val * discount_factor
    else:
        final_value += state.val * state.noises[3] * discount_factor
    state.val = final_value


def get_max_value(state, left_noise, up_noise, right_noise, down_noise, discount_factor, states, grid_size):
    temp_noises = [left_noise, up_noise, right_noise, down_noise]
    state.set_initial_policy(temp_noises)
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


def update_policy(discount_factor, noises, states, grid_size):
    policy_stable = True
    for row_val in states:
        for index, state in enumerate(row_val):
            if state.is_terminal:
                continue
            next_states = [copy.copy(state), copy.copy(state), copy.copy(state), copy.copy(state)]
            # they cover all situations because there are always two noises which have same value
            get_max_value(next_states[0], noises[0], noises[1], noises[2], noises[3], discount_factor, states, grid_size)
            get_max_value(next_states[1], noises[3], noises[0], noises[1], noises[2], discount_factor, states, grid_size)
            get_max_value(next_states[2], noises[2], noises[3], noises[0], noises[1], discount_factor, states, grid_size)
            get_max_value(next_states[3], noises[1], noises[2], noises[3], noises[0], discount_factor, states, grid_size)
            max_state = next_states[0]
            for next_state in next_states:
                if next_state.val > max_state.val:
                    max_state = next_state
            if max_state.noises != state.noises:
                policy_stable = False
    if policy_stable:
        return True
    return False




def policy_iteration(discount_factor, noises, states, grid_size, acceptable_difference):
    old_states = copy.deepcopy(states)
    max_difference = 0
    for row_val in states:
        for state in row_val:
            if state.is_terminal:
                continue
            old_val = state.val
            update_value(state, old_states, grid_size, discount_factor)
            max_difference = max(max_difference, abs(state.val - old_val))
    # print(max_difference)
    if max_difference < acceptable_difference:
        #update_policy(discount_factor, noises, states, grid_size)
        if_end = update_policy(discount_factor, noises, states, grid_size)
        return if_end
    return False


def init_policy(states, noises):
    for row_val in states:
        for state in row_val:
            state.set_initial_policy(noises)


def do_several_policy_iterations(discount_factor, noises, states, grid_size):
    time_start = time.time()
    get_optimal_policy = False
    acceptable_difference = 0.0001
    init_policy(states, noises)
    # for i in range(100):
    #     policy_iteration(discount_factor, noises, states, grid_size, acceptable_difference)
    # time_end = time.time()
    # print('\n')
    # print("Policy iteration run ", time_end - time_start, ' s')
    # printStates(states, grid_size)
    # return
    while not get_optimal_policy:
        get_optimal_policy = policy_iteration(discount_factor, noises, states, grid_size, acceptable_difference)
        if get_optimal_policy:
            time_end = time.time()
            print('\n')
            print("Policy iteration run ", time_end - time_start, ' s')
            printStates(states, grid_size)
            return



