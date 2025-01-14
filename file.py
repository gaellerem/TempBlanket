import pandas as pd

def get_color(temp):
    if temp < 0 :
        return '#332E57'
    elif 0 <= temp < 3:
        return '#3C1B4F'
    elif 3 <= temp < 6:
        return '#5e237f'
    elif 6 <= temp < 9:
        return '#6D5BAE'
    elif 9 <= temp < 12:
        return '#825286'
    elif 12 <= temp < 15:
        return '#9F589E'
    elif 15 <= temp < 18:
        return '#D5C7E9'
    elif 18 <= temp < 21:
        return '#F6CFDF'
    elif 21 <= temp < 24:
        return '#B62C81'
    elif 24 <= temp < 27:
        return '#AE2958'
    elif 27 <= temp < 30:
        return '#F36973'
    elif 30 <= temp < 33:
        return '#F74E3C'
    elif 33 <= temp < 36:
        return '#E80128'
    elif 36 <= temp :
        return '#811530'

def extract_data(filepath):
    df = pd.read_csv(filepath, sep=';', names=['Date', 'TempMin', 'TempMax'])
    df['Date'] = pd.to_datetime(df["Date"], format='%d/%m/%Y')
    df['ColorMin'] = ""
    df['ColorMax'] = ""

    for i, row in df.iterrows():
        df.at[i, 'ColorMin'] = get_color(row['TempMin'])
        df.at[i, 'ColorMax'] = get_color(row['TempMax'])
    return df