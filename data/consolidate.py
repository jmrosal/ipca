######################################################################
# consolidates ipca core data
# initial date: 16/11/2016
######################################################################
import pandas as pd
import os
from decomposition import decomposition


dat = '2016-10-01'

dipca = pd.read_csv('ipca.csv', index_col=[0, 1])

if not os.path.exists('consolidated.csv'):
    idx = dipca.index.get_level_values(0).unique()
    df = pd.DataFrame(index=idx)
    for i in idx:
        print decomposition(dipca, i)
