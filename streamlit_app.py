import streamlit as st
import boto3
from io import StringIO
import pandas as pd
from heatmap import heatmap2
from hourly_consumption import hourly_consumption2
from power_hour_count import power_hour_count
from day_consumption import day_consumption_outliersremoved
from fbprophet_plot import fbprophet_plot
import pickle
from io import BytesIO
from joblib import load
from sklearn.linear_model import LinearRegression



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

def df_getter_all():
    session = boto3.Session(
        aws_access_key_id = st.secrets['AWS']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = st.secrets['AWS']['AWS_SECRET_ACCESS_KEY'])


    # Create an S3 resource object using the session
    s3 = session.resource('s3')

    obj = s3.Object('electric1hcsvs', f'combined_1h/6_months_data.csv')
    response = obj.get()

    # The object's data is in the 'Body' field of the response
    data = response['Body'].read().decode('utf-8')

    # Use pandas to read the CSV data into a DataFrame
    df = pd.read_csv(StringIO(data))
    df.time = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    return df

def model_maker(forecast_time):
    forecast_time = int(forecast_time)
    #area under work
    session = boto3.Session(
    aws_access_key_id = st.secrets['AWS']['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = st.secrets['AWS']['AWS_SECRET_ACCESS_KEY'])

    s3 = session.resource('s3')
    fbprophet_model = s3.Object('electric1hcsvs', 'models/model.pkl').get()
    bytestream = BytesIO(fbprophet_model['Body'].read())
    m = load(bytestream)
    future = m.make_future_dataframe(periods=forecast_time, freq='H')
    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat']]
    #st.write(forecast)
    #st.write(future)
    return forecast

def model_maker_linear_1h():
    session = boto3.Session(
    aws_access_key_id = st.secrets['AWS']['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = st.secrets['AWS']['AWS_SECRET_ACCESS_KEY'])

    s3 = session.resource('s3')
    fbprophet_model = s3.Object('electric1hcsvs', 'models/linear_6_all_1h.pkl').get()
    bytestream = BytesIO(fbprophet_model['Body'].read())
    m = load(bytestream)
    return m






df_1h_all = df_getter_all()

df_topredict = df_1h_all.tail(1)[['temperature_2m (°C)', 'relative_humidity_2m (%)',
       'weather_code (wmo code)', 'wind_speed_10m (km/h)',
       'wind_direction_10m (°)', 'day', 'hour', 'electric-combined',
       'electric-combined-yesterday', 'electric-combined-last-week']]
model_linear_1h= model_maker_linear_1h()
st.write(df_topredict)
predictions = model_linear_1h.predict(df_topredict)
predictiondf = pd.DataFrame(predictions, columns=['electric-combined-next-hour'],index = df_topredict.index +1)
st.write(predictiondf)


#predictiondf= pd.DataFrame(model_linear_1h.predict(df_topredict) ,index = df_topredict.index +1, columns=['electric-combined-next-hour'])



tab1, tab2, tab3, tab4 = st.tabs(["House Breakdown", "Forecasting", 'Coummunity','Dataframe'])

houses = ['hourly_61', 'hourly_62']


# with st.sidebar:
#     for house in houses:
#         st.checkbox(house)

        
houses = ['61', '62', '63', '65', '73', '90', '96', '106', '105', '136', '128', '139', '140', '145', '146', '168', '169', '171', '162', '175', '208', '212', '225', '228', '227', '231', '238', '242', '249', '255', '262', '264', '263', '266', '268', '259', '276', '311', '328']
enhanced_houses =['61', '62', '63', '65', '73', '90', '96', '106', '105', '136', '128', '139', '140', '145', '146', '168', '169', '171', '162', '175', '208', '212', '225', '228', '227', '231', '238', '242', '249', '255', '262', '264', '263', '266', '268', '259', '276', '311', '328']

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
    df = df_getter(106)
else:
    df = df_getter(selected_house) 

with tab1:
    with st.container():
        st.header('House breakdown')


        top_section= st.empty()

        time_periods = ['Last 7 days','Last 30 days', 'Last 365 days', 'All']

        # Create the dropdown menu and get the selected time period
        selected_time_period = st.selectbox('Select time period', time_periods, key = 'chosen_house')

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

       

        #lets try to make the area chart
        electric_appliances = [
            'gasfire', 'electricheater', 'fridge', 'freezer', 'fridgefreezer', 'gashob', 'electrichob', 'gasoven', 'electricoven',
            'grill', 'toaster', 'microwave', 'shower', 'electricshower','washingmachine', 'tumbledrier', 'washingmachinetumbledrier',
            'dishwasher','kettle', 'dehumidifier', 'vacuumcleaner', 'other', 'electric-combined'
        ]
        if selected_house in enhanced_houses:
            electric_appliances = [val for val in electric_appliances if val in df2.columns]
            df2 = df2.reset_index()
            st.area_chart(
                df2, x='time', y=electric_appliances
            )


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
    #st.write(predictiondf)
    #slider for projection amount
    forecast_time = st.select_slider(
        'Select a color of the rainbow',
        options=['24', '48', '72', '96', '120'])
    st.write('forecasted projection', forecast_time)

    fbprophet_dataframe = model_maker(forecast_time)
    fbprophet_dataframe.index = fbprophet_dataframe['ds']
    fbprophet_dataframe = fbprophet_dataframe.drop(columns = ['ds'])


    #fbprophet_dataframe= fbprophet_dataframe.rename(columns = {'ds':'time'})
    merged_df = fbprophet_dataframe.join(df_1h_all, how='left')

    #merged_df = fbprophet_dataframe.merge(df_1h_all, on = 'time')
    

    #merged_df = fbprophet_dataframe.merge(df_1h_all, on = 'time', how='left')

    #forecast_merge_actual = forecast_pred.merge(df_electric_test, on = 'ds')

    merged_df = merged_df[-(24*31):]
    fig_fbprophet = fbprophet_plot(merged_df)
    st.plotly_chart(fig_fbprophet, use_container_width=True)


with tab3:
    with st.container():
        st.write('boob')
        st.dataframe(data=df_1h_all.tail(148))
        st.header('Community breakdown')


        top_section= st.empty()

        time_periods = ['Last 7 days','Last 30 days', 'Last 365 days', 'All']

        # Create the dropdown menu and get the selected time period
        selected_time_period_all = st.selectbox('Select time period', time_periods, key = 'all_houses')

        # Filter the DataFrame based on the selected time period
        if selected_time_period_all == 'Last 7 days':
            df_1h_all_2 = df_1h_all[-24*7:]
        elif selected_time_period_all == 'Last 30 days':
            df_1h_all_2 = df_1h_all[-24*30:]
        elif selected_time_period_all == 'Last 365 days':
            df_1h_all_2 = df_1h_all[-24*365:]
        elif selected_time_period_all == 'All':
            df_1h_all_2 = df_1h_all
        else:
            df_1h_all_2 = df_1h_all[-30*24:]

       
        fig_hourly_consumption_all = hourly_consumption2(df_1h_all_2)
        st.plotly_chart(fig_hourly_consumption_all,use_container_width=True)


    col3, col4 = st.columns([3,2])

    with col4:
        fig_all_heat = heatmap2(df_1h_all_2)
        fig_all_heat.update_layout(autosize = True)

        st.plotly_chart(fig_all_heat,use_container_width =True)


    with col3:
        fig_all_day = day_consumption_outliersremoved(df_1h_all_2)
        st.pyplot(fig_all_day)


with tab4:
    st.header('Dataframe_1W')
    st.dataframe(data=df.tail(148))



