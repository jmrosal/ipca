# coding: utf-8

######################################################################
# fetch data for ipca from sidra ipca
# initial date: 10/07/2016
######################################################################
from ibge import ibge_fetch
import pandas as pd
import os


__all__ = ['update_db']


# fetch data
def _fetch_data(serie, period):
    '''
    fetch the appropriated data about ipca from the ibge, by building
    the ibge's api uri
    input:
    - name: string
    - serie: str(int) - code from ibge api (63 for mom or 66 for weight)
    - period: str
    ouput:
    - dataframe
    '''
    address = "http://www.sidra.ibge.gov.br/api/values/t/1419" + \
              "/p/{}/v/{}/c315/all/h/n/n1/1/f/a".format(period, serie)
    df = pd.read_json(address).loc[:, ['D1C', "D3C", "V"]]
    df_new = pd.DataFrame(df[['V']].values, index = df['D3C'].T.values,
                        columns=[pd.to_datetime(period, format="%Y%m")])
    df_new.index.name = 'date'
    return df_new


def _fetch_ipca(info, period):
    '''
    Help function. Given a period, fetches all ipca items mom changes and weights
    of that period.
    input:
    -----
    - info: str [mom, peso]
    - period: str (201610)
    output:
    -----
    - dataframe
    '''
    if info == 'mom':
        return _fetch_data(63, period)
    return _fetch_data(66, period)


def update_db(dat_file, info, dat):
    '''
    Given a period, fetches all ipca changes and weight of the all items
    and save it in csv file.
    input:
    -----
    - dat_file: str
    - info: str
    - dat: str (all)
    output:
    - None
    '''
    if os.path.exists(dat_file):
        dold = pd.read_csv(dat_file, index_col=[0])
        d = pd.to_datetime(dat, format="%Y%m").strftime(format="%Y-%m-%d")
        if not d in dold.columns[0]:
            dnew = _fetch_ipca(info, dat)
            df = pd.merge(dold, dnew,
                          left_index=True, right_index=True, how='outer').sort_index(axis=1)
            df.to_csv(dat_file, index=True, header=True)
    else:
        _fetch_ipca(info, dat).to_csv(dat_file, index=True, header=True, mode='w')
