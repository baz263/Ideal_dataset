import streamlit as st
import boto3
from io import StringIO
import pandas as pd
from heatmap import heatmap2
from hourly_consumption import hourly_consumption2
from power_hour_count import power_hour_count
from day_consumption import day_consumption_outliersremoved


st.set_page_config(layout="wide")



def df_getter(homeid):
    session = boto3.Session(
        aws_access_key_id = st.secrets['AWS']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = st.secrets['AWS']['AWS_SECRET_ACCESS_KEY'])


    # Create an S3 resource object using the session
    s3 = session.resource('s3')

    obj = s3.Object('electric1hcsvs', f'1H_csv/hourly_{homeid}.csv')
    response = obj.get()

    # The object's data is in the 'Body' field of the response
    data = response['Body'].read().decode('utf-8')

    # Use pandas to read the CSV data into a DataFrame
    df = pd.read_csv(StringIO(data))
    df.time = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    return df


tab1, tab2 = st.tabs(["House Breakdown", "Forecasting"])

houses = ['hourly_61', 'hourly_62']


# with st.sidebar:
#     for house in houses:
#         st.checkbox(house)

        
houses = ['61', '62', '63', '65', '73', '90', '96', '106', '105', '136', '128', '139', '140', '145', '146', '168', '169', '171', '162', '175', '208', '212', '225', '228', '227', '231', '238', '242', '249', '255', '262', '264', '263', '266', '268', '259', '276', '311', '328']

# with st.sidebar:
#     for house in houses:
#         if st.checkbox(house):
#             selected_house = house
#             break
# if selected_house is None:
#     df = df_getter(61)
# else:
#     df = df_getter(selected_house)  # Load the DataFrame for the selected house

session_state = st.session_state

# Initialize the session state for the checkboxes if it doesn't exist
for house in houses:
    if house not in session_state:
        session_state[house] = False  # Initially, all checkboxes are unchecked

with st.sidebar:
    st.write('House choices:')
    for house in houses:
        # Create a checkbox for each house and link it to the session state
        was_checked = session_state[house]
        session_state[house] = st.checkbox(house, value=was_checked)

        # If this checkbox was just checked, uncheck all other checkboxes
        if session_state[house] and not was_checked:
            for other_house in houses:
                if other_house != house:
                    session_state[other_house] = False

# Find the selected house
selected_house = next((house for house in houses if session_state[house]), None)

if selected_house is None:
    df = df_getter(61)
else:
    df = df_getter(selected_house) 

with tab1:
    st.header('House breakdown')


    top_section= st.empty()

    time_periods = ['Last 7 days','Last 30 days', 'Last 365 days', 'All']

    # Create the dropdown menu and get the selected time period
    selected_time_period = st.selectbox('Select time period', time_periods)

    # Filter the DataFrame based on the selected time period
    if selected_time_period == 'Last 7 days':
        df2 = df[-7*24:]
    elif selected_time_period == 'Last 30 days':
        df2 = df[-30*24:]
    elif selected_time_period == 'Last 365 days':
        df2 = df[-7*24*365:]
    elif selected_time_period == 'All':
        df2 = df
    else:
        df2 = df[-30*24:]


    fig2 = hourly_consumption2(df2)
    st.plotly_chart(fig2,use_container_width=True)

    col1, col2 = st.columns([3,2])

with col2:
    fig1 = heatmap2(df)
    fig1.update_layout(autosize = True)

    st.plotly_chart(fig1,use_container_width =True)


with col1:
    fig3 = power_hour_count(df)
    st.pyplot(fig3)

    fig4 = day_consumption_outliersremoved(df)
    st.pyplot(fig4)

with tab2:
    st.write('boob')



