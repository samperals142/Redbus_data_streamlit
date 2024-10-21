import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy as sa



# Set page config for wider layout
st.set_page_config(layout="wide")

# Inject custom CSS to make the DataFrame wider
st.markdown(
    """
    <style>
    .streamlit-container {
        max-width: 1300px;  /* You can adjust this value */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Function to load data from MySQL
def load_data(query):
    try:

        engine = sa.create_engine(
        'mysql+mysqlconnector://root:root@localhost/bus_routes',
        #connect_args={'auth_plugin': 'mysql_native_password'}
        )

        #Load data using the engine
        df = pd.read_sql(query,engine)

        #close the engine
        engine.dispose()
        #return the DF
        return df
    except Exception as e:
        st.error(f'Error loading data: {e}')
        return pd.DataFrame()

def main():
    st.title("redbus.in acquired from MySql")

    # Query to get data (customize as per your table and data)
    query = """SELECT route_name as Route_Name, route_link as Route_Link, busname as Bus_Name,
                bustype as Bus_Type, departing_time as Departing_Time, duration as Duration,
                reaching_time as Reaching_Time, star_rating as Star_Rating, price as Price, 
                seats_available as Seat_Availability FROM bus_routes"""
    
    df = load_data(query)

    # Convert 'Route_Link' column into clickable links using Markdown
    df['Route_Link'] = df['Route_Link'].apply(lambda x: f"[Link]({x})")

    

    # Filters: Generate filter options based on the column data
    columns = [''] + df.columns.tolist()  # '' for no selection
    st.sidebar.header("Filter Options")
    
    # Select column and value for filtering
    selected_column = st.sidebar.selectbox("Select a column to filter", columns)
    
    if selected_column:  # If a column is selected
        unique_values = [''] + df[selected_column].unique().tolist()  # '' for no value selected
        selected_value = st.sidebar.selectbox(f"Filter {selected_column} by", unique_values)
    else:
        selected_value = ''  # No filtering
    
    # Dataframe filtering logic
    if selected_column != '' and selected_value != '':  # If both column and value are selected
        filtered_df = df[df[selected_column] == selected_value]
        #st.dataframe(filtered_df, use_container_width=True, height=700, unsafe_allow_html=True)
        st.subheader("Filtered Bus Routes Table")
        st.data_editor(filtered_df,use_container_width=True, height=700)


    else:
        # Show the data in Streamlit
        st.subheader("All Bus Routes Table")

        # Show full DataFrame when no column or value is selected
        st.data_editor(df,use_container_width=True, height=700)
        #st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

        

if __name__ == "__main__":
    main()
