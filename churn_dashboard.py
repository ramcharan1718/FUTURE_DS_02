import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import webbrowser

# -----------------------------
# LOAD DATA
# -----------------------------
file_path = "churn_data.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame({
        "customer_id": range(1, 101),
        "gender": ["Male","Female"] * 50,
        "tenure": [i % 24 + 1 for i in range(100)],
        "MonthlyCharges": [round(300 + i*5, 2) for i in range(100)],
        "Contract": ["Month-to-month","One year","Two year","Month-to-month"] * 25,
        "InternetService": ["Fiber optic","DSL","No","Fiber optic"] * 25,
        "Churn": ["Yes" if i % 3 == 0 else "No" for i in range(100)]
    })

# -----------------------------
# CLEANING
# -----------------------------
df.dropna(inplace=True)
df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})

# -----------------------------
# KPIs
# -----------------------------
total_customers = len(df)
churn_rate = round(df["ChurnFlag"].mean()*100, 2)
avg_tenure = round(df["tenure"].mean(), 1)
avg_revenue = round(df["MonthlyCharges"].mean(), 2)

# -----------------------------
# DATA PREP
# -----------------------------
contract_churn = df.groupby("Contract")["ChurnFlag"].mean().reset_index()
internet_churn = df.groupby("InternetService")["ChurnFlag"].mean().reset_index()

# -----------------------------
# DASHBOARD LAYOUT
# -----------------------------
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "domain"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.08,
    subplot_titles=(
        "Total Customers", "Churn Rate",
        "Churn by Contract", "Tenure Distribution",
        "Charges vs Churn", "Internet Service"
    )
)

# -----------------------------
# KPI CARDS (FIXED SIZE)
# -----------------------------
fig.add_trace(go.Indicator(
    mode="number",
    value=total_customers,
    number={'font': {'size': 55}},
    title={"text": "👥 Customers"},
), row=1, col=1)

fig.add_trace(go.Indicator(
    mode="number",
    value=churn_rate,
    number={'suffix': "%", 'font': {'size': 55}},
    title={"text": "⚠️ Churn Rate"},
), row=1, col=2)

# -----------------------------
# CHARTS
# -----------------------------
fig.add_trace(go.Bar(
    x=contract_churn["Contract"],
    y=contract_churn["ChurnFlag"],
    text=contract_churn["ChurnFlag"].round(2),
    textposition="auto",
    name="Contract"
), row=2, col=1)

hist = px.histogram(df, x="tenure", color="Churn", nbins=20)
for t in hist.data:
    fig.add_trace(t, row=2, col=2)

box = px.box(df, x="Churn", y="MonthlyCharges")
for t in box.data:
    fig.add_trace(t, row=3, col=1)

fig.add_trace(go.Pie(
    labels=internet_churn["InternetService"],
    values=internet_churn["ChurnFlag"],
    hole=0.5
), row=3, col=2)

# -----------------------------
# FINAL LAYOUT (🔥 FULL SCREEN FIX)
# -----------------------------
fig.update_layout(
    template="plotly_dark",
    autosize=True,
    height=None,
    width=None,

    title={
        "text": "🚀 Customer Churn Analytics Dashboard",
        "x": 0.5,
        "font": {"size": 26}
    },

    margin=dict(l=20, r=20, t=70, b=20),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# -----------------------------
# SAVE & OPEN
# -----------------------------
output_file = "premium_dashboard.html"

fig.write_html(
    output_file,
    config={'responsive': True}
)

webbrowser.open("file://" + os.path.realpath(output_file))

print("✅ Premium dashboard opened in full screen!")