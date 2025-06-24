import pandas as pd

df_mental = pd.read_csv('alcohol vs happiness/data/clean_mental.csv')
df_alcohol = pd.read_csv('alcohol vs happiness/data/clean_alcohol.csv')

print(df_mental.columns)
print(df_alcohol.columns)

df_merged = pd.merge(
    df_mental,
    df_alcohol,
    on=['Entity','Year'],
    how='inner',
    validate='many_to_many'
)

print(f"Samengevoegd: {df_merged.shape[0]} rijen × {df_merged.shape[1]} kolommen")
print(df_merged.head())

df_merged.to_csv('alcohol vs happiness/data/merged_mental_alcohol.csv', index=False)