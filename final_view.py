import streamlit as st
import pandas as pd
import sqlalchemy as sa

# Set page config for wider layout
st.set_page_config(layout="wide")

# Function to load data from MySQL
@st.cache_data(show_spinner=True)
def load_data(query):
    try:
        engine = sa.create_engine('mysql+mysqlconnector://root:root@localhost/bus_routes')
        df = pd.read_sql(query, engine)
        engine.dispose()
        return df
    except Exception as e:
        st.error(f'Error loading data: {e}')
        return pd.DataFrame()

def main():
    st.title("redbus.in acquired from MySQL")

    query = """SELECT route_name as Route_Name, route_link as Route_Link, busname as Bus_Name,
               bustype as Bus_Type, departing_time as Departing_Time, duration as Duration,
               reaching_time as Reaching_Time, star_rating as Star_Rating, price as Price, 
               seats_available as Seat_Availability, State_Transport FROM bus_routes"""

    # Load data
    data = load_data(query)

    st.sidebar.header("Filter Options")

    # Ensure session state variables are initialized
    if "selected_state_transport" not in st.session_state:
        st.session_state.selected_state_transport = ''
    if "selected_route_name" not in st.session_state:
        st.session_state.selected_route_name = ''
    if "selected_star_rating" not in st.session_state:
        st.session_state.selected_star_rating = (0.0, 5.0)
    if "rows_to_display" not in st.session_state:
        st.session_state.rows_to_display = 20

    # Populate State Transport filter options
    state_transport = [''] + data['State_Transport'].unique().tolist()
    selected_state_transport = st.sidebar.selectbox(
        "Select a State Transport to filter", state_transport, 
        index=state_transport.index(st.session_state.selected_state_transport)
    )

    # Update session state
    st.session_state.selected_state_transport = selected_state_transport

    # Filter DataFrame by selected State Transport
    filtered_df = data[data['State_Transport'] == selected_state_transport] if selected_state_transport else data

    # Populate Route Name filter options
    route_name = [''] + filtered_df['Route_Name'].unique().tolist()
    selected_route_name = st.sidebar.selectbox(
        "Select a Route Name to filter", route_name, 
        index=route_name.index(st.session_state.selected_route_name)
    )

    # Update session state
    st.session_state.selected_route_name = selected_route_name

    # Filter DataFrame by selected Route Name
    filtered_df2 = filtered_df[filtered_df['Route_Name'] == selected_route_name] if selected_route_name else filtered_df

    # Populate Star Rating filter options
    star_rating = st.sidebar.slider(
        "Select a Star Rating range to filter",
        min_value=float(data["Star_Rating"].min()),
        max_value=float(data["Star_Rating"].max()),
        value=st.session_state.selected_star_rating,
        step=0.1
    )

    # Update session state
    st.session_state.selected_star_rating = star_rating

    # Filter DataFrame by selected Star Rating
    final_filtered_df = filtered_df2[
        (filtered_df2['Star_Rating'] >= star_rating[0]) & 
        (filtered_df2['Star_Rating'] <= star_rating[1])
    ]

    # Limit the number of rows displayed
    rows_to_display = st.sidebar.slider("Number of rows to display", min_value=10, max_value=100, value=st.session_state.rows_to_display)
    st.session_state.rows_to_display = rows_to_display

    # Convert 'Route_Link' column into clickable links using Markdown
    final_filtered_df['Route_Link'] = final_filtered_df['Route_Link'].apply(lambda x: f"[Link]({x})")

    # Display data using markdown
    st.write(f"Current route has {len(final_filtered_df)} buses.")
    st.markdown(final_filtered_df.head(rows_to_display).to_markdown(index=False), unsafe_allow_html=True)

    # Reset button logic
    if st.sidebar.button("Reset", type="primary"):
        st.write("Reset button clicked.")

        # Clear session state
        st.session_state.selected_state_transport = ''
        st.session_state.selected_route_name = ''
        st.session_state.selected_star_rating = (0.0, 5.0)
        st.session_state.rows_to_display = 20

        # Reset the state of the filters
        st.experimental_set_query_params(reset="true")

    # Check if reset was requested
    if st.experimental_get_query_params().get("reset") == ["true"]:
        # Clear the query params
        st.experimental_set_query_params()
        #st.experimental_rerun()  # Trigger the rerun after clearing query params

if __name__ == "__main__":
    main()
