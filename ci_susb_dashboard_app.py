import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("ci_naics_crosswalk_6digit_major.csv")  # ← use your uploaded real file

df = load_data()

st.title("CI–NAICS Crosswalk Viewer")

# Step 1: Select CI Sector
sectors = df['CI_Sector'].dropna().unique()
selected_sector = st.selectbox("Select a CI Sector", sectors)

filtered_df = df[df['CI_Sector'] == selected_sector]

# Step 2: Optional Subsector filter
if 'Subsector' in filtered_df.columns and filtered_df['Subsector'].notnull().any():
    subsectors = filtered_df['Subsector'].dropna().unique()
    selected_subsector = st.selectbox("Select a Subsector (optional)", ['All'] + list(subsectors))
    if selected_subsector != 'All':
        filtered_df = filtered_df[filtered_df['Subsector'] == selected_subsector]

# Step 3: Display Filtered Results
st.subheader("Matching NAICS Codes")
st.dataframe(filtered_df)

# Step 4: Download filtered results
st.download_button("Download Filtered Results as CSV", filtered_df.to_csv(index=False), file_name="filtered_ci_naics.csv", mime="text/csv")
