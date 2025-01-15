from draw import draw_hexagons
from file import extract_data

df = extract_data('data.csv')
draw_hexagons(22, 18, 1, df)