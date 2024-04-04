import streamlit as st
import boto3
from io import StringIO
import pandas as pd
from heatmap import heatmap2
from hourly_consumption import hourly_consumption2
from power_hour_count import power_hour_count
from day_consumption import day_consumption_outliersremoved


def df_getter():
    session = boto3.Session(
        aws_access_key_id = st.secrets['AWS']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = st.secrets['AWS']['AWS_SECRET_ACCESS_KEY'])


    # Create an S3 resource object using the session
    s3 = session.resource('s3')

    obj = s3.Object('electric1hcsvs', '1H_csv/hourly_136.csv')
    response = obj.get()

    # The object's data is in the 'Body' field of the response
    data = response['Body'].read().decode('utf-8')

    # Use pandas to read the CSV data into a DataFrame
    df = pd.read_csv(StringIO(data))
    df.time = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    return df

df = df_getter()

top_section= st.empty()
fig2 = hourly_consumption2(df)
plotly_chart(fig2)

col1, col2 = st.columns([3,2])


fig1 = heatmap2(df)
fig1.update_layout(autosize=False, width=400)
col1.plotly_chart(fig)



fig3 = power_hour_count(df)
fig3.update_layout(autosize=False, width=400)
col2.pyplot(fig3)

fig4 = day_consumption_outliersremoved(df)
fig4.update_layout(autosize=False, width=400)

col2.pyplot(fig4)


