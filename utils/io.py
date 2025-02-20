import pandas as pd
import numpy_financial as npf
import seaborn as sns
import matplotlib.pyplot as plt
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

def filter_data(df, f_filter, p_filter, s_filter):
    f_string = ""
    if (f_filter != 'All'):
        df = df[df['Feedstock'] == f_filter]
        f_string += f"{f_filter}_"
    if (p_filter != 'All'):
        df = df[df['Product Displaced'] == p_filter]
        f_string += f"{p_filter}_"
    if (s_filter != 'All'):
        df = df[df['Standard'] == s_filter]
        f_string += f"{s_filter}_"

    if(f_string == ""):
        f_string = "NoFilter_"
    
    return df, f_string

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

def create_output_folder(f_string):
    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    folder_string = f"{f_string}{date_time}"


    # Get the current directory of the script
    current_dir = os.path.dirname(__file__)

    # Construct the path to the output directory
    output_dir = os.path.join(current_dir, '..', 'output')

    # Create a new folder with the timestamp and filters
    folder_name = os.path.join(output_dir, folder_string)
    os.makedirs(folder_name, exist_ok=True)

    return folder_name
    
def print_npv_results(npv_rate, values, yearly_production, output_folder, scen, f):
    # Calculate NPV Results
    npv = round(npf.npv(npv_rate, values),2)
    npv_fac_per_prod = round(npv / sum(yearly_production),2)
    net_pot_per_prod = round(sum(values) / sum(yearly_production),2)

    print(f"{scen}:\tNPV: {npv}\tNPV By Facility Size: {npv_fac_per_prod}\tNet Potential By Total Production: {net_pot_per_prod}",file=f)

def plot_graphs(years, max, min, median, output_folder, type, f_string):
    # Organize yearly scenario data
    data = pd.DataFrame({'year': years,
                        'MAX': max,
                        'MIN': min,
                        'MEDIAN' : median})
    
    # Format filters for plot titles.
    if(f_string == "NoFilter_"):
        f_title = "All Data"
    else:
        f_title = f_string[:-1]
        f_title = str.replace(f_title,"_","/")

    # Plot Scenario Graph
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(10,5))
    sns.lineplot(x='year', y='value', hue='variable', 
             data=pd.melt(data, ['year']),
             palette=['red', 'blue', 'purple'])
    
    plt.xlabel('Year')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    if(type == 'GHG'):
        plt.ylabel('GHG Tonnes')
        plt.title(f'GHG Tonnes per Year ({f_title})')
    elif(type == 'NPV'):
        plt.ylabel('Net Potential $')
        plt.title(f'Net Potential $ per Year ({f_title})')
    
    plt.savefig(f"{output_folder}/{f_string}_{type}_Plot.png", bbox_inches='tight')