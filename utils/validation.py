import pandas as pd

def check_data(data,whichdf='Data'):

    if(whichdf == 'Data'):
        data_cols = {'Case Number', 'Product Made', 'Baseline', 'Feedstock', 'Product Displaced', 'Standard', 'Fertilizer Displacement TPA',  'Waste Diversion TPA', 'Soil Sequestration TPA', 'Soil N2O TPA'}
    else:
        data_cols = {'Scenario Name', 'Number of Years', 'N2O Present', 'Production (tonnes/year)', 'Fee Allowance Portion', 'NPV'}
    
    # Check Required Columns
    if(data_cols.issubset(data.columns) == False):
        raise ValueError(f'Invalid Columns. {data_cols} are required.')
    
    # Check for NaN
    if(whichdf == 'Data'):
        data = data.drop(columns=['Fertilizer Displacement TPA'])
    if(data.isnull().values.any()):
        raise ValueError('Data contains Null Values.')
    
