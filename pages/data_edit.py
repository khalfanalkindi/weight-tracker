import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(
    page_title="Edit Weight Data",  # Title shown in the browser tab
    page_icon="✏️",  # Icon for the browser tab and sidebar
    layout="wide"
)

# Fetch data from DuckDB
def get_data():
    conn = duckdb.connect("weight_tracker.db")
    df = conn.execute("SELECT date, weight FROM weight_data ORDER BY date").fetchdf()
    conn.close()
    return df

# Update data in DuckDB
def update_data(date, weight):
    conn = duckdb.connect("weight_tracker.db")
    conn.execute("UPDATE weight_data SET weight = ? WHERE date = ?", (weight, date))
    conn.close()

st.title("Edit Weight Data ✏️")

# Fetch data
df = get_data()


# Display editable table using st.data_editor
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Save updates
if st.button("Save Changes"):
    for index, row in edited_df.iterrows():
        update_data(row["date"], row["weight"])
    st.success("Changes saved!")
