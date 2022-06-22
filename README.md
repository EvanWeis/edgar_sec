Distribution and use of the files within this repository take place under the creative commons license and are free to use and improve.

creator: Evan Weis
email: weis.evan.c@gmail.com

EDGAR_SEC is a small python library useful for downloading and analyzing annual and quarterly GAAP filings from publicly traded companies.

## CIK TO TICKER ##
ciktotiicker.py is a set of tools useful for fetching and mapping the SEC's official flat file containing the CIK number, Ticker symbol, and name of all publicly traded companies’ company. This is useful as CIK is used for requests to obtain company profiles and specific reports and is not commonly known. This python dictionary is the foundation for downloading company profiles and reports by the more commonly known Ticker Symbol rather than painstakingly looking for the CIK number on the SEC website.

Usage: 

get_raw_map() looks in the current working directory for an assets file and creates one if necessary. Once created the function makes a url GET request to the SEC url 'https://www.sec.gov/files/company_tickers.json' retrieving the json file and returns a python dictionary with all the information from the GET request. This file is stored in assets and referenced for future requests for the dictionary

format: {1: {cik_str: CIK, 'ticker': 'Ticker', 'title': 'Company name}}

## 

clean_map() takes the raw dictionary object obtained by get_raw_map() and returns a clean dictionary with CIK and Ticker symbol. The function takes two arguments, the raw dictionary and either 'cik', or 'ticker' to specify the key and value of the dictionary. Ticker is the standard key as it is commonly used as the locator for the CIK value when requesting additional company information.