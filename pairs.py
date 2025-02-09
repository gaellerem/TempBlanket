from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def get_color_pairs(df):
    # Créer une liste de tuples (ColorMin, ColorMax)
    color_pairs = list(zip(df["ColorMin"], df["ColorMax"]))

    # Compter les occurrences de chaque duo
    pair_counts = Counter(color_pairs)

    # Exporter les données en csv et en png
    export_color_pairs_to_csv(pair_counts, "color_pairs.csv")
    for pair in pair_counts.keys():
        export_color_pairs_to_png(pair[1], pair[0])
    return pair_counts

def export_color_pairs_to_csv(pair_counts, output_filepath):
    # Convertir le dictionnaire en DataFrame
    df_color_pairs = pd.DataFrame(pair_counts.items(), columns=["ColorMin_ColorMax", "Count"])
    
    # Séparer les couleurs en deux colonnes
    df_color_pairs[['ColorMin', 'ColorMax']] = df_color_pairs['ColorMin_ColorMax'].apply(lambda x: pd.Series(x))
    
    # Supprimer la colonne combinée
    df_color_pairs = df_color_pairs.drop(columns=["ColorMin_ColorMax"])
    
    # Sauvegarder en CSV
    df_color_pairs.to_csv(output_filepath, index=False, sep=';')
    print(f"Fichier exporté : {output_filepath}")

def export_color_pairs_to_png(color_max, color_min):
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