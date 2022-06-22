#! /bin/env/python
############################################################################
# Python script to download, cache and map SEC CIK numbers to Stock Ticker #
############################################################################
# Author: Evan Weis
# e-mail weis.evan.c@gmail.com

import os, json
from urllib import request

_base_path = os.getcwd()

def get_raw_map():
    ''' 
    function to retrieve SEC EDGAR CIK to ticker json.
    returns a python dictionary in the format of 
    {1: {cik_str: CIK, 'ticker': 'Ticker', 'title': 'Company name}}
    '''
    if not os.path.isdir( _base_path + '\\assets'):
        os.mkdir(_base_path + '\\assets')
        print("Making directory to cache .json file {}...".format(_base_path))
        os.chdir(_base_path + '\\assets')
        print("Done.")
    else:
        os.chdir(_base_path + '\\assets')
    
    # check if a cached copy of cik_to_ticker exists
    if not os.path.exists("cik_to_ticker.json"): 
        # get the file from "https://www.sec.gov/files/company_tickers.json"
        cik_map = _get_json_map()
        # save json file in asset cache for future mapping
        with open('cik_to_ticker.json', 'w') as f:
            json.dump(cik_map, f)

        return cik_map
    else: 
        with open('cik_to_ticker.json', 'r') as f:
            cik_map = json.load(f)

        return cik_map

def clean_map(raw_map, order):
    '''
    function to reduce the complicated dict 
    to cik as the key and ticker as the value and
    returns the cleaned dict in the format {cik: ticker}
    '''
    clean_map = {}
    if order == 'cik':
        for i in raw_map: #iterate over raw_map and set cik to key and ticker to value
            clean_map[raw_map[i]['cik_str']] = raw_map[i]['ticker']

        return clean_map

    elif order == 'ticker':
        for i in raw_map: #iterate over raw_map and set cik to key and ticker to value
            clean_map[raw_map[i]['ticker']] = raw_map[i]['cik_str']

        return clean_map
    else: print("please specifiy a key")


def _get_json_map():
    company_tickers_url = r'https://www.sec.gov/files/company_tickers.json'
    try:
        print("getting sec flat file")
        response = request.urlopen(company_tickers_url)
        print ("Mapping...")
        cik_map = json.load(response)
    except:
        print("ERROR: failed to map cik to ticker...")

    return cik_map



def main():
    cik_to_ticker = get_raw_map()
    cleaned = clean_map(cik_to_ticker, 'cik')
    for k, v in cleaned.items():
        print(k,":",v)

if __name__=="__main__": main()