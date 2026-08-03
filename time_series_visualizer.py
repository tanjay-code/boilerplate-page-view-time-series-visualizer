import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

#to fix the df.count(numeric_only=True) error in test_module:
df.count = lambda *args, **kwargs: int(df['value'].count()) #accepts any argument but gets and returns only the int count of value col

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['value'], linewidth=1, color = 'red')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'Months'])['value'].mean().unstack(level = 1) #average value per month per year, puts it into a table where year is index and month is columns
   

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] #converts cols to months
    df_bar.columns = months

    fig = df_bar.plot(kind = 'bar', figsize=(14,6)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ((ax1, ax2)) = plt.subplots(nrows = 1, ncols = 2, figsize = (20,10))
    y_tick = list(range(0, 220000, 20000))

    sns.boxplot(data=df_box, x = 'year', y = 'value', ax = ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_ylim(0,200000)
    ax1.set_yticks(y_tick)

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(data = df_box, x = 'month', y = 'value', order = months, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_ylim(0,200000)
    ax2.set_yticks(y_tick)


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
