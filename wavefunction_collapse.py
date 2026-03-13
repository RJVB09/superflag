import numpy as np
import pickle
import random as r
import matplotlib.pyplot as plt

directions = {"up" : (-1, 0), "down" : (1, 0), "left" : (0, -1), "right" : (0, 1)}

with open('adjacency_rules.pkl', 'rb') as f:
    adjacency_rules = pickle.load(f)

flag_indeces = adjacency_rules.keys()

# Add an empty flag for easy convergence, It can border with itself and all other flags
ADD_EMPTY_FLAG = False

# Create wave function
super_flag_size = (32, 32)

wavefunction = []
entropy = []

for x in range(super_flag_size[0]):
    column = []
    column_ent = []
    for y in range(super_flag_size[1]):
        column.append(set(flag_indeces))
        column_ent.append(len(flag_indeces))
    
    wavefunction.append(column)
    entropy.append(column_ent)

#print(wavefunction[0][0])

def collapse_and_propagate(X, Y, set_value = None):
    if set_value == None:
        wavefunction[X][Y] = {r.choice(list(wavefunction[X][Y]))}
        #print(wavefunction[X][Y])
    else:
        wavefunction[X][Y] = set([set_value])

    changes = 1
    # Propagate the correction on the distributions
    while changes > 0:
        changes = 0

        for x in range(super_flag_size[0]):
            for y in range(super_flag_size[1]):
                distribution = wavefunction[x][y]
                adjacency_rule = [set(),set(),set(),set()]

                # Get the total adjacency rule for this cell
                for index in distribution:
                    for i, adjacency in enumerate(adjacency_rules[index]):
                        adjacency_rule[i] |= adjacency

                # If a wavefunction cell is set to the empty flag, allow it to border anything (maybe add the empty flag later to the ruleset)
                if len(distribution) == 0 and not ADD_EMPTY_FLAG:
                    for i in range(4):
                        adjacency_rule[i] |= set(flag_indeces)

                # Update the distributions of the neighbours
                for (nx, ny), allowed_adjacent in zip(directions.values(), adjacency_rule):
                    # Test if neighbour lies outside
                    if x+nx >= super_flag_size[0] or x+nx < 0 or y+ny >= super_flag_size[1] or y+ny < 0:
                        continue
                    
                    length_before = len(wavefunction[x+nx][y+ny])

                    # Check if collapsed
                    if length_before == 1:
                        continue

                    wavefunction[x+nx][y+ny] &= allowed_adjacent

                    changes += length_before - len(wavefunction[x+nx][y+ny])

                entropy[x][y] = len(wavefunction[x][y])

                # if x == 10 and y == 4:
                #     print(distribution, adjacency_rule)

        #print(changes)

def get_lowest_entropy_cell(entropy):
    arr = np.array(entropy)

    idx = np.argmin(np.where(arr != 1, arr, np.inf))
    return np.unravel_index(idx, arr.shape)


# collapse_and_propagate(16,16, set_value=5)
# collapse_and_propagate(16,17, set_value=5)

# plt.imshow(entropy)
# plt.show()

# print(get_lowest_entropy_cell(entropy))

# print(wavefunction[0][0])

collapses = 1

# First collapse
collapse_and_propagate(super_flag_size[0] // 2, super_flag_size[1] // 2, set_value=5)

while collapses < super_flag_size[0] * super_flag_size[1]:
    cx, cy = get_lowest_entropy_cell(entropy)

    collapse_and_propagate(cx, cy)

    plt.imshow(entropy)
    plt.draw()
    plt.pause(0.001)
    plt.clf()

    collapses += 1

    print(np.round((collapses / (super_flag_size[0] * super_flag_size[1]))*100,2))

print(wavefunction)

with open('collapsed_wavefunction.pkl', 'wb') as f:
    pickle.dump(wavefunction, f)