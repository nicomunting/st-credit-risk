import os

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import vars, var_labels


# From https://www.kaggle.com/datasets/laotse/credit-risk-dataset/
df = pd.read_csv(os.path.join("..", "..", "data", "credit_risk_dataset.csv"))

df["loan_status"] = (
    df["loan_status"].astype("category")
    .cat.rename_categories({0: "Non-Default", 1: "Default"})
)

cat_order = {"loan_status": ["Non-Default", "Default"]}

tabs = st.tabs(["Overview", "Univariate"])

with tabs[0]:
    count_fig = px.histogram(df, x="loan_status", category_orders=cat_order, labels=var_labels)
    st.plotly_chart(count_fig)

    st.write(df)

with tabs[1]:
    variable = st.selectbox("Variable", vars, format_func=lambda x: var_labels[x])
    var_is_numeric = variable in df.select_dtypes(include="number")

    if var_is_numeric:
        value_range = st.slider(
            "Value range", 
            min_value=df[variable].min(), max_value=df[variable].max(), 
            value=(df[variable].min(), df[variable].max())
        )
        hist_df = df.loc[df[variable].between(value_range[0], value_range[1]), :]
    else:
        hist_df = df

    hist_fig = px.histogram(
        hist_df, 
        x=variable, color="loan_status", 
        category_orders=cat_order, labels=var_labels,
    )
    st.plotly_chart(hist_fig, use_container_width=True)

    if var_is_numeric:
        violin_fig = px.violin(
            df, 
            x=variable, color="loan_status", 
            category_orders=cat_order, labels=var_labels,
            points="outliers", box=True
        )
        st.plotly_chart(violin_fig, use_container_width=True)

