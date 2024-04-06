import pickle
import pandas as pd
from prophet import Prophet

# Load the pickled model
with open('/Users/barry/CodeAcademy/Ideal_dataset/coding/models/model.pkl', 'rb') as f:
    m = pickle.load(f)

# Create a DataFrame for future predictions
def fbprophet_model(m):
    future = m.make_future_dataframe(periods=24, freq='H')

# Use the loaded model to make predictions
    forecast = m.predict(future)
    st.write(forecast)
