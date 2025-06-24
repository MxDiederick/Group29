import pandas as pd

df_centril_alcohol = pd.read_csv('alcohol vs happiness/data/merged_cantril_alcohol.csv')
df_mental_alcohol = pd.read_csv('alcohol vs happiness/data/merged_mental_alcohol.csv')


print(df_centril_alcohol.columns)
print(df_mental_alcohol.columns)


df_merged = pd.merge(
    df_centril_alcohol,
    df_mental_alcohol,
    on=['Entity','Year','Alcohol_consumption'],
    how='inner',
    validate='many_to_many'
)

print(f"Samengevoegd: {df_merged.shape[0]} rijen × {df_merged.shape[1]} kolommen")
print(df_merged.head())

df_merged.to_csv('alcohol vs happiness/data/merged_all.csv', index=False)