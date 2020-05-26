"""
Simple script showing how to download NTS demand data and plot a chart
"""

import datetime as dt
from matplotlib import pyplot as plt
from mipi import Mipi

M = Mipi()
start = dt.date(2020,1,1)
stop = dt.date(2020,4,30)
df = M.get_physical_flows(start, stop)

df = df.set_index('ApplicableFor')
df['Value'].plot()
plt.ylabel('Gas Demand in million cubic metres')
plt.title('UK NTS Daily Gas Demand')
plt.show()