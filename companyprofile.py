#! /bin/env/python
# python module for downloading a public companies profile 

# Author: Evan Weis
# e-mail weis.evan.c@gmail.com 


import requests, tickertocik
from bs4 import BeautifulSoup

def get_bulk(req: str, uagent: str = 'Mozilla/5.0') -> None:
    facts_url = 'https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip'
    submissions_url = 'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip '
    header = {'User-agent': uagent}

    if req.lower() == 'facts':
        print("Fecthing facts... This download is large and may take some time")
        r = requests.get(facts_url, headers=header)
        filename = 'EDGARcomapnyfacts.zip'
        
    elif req.lower() == 'submissions':
        print("Fecthing Submissions... This dodwnload is large and may take some time")
        r = requests.get(submissions_url, headers=header)
        filename = 'EDGARsubmissions.zip'
    else:
        print("ERROR: {} is not a valid argument. expecting 'facts' or 'submissions'")
    
    zfile = open(filename, 'wb')
    zfile.write(r)
    zfile.close()



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

    def _get_last_close(self) -> str:
        self.price_url = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(self.ticker, self.ticker)
        self.html_doc = requests.get(self.price_url, headers=self.header)
    
        self.header = {'User-agent': self.uagent}
        self.response = requests.get(self.price_url, headers=self.header)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.last_close = self.soup.find_all('td', attrs = {'data-test':'PREV_CLOSE-value'})[0].string
        return self.last_close

    
    def _map_tickertocik(self) -> str:
        if self.ticker == None:
            self.ticker = self.cik_map[self.cik]
            return self.ticker
        elif self.cik == None:
            self.cik = self.ticker_map[self.ticker]
            return self.cik
        else:
            print("ERROR: failed to map values")

    def _build_url(self, req: str) -> str: #url factory for request objects
        self.submissions_base = 'https://data.sec.gov/submissions/' 
        self.facts_base = 'https://data.sec.gov/api/xbrl/companyfacts/' 
        self.file_type = '.json'

        if req.lower() == 'submissions':
            if self.cik:
                self.request_url = self.submissions_base + 'CIK' + self.cik + self.file_type
                return self.request_url
        elif req.lower() == 'facts':
            if self.cik:
                self.request_url = self.facts_base + 'CIK' + self.cik + self.file_type
                return self.request_url
        else:
            print("ERROR: {} url failed to build".format(req))

    def profile(self) -> dict:
        self.r_url = self._build_url('submissions')
        self.header = {"User-agent": self.uagent}
        self.response = requests.get(self.r_url, headers = self.header)
        self.subs = self.response.json()

        self.company_profile = {
            'Name': self.subs['name'],
            'CIK': self.cik,
            'Tickers': self.subs['tickers'],
            'SIC': self.subs['sic'],
            'SIC Description': self.subs['sicDescription'],
            'Previous Close': '$' + self._get_last_close()
        }
        return self.company_profile

    def get_recent(self) -> dict:
        try:
            if not self.subs:
                self.profile()
                self.recent_filings = {
                    'Accession Number' : self.subs['filings']['recent']['accessionNumber']
                }
            else:
                self.recent_filings = {
                    'Accession Number' : self.subs['filings']['recent']['accessionNumber']
                }

            return self.recent_filings
        except KeyError as e:
            print('An ERROR Occured')
            print(e)

    def get_facts(self) -> dict:
        self.r_url = self._build_url('facts')
        self.header = {"User-agent": self.uagent}
        self.response = requests.get(self.r_url, headers = self.header)
        self.facts = self.response.json()

        return self.facts   
    
def main():
    plug = Company('plug')
    print(plug.profile())
    print(plug.get_facts())
if __name__=="__main__": main()
