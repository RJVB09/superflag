import numpy as np

def rgb_to_hsv(rgb):
    rgb = rgb.astype(float) / 255.0  # normalize to 0-1
    r, g, b = rgb[:,0], rgb[:,1], rgb[:,2]

    cmax = np.max(rgb, axis=1)
    cmin = np.min(rgb, axis=1)
    delta = cmax - cmin

    # Hue calculation
    h = np.zeros_like(cmax)
    mask = delta != 0

    # Red is max
    idx = (cmax == r) & mask
    h[idx] = (60 * ((g[idx] - b[idx]) / delta[idx])) % 360

    # Green is max
    idx = (cmax == g) & mask
    h[idx] = (60 * ((b[idx] - r[idx]) / delta[idx]) + 120) % 360

    # Blue is max
    idx = (cmax == b) & mask
    h[idx] = (60 * ((r[idx] - g[idx]) / delta[idx]) + 240) % 360

    # Saturation
    s = np.zeros_like(cmax)
    s[cmax != 0] = delta[cmax != 0] / cmax[cmax != 0]

    # Value
    v = cmax

    return np.stack([h, s, v], axis=1)