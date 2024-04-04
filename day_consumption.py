import matplotlib.pyplot as plt
import seaborn as sns

def day_consumption(df, homeid = None):
    fig, axs = plt.subplots(1,1, figsize = (10, 5))
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'holiday']
    sns.boxplot(data = df, x = df.day, y = 'electric-combined', ax=axs, order = order)
    plt.title(f'daily consumption for home {homeid}')
    #axs.get_yaxis().get_major_formatter().set_scientific(False)
    

    return fig