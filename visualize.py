from PIL import Image
import numpy as np
import pickle
import matplotlib.pyplot as plt

with open('collapsed_wavefunction.pkl', 'rb') as f:
    wavefunction = pickle.load(f)

with open('flag_bitmaps.pkl', 'rb') as f:
    flag_bitmaps = pickle.load(f)

field = wavefunction.copy()

for x in range(len(wavefunction)):
    for y in range(len(wavefunction[0])):
        field[x][y] = list(wavefunction[x][y])[0]

field = np.array(field)

tiling_res = field.shape
flag_res = flag_bitmaps[0].shape

superflag = np.zeros((tiling_res[0]*flag_res[0], tiling_res[1]*flag_res[1], 3), dtype = int)


for id, flag_index in np.ndenumerate(field):
    flag = flag_bitmaps[flag_index]

    superflag[id[0]*flag_res[0]:((id[0]+1)*flag_res[0]), id[1]*flag_res[1]:((id[1]+1)*flag_res[1])] = flag

plt.imshow(superflag)
plt.show()

img = Image.fromarray(superflag.astype(np.uint8), "RGB")
img.save("superflag.png")
