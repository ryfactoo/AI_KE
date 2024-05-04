import matplotlib.pyplot as plt
import numpy as np

# Definicja funkcji wypełniającej tablicę
def fill_heatmap(initial_value, end_zone):
    heatmap = [[abs((16 -x + 16 -y) + abs(x - y)) + 10 for x in range(16)] for y in range(16)]
    for i in range(1, 6):
        for j in range(1, 6):
            if i + j < 8:
                heatmap[16-i][16-j] -= 10
    return heatmap

# Wartość początkowa dla heatmape
initial_value = 50

# Utwórz heatmapę
end_zone = []
heatmap_data = fill_heatmap(initial_value, end_zone)

# Stwórz wykres heatmapy
plt.figure(figsize=(8, 6))
plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
plt.colorbar(label='Wartości')
plt.title('Heatmapa')
plt.show()
