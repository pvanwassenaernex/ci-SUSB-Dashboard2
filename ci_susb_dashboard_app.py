import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("mock_ci_susb_crosswalk.csv")
    return df

df = load_data()

st.title("CI-SUSB Dashboard MVP")

sectors = df['CI Sector'].dropna().unique()
sector = st.selectbox("Select CI Sector", sectors)

filtered_df = df[df['CI Sector'] == sector]

if 'CI Subsector' in filtered_df.columns and filtered_df['CI Subsector'].notnull().any():
    subsectors = filtered_df['CI Subsector'].dropna().unique()
    subsector = st.selectbox("Select CI Subsector", ['All'] + list(subsectors))
    if subsector != 'All':
        filtered_df = filtered_df[filtered_df['CI Subsector'] == subsector]

st.dataframe(filtered_df)