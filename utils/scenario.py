import pandas as pd

EMISSIONS_FACTORS = {'AS': {'5': 0.33, '10': 0.33, '15': 0.33, '20': 0.33}, 
                       'AN': {'5': 0.91, '10': 0.91, '15': 0.91, '20': 0.91}, 
                       'U': {'5': 0.45, '10': 0.45, '15': 0.45, '20': 0.45}, 
                       'UN': {'5': 0.57, '10': 0.57, '15': 0.57, '20': 0.57}} 
OFFSET_RATE = 0.08
OFFSET_DISCOUNT = 0.2
TRANSACTION_COST = 1.00
    
def get_scenario(scenario, row):
    """
    Retrieve scenario parameters from a DataFrame row.

    Args:
        scenario (pd.DataFrame): The DataFrame containing scenario data.
        row (int): The row index to retrieve data from.

    Returns:
        tuple: A tuple containing the following scenario parameters:
            - n2o_present (str): Indicator if N2O is present.
            - production (float): The production value.
            - fap (float): The fee allowance portion.
            - epp (float): The emissions permit price.
    """
    if row >= 0:
        n2o_present = scenario['N2O Present'].iloc[row]
        production = scenario['Production (tonnes/year)'].iloc[row]
        fap = scenario['Fee Allowance Portion'].iloc[row]
        epp = scenario['Emissions Permit Price'].iloc[row]
    return n2o_present, production, fap, epp

def get_fert_disp(p_made, p_disp, production, fap, epp, df_nutriant): # Combine with emissions_short IF all calculations are not needed.
    """
    Calculate fertilizer displacement values.

    Args:
        p_made (str): The product made.
        p_disp (str): The product displaced.
        production (float): The production value.
        fap (float): The fee allowance portion.
        epp (float): The emissions permit price.
        df_nutriant (pd.DataFrame): The DataFrame containing nutrient data.

    Returns:
        list: A list containing fertilizer displacement values.
    """
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
    """
    Calculate the emissions shortfall.

    Args:
        p_made (str): The product made.
        p_disp (str): The product displaced.
        production (float): The production value.
        fap (float): The fee allowance portion.
        epp (float): The emissions permit price.
        df_nutriant (pd.DataFrame): The DataFrame containing nutrient data.

    Returns:
        float: The emissions shortfall.
    """
    fert_disp = get_fert_disp(p_made, p_disp, production, fap, epp, df_nutriant)
    return fert_disp[6]

def get_discount(feedstock, baseline, standard, df_discvol):
    """
    Calculate the discount rate for a given feedstock, baseline, and standard.

    Args:
        feedstock (str): The feedstock type.
        baseline (str): The baseline type.
        standard (str): The standard type.
        df_discvol (pd.DataFrame): The DataFrame containing discount volume data.

    Returns:
        float: The discount rate.
    """
    if(feedstock != 'Land Use'):
        feedstock = feedstock.capitalize()    
    baseline = baseline.capitalize()
    standard = standard.capitalize()

    return  (1 - df_discvol.loc[(feedstock,baseline),standard]) 

def get_cash_per_tonnes_short(p_made, p_disp, production, fap, epp, df_nutriant):
    """
    Calculate the cash per tonnes shortfall.

    Args:
        p_made (str): The product made.
        p_disp (str): The product displaced.
        production (float): The production value.
        fap (float): The fee allowance portion.
        epp (float): The emissions permit price.
        df_nutriant (pd.DataFrame): The DataFrame containing nutrient data.

    Returns:
        float: The cash per tonnes shortfall.
    """
    fert_disp = get_fert_disp(p_made, p_disp, production, fap, epp, df_nutriant)
    return fert_disp[10]

def get_standard_prices(df_pricing):
    """
    Calculate standard prices based on pricing data.

    Args:
        df_pricing (pd.DataFrame): The DataFrame containing pricing data.

    Returns:
        list: A list containing standard prices for waste, land use, and N2O.
    """
    # Calculate Market Prices
    volume_average = round(df_pricing['Total'].loc[0] / df_pricing['Total Volume'].loc[0],2)
    waste_adjustment_average = round(df_pricing['Waste'].loc[0] / volume_average,2)
    land_use_adjustment_average = round(df_pricing['Land Use'].loc[0] / volume_average,2)
    n2o_adjustment_average = round(df_pricing['N2O (industrial)'].loc[0] / volume_average,2)
    
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

    return standard_prices
    
def get_pricing(pdisp, standard, standard_prices):
    """
    Retrieve the pricing for a given product displaced and standard.

    Args:
        pdisp (str): The product displaced.
        standard (str): The standard type.
        standard_prices (list): The list of standard prices.

    Returns:
        float: The pricing value.
    """
    if(pdisp == 'Waste'):
        if(standard == 'Gold'):
            return standard_prices[0]
        else:
            return standard_prices[1]
    elif(pdisp == 'Land Use'):
        if(standard == 'Gold'):
            return standard_prices[2]
        else:
            return standard_prices[3]
    else:
        if(standard == 'Gold'):
            return standard_prices[4]
        else:
            return standard_prices[5]

