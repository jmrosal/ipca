# coding: utf-8

######################################################################
# decomposion of ipca into its differents subcomponents
# initial date: 31/10/2016
######################################################################
import pandas as pd
import numpy as np
import json

__all__ = ['decomposition']


_decompo = json.loads(open('./decomposition.json').read())


# help functions
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
    return df['peso'].loc[dat].loc[category].sum()


def _tradables_weights(dipca, dat):
    return weights(dipca, _decompo[0]['comercializaveis'], dat)


def _monitored_weights(dipca, dat):
    return weights(dipca, _decompo[0]['monitorados'], dat)


def _ipca(dipca, dat):
    return dipca['mom'].loc[dat].loc[7169]


# Functions to export
# ok
def serv(dipca, dat):
    return decomp(dipca, _decompo[0]['servicos'], dat)

# ok
def serv_core(dipca, dat):
    return decomp(dipca, _decompo[0]['servicos_nucleo'], dat)

# ok
def duraveis(dipca, dat):
    return decomp(dipca, _decompo[0]['duraveis'], dat)

# problemas
def nduraveis(dipca, dat):
    return decomp(dipca, _decompo[0]['nao-duraveis'], dat)


# problemas
def semi(dipca, dat):
    return decomp(dipca, _decompo[0]['semiduraveis'], dat)


#ok
def monitorados(dipca, dat):
    return decomp(dipca, _decompo[0]['monitorados'], dat)


def livres(dipca, dat):
    p = _monitored_weights(dat)/100
    return 1/(1-p) * (dipca(dat) - p*monitorados(dat))


# problemas
# def comercializaveis(dat):
#     return decomp(_dipca, _decompo[0]['comercializaveis'], dat)


# problemas
# def ncomercializaveis(dat):
#     p = _tradables_weights(dat)/100
#     q = _monitored_weights(dat)/100
#     return 1/(1 - p - q)*(_ipca(dat) - p*comercializaveis(dat) - q*monitorados(dat))

# problemas
def core_ex2(dipca, dat):
    ex2 = decomp(dipca, _decompo[0]['ex2'], dat)
    p = weights(_ipca, _decompo[0]['ex2'], dat)/100
    return (1/(1 - p)) * (_ipca(dat) - p * ex2)


# consolidado
def decomposition(dipca, dat):
    consolidado = [_ipca, serv, serv_core, duraveis, monitorados]
    names = ['ipca', 'servicos', 'nucleo - servicos', 'duraveis', 'monitorados']
    return pd.DataFrame(np.array([c(dipca, dat) for c in consolidado]).reshape(1, len(names)),
                        index=[dat], columns=names)
