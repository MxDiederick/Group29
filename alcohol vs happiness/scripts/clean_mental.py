import pandas as pd

df = pd.read_csv('alcohol vs happiness/data/1-mental-illnesses-prevalence.csv')

df.drop(columns=['Code'], inplace=True)

df.to_csv('alcohol vs happiness/data/clean_mental.csv', index=False)