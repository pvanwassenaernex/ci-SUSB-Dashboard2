from pathlib import Path

# Define the path for the updated app file
updated_app_path = Path("/mnt/data/ci_susb_dashboard_app_updated.py")

# Updated app code as a Python string
updated_app_code = """
import streamlit as st
import pandas as pd

# Load CI-to-NAICS crosswalk
crosswalk_df = pd.read_csv("ci_naics_crosswalk_6digit_major.csv", dtype=str)

# Load full SUSB dataset
susb_df = pd.read_csv("us_state_6digitnaics_2022.csv", dtype=str)

# Clean up numeric columns
for col in ["Firms*", "Establishments*", "Employment*", "Annual Payroll ($1,000)", "Receipts ($1,000)"]:
    if col in susb_df.columns:
        susb_df[col] = susb_df[col].str.replace(",", "").astype(float)

# Filter SUSB to national total and overall firm size
susb_df = susb_df[(susb_df["State"] == "00") & (susb_df["Enterprise Size"] == "01: Total")]

st.title("CI-SUSB Dashboard MVP")

# CI sector filter
ci_sectors = sorted(crosswalk_df["CI_Sector"].unique().tolist())
ci_sector = st.selectbox("Select CI Sector", ["All"] + ci_sectors)

# Subsector filter
if ci_sector != "All":
    filtered_subs = sorted(crosswalk_df[crosswalk_df["CI_Sector"] == ci_sector]["Subsector"].unique())
else:
    filtered_subs = sorted(crosswalk_df["Subsector"].unique())
subsector = st.selectbox("Select Subsector (optional)", ["All"] + filtered_subs)

# Filter NAICS codes
filtered_crosswalk = crosswalk_df.copy()
if ci_sector != "All":
    filtered_crosswalk = filtered_crosswalk[filtered_crosswalk["CI_Sector"] == ci_sector]
if subsector != "All":
    filtered_crosswalk = filtered_crosswalk[filtered_crosswalk["Subsector"] == subsector]

naics_codes = filtered_crosswalk["NAICS_Code"].unique()
filtered_susb = susb_df[susb_df["NAICS"].isin(naics_codes)]

# Merge descriptions from crosswalk
merged_df = pd.merge(filtered_crosswalk, filtered_susb, left_on="NAICS_Code", right_on="NAICS", how="left")

# Display table
st.subheader("Filtered NAICS + SUSB Data:")
st.dataframe(merged_df[[
    "CI_Sector", "Subsector", "NAICS_Code", "NAICS_Description", 
    "Firms*", "Establishments*", "Employment*", 
    "Annual Payroll ($1,000)", "Receipts ($1,000)"
]])

# Download button
st.download_button(
    label="Export to CSV",
    data=merged_df.to_csv(index=False).encode('utf-8'),
    file_name="filtered_ci_susb_data.csv",
    mime="text/csv"
)
"""

# Write the updated code to file
updated_app_path.write_text(updated_app_code)

# Return path for user to download or deploy
updated_app_path.name
