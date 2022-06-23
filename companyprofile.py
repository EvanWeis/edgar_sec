#! /bin/env/python
# python module for downloading a public companies profile 

# Author: Evan Weis
# e-mail weis.evan.c@gmail.com 


from urllib import request
import json, os, tickertocik

class Company:
    def __init__(self, ticker: str = None, cik: str = None) -> None:
        self.clean_map = tickertocik.
        if not ticker == None: # if ticker is provided, assign and get cik
            self.ticker = ticker
            self.cik = self._map_tickertocik(self.ticker)

        if not cik == None: # if cik is provided, assign and get ticker
            if len(cik) < 10:
              self.leading_zeros = '0' *  (10 - len(cik))
              self.cik = self.leading_zeros + cik  
            elif len(cik) > 10:
                print('ERROR: Invalid CIK, expecting CIK 10 character long')
            else:
             self.cik = cik

            self.ticker = self._map_tickertocik(self.cik)

        self.company_url = self._build_url()

    def _map_tickertocik(self):
        pass

    def _build_url(self):
        self.base_url = r'https://data.sec.gov/api/xbrl/companyfacts/'  
        self.file_type = r'.json'

        if self.cik:
            self.request_url = self.base_url + 'CIK' + self.cik + self.file_type
            return self.request_url

    def profile(self):
        pass


def main():
    pass


if __name__=="__main__": main()
