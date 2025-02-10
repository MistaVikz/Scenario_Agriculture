import pandas as pd
from utils.validation import *
from utils.scenario import *

def main():
    # Get Data
    df_ag = pd.read_excel('data/ag_data.xlsx',sheet_name='Data')
    df_scenario = pd.read_excel('data/ag_data.xlsx', sheet_name='Scenario Input')

    # Validate Data
    check_data(df_ag,'Data')
    check_data(df_scenario,'Scenario')

    scenario_name, max_year, n2o_present, production, fap, npv = get_scenario(df_scenario,0)

    #print(df_ag.head())
    #print(df_ag.info())
    #print(df_scenario.head())
    #print(df_scenario.info())

if __name__ == '__main__':
    main()