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

def print_results(df, stat, stat_type):
      
    feedstock = df['Feedstock'].iloc[stat]
    product_displaced = df['Product Displaced'].iloc[stat]
    standard = df['Standard'].iloc[stat]

    print(f" {stat_type}\tFeedstock: {feedstock}\t Product Displaced: {product_displaced}\t Standard: {standard}")
