import streamlit as st
import pandas as pd
import os

# Load the guest list
@st.cache_data
def load_data():
    df = pd.read_csv('seating_list.csv')
    df = df.dropna(subset=['First Name', 'Last Name'])
    df['First Name'] = df['First Name'].astype(str).str.strip()
    df['Last Name'] = df['Last Name'].astype(str).str.strip()
    # Table Number is converted to a whole number
    df['Table Number'] = pd.to_numeric(df['Table Number'], errors='coerce').fillna(0).astype(int)
    return df

df = load_data()

# App Header
st.set_page_config(page_title="Imperial Awards 2025", page_icon="🏆")

# Display Logo if it exists
if os.path.exists('logo.png'):
    st.image('logo.png', width=200)

st.title("Imperial Awards and Gala 2025")
st.write("Enter your name to find your table.")

# Input fields
first_name = st.text_input("First Name").strip()
last_name = st.text_input("Last Name").strip()

if st.button("Find My Table"):
    if first_name and last_name:
        # Search for the guest
        match = df[
            (df['First Name'].str.lower() == first_name.lower()) & 
            (df['Last Name'].str.lower() == last_name.lower())
        ]
        
        if not match.empty:
            table = match.iloc[0]['Table Number']
            # Format with leading zero (e.g., 01)
            table_fmt = f"{table:02d}"
            
            st.success(f"Welcome, {first_name}!")
            st.subheader(f"Your Table: {table_fmt}")
        else:
            st.error("Name not found. Please check your spelling.")
    else:
        st.warning("Please enter both names.")

st.markdown("---")
st.caption("10th January 2025 | Shangri-La Colombo")
