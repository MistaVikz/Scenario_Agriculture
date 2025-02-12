EMISSIONS_FACTORS = {'AS': {'5': 0.33, '10': 0.33, '15': 0.33, '20': 0.33}, 
                       'AN': {'5': 0.91, '10': 0.91, '15': 0.91, '20': 0.91}, 
                       'U': {'5': 0.45, '10': 0.45, '15': 0.45, '20': 0.45}, 
                       'UN': {'5': 0.57, '10': 0.57, '15': 0.57, '20': 0.57}} 
OFFSET_RATE = 0.08
OFFSET_DISCOUNT = 0.2
    
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

def get_fert_disp(p_made, p_disp, production, fap, epp, df_nutriant): # Combine with emissions_short IF all calculations are not needed.
    # Calculate Fertilizer Displacement Values
    emission_factor = EMISSIONS_FACTORS[p_disp][p_made]
    fert_disp_factor = df_nutriant.loc[p_made,p_disp]
    disp_production = production * fert_disp_factor
    fee_allowance = fap * disp_production
    net_req_cover = disp_production - fee_allowance
    emissions_short = net_req_cover * emission_factor
    offsets_used = emissions_short * OFFSET_RATE
    allowances_needed = emissions_short- offsets_used
    value_of_displacement = round((offsets_used * epp * (1 - OFFSET_DISCOUNT)) + (epp * allowances_needed),2)
    cash_per_tonnes_short = round(value_of_displacement / emissions_short,2)

    # Return Fertilizer Displacement Values
    fert_disp = []
    fert_disp.append(emission_factor)
    fert_disp.append(production)
    fert_disp.append(fert_disp_factor)
    fert_disp.append(disp_production)
    fert_disp.append(fee_allowance)
    fert_disp.append(net_req_cover)
    fert_disp.append(emissions_short)
    fert_disp.append(offsets_used)
    fert_disp.append(allowances_needed)
    fert_disp.append(value_of_displacement)
    fert_disp.append(cash_per_tonnes_short)
    return fert_disp

def get_emissions_short(p_made, p_disp, production, fap, epp, df_nutriant):
    fert_disp = get_fert_disp(p_made, p_disp, production, fap, epp, df_nutriant)
    return fert_disp[6]

def get_discount(feedstock, baseline, standard, df_discvol):
    if(feedstock != 'Land Use'):
        feedstock = feedstock.capitalize()    
    baseline = baseline.capitalize()
    standard = standard.capitalize()

    return  (1 - df_discvol.loc[(feedstock,baseline),standard]) 

def get_market_prices(df_pricing):
    # Calculate Market Prices
    volume_average = round(df_pricing['Total'].loc[0] / df_pricing['Total Volume'].loc[0],2)
    waste_adjustment_average = round(df_pricing['Waste'].loc[0] / volume_average,2)
    land_use_adjustment_average = round(df_pricing['Land Use'].loc[0] / volume_average,2)
    n2o_adjustment_average = round(df_pricing['N2O (industrial)'].loc[0] / volume_average,2)
    
    # Return Market Prices
    market_prices = []
    market_prices.append(volume_average)
    market_prices.append(waste_adjustment_average)
    market_prices.append(land_use_adjustment_average)
    market_prices.append(n2o_adjustment_average)    

    # Calculate Standard Prices
    waste_gold_price = round(df_pricing['Gold Average'].loc[0] * waste_adjustment_average,2)
    waste_verra_price = round(df_pricing['Verra Average'].loc[0] * waste_adjustment_average,2)
    land_use_gold_price = round(df_pricing['Gold Average'].loc[0] * land_use_adjustment_average,2)
    land_use_verra_price = round(df_pricing['Verra Average'].loc[0] * land_use_adjustment_average,2)
    n2o_gold_price = round(df_pricing['Gold Average'].loc[0] * n2o_adjustment_average,2)
    n2o_verra_price = round(df_pricing['Verra Average'].loc[0] * n2o_adjustment_average,2)
    
    # Return Standard Prices
    standard_prices = []
    standard_prices.append(waste_gold_price)
    standard_prices.append(waste_verra_price)
    standard_prices.append(land_use_gold_price)
    standard_prices.append(land_use_verra_price)
    standard_prices.append(n2o_gold_price)
    standard_prices.append(n2o_verra_price)

    return market_prices, standard_prices
    