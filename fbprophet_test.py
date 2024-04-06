import pickle
import pandas as pd
from prophet import Prophet
import boto3
import os
from dotenv import load_dotenv
from io import BytesIO 


# Load the pickled model
# with open('/Users/barry/CodeAcademy/Ideal_dataset/coding/models/model.pkl', 'rb') as f:
#     m = pickle.load(f)

# # Create a DataFrame for future predictions
# def fbprophet_model(m):
#     future = m.make_future_dataframe(periods=24, freq='H')

# # Use the loaded model to make predictions
#     forecast = m.predict(future)
#     st.write(forecast)


def model_maker():
    load_dotenv()
    #area under work
    session = boto3.Session(
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'])
    # Create an S3 resource object using the session
    s3 = session.resource('s3')
    fbprophet_model = s3.Object('electric1hcsvs', 'models/model.pkl').get()
    bytestream = BytesIO(fbprophet_model['Body'].read())
    m = pickle.load(bytestream)
    future = m.make_future_dataframe(periods=72, freq='H')
    print(future)
    return future



def plotly_plt(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.ds, y=df['yhat'], mode='lines', name='yhat'))
    #fig.add_trace(go.Scatter(x=df.ds, y=df['yhat_lower'], fill=None, mode='lines', line_color='rgba(255,0,0,0.2)', name='yhat_lower'))
    #fig.add_trace(go.Scatter(x=df.ds, y=df['yhat_upper'], fill='tonexty', mode='lines', line_color='rgba(255,0,0,0.2)', name='yhat_upper'))
    fig.add_trace(go.Scatter(x=df.ds, y=df['electric-combined'], mode='lines', name='electric-combined'))
    return fig

df = model_maker()

# Calculate the difference between consecutive entries
df['time_diff'] = df['ds'].diff()

# Check if there are any differences that are not equal to 1 hour
gaps = df[df['time_diff'] != pd.Timedelta(hours=1)]
print(len(gaps))