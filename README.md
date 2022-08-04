# SEC EDGAR PYTHON

EDGAR_SEC is a small python library useful for downloading and analyzing annual and quarterly GAAP filings from publicly traded companies.

## Ticker to CIK 

**ciktotiicker.py** is a tool which leverages the SEC's official flat file containing the CIK number, Ticker symbol, and name of all publicly traded companies in the EDGAR database. 

Knowledge of CIK is much less common than Tickers when considering stock research and analysis, so having a convient way to access company information and filings using Ticker symbols is a nice thing to have.

The script has two functions, `get_raw_map` which is the workhorse function relied upon by others to make a local diretory and cache a copy of *cik_to_ticker.json* to reduce repeat requests to the SEC server.

`get_clean_map` takes one argument of either *ticker8 or *cik* which defines the dictionary key. Preference is up to the user. Although ticker is the standard usage as it is commonly used to look up CIK.

`get_raw_map` Usage:

```python
raw = get_raw_map()
```
Output format:

```python
{1: {'cik_str': 'CIK', 'ticker': 'Ticker', 'title': 'Company name'}}
```

`get_clean_map` Usage:

```python
clean = get_clean_map('ticker')
clean = get_clean_map('cik')
```

Output format:

```python
{'ticker': 'cik'}
{'cik': 'ticker'}
```


## Company Profile

**companyprofile.py** is comprised of a `Company` class with several methods for retreiving the basic profile, the recent filings, and the company facts (the financial details of every filing submitted to the SEC) notabliy including 10-K and 10-Q financials.

Usage:

```python
plug = Company(ticker='plug') #class instance of Company

plug.profile() #profile method returns basic info and last close price

plug.get_recent() #get_recent method returns dict of all recent filings

plug.get_facts() #get_facts method returns all SEC company facts
```

For more information on how the API works and what is included in the EDGAR database visit the SECs [website](https://www.sec.gov/edgar/sec-api-documentation)

**NOTE:**

The get_bulk method is underdevelopment and downloads the .zip files of all company [facts](https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip) and [submissions](https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip) These files are 7 Gb and 13 Gb respectively and can take a lot of time to download.