# coding: utf-8

######################################################################
# fetch data for ipca from sidra ipca
# initial date: 10/07/2016
######################################################################
from ibge import ibge_fetch
import pandas as pd


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
              "/p/{}/v/{}/c315/all/n1/1/f/a".format(period, serie)
    df = pd.DataFrame(ibge_fetch([address]).stack())
    df.index.names = ['date', 'items']
    df.columns = ['mom' if int(serie) == 63 else 'peso']
    return df


def _fetch_ipca(period):
    '''
    Help function. Given a period, fetches all ipca items mom changes and weights
    of that period.
    input:
    -----
    - period: str (all, last, 12 last)
    output:
    -----
    - dataframe
    '''
    df_ch = _fetch_data(63, period)
    df_weight = _fetch_data(66, period)
    df_final = pd.merge(df_ch, df_weight,
                        right_index=True,
                        left_index=True, how='outer')
    return df_final


def update_db(period):
    '''
    Given a period, fetches all ipca changes and weight of the all items
    and save it in csv file.
    input:
    -----
    - period: str (all)
    output:
    - None
    '''
    if os.path.exists('ipca.csv'):
        dold = pd.read_csv('ipca.csv', index_col=[0, 1], parse_dates=[0])
        dnew = _fetch_ipca(period)
        df = pd.concat([dold, dnew]).drop_duplicates().sortlevel(level=0)
        df.to_csv('ipca.csv', index=True, header=True)
    else:
        _fetch_ipca(period).to_csv('ipca.csv', index=True, header=True)
