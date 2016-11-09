# coding: utf-8

######################################################################
# decomposion of ipca into its differents subcomponents
# initial date: 31/10/2016
######################################################################
import pandas as pd
import numpy as np
import json

__all__ = ['decomposition']


_dipca = pd.read_csv('./ipca.csv', index_col = [0, 1], na_values=['...']).drop_duplicates()
_decompo = json.loads(open('./decomposition.json').read())


# help function
def decomp(df, category, dat):
    '''
    returns index of given category of core
    input:
    -----
    - df: data frame
    - category: list (indexes of the core)
    - dat: date (ex: 2016-09-01)
    output:
    ------
    - double
    '''
    dmonth = df.loc[dat]
    ch = dmonth['mom'].loc[category].dropna()
    wg = dmonth['peso'].loc[category].dropna()
    return ch.dot(wg)/sum(wg)


def weights(df, category, dat):
    '''
    returns weights of given category of core
    input:
    -----
    - df: data frame
    - category: list (indexes of the core)
    - dat: date (ex: 2016-09-01)
    output:
    ------
    - double
    '''
    return  df['peso'].loc[dat].loc[category].sum()


def _tradables_weights(dat):
    return weights(_dipca, _decompo[0]['comercializaveis'], dat)


def _monitored_weights(dat):
    return weights(_dipca, _decompo[0]['monitorados'], dat)


def _ipca(dat):
    return _dipca['mom'].loc[dat].loc[7169]


# Functions to export
def serv(dat):
    return decomp(_dipca, _decompo[0]['servicos'], dat)


def serv_core(dat):
    return decomp(_dipca, _decompo[0]['servicos_nucleo'], dat)


def duraveis(dat):
    return decomp(_dipca, _decompo[0]['duraveis'], dat)


def semi(dat):
    return decomp(_dipca, _decompo[0]['semiduraveis'], dat)


def nduraveis(dat):
    return decomp(_dipca, _decompo[0]['nao-duraveis'], dat)


def monitorados(dat):
    return decomp(_dipca, _decompo[0]['monitorados'], dat)


def livres(dat):
    p = _monitored_weights(dat)/100
    return 1/(1-p) * (_ipca(dat) - p*monitorados(dat))


def comercializaveis(dat):
    return decomp(_dipca, _decompo[0]['comercializaveis'], dat)


def ncomercializaveis(dat):
    p = _tradables_weights(dat)/100
    q = _monitored_weights(dat)/100
    return 1/(1 - p - q)*(_ipca(dat) - p*comercializaveis(dat) - q*monitorados(dat))


def core_ex0(dat):
    food_home = _dipca['mom'].loc[dat].loc[7171]
    p = _dipca['peso'].loc[dat].loc[7171]/100
    q = _monitored_weights(dat)/100
    return 1/(1 - p - q) * (_ipca(dat)-p * food_home - q * monitorados(dat))


def core_ex1(dat):
    ex1 = decomp(_dipca, _decompo[0]['ex1'], dat)
    p = weights(_dipca, _decompo[0]['ex1'], dat)
    return 1/(1 - p) * (_ipca(dat) - p * ex1)


# consolidado
def decomposition(dat):
    consolidado = [serv, serv_core, duraveis, semi, nduraveis,
                   monitorados, livres, comercializaveis,
                   ncomercializaveis, core_ex0, core_ex1]
    names = ['servicos', 'nucleo - servicos', 'duraveis', 'semi-duraveis',
             'nao-duraveis', 'monitorados', 'livres', 'tradables', 'non-tradables',
             'nucleo-ex0', 'nucleo-ex1']
    return pd.DataFrame(np.array([c(dat) for c in consolidado]).reshape(1, 11),
                        index = [dat], columns = names)
