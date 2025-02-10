import pandas as pd
from utils.validation import *
from utils.scenario import *
from utils.calculation import *
from utils.io import *

def main():
    # Get Data
    df_ag, df_scenario, df_fert = load_data()

    # Validate Data
    check_data(df_ag,'Data')
    check_data(df_scenario,'Scenario')
    check_data(df_fert,'Fert')
    valid_fert(df_fert)

    # Get and validate scenario.
    scenario_name, max_year, n2o_present, production, fap, npv, epp = get_scenario(df_scenario,0)
    valid_scenario(scenario_name,max_year,n2o_present,production,fap,npv,epp)
    
    # Fertilizer Displacement
    df_ag = calc_fert_disp(df_ag)
    
    #print(df_ag.head())
    #print(df_ag.info())

    #print(df_scenario.head())
    #print(df_scenario.info())

    print(df_fert)
    print(df_fert.info())

if __name__ == '__main__':
    main()