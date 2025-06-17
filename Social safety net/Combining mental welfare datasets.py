import pandas as pd
from scipy.stats import zscore

# ---------- 1. Inlezen ----------
su = pd.read_csv("suicide.csv")
mi = pd.read_csv("1- mental-illnesses-prevalence.csv")
hap = pd.read_csv("happiness-cantril-ladder.csv")

# ---------- 2. Suicide samenvatten ----------
su_agg = (su.groupby(["country", "year"], as_index=False)
            .agg({"suicides_no": "sum", "population": "sum"}))
su_agg["suicides_per_100k"] = 1e5 * su_agg["suicides_no"] / su_agg["population"]
su_agg = su_agg[["country", "year", "suicides_per_100k"]]

# ---------- 3. Mental-illness kolommen ----------
mi = mi.rename(columns={"Entity":"country", "Code":"iso3", "Year":"year"})
# Pak automatisch alle kolommen die op 'share of population' eindigen
ill_cols = [c for c in mi.columns if c.endswith("share of population) - Sex: Both - Age: Age-standardized")]
# Kortere namen
short = {c: c.split(" disorders")[0].lower().replace(" ", "_")+"_prev" for c in ill_cols}
mi = mi.rename(columns=short)
ill_cols = list(short.values())
mi["total_mental_illness_prev"] = mi[ill_cols].sum(axis=1)
mi = mi[["country","year"] + ill_cols + ["total_mental_illness_prev"]]

# ---------- 4. Happiness ----------
hap = (hap.rename(columns={"Entity":"country", "Code":"iso3", "Year":"year",
                           "Cantril ladder score":"ladder"})
          [["country","year","ladder"]])

# ---------- 5. Merge ----------
dfs = [su_agg, mi, hap]
mental_wellness = dfs[0]
for d in dfs[1:]:
    mental_wellness = mental_wellness.merge(d, on=["country","year"], how="inner")

# ---------- 6. Optioneel: samengestelde index ----------
z_cols = ["suicides_per_100k", "total_mental_illness_prev", "ladder"]
mental_wellness[z_cols] = mental_wellness[z_cols].apply(zscore)
mental_wellness["mental_wellness_index"] = (
    - mental_wellness["suicides_per_100k"]
    - mental_wellness["total_mental_illness_prev"]
    + mental_wellness["ladder"]
)

print(mental_wellness.head())

mental_wellness.to_csv("mental_welfare_dataset.csv")
