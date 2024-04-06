import plotly.graph_objects as go

def fbprophet_plot(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['yhat'], mode='lines', name='yhat'))
    #fig.add_trace(go.Scatter(x=df.ds, y=df['yhat_lower'], fill=None, mode='lines', line_color='rgba(255,0,0,0.2)', name='yhat_lower'))
    #fig.add_trace(go.Scatter(x=df.ds, y=df['yhat_upper'], fill='tonexty', mode='lines', line_color='rgba(255,0,0,0.2)', name='yhat_upper'))
    fig.add_trace(go.Scatter(x=df.index, y=df['electric-combined'], mode='lines', name='electric-combined'))
    fig.update_layout(title_text='Electricity consumption forecast using Facebook Prophet')
    return fig

