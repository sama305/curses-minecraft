import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=2, seed=10)
xpix, ypix = 16, 16
pic = [[noise([i/xpix, j/ypix, 1]) for j in range(xpix)] for i in range(ypix)]

plt.imshow(pic, cmap='gray')
plt.show()