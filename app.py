import streamlit as st
import pandas as pd

# Load the guest list
@st.cache_data
def load_data():
    # Read the file
    df = pd.read_csv('seating_list.csv')
    
    # Remove rows where the name is missing
    df = df.dropna(subset=['First Name', 'Last Name'])
    
    # Clean strings and ensure names are treated as text
    df['First Name'] = df['First Name'].astype(str).str.strip()
    df['Last Name'] = df['Last Name'].astype(str).str.strip()
    
    # Safely convert numbers to integers, replacing errors with 0
    df['Table Number'] = pd.to_numeric(df['Table Number'], errors='coerce').fillna(0).astype(int)
    df['Seat Number'] = pd.to_numeric(df['Seat Number'], errors='coerce').fillna(0).astype(int)
    
    return df

df = load_data()

# App Header
st.set_page_config(page_title="Imperial Awards 2025", page_icon="🏆")
st.title("Imperial Awards and Gala 2025")
st.write("Enter your name to find your seating details.")

# Input fields
first_name = st.text_input("First Name").strip()
last_name = st.text_input("Last Name").strip()

if st.button("Find My Table"):
    if first_name and last_name:
        # Search for the guest (case-insensitive)
        match = df[
            (df['First Name'].str.lower() == first_name.lower()) & 
            (df['Last Name'].str.lower() == last_name.lower())
        ]
        
        if not match.empty:
            table = match.iloc[0]['Table Number']
            seat = match.iloc[0]['Seat Number']
            
            # Format with leading zeros (e.g., 01, 02)
            table_fmt = f"{table:02d}"
            seat_fmt = f"{seat:02d}"
            
            st.success(f"Welcome, {first_name}!")
            st.subheader(f"Table {table_fmt} — Seat {seat_fmt}")
        else:
            st.error("Name not found. Please check your spelling.")
    else:
        st.warning("Please enter both names.")

st.markdown("---")
st.caption("10th January 2025 | Shangri-La Colombo")
