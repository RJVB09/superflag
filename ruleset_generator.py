from PIL import Image
from pathlib import Path
import numpy as np
import pickle
from rgb_converters import rgb_to_hsv

folder_scaled = Path("flags_scaled")
start_flag = folder_scaled / "nl.png"

#   Neighbour position      row self        row neighbour
#   Upper                   0x              -1x                 
#   Lower                   -1x             0x
#   Left                    0y              -1y
#   Right                   -1y             0y
# direction, (row, col, n_row, n_col)
slice_directions = {
    "upper": (0, slice(None), -1, slice(None)),
    "lower": (-1, slice(None), 0, slice(None)),
    "left":  (slice(None), 0, slice(None), -1),
    "right": (slice(None), -1, slice(None), 0)
}

accepted_color_distance = 0.25

# Compares two lists of rgb255 colors and returns a value regarding how similar they are.
# The test uses the average distance between the colors in the HSV cylinder radius: saturation, height: value, longitude: hue
def color_test(list1, list2):

    # the cylinder height is 0 to 1 and radius is 0 to 1

    # convert to hsv
    hsv1 = rgb_to_hsv(list1)
    hsv2 = rgb_to_hsv(list2)

    #hue_MSE = np.average((np.minimum((hsv1[:,0]-hsv2[:,0]) % 180, (hsv2[:,0]-hsv1[:,0]) % 180))**2)

    v_dist = (hsv1[:, 2] - hsv2[:, 2])**2
    hs_dist = (hsv1[:, 1]*np.sin(np.deg2rad(hsv1[:, 0])) - hsv2[:, 1]*np.sin(np.deg2rad(hsv2[:, 0])))**2 + (hsv1[:, 1]*np.cos(np.deg2rad(hsv1[:, 0])) - hsv2[:, 1]*np.cos(np.deg2rad(hsv2[:, 0])))**2

    cyl_distance = np.average(np.sqrt(v_dist + hs_dist))

    return cyl_distance


# Generate list of flag names:
flag_bitmaps = {}
flag_names = {}

flag_indeces = []

index = 0

# Add an empty flag for easy convergence, It can border with itself and all other flags
ADD_EMPTY_FLAG = False

if ADD_EMPTY_FLAG:
    flag_indeces.append(index)
    flag_names[index] = 'empty'
    flag_bitmaps[index] = 0


for file in folder_scaled.glob("*.png"):
    flag_indeces.append(index)
    with Image.open(file).convert("RGB") as img:
        flag_names[index] = file.name
        flag_bitmaps[index] = np.array(img)

    index += 1

if ADD_EMPTY_FLAG:
    flag_bitmaps[0] = np.zeros_like(flag_bitmaps[1])

#print(flag_names)

# Create adjacency rules, key: flag index, value: [upper allowed, lower allowed, left allowed, right allowed]
adjacency_rules = {}


for index, bitmap in flag_bitmaps.items():
    if index == 0 and ADD_EMPTY_FLAG:
        adjacency_rules[0] = [set(flag_bitmaps.keys()), set(flag_bitmaps.keys()), set(flag_bitmaps.keys()), set(flag_bitmaps.keys())]
        print(0, adjacency_rules[0])
        continue

    adjacency_rules[index] = []

    #print(index, adjacency_rules[index])

    # # Iterate through the possible neighbours and decide if they're suitable
    for direction, (row, col, n_row, n_col) in slice_directions.items():
        allowed = set([])
        if ADD_EMPTY_FLAG:
            allowed = set([0])

        for n_index, n_bitmap in flag_bitmaps.items():
            #MSE = np.average((bitmap[-1, :, :] - n_bitmap[0, :, :]) ** 2) # Mean squared error

            side = bitmap[row, col, :]
            #print(side)

            n_side = n_bitmap[n_row, n_col, :]
            #print(n_side)
            color_distance = color_test(side, n_side)

            # Add it if the color matches within tolerance on the edge and its a different flag
            if color_distance < accepted_color_distance and n_index != index:
                allowed.add(n_index)

            #print(index, n_index)

        adjacency_rules[index].append(allowed)
    print(index, adjacency_rules[index])

with open('adjacency_rules.pkl', 'wb') as f:
    pickle.dump(adjacency_rules, f)
    print('Saved adjacency_rules.pkl')

with open('flag_names.pkl', 'wb') as f:
    pickle.dump(flag_names, f)
    print('Saved flag_names.pkl')

with open('flag_bitmaps.pkl', 'wb') as f:
    pickle.dump(flag_bitmaps, f)
    print('Saved flag_bitmaps.pkl')

# Create wave function
# super_flag_size = (32, 32)

# wavefunction = []

# for x in range(super_flag_size[0]):
#     column = []
#     for y in range(super_flag_size[1]):
#         column.append(flag_indeces)
    
#     wavefunction.append(column)

#print(wavefunction)

# 0, 1, 2, 3 = upper, left, lower, right
# def compare_single_edge(flag_name, neighbour_flag_name, edge):
#     if edge == 0:
# bitmap = flag_bitmaps[5] # albania
# print(flag_names[5])
# n_bitmap = flag_bitmaps[21]
# print(flag_names[21])

# color_top_edge = np.average(bitmap[-1, :])
#print(rgb_to_hsv(n_bitmap[:, -1, :]))

# MSE = color_test(bitmap[0, :, :], n_bitmap[-1, :, :]) # Mean squared error

#   Neighbour position      row self        row neighbour
#   Upper                   0x              -1x                 
#   Lower                   -1x             0x
#   Left                    0y              -1y
#   Right                   -1y             0y
