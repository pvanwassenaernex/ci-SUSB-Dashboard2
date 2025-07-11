import streamlit as st
import pandas as pd
import requests

CENSUS_API_KEY = "2cdb75bfaa3c0d34543d6f866676c97e3c8e9751"

@st.cache_data
def load_crosswalk():
    return pd.read_csv("ci_naics_crosswalk_6digit_major.csv", dtype=str)

@st.cache_data
def fetch_susb_data(naics_list):
    all_data = []
    base_url = "https://api.census.gov/data/2022/susb"
    variables = ["FIRM", "ESTAB", "EMP", "AP", "RCP"]

    for naics in naics_list:
        params = {
            "get": ",".join(variables),
            "for": "us:*",
            "NAICS2022": naics,
            "key": CENSUS_API_KEY
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            json_data = response.json()
            headers = json_data[0]
            values = json_data[1]
            record = dict(zip(headers, values))
            record["NAICS_Code"] = naics
            all_data.append(record)
        except Exception as e:
            st.warning(f"❌ {naics}: {e}")
    return pd.DataFrame(all_data)

# Load NAICS crosswalk
df_crosswalk = load_crosswalk()

# Sidebar or main filters
st.title("CI-SUSB Dashboard MVP")

sector_options = sorted(df_crosswalk["CI_Sector"].dropna().unique())
selected_sector = st.selectbox("Select CI Sector", ["All"] + sector_options)

if selected_sector == "All":
    df_filtered = df_crosswalk.copy()
else:
    df_filtered = df_crosswalk[df_crosswalk["CI_Sector"] == selected_sector]

if "Subsector" in df_filtered.columns and df_filtered["Subsector"].notnull().any():
    subsector_options = sorted(df_filtered["Subsector"].dropna().unique())
    selected_subsector = st.selectbox("Select Subsector (optional)", ["All"] + subsector_options)

    if selected_subsector != "All":
        df_filtered = df_filtered[df_filtered["Subsector"] == selected_subsector]

# Show filtered NAICS codes
st.write("Filtered NAICS Codes:")
st.dataframe(df_filtered[["CI_Sector", "Subsector", "NAICS_Code", "NAICS_Description"]])

# Fetch SUSB data
if st.button("Fetch SUSB Data"):
    with st.spinner("Pulling SUSB records from Census API..."):
        susb_data = fetch_susb_data(df_filtered["NAICS_Code"].unique().tolist())

        if not susb_data.empty:
            merged = df_filtered.merge(susb_data, on="NAICS_Code", how="left")
            st.success("✅ SUSB data retrieved for available NAICS codes.")
            st.dataframe(merged)

            csv = merged.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, file_name="ci_susb_merged_data.csv", mime="text/csv")
        else:
            st.error("No data retrieved. Check API key or selected NAICS availability.")
