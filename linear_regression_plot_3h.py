import plotly.graph_objects as go


# Create a line plot for the predicted data
def linear_regression_plot_3h(predictiondf, df):
    trace1 = go.Scatter(
        x=predictiondf.time,
        y=predictiondf['electric-combined_3H-forecast'],
        
        name='predicted',
        marker=dict(
            size=10,  # Adjust the size as needed
            color='#83c9ff',  # Adjust the color as needed
        )
        
    )

    # Create a line plot for the actual data
    trace2 = go.Scatter(
        x=df.tail(48).index,
        y=df.tail(48)['electric-combined'],
        mode='lines',
        name='electric-combined'
    )

    # Combine the two plots
    data = [trace1, trace2]

    # Create a layout
    layout = go.Layout(
        title='Electricity consumption forecast',
        xaxis=dict(title='time'),
        yaxis=dict(
            title='Electricity consumption',
            range=[df['electric-combined'].min() * 0.95, df['electric-combined'].max() * 1.05]  # Adjust the padding as needed
        )
    )

    # Create a figure and plot it
    fig = go.Figure(data=data, layout=layout)
    return fig