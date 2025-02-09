from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def get_color_pairs(df):
    # Créer une liste de tuples (ColorMin, ColorMax)
    color_pairs = list(zip(df["ColorMin"], df["ColorMax"]))

    # Compter les occurrences de chaque duo
    pair_counts = Counter(color_pairs)
    for pair in pair_counts.keys():
        save_pair(pair[1], pair[0])
    return pair_counts

def save_pair(color_max, color_min):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    hex = RegularPolygon((1, 1), numVertices=6, radius=1, color='k', fill=False)
    ax.add_patch(hex)

    circle = plt.Circle((1, 1), 0.75, color=color_max, fill=True)
    ax.add_artist(circle)
    circle = plt.Circle((1, 1), 0.3, color=color_min, fill=True)
    ax.add_artist(circle)
    plt.axis('off')
    plt.autoscale(enable=True)
    plt.savefig(f"pairs/{color_min}_{color_max}.png", dpi=300, bbox_inches='tight')
    plt.close()