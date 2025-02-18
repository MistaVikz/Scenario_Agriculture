import pandas as pd
import datetime
import os

def load_data():
    # Load Data
    ag = pd.read_excel('data/ag_data.xlsx',sheet_name='Data')
    scenario = pd.read_excel('data/ag_data.xlsx', sheet_name='Scenario Input')
    nutriant = pd.read_excel('data/ag_data.xlsx', sheet_name='Nutriant Table')
    discvol = pd.read_excel('data/ag_data.xlsx', sheet_name='Discounts to Volume Table')
    pricing = pd.read_excel('data/ag_data.xlsx', sheet_name='Pricing Table')

    # Format Data
    ag['Product Made'] = ag['Product Made'].astype('str')
    scenario['Emissions Permit Price'] = scenario['Emissions Permit Price'].astype('float64')
    nutriant['Product Made'] = nutriant['Product Made'].astype('str')
    nutriant.set_index('Product Made', inplace=True)
    discvol.set_index(['Waste Diversion','Location'], inplace=True)
    
    return ag, scenario, nutriant, discvol, pricing

def print_results(df, stat, stat_cols, year, f):
    # Get name and year
    scenario = {'MAX' :stat[stat_cols[4]].iloc[0], 'MIN': stat[stat_cols[5]].iloc[0], 'MEDIAN': stat[stat_cols[6]].iloc[0]}
    name = stat.columns.values[1].replace('(MAX VALUE)','')

    # Print MIN, MAX, MEDIAN
    print(f"{name}\tYear: {year+1}",file=f)
    for scen, row in scenario.items():
        if(scen=='MAX'):
            value = stat[stat_cols[1]].iloc[0]
        elif(scen=='MIN'):
            value = stat[stat_cols[2]].iloc[0]
        else:
            value = stat[stat_cols[3]].iloc[0]
  
        feedstock = df['Feedstock'].iloc[row]
        product_displaced = df['Product Displaced'].iloc[row]
        standard = df['Standard'].iloc[row]
        print(f"{scen}:\tFeedstock: {feedstock}\t Product Displaced: {product_displaced}\t Standard: {standard}\t Value: {value}",file=f)

    print('\n',file=f)

def create_output_folder():
    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")

    # Get the current directory of the script
    current_dir = os.path.dirname(__file__)

    # Construct the path to the output directory
    output_dir = os.path.join(current_dir, '..', 'output')

    # Create a new folder with the timestamp
    folder_name = os.path.join(output_dir, date_time)
    os.makedirs(folder_name, exist_ok=True)

    return folder_name
    
    