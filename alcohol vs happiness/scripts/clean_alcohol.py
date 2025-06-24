import pandas as pd

df = pd.read_csv('alcohol vs happiness/data/total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv')

df.drop(columns=['Code'], inplace=True)

df.to_csv('alcohol vs happiness/data/clean_alcohol.csv', index=False)