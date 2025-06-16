import pandas as pd

df_centril = pd.read_csv('data/alcohol vs happiness/happiness-cantril-ladder.csv')
df_alcohol = pd.read_csv('data/alcohol vs happiness/total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv')

print(df_centril.columns)
print(df_alcohol.columns)

df_merged = pd.merge(
    df_centril,
    df_alcohol,
    on=['Entity','Year'],
    how='inner',
    validate='many_to_many'
)

print(f"Samengevoegd: {df_merged.shape[0]} rijen × {df_merged.shape[1]} kolommen")
print(df_merged.head())

df_merged.to_csv('data/merged_centril_alcohol.csv', index=False)