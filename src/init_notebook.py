"""
Common notebook setup. First cell in your notebook should be:

    from init_notebook import *
    %matplotlib inline

Will make matplotlib available as `plt`, defines a `CMAP` for tab-complete color aliases, and a few more.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mplt_dates
import matplotlib.colors as mplt_colors

import importlib

# dark like the world without any solar
plt.style.use('dark_background')


class MatplotlibCMapAliases:
    # Default dark-mode color palette
    # (Define as class instead of a dict for attribute tab-completes)
    teal = 'C0'
    yellow = 'C1'
    lilac = 'C2'
    red = 'C3'
    blue = 'C4'
    orange = 'C5'
    green = 'C6'
    purple = 'C7'
    pale_yellow = 'C8'
    bright_yellow = 'C9'


CMAP = MatplotlibCMapAliases()

print('HEY NOTEBOOKER -- common notebook config successful. One last thing... add to cell execution:')
print('  %matplotlib inline')
print('(Include the magic %)')

