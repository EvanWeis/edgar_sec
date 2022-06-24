#! /bin/env/python
# python module for downloading a public companies profile 

# Author: Evan Weis
# e-mail weis.evan.c@gmail.com 


import requests
import json, os, tickertocik

class Company:
    def __init__(self, ticker: str = None, cik: str = None, uagent: str = 'Mozilla/5.0') -> None:
        self.cik = None
        self.ticker = None
        self.uagent = uagent #declare an optional User Agent for SEC scripted request complaince

        if not ticker == None: # if ticker is provided, assign and get cik
            self.ticker_map = tickertocik.get_clean_map('ticker') # create ticker map
            if ticker.upper() not in self.ticker_map.keys(): # validate ticker
                print('ERROR: Ticker not found in map, \nPlease check to make sure your Ticker is correct')
            else:
                self.ticker = ticker.upper()
                self.cik = self._map_tickertocik() # map and assign cik from ticker

        if not cik == None: # if cik is provided, assign and get ticker
            self.cik_map = tickertocik.get_clean_map('cik') # create cik map
            if len(cik) < 10: #check length and format if necessary
                self.leading_zeros = '0' *  (10 - len(cik))
                cik = self.leading_zeros + cik 
                if cik not in self.cik_map.keys(): #validate cik
                    print('ERROR: CIK not found in map, \nPlease check to make sure your CIK is correct')
                else:
                    self.cik = cik
                    self.ticker = self._map_tickertocik()
            elif len(cik) > 10:
                print('ERROR: Invalid CIK, expecting CIK 10 character long')
            elif cik not in self.cik_map.keys():
                print('ERROR: CIK not found in map, \nPlease check to make sure your CIK is correct')
            else:
                self.cik = cik
                self.ticker = self._map_tickertocik() # map and assign ticker from cik

        self.company_url = self._build_url() #build a url for requets

    def _map_tickertocik(self) -> str:
        if self.ticker == None:
            self.ticker = self.cik_map[self.cik]
            return self.ticker
        elif self.cik == None:
            self.cik = self.ticker_map[self.ticker]
            return self.cik
        else:
            print("ERROR: failed to map values")

    def _build_url(self) -> str:
        self.base_url = 'https://data.sec.gov/submissions/'  
        self.file_type = '.json'

        if self.cik:
            self.request_url = self.base_url + 'CIK' + self.cik + self.file_type
            return self.request_url
        else:
            print("ERROR: url failed to build")

    def profile(self) -> dict:

        self.header = {"User-agent": self.uagent}
        self.response = requests.get(self.request_url, headers = self.header)
        self.data = self.response.json()

        self.company_profile = {
            'Name': self.data['name'],
            'CIK': self.cik,
            'Tickers': self.data['tickers'],
            'SIC': self.data['sic'],
            'SIC Description': self.data['sicDescription'],
        }
        return self.company_profile

    def get_recent(self) -> dict:
        try:
            if not self.data:
                self.profile()
                self.recent_filings = {
                    'Accession Number' : self.data['filings']['recent']['accessionNumber']
                }
            else:
                self.recent_filings = {
                    'Accession Number' : self.data['filings']['recent']['accessionNumber']
                }

            return self.recent_filings
        except KeyError as e:
            print('An ERROR Occured')
            print(e)
        

def main():
    ck = Company(cik = '320193')
    print(ck.ticker)
    print(ck.cik)
    print(ck.company_url)

    print('\n')

    aapl = Company(ticker = 'aapl')
    print(aapl.ticker)
    print(aapl.cik)
    print(aapl.company_url)
    print('\n')
    Apple_Profile = aapl.profile()
    for k, v in Apple_Profile.items():
        print(k,':',v)
    print('\n') 

    Apple_Recent = aapl.get_recent()
    for i in Apple_Recent['Accession Number']:
        print(i)


if __name__=="__main__": main()
