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
    
    # Calculate Standard Volumes Discount
    df_ag['Fertilizer Displacement TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Fertilizer Displacement TPA']
    df_ag['Waste Diversion TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Waste Diversion TPA'] * df_ag.apply(lambda x : get_discount(x['Feedstock'], x['Baseline'], x['Standard'], df_discvol) , axis=1)
    df_ag['Soil Sequestration TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Soil Sequestration TPA'] * df_ag.apply(lambda x : get_discount('Land Use', 'All', x['Standard'], df_discvol) , axis=1)
    if(n2o_present == 'Yes'):
        df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Soil N2O TPA'] * df_ag.apply(lambda x : get_discount('Land Use', 'All', x['Standard'], df_discvol) , axis=1)
    else:
        df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] = 0
    
    # Calculate Yearly Volumes Adjusted for Production Volumes
    df_ag['Fertilizer Displacement TPA (Yearly Adjusted Volumes)'] = df_ag['Fertilizer Displacement TPA'] * production / 100000
    df_ag['Waste Diversion TPA (Yearly Adjusted Volumes)'] = df_ag['Waste Diversion TPA'] * production / 100000
    df_ag['Soil Sequestration TPA (Yearly Adjusted Volumes)'] = df_ag['Soil Sequestration TPA'] * production / 100000
    df_ag['Soil N2O TPA (Yearly Adjusted Volumes)'] = df_ag['Soil N2O TPA'] * production / 100000
    df_ag['Total GHG TPA'] = df_ag['Fertilizer Displacement TPA (Adjusted for Standard Volumes Discount)'] + df_ag['Waste Diversion TPA (Adjusted for Standard Volumes Discount)'] + df_ag['Soil Sequestration TPA (Adjusted for Standard Volumes Discount)'] + df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)']
    
    # Calculate Yearly Prices
    standard_prices = get_standard_prices(df_pricing)
    cash_per_tonnes_short = get_cash_per_tonnes_short('5', 'AS', production, fap, epp, df_nutriant)

    df_ag['Fertilizer Displacement TPA Revenue ($/Year)'] = round(df_ag['Fertilizer Displacement TPA (Adjusted for Standard Volumes Discount)'] * cash_per_tonnes_short,2)
    df_ag['Waste Diversion TPA Revenue ($/Year)'] = round(df_ag['Waste Diversion TPA (Adjusted for Standard Volumes Discount)'] * df_ag.apply(lambda x : get_pricing('Waste',x['Standard'], standard_prices) , axis=1),2)
    df_ag['Soil Sequestration TPA Revenue ($/Year)'] = round(df_ag['Soil Sequestration TPA (Adjusted for Standard Volumes Discount)'] * df_ag.apply(lambda x : get_pricing('Land Use',x['Standard'], standard_prices) , axis=1),2)
    df_ag['Soil N2O TPA Revenue ($/Year)'] = round(df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] * df_ag.apply(lambda x : get_pricing('N2O (industrial)',x['Standard'], standard_prices) , axis=1),2)

    df_ag['Transaction Cost ($/Year)'] = round(production * TRANSACTION_COST,2)
    df_ag['NPV from GHG ($/Year)'] = round(df_ag['Fertilizer Displacement TPA Revenue ($/Year)'] + df_ag['Waste Diversion TPA Revenue ($/Year)'] + df_ag['Soil Sequestration TPA Revenue ($/Year)'] + df_ag['Soil N2O TPA Revenue ($/Year)'] - df_ag['Transaction Cost ($/Year)'],2)
    df_ag['NPV from GHG per Tonne ($/Year)'] = round(df_ag['NPV from GHG ($/Year)'] / production,2)
    
    print(df_ag.head())
    print(df_ag.info())

    # print(df_scenario.head())
    # print(df_scenario.info())

    #print(df_nutriant)
    #print(df_nutriant.info())

    #print(df_discvol)
    #print(df_discvol.info())

    #print(df_pricing)
    #print(df_pricing.info())

if __name__ == '__main__':
    main()