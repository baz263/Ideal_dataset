import streamlit as st
import boto3
from io import StringIO


# def df_getter():
#     session = boto3.Session(
#         aws_access_key_id = st.secrets('AWS_ACCESS_KEY_ID'),
#         aws_secret_access_key = st.secrets('AWS_SECRET_ACCESS_KEY'))


#     # Create an S3 resource object using the session
#     s3 = session.resource('s3')

#     obj = s3.Object('electric1hcsvs', '1H_csv/hourly_105.csv')
#     response = obj.get()

#     # The object's data is in the 'Body' field of the response
#     data = response['Body'].read().decode('utf-8')

#     # Use pandas to read the CSV data into a DataFrame
#     df = pd.read_csv(StringIO(data))
#     return df

# df = df_getter()

# st.dataframe(df)
st.write('boob')
