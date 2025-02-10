import pandas as pd

def get_scenario(scenario, row):
    if row >= 0:
        scenario_name = scenario['Scenario Name'].iloc[row]
        max_year = scenario['Number of Years'].iloc[row]
        n2o_present = scenario['N2O Present'].iloc[row]
        production = scenario['Production (tonnes/year)'].iloc[row]
        fap = scenario['Fee Allowance Portion'].iloc[row]
        npv = scenario['NPV'].iloc[row]
        epp = scenario['Emissions Permit Price'].iloc[row]
    return scenario_name, max_year, n2o_present, production, fap, npv, epp
