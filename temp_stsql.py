import streamlit as st
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy as sa

# MySQL connection setup
def create_connection():
    return mysql.connector.connect(
        host="localhost",        # Update with your DB host
        user="root",    # Update with your DB username
        password="root",# Update with your DB password
        database="dswdtb4" # Update with your DB name
    )

# Function to load data from the database
def load_data(query):

    engine = sa.create_engine(
    'mysql+mysqlconnector://root:root@localhost/dswdtb4',
    connect_args={'auth_plugin': 'mysql_native_password'}
    )

    #Load data using the engine
    df = pd.read_sql(query,engine)

    #close the engine
    engine.dispose()
    #return the DF
    return df

# Streamlit app layout
def main():
    st.title("redbus.in acquired from MySql")

    # Query to get data (customize as per your table and data)
    query = """SELECT route_name as Route_Name, route_link as Route_Link, busname as Bus_Name,
                bustype as Bus_Type, departing_time as Departing_Time, duration as Duration,
                reaching_time as Reaching_Time, star_rating as Star_Rating, price as Price, 
                seats_available as Seat_Availability FROM bus_routes"""
    df = load_data(query)

    # Show the data in Streamlit
    st.subheader("All Bus Routes Table")
    #st.dataframe(df)

    # Filters: Generate filter options based on the column data
    columns = ['']+df.columns.tolist()

    st.sidebar.header("Filter Options")
    selected_column = st.sidebar.selectbox("Select a column to filter", columns)
    
    unique_values = df[selected_column].unique().tolist()
    selected_value = st.sidebar.selectbox(f"Filter {selected_column} by", unique_values)

    # Apply filter to dataframe
    filtered_df = df[df[selected_column] == selected_value]

    # Show filtered data
    st.subheader(f"Filtered Data by {selected_column}: {selected_value}")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
