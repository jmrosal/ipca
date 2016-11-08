######################################################################
# sets path to send data to
# intial date: 21/10/2106
######################################################################
import json

def data_path():
    '''
    sends path of directory of where the data should be sent to
    output:
    - str: 
    '''
    _f_dir = "/home/user/Documents/BGC/research/caminhos_bgc.json"
    return json.loads(open(_f_dir).read())['data'].encode('utf-8')
