import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import plotly.graph_objects as go

###########################################################################################
# Scatterplot 1
###########################################################################################

# Dataset laden
df = pd.read_csv("alcohol vs happiness/data/merged_all.csv")

mental_vars = [
    "Schizophrenia_disorders",
    "Depressive_disorders",
    "Anxiety_disorders",
    "Bipolar_disorders",
    "Eating_disorders"
]
mental_labels = [
    "Schizofrenie stoornissen",
    "Depressie stoornissen",
    "Angst stoornissen",
    "Bipolaire stoornissen",
    "Eet stoornissen"
]
colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

# Selecteer relevante kolommen en verwijder rijen met missende waarden
df_clean = df[["Entity", "Year", "Alcohol_consumption"] + mental_vars].dropna()

fig = go.Figure()
buttons = []

for i, var in enumerate(mental_vars):
    x = df_clean["Alcohol_consumption"]
    y = df_clean[var]
    country = df_clean["Entity"]
    year = df_clean["Year"]

    # Pearson correlatie
    corr, _ = stats.pearsonr(x, y)
    corr_text = f"<b>{var}</b><br>Pearson r = {corr:.2f}"

    # Regressielijn
    slope, intercept, _, _, std_err = stats.linregress(x, y)
    reg_x = np.linspace(x.min(), x.max(), 100)
    reg_y = slope * reg_x + intercept
    y_err = std_err * 1.96
    upper = reg_y + y_err
    lower = reg_y - y_err
    rgba = f'rgba{tuple(int(colors[i].lstrip("#")[j:j+2], 16) for j in (0, 2, 4)) + (0.2,)}'

    # Punten met hoverinfo
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="markers",
        marker=dict(size=4, color=colors[i]),
        name=var,
        visible=(i == 0),
        text=[f"{c}, {y}" for c, y in zip(country, year)],
        hovertemplate="<b>%{text}</b><br>Alcohol: %{x}<br>Prevalentie: %{y}<extra></extra>"
    ))

    # CI bovenlijn
    fig.add_trace(go.Scatter(
        x=reg_x, y=upper, mode="lines",
        line=dict(width=0), hoverinfo="skip",
        visible=(i == 0), showlegend=False
    ))

    # CI onderlijn met fill
    fig.add_trace(go.Scatter(
        x=reg_x, y=lower, mode="lines",
        fill="tonexty", fillcolor=rgba,
        line=dict(width=0), hoverinfo="skip",
        visible=(i == 0), showlegend=False
    ))

    # Regressielijn
    fig.add_trace(go.Scatter(
        x=reg_x, y=reg_y, mode="lines",
        line=dict(color="black", width=3),
        name=f"{var} regressielijn",
        visible=(i == 0)
    ))

    # Visibility logica
    vis = [False] * (4 * len(mental_vars))
    for j in range(4):
        vis[i * 4 + j] = True

    # Annotations vervangen per selectie
    buttons.append(dict(
        label=var,
        method="update",
        args=[
            {"visible": vis},
            {
                "title": f"Alcoholgebruik vs {mental_labels[i]}",
                "annotations": [dict(
                    x=1.03, y=0.8,
                    xref="paper", yref="paper",
                    text=corr_text,
                    showarrow=False,
                    align="left",
                    font=dict(size=13),
                    xanchor="left"
                )]
            }
        ]
    ))

# Begin-annotatie (eerste variabele)
initial_corr, _ = stats.pearsonr(df_clean["Alcohol_consumption"], df_clean[mental_vars[0]])
initial_text = f"<b>{mental_labels[0]}</b><br>Pearson r = {initial_corr:.2f}"

fig.update_layout(
    title=f"Alcoholgebruik vs {mental_labels[0]}",  
    xaxis_title="Alcoholgebruik (liters per capita)",
    yaxis_title="Prevalentie (%)",
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        showactive=True,
        x=1.03, y=0.6,
        xanchor="left", yanchor="top"
    )],
    annotations=[dict(
        x=1.03, y=0.8,
        xref="paper", yref="paper",
        text=initial_text,
        showarrow=False,
        align="left",
        font=dict(size=13),
        xanchor="left"
    )],
    height=500,
    margin=dict(t=80, r=160, b=60, l=60)  # extra ruimte rechts voor tekst
)

fig.show()

fig.write_html("docs/scatter1.html", include_plotlyjs="cdn")


###########################################################################################
# Scatterplot 2
###########################################################################################
# Opschonen
df_clean = df[["Entity", "Year", "Alcohol_consumption", "Cantril ladder score"]].dropna()

x = df_clean["Alcohol_consumption"]
y = df_clean["Cantril ladder score"]
country = df_clean["Entity"]
year = df_clean["Year"]

# Regressie en CI
slope, intercept, _, _, std_err = stats.linregress(x, y)
reg_x = np.linspace(x.min(), x.max(), 100)
reg_y = slope * reg_x + intercept
y_err = std_err * 1.96
upper = reg_y + y_err
lower = reg_y - y_err

# Correlatie berekenen
corr, _ = stats.pearsonr(x, y)
corr_text = f"<b>Cantril ladder score</b><br>Pearson r = {corr:.2f}"

# Plot bouwen
fig = go.Figure()

# Punten
fig.add_trace(go.Scatter(
    x=x, y=y, mode="markers",
    marker=dict(size=4, color="#00CC96"),
    name="Cantril ladder score",
    text=[f"{c}, {y}" for c, y in zip(country, year)],
    hovertemplate="<b>%{text}</b><br>Alcohol: %{x}<br>Score: %{y}<extra></extra>"
))

# Bovenlijn CI
fig.add_trace(go.Scatter(
    x=reg_x, y=upper, mode="lines",
    line=dict(width=0), hoverinfo="skip", showlegend=False
))

# Onderlijn CI met fill
fig.add_trace(go.Scatter(
    x=reg_x, y=lower, mode="lines",
    fill="tonexty", fillcolor='rgba(0, 0, 0, 0.2)',
    line=dict(width=0), hoverinfo="skip", showlegend=False
))

# Regressielijn (zwart)
fig.add_trace(go.Scatter(
    x=reg_x, y=reg_y, mode="lines",
    line=dict(color="black", width=3),
    name="Regressielijn"
))

# Layout & annotatie
fig.update_layout(
    title="Alcoholgebruik vs Cantril ladder score",
    xaxis_title="Alcoholgebruik (liters per capita)",
    yaxis_title="Centril ladder score (1-10)",
    annotations=[dict(
        x=1.03, y=0.8,
        xref="paper", yref="paper",
        text=corr_text,
        showarrow=False,
        align="left",
        font=dict(size=13),
        xanchor="left"
    )],
    height=500,
    margin=dict(t=80, r=160, b=60, l=60)
)

fig.show()

fig.write_html("docs/scatter2.html", include_plotlyjs="cdn")