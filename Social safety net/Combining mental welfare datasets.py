import pandas as pd
from scipy.stats import zscore

# ---------- 1. Inlezen ----------
su   = pd.read_csv("suicide.csv")
mi   = pd.read_csv("1- mental-illnesses-prevalence.csv")
hap  = pd.read_csv("happiness-cantril-ladder.csv")

# ---------- 2. Suicide condenseren ----------
su_agg = (su.groupby(["country", "year"], as_index=False)
            .agg({"suicides_no": "sum", "population": "sum"}))
su_agg["suicides_per_100k"] = 1e5 * su_agg["suicides_no"] / su_agg["population"]
su_agg = su_agg[["country", "year", "suicides_per_100k"]]

# ---------- 3. Mental-illness totalen ----------
mi = mi.rename(columns={"Entity": "country", "Year": "year", "Code": "iso3"})

# alle leeftijd-gestandaardiseerde kolommen verzamelen
ill_cols = [c for c in mi.columns if c.endswith("Age-standardized")]
mi["ill_prev_total"] = mi[ill_cols].sum(axis=1)
mi = mi[["country", "year", "ill_prev_total"]]

# ---------- 4. Happiness ----------
hap = (hap.rename(columns={"Entity": "country", "Year": "year",
                           "Cantril ladder score": "ladder"})
          [["country", "year", "ladder"]])

# ---------- 5. Merge ----------
df = su_agg.merge(mi, on=["country", "year"]) \
           .merge(hap, on=["country", "year"])

# ---------- 6. Export ----------
df.to_csv("mental_welfare_dataset.csv", index=False)

# (optioneel) even laten zien welke mentale-aandoening-kolommen zijn gesommeerd
print("Illness columns summed:", ill_cols)

