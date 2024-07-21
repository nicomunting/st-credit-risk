import os

import pandas as pd
import plotly.express as px
import streamlit as st

from st_credit_risk.utils import vars, var_labels


st.set_page_config("Credit Risk EDA", page_icon=":credit_card:", layout="wide")

st.title("Credit Risk - Exploratory Data Analysis")


# From https://www.kaggle.com/datasets/laotse/credit-risk-dataset/
df = pd.read_csv(os.path.join("data", "credit_risk_dataset.csv"))

df["loan_status"] = (
    df["loan_status"].astype("category")
    .cat.rename_categories({0: "Non-Default", 1: "Default"})
)

categories_order = {
    "loan_status": ["Non-Default", "Default"],
    "loan_grade": ["A", "B", "C", "D", "E", "F", "G"],
}

tabs = st.tabs(["Overview", "Univariate", "Bivariate"])

with tabs[0]:
    col1, col2 = st.columns([1, 3], gap="large")
    with col1:
        count_fig = px.histogram(df, x="loan_status", category_orders=categories_order, labels=var_labels)
        st.plotly_chart(count_fig, use_container_width=False)

    with col2:
        st.write(df)

with tabs[1]:
    col1, col2 = st.columns([1, 3], gap="large")

    variable = col1.selectbox("Variable", vars, format_func=lambda x: var_labels[x])
    var_is_numeric = variable in df.select_dtypes(include="number")

    if var_is_numeric:
        value_range = col2.slider(
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
        category_orders=categories_order, labels=var_labels,
        marginal="rug" if var_is_numeric else None,
        title="Histogram of " + var_labels[variable]
    )
    st.plotly_chart(hist_fig, use_container_width=True)

    if var_is_numeric:
        violin_fig = px.violin(
            df, 
            x=variable, color="loan_status", 
            category_orders=categories_order, labels=var_labels,
            points="outliers", box=True,
            title="Violin plot of " + var_labels[variable]
        )
        st.plotly_chart(violin_fig, use_container_width=True)

with tabs[2]:
    corr_df = df.corr(numeric_only=True)

    st.write(corr_df)

st.write("#")
st.caption("Data from [Credit Risk Dataset from Kaggle](https://www.kaggle.com/datasets/laotse/credit-risk-dataset/).")
