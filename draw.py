import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon

def draw_hexagons(cols, rows, hex_radius, df):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    offset_x = hex_radius * np.sqrt(3)
    offset_y = hex_radius * 1.5
    index = 0
    for y in range(rows):
        for x in range(cols):
            if index > len(df) - 1 : continue
            x_center = x * offset_x
            y_center = (rows - 1 - y) * offset_y
            if y % 2 == 1 :
                if x == cols-1:
                    continue
                x_center += offset_x/2
            hex = RegularPolygon((x_center, y_center), numVertices=6, radius=hex_radius, color='k', fill=False)
            ax.add_patch(hex)

            circle = plt.Circle((x_center, y_center), 0.75, color=df["ColorMax"].iloc[index], fill=True)
            ax.add_artist(circle)
            circle = plt.Circle((x_center, y_center), 0.3, color=df["ColorMin"].iloc[index], fill=True)
            ax.add_artist(circle)

            if df["Date"].iloc[index].day == 1:
                circle = plt.Circle((x_center, y_center), 0.75, color="r", fill=False)
                ax.add_artist(circle)
            index+=1
    plt.autoscale(enable=True)
    plt.axis('off')
    plt.show()
