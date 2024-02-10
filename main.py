import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

def align_y_axis(ax1, ax2, minresax1, minresax2):
    """ Sets tick marks of twinx axes to line up with 7 total tick marks

    ax1 and ax2 are matplotlib axes
    Spacing between tick marks will be a factor of minresax1 and minresax2"""

    ax1ylims = ax1.get_ybound()
    ax2ylims = ax2.get_ybound()
    ax1factor = minresax1 * 6
    ax2factor = minresax2 * 6
    ax1.set_yticks(np.linspace(ax1ylims[0],
                               ax1ylims[1]+(ax1factor -
                               (ax1ylims[1]-ax1ylims[0]) % ax1factor) %
                               ax1factor,
                               7))
    ax2.set_yticks(np.linspace(ax2ylims[0],
                               ax2ylims[1]+(ax2factor -
                               (ax2ylims[1]-ax2ylims[0]) % ax2factor) %
                               ax2factor,
                               7))


df = pd.read_csv('toronto-movies.csv', sep=',')
df_exc = pd.read_csv('EXCAUS.csv', sep=',')
df_exc['DATE']=pd.to_datetime(df_exc['DATE'],yearfirst=True)
df['year']=df['year'].astype(int)
df_exc['year'] = pd.DatetimeIndex(df_exc['DATE']).year
df_m = np.full(268, 7, dtype=np.int64)
df_d = np.full(268, 28, dtype=np.int64)
s = pd.to_datetime(pd.DataFrame({'year':df['year'], 'month':df_m, 'day':df_d})).dt.date
df['time']= s
df.set_index(['time'],inplace=True)
plt.figure(figsize=(12,8))
sns.set_style(rc = {'axes.facecolor': '#ffb997'})
ax = sns.histplot(x=mdates.date2num(df.index), bins = 45, ec= '#ffb997', color = "#db4268",legend= False)

df_exc.set_index(['DATE'],inplace=True)
sns.set_style('whitegrid', {'grid.color' : '#db4268','grid.linestyle': '--'})
ax2 = plt.twinx()
sns.lineplot(x=mdates.date2num(df_exc.index), y=df_exc["EXCAUS"], color = '#621940', ax=ax2, lw = 1.5, legend= False)
ax.set_xlim([df_exc.index[0], df_exc.index[-1]])

ax2.set_ylim([0.5,1.75])
ax.set(ylabel = 'Number of Movies Filmed', xlabel = "Year")
ax2.set(xlabel="Year", ylabel="CAD per USD")
align_y_axis(ax,ax2, 1,.25)
ax.axvline(x = np.datetime64("1997-01-27"), ymin = 0, ymax = 1, color = "#FFE2D5", lw = 2, linestyle="dashed")
plt.suptitle("How Effective Were the 1997 Tax Breaks to Promoting Toronto Movie Filming?")
plt.show()