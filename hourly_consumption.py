
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt



def hourly_consumption2(df, homeid=None):
    # Calculate the average hourly consumption
    average_consumption = df['electric-combined'].mean()


    fig = go.Figure()

    # Add line plot
    fig.add_trace(go.Scatter(x=df.index, y=df['electric-combined'], mode='lines', name='mains'))

    # Add horizontal line at the average consumption
    fig.add_shape(type="line",
                  x0=df.index.min(), y0=average_consumption,
                  x1=df.index.max(), y1=average_consumption,
                  line=dict(color="Red", width=2, dash="dash"))

    fig.update_layout(
        title=f'Hourly electricity consumption for home {homeid}',
        xaxis_title="Date",
        yaxis_title="Electric Combined",
        autosize=False,
        width=1000,
        height=500,
        xaxis=dict(
            tickformat="%Y-%m-%d %H:%M"  # Display x-axis labels in the format "Year-Month-Day Hour:Minute"
        )
    )
    return fig

def hourly_consumption(df):
    df = df['electric-combined'].copy().reset_index()
    fig, ax = plt.subplots()  # Create a new figure and axes
    sns.boxplot(data = df, x = df.time.dt.hour, y = 'electric-combined', ax=ax)  # Plot on the created axes
    ax.set_title('Hourly electricity consumption')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Electricity consumption')
    return fig