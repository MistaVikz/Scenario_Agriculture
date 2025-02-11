import pandas as pd

def load_data():
    ag = pd.read_excel('data/ag_data.xlsx',sheet_name='Data')
    scenario = pd.read_excel('data/ag_data.xlsx', sheet_name='Scenario Input')
    fert = pd.read_excel('data/ag_data.xlsx', sheet_name='Fertilizer Displacement Table')
    discvol = pd.read_excel('data/ag_data.xlsx', sheet_name='Discounts to Volume Table')
    pricing = pd.read_excel('data/ag_data.xlsx', sheet_name='Pricing Table')

    scenario['Emissions Permit Price'] = scenario['Emissions Permit Price'].astype('float64')
    
    return ag, scenario,fert, discvol, pricing