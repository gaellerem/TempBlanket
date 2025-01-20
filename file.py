import pandas as pd

def get_color(temp):
    if temp < 0 :
        return '#332E57'
    elif 0 <= temp < 3:
        return '#3C1B4F'
    elif 3 <= temp < 6:
        return '#6D5BAE'
    elif 6 <= temp < 9:
        return '#825286'
    elif 9 <= temp < 12:
        return '#9F589E'
    elif 12 <= temp < 15:
        return '#D5C7E9'
    elif 15 <= temp < 18:
        return '#F0B2CB'
    elif 18 <= temp < 21:
        return '#F785C9'
    elif 21 <= temp < 24:
        return '#B62C81'
    elif 24 <= temp < 27:
        return '#AE2958'
    elif 27 <= temp < 30:
        return '#632243'
    elif 30 <= temp < 33:
        return '#811530'
    elif 33 <= temp < 36:
        return '#E80128'
    elif 36 <= temp :
        return '#F74E3C'

def extract_data(filepath):
    df = pd.read_csv(filepath, sep=';', names=['Date', 'TempMin', 'TempMax'])
    df['Date'] = pd.to_datetime(df["Date"], format='%d/%m/%Y')
    df['ColorMin'] = ""
    df['ColorMax'] = ""

    for i, row in df.iterrows():
        df.at[i, 'ColorMin'] = get_color(row['TempMin'])
        df.at[i, 'ColorMax'] = get_color(row['TempMax'])
    return df