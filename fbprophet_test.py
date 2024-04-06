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
    future = m.make_future_dataframe(periods=24, freq='H')
    print(future)
    return future

model_maker()