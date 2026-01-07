import streamlit as st
import pandas as pd

# Load the guest list
@st.cache_data
def load_data():
    df = pd.read_csv('seating_list.csv')
    # Clean strings to make searching easier
    df['First Name'] = df['First Name'].str.strip()
    df['Last Name'] = df['Last Name'].str.strip()
    return df

df = load_data()

# App Header
st.set_page_config(page_title="Imperial Awards 2025", page_icon="🏆")
st.title("Imperial Awards and Gala 2025")
st.subheader("Welcome to Shangri-La Colombo")
st.write("Please enter your name below to find your table and seat.")

# Input fields
first_name = st.text_input("First Name").strip()
last_name = st.text_input("Last Name").strip()

if st.button("Find My Table"):
    if first_name and last_name:
        # Filter data based on input
        match = df[
            (df['First Name'].str.lower() == first_name.lower()) & 
            (df['Last Name'].str.lower() == last_name.lower())
        ]
        
        if not match.empty:
            table = match.iloc[0]['Table Number']
            seat = match.iloc[0]['Seat Number']
            
            st.success(f"Welcome, {first_name}!")
            st.balloons()
            col1, col2 = st.columns(2)
            col1.metric("Table Number", f"{table}")
            col2.metric("Seat Number", f"{seat}")
        else:
            st.error("Name not found. Please check your spelling or see the registration desk.")
    else:
        st.warning("Please enter both your first and last name.")

# Footer
st.markdown("---")
st.caption("10th January 2025 | 6:00 PM onwards")