from pandas.api.types import is_numeric_dtype

def valid_data(data,whichdf='Data'):
    if(whichdf == 'Data'):
        data_cols = {'Product Made', 'Baseline', 'Feedstock', 'Product Displaced', 'Standard',  'Waste Diversion TPA', 'Soil Sequestration TPA', 'Soil N2O TPA'}
    elif(whichdf == 'Scenario'):
        data_cols = {'N2O Present', 'Production (tonnes/year)', 'Fee Allowance Portion', 'NPV', 'Emissions Permit Price'}
    elif(whichdf == 'Nutriant'):
        data_cols = {'N','P','K','S','C','AS','MAP','DAP','AN','U', 'UN'}
    elif(whichdf == 'Discvol'):
        data_cols = {'Gold','Verra'}
    elif(whichdf == 'Pricing'):
        data_cols = {'Waste', 'Land Use', 'N2O (industrial)', 'Total', 'Total Volume', 'Gold Average', 'Verra Average', 'Offset Discrount', 'Transaction Cost'}
    else:
        raise ValueError('Invalid DataFrame. Must be either Data, Scenario, Nutriant, Discvol, or Pricing.')

    # Check Required Columns
    if(data_cols.issubset(data.columns) == False):
        raise ValueError(f'Invalid Columns. {data_cols} are required.')
    
    # Check for NaN
    if(whichdf != 'Discvol'):
        if(data.isnull().values.any()):
            raise ValueError('Data contains Null Values.')
    
def valid_scenario(n2o_present, production, fap, npv, epp):
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
    
def valid_numeric(data):
    # Check if all columns are numeric
    df_numeric = data.select_dtypes(include=["number"])

    # Verify if the DataFrame is fully numeric
    if (data.shape[1] != df_numeric.shape[1]):
        raise ValueError('Values in the Nutriant and/or Pricing Table must all be numeric.')
    
def valid_discvol(discvol):
    if(is_numeric_dtype(discvol['Gold']) != True or is_numeric_dtype(discvol['Verra']) != True):
        raise ValueError('The Gold/Verra Discounts to Volume rates must all be numeric.')

def valid_nutriant(nutriant):
    if(is_numeric_dtype(nutriant['N']) != True or is_numeric_dtype(nutriant['P']) != True or is_numeric_dtype(nutriant['K']) != True or is_numeric_dtype(nutriant['S']) != True or is_numeric_dtype(nutriant['C']) != True or is_numeric_dtype(nutriant['AS']) != True or is_numeric_dtype(nutriant['MAP']) != True or is_numeric_dtype(nutriant['DAP']) != True or is_numeric_dtype(nutriant['AN']) != True or is_numeric_dtype(nutriant['U']) != True or is_numeric_dtype(nutriant['UN']) != True):
        raise ValueError('The nutriant Table values must all be numeric.')
    
def valid_yearly_scenario(scenario):
    if(len(scenario) == 0 or len(scenario) > 10):
        raise ValueError('Please enter scenario input for between 1 and 10 years.')