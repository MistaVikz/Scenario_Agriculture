from pandas.api.types import is_numeric_dtype

def valid_data(data,whichdf='Data'):
    """
    Validate the data in the DataFrame based on the specified type.

    Args:
        data (pd.DataFrame): The DataFrame to validate.
        whichdf (str): The type of DataFrame ('Data', 'Scenario', 'Nutriant', 'Discvol', 'Pricing').

    Raises:
        ValueError: If the DataFrame does not contain the required columns or contains null values.
    """
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

def valid_npv(npv):
    """
    Validate the NPV value.

    Args:
        npv (float): The NPV value to validate.

    Raises:
        ValueError: If the NPV value is not between 0 and 1.
    """
    if(npv < 0 or npv > 1):
        raise ValueError('NPV must be between 0 and 1.')

def valid_yearly_scenario(scenario):
    """
    Validate the yearly scenario data.

    Args:
        scenario (pd.DataFrame): The DataFrame containing the scenario data.

    Raises:
        ValueError: If the scenario data does not contain between 1 and 10 years.
    """
    if(len(scenario) == 0 or len(scenario) > 10):
        raise ValueError('Please enter scenario input for between 1 and 10 years.')

def valid_scenario(n2o_present, production, fap, epp):
    """
    Validate the scenario parameters.

    Args:
        n2o_present (str): Indicator if N2O is present ('Yes' or 'No').
        production (float): The production value.
        fap (float): The fee allowance portion.
        epp (float): The emissions permit price.

    Raises:
        ValueError: If any of the parameters are invalid.
    """
    if(n2o_present.lower() != "yes" and n2o_present.lower() != 'no'):
        raise ValueError('N2O Present must be either Yes or No.')
    if(production <= 0):
        raise ValueError('Production must be >= 0.')
    if(fap < 0 or fap > 1):
        raise ValueError('Fee Allowance Portion must be between 0 and 1.')
    if(epp < 0):
        raise ValueError('Emissions Permit Price must be a positive value.')
    
def valid_numeric(data):
    """
    Validate that all columns in the DataFrame are numeric.

    Args:
        data (pd.DataFrame): The DataFrame to validate.

    Raises:
        ValueError: If any column in the DataFrame is not numeric.
    """
    # Check if all columns are numeric
    df_numeric = data.select_dtypes(include=["number"])

    # Verify if the DataFrame is fully numeric
    if (data.shape[1] != df_numeric.shape[1]):
        raise ValueError('Values in the Nutriant and/or Pricing Table must all be numeric.')
    
def valid_discvol(discvol):
    """
    Validate the discount volume data.

    Args:
        discvol (pd.DataFrame): The DataFrame containing the discount volume data.

    Raises:
        ValueError: If the Gold or Verra columns are not numeric.
    """
    if(is_numeric_dtype(discvol['Gold']) != True or is_numeric_dtype(discvol['Verra']) != True):
        raise ValueError('The Gold/Verra Discounts to Volume rates must all be numeric.')

def valid_nutriant(nutriant):
    """
    Validate the nutrient data.

    Args:
        nutriant (pd.DataFrame): The DataFrame containing the nutrient data.

    Raises:
        ValueError: If any column in the nutrient data is not numeric.
    """
    if(is_numeric_dtype(nutriant['N']) != True or is_numeric_dtype(nutriant['P']) != True or is_numeric_dtype(nutriant['K']) != True or is_numeric_dtype(nutriant['S']) != True or is_numeric_dtype(nutriant['C']) != True or is_numeric_dtype(nutriant['AS']) != True or is_numeric_dtype(nutriant['MAP']) != True or is_numeric_dtype(nutriant['DAP']) != True or is_numeric_dtype(nutriant['AN']) != True or is_numeric_dtype(nutriant['U']) != True or is_numeric_dtype(nutriant['UN']) != True):
        raise ValueError('The nutriant Table values must all be numeric.')
    
