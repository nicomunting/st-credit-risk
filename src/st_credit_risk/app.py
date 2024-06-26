import os

import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv(os.path.join("..", "..", "data", "credit_risk_dataset.csv"))

df["loan_status"] = (
    df["loan_status"].astype("category")
    .cat.rename_categories({0: "Non-Default", 1: "Default"})
)

cat_order = {"loan_status": ["Non-Default", "Default"]}

count_fig = px.histogram(df, x="loan_status", category_orders={"loan_status": ["Non-Default", "Default"]})
st.plotly_chart(count_fig)

variable = st.selectbox("Variable", ["person_age", "person_income", "person_home_ownership"])
hist_fig = px.histogram(df, x=variable, color="loan_status", category_orders=cat_order)
st.plotly_chart(hist_fig)

st.write(df)
