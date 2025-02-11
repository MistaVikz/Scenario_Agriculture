from utils.validation import *
from utils.scenario import *
from utils.io import *

def main():
    # Get Data
    df_ag, df_scenario, df_nutriant, df_discvol, df_pricing = load_data()

    # Validate Data
    valid_data(df_ag,'Data')
    valid_data(df_scenario,'Scenario')
    valid_data(df_nutriant,'Nutriant')
    valid_data(df_discvol,'Discvol')
    valid_nutriant(df_nutriant)
    valid_numeric(df_pricing)
    valid_discvol(df_discvol)

    # Get and validate scenario.
    scenario_name, max_year, n2o_present, production, fap, npv, epp = get_scenario(df_scenario,0)
    valid_scenario(scenario_name,max_year,n2o_present,production,fap,npv,epp)
    
    # Calculate Fertilizer Displacement For 100000 TPA Production
    df_ag['Fertilizer Displacement TPA']=df_ag.apply(lambda x : get_emissions_short(x['Product Made'], x['Product Displaced'], production, fap, epp, df_nutriant) , axis=1)
    
    print(df_ag.head())
    print(df_ag.info())

    #print(df_scenario.head())
    #print(df_scenario.info())

    #print(df_nutriant)
    #print(df_nutriant.info())

    #print(df_discvol)
    #print(df_discvol.info())

    #print(df_pricing)
    #print(df_pricing.info())

if __name__ == '__main__':
    main()