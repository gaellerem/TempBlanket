import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from config import APP_PATH
import pandas as pd

def get_color(temp):
    if temp < 0 :
        return '#332E57',611
    elif 0 <= temp < 3:
        return '#3C1B4F', 840
    elif 3 <= temp < 6:
        return '#6D5BAE', 884
    elif 6 <= temp < 9:
        return '#825286', 701
    elif 9 <= temp < 12:
        return '#9F589E', 669
    elif 12 <= temp < 15:
        return '#D5C7E9', 959
    elif 15 <= temp < 18:
        return '#EFABDD', 958
    elif 18 <= temp < 21:
        return '#F785C9', 992
    elif 21 <= temp < 24:
        return '#B62C81', 984
    elif 24 <= temp < 27:
        return '#AE2958', 689
    elif 27 <= temp < 30:
        return '#632243', 679
    elif 30 <= temp < 33:
        return '#811530', 841
    elif 33 <= temp < 36:
        return '#E80128', 977
    elif 36 <= temp :
        return '#F74E3C', 728

def extract_data(filepath):
    df = pd.read_csv(filepath, sep=';', names=['Date', 'TempMin', 'TempMax'])
    df['Date'] = pd.to_datetime(df["Date"], format='%d/%m/%Y')
    df['WoolMin'] = ""
    df['WoolMax'] = ""

    for i, row in df.iterrows():
        color, wool = get_color(row['TempMin'])
        df.at[i, 'ColorMin'] = color
        df.at[i, 'WoolMin'] = wool
        color, wool = get_color(row['TempMax'])
        df.at[i, 'ColorMax'] = color
        df.at[i, 'WoolMax'] = wool
    return df

def load_ui(ui_file_name, parent=None):
    ui_file = QFile(os.path.join(APP_PATH, f"view/ui/{ui_file_name}.ui"))
    ui_file.open(QIODevice.ReadOnly)
    loader = QUiLoader()
    widget = loader.load(ui_file, parent)
    ui_file.close()
    return widget
