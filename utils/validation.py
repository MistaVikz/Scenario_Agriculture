import pandas as pd

def check_data(data,whichdf='Data'):
    if(whichdf == 'Data'):
        data_cols = {'Case Number', 'Product Made', 'Baseline', 'Feedstock', 'Product Displaced', 'Standard',  'Waste Diversion TPA', 'Soil Sequestration TPA', 'Soil N2O TPA'}
    elif(whichdf == 'Scenario'):
        data_cols = {'Scenario Name', 'Number of Years', 'N2O Present', 'Production (tonnes/year)', 'Fee Allowance Portion', 'NPV', 'Emissions Permit Price'}
    else:
        data_cols = {'N','P','K','S','C','Ratio to AS','Ratio to MAP','Ratio to DAP','Ratio to AN','Ratio to Urea', 'Ratio to UAN'}

    # Check Required Columns
    if(data_cols.issubset(data.columns) == False):
        raise ValueError(f'Invalid Columns. {data_cols} are required.')
    
    # Check for NaN
    if(data.isnull().values.any()):
        raise ValueError('Data contains Null Values.')
    
def valid_scenario(scenario_name, max_year, n2o_present, production, fap, npv, epp):
    if(len(scenario_name) == 0):
        raise ValueError('Scenario Name required.')
    if(max_year < 1 or max_year > 10):
        raise ValueError('Number of Years must be between 1 and 10.')
    if(n2o_present.lower() != "yes" and n2o_present.lower() != 'no'):
        raise ValueError('N2O Present must be either Yes or No.')
    if(production <= 0):
        raise ValueError('Production must be >= 0.')
    if(fap < 0 or fap > 1):
        raise ValueError('Fee Allowance Portion must be between 0 and 1.')
    if(npv < 0 or npv > 1):
        raise ValueError('NPV must be between 0 and 1.')
    if(epp < 0):
        raise ValueError('Emissions Permit Price must be a positive value.')
    
def valid_fert(fert):
    # Check if all columns are numeric
    df_numeric = fert.select_dtypes(include=["number"])

    # Verify if the DataFrame is fully numeric
    if (fert.shape[1] != df_numeric.shape[1]):
        raise ValueError('Values in the Fertilizer Displacement Table must all be numeric.')
    