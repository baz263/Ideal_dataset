import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def bin_builder(df):
    count_under_10000 = df[(df['electric-combined'] < 10)].gas.count()
    count_between_10000_20000 = df[(df['electric-combined'] >= 10) & (df['electric-combined'] < 20)].gas.count()
    count_between_20000_30000 = df[(df['electric-combined'] >= 20) & (df['electric-combined'] < 30)].gas.count()
    count_between_30000_40000 = df[(df['electric-combined'] >= 30) & (df['electric-combined'] < 40)].gas.count()
    count_between_40000_50000 = df[(df['electric-combined'] >= 50) & (df['electric-combined'] < 60)].gas.count()
    count_between_50000_60000 = df[(df['electric-combined'] >= 60) & (df['electric-combined'] < 70)].gas.count()
    count_between_60000_70000 = df[(df['electric-combined'] >= 80) & (df['electric-combined'] < 80)].gas.count()
    count_between_70000_80000 = df[(df['electric-combined'] >= 90) & (df['electric-combined'] < 90)].gas.count()

 
    count_over_80000 = df[(df['electric-combined'] >= 80000)].gas.count()
    bins = [count_under_10000, count_between_10000_20000, count_between_20000_30000, count_between_30000_40000, count_between_40000_50000,count_between_50000_60000,count_between_60000_70000,count_between_70000_80000, count_over_80000]
    return bins
def power_hour_count(df, homeid=None):

    bins = bin_builder(df)


    counts = {
        'count_under_10': bins[0],
        'count_between_10_20': bins[1],
        'count_between_20_30': bins[2],
        'count_between_30_40': bins[3],
        'count_between_40_50': bins[4],
        'count_between_50_60': bins[5],
        'count_between_60_70': bins[6],
        'count_between_70_80':bins[7],
        'count_over_80': bins[7]
    }

    # Convert the dictionary to a pandas DataFrame
    df_counts = pd.DataFrame(list(counts.items()), columns=['Range', 'Count'])

    # # Create the barplot
    # sns.barplot(x='Count', y='Range', data=df_counts)
    # plt.title('Number of hours where electricity consumption falls within a given range')

    # for i in range(df_counts.shape[0]):
    #     plt.text(df_counts.Count[i], i, df_counts.Count[i], va='center')

    #    # Calculate the average
    # avg = df_counts['Count'].mean()

    # # Draw a vertical line at the average point
    # plt.axvline(x=avg, color='r', linestyle='--')


    # fig = plt.gcf()
    # # Show the plot
    # return fig
    fig, ax = plt.subplots()
    fig.set_facecolor('black')
    # Create the barplot on the axes
    sns.barplot(x='Count', y='Range', data=df_counts, ax=ax, palette= 'mako')

    # Set the title of the axes
    ax.set_title('Number of hours where electricity consumption falls within a given range', color='white')
    ax.set_facecolor('lightgray')
    ax.tick_params(axis= 'x', colors= 'white')
    ax.tick_params(axis= 'y', colors= 'white')

    

    for i in range(df_counts.shape[0]):
        ax.text(df_counts.Count[i], i, df_counts.Count[i], va='center')

    # Calculate the average
    avg = df_counts['Count'].mean()

    # Draw a vertical line at the average point
    ax.axvline(x=avg, color='r', linestyle='--')

    # Return the figure
    return fig