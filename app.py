import streamlit as st
import pandas as pd
import os

# Load the guest list
@st.cache_data
def load_data():
    df = pd.read_csv('seating_list.csv')
    # Remove empty rows
    df = df.dropna(subset=['First Name', 'Last Name'])
    # Clean names
    df['First Name'] = df['First Name'].astype(str).str.strip()
    df['Last Name'] = df['Last Name'].astype(str).str.strip()
    # Ensure Table Number is a clean integer
    df['Table Number'] = pd.to_numeric(df['Table Number'], errors='coerce').fillna(0).astype(int)
    return df

df = load_data()

# App Page Config
st.set_page_config(page_title="Imperial Awards 2025", page_icon="🏆")

# 1. LOGO LOGIC
# This checks for 'logo.png' in your GitHub folder
if os.path.exists('logo.png'):
    st.image('logo.png', width=180)
else:
    st.info("Logo file 'logo.png' not found. Please check the filename in GitHub.")

st.title("Imperial Excellence Awards and Gala 2025")
st.write("Enter your name to find your table.")

# 2. INPUT FIELDS
first_name = st.text_input("First Name").strip()
last_name = st.text_input("Last Name").strip()

# 3. SEARCH LOGIC
if st.button("Find My Table"):
    if first_name and last_name:
        # Search case-insensitive
        match = df[
            (df['First Name'].str.lower() == first_name.lower()) & 
            (df['Last Name'].str.lower() == last_name.lower())
        ]
        
        if not match.empty:
            table = match.iloc[0]['Table Number']
            # Format to 2 digits (e.g. 01)
            table_fmt = f"{table:02d}"
            
            st.success(f"Welcome, {first_name}!")
            # Big, clear table number
            st.markdown(f"### YOUR TABLE NUMBER")
            st.title(f"Table {table_fmt}")
        else:
            st.error("Name not found. Please check your spelling or see the registration desk.")
    else:
        st.warning("Please enter both your first and last name.")

st.markdown("---")
st.caption("10th January 2025 | Shangri-La Colombo")

