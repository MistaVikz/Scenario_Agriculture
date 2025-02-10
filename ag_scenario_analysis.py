import pandas as pd
from utils.validation import *

df_ag = pd.read_excel('data/ag_data.xlsx',sheet_name='Data')
df_scenario = pd.read_excel('data/ag_data.xlsx', sheet_name='Scenario Input')

check_data(df_ag,'Data')
check_data(df_scenario,'Scenario')


#print(df_ag.head())
#print(df_ag.info())
#print(df_scenario.head())
#print(df_scenario.info())