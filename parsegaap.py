#! /usr/env/python3
# python module for parsing gaap json from sec EDGAR
# functions defined here are designed to work with Company Facts object
# obtained with Company.get_facts() method from companyprofile.py

from companyprofile import Company

def analyze(company: dict, fy: str = 'current'):
    pass

def balance_sheet(company: dict, fy: str = 'current'):
    pass

def income_statement(company: dict, fy: str = 'current'):
    pass

def cash_flow(company: dict, fy: str = 'current'):
    pass


def main():

    plug = Company('plug')
    plug_facts = plug.get_facts()
    print(type(plug_facts))

if __name__=="__main__": main()