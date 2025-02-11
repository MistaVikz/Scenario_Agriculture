import pandas as pd

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

def get_fert_disp(p_made, p_disp, production, fap, epp, df_nutriant):
    # Calculate Fertilizer Displacement Values
    emission_factor = EMISSIONS_FACTORS[p_disp][p_made]
    fert_disp_factor = df_nutriant.loc[p_made,p_disp]
    disp_production = production * fert_disp_factor
    fee_allowance = fap * disp_production
    net_req_cover = disp_production - fee_allowance
    emissions_short = net_req_cover * emission_factor
    offsets_used = emissions_short * OFFSET_RATE
    allowances_needed = emissions_short- offsets_used
    value_of_displacement = (offsets_used * epp * (1 - OFFSET_DISCOUNT)) + (epp * allowances_needed)
    cash_per_tonnes_short = value_of_displacement / emissions_short

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

