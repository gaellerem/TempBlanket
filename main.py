from draw import draw_hexagons
from file import extract_data
from pairs import get_color_pairs
from ui_template.template import make_ui

df = extract_data('data.csv')
# draw_hexagons(22, 18, 1, df)
# get_color_pairs(df)

make_ui()