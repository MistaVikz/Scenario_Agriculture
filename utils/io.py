import pandas as pd

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

    scenario = {'MAX' :stat[stat_cols[4]].iloc[0], 'MIN': stat[stat_cols[5]].iloc[0], 'MEDIAN': stat[stat_cols[6]].iloc[0]}
    name = stat.columns.values[1].replace('(MAX VALUE)','')

    print(f"{name}\tYear: {year}",file=f)
    for scen, row in scenario.items():
        feedstock = df['Feedstock'].iloc[row]
        product_displaced = df['Product Displaced'].iloc[row]
        standard = df['Standard'].iloc[row]
        print(f"{scen}\tFeedstock: {feedstock}\t Product Displaced: {product_displaced}\t Standard: {standard}",file=f)

    print('\n',file=f)
    
    