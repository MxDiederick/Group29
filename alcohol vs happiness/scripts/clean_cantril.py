import pandas as pd

df = pd.read_csv('alcohol vs happiness/data/happiness-cantril-ladder.csv')

df.drop(columns=['Code'], inplace=True)

df.to_csv('alcohol vs happiness/data/clean_centril.csv', index=False)