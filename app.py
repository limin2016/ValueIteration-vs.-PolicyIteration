from valueIteration import do_several_value_iterations
from policyIteration import do_several_policy_iterations
from utils import create_grid

file_name = 'i1.txt'

# create a new Grid
rlt = create_grid(file_name) # [size, discount_factor, noises, states]
grid_size = rlt[0]
discount_factor = rlt[1]
noises = rlt[2]
states = rlt[3]

do_several_value_iterations(discount_factor, noises, states, grid_size)

rlt = create_grid(file_name) # [size, discount_factor, noises, states]
grid_size = rlt[0]
discount_factor = rlt[1]
noises = rlt[2]
states = rlt[3]
do_several_policy_iterations(discount_factor, noises, states, grid_size)
