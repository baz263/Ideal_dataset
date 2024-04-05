import matplotlib.pyplot as plt
import seaborn as sns

def day_consumption_outliersremoved(df):
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']
    fig, ax = plt.subplots(figsize = (9,6))

    df = df['electric-combined'].copy().reset_index()
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    #df = df[(df > (Q1 - 1.5 * IQR)) & (df < (Q3 + 1.5 * IQR))]
    sns.boxplot(data = df, x = df.time.dt.day_name(), y = 'electric-combined', ax=ax, order = order, palette = 'mako' )
    ax.set_title('Daily hour consumption - averaged', color='white')

    fig.set_facecolor('black')
    ax.set_facecolor('lightgray')
    ax.tick_params(axis= 'x', colors= 'white')
    ax.tick_params(axis= 'y', colors= 'white')
    return fig