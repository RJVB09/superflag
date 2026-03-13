from PIL import Image
from pathlib import Path
import numpy as np

folder = Path("flags")
folder_scaled = Path("flags_scaled")

for file in folder.glob("*.png"):
    with Image.open(file) as img:
        new_img = img.resize((128, 64))
        print(np.array(new_img).shape)
        new_img.save(folder_scaled / file.name)