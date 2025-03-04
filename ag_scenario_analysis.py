import argparse
from utils.validation import *
from utils.scenario import *
from utils.io import *
from utils.statistics import *

def main(f_filter = 'All', p_filter = 'All', s_filter = 'All', npv = 0.1):
    # Get Data
    df_ag, df_scenario, df_nutriant, df_discvol, df_pricing = load_data()

    # Validate Data
    valid_data(df_ag,'Data')
    valid_data(df_scenario,'Scenario')
    valid_data(df_nutriant,'Nutriant')
    valid_data(df_discvol,'Discvol')
    valid_nutriant(df_nutriant)
    valid_numeric(df_pricing)
    valid_discvol(df_discvol)
    valid_npv(npv)

    # Filter Based on Command Line arguments
    df_ag, f_string = filter_data(df_ag, f_filter, p_filter, s_filter)
    df_ag =df_ag.reset_index()

    # Build empty statistics dataframes
    fert_vol_columns = ['Year', 'Fertilizer Displacement TPA (MAX VALUE)', 'Fertilizer Displacement TPA (MIN VALUE)', 'Fertilizer Displacement TPA (MEDIAN VALUE)', 
                     'Fertilizer Displacement TPA (MAX INDEX)', 'Fertilizer Displacement TPA (MIN INDEX)', 'Fertilizer Displacement TPA (MEDIAN INDEX)']                     
    df_fert_vol = pd.DataFrame(columns=fert_vol_columns)
    waste_vol_columns =  ['Year', 'Waste Diversion TPA (MAX VALUE)', 'Waste Diversion TPA (MIN VALUE)', 'Waste Diversion TPA (MEDIAN VALUE)',
                        'Waste Diversion TPA (MAX INDEX)', 'Waste Diversion TPA (MIN INDEX)', 'Waste Diversion TPA (MEDIAN INDEX)']
    df_waste_vol = pd.DataFrame(columns=waste_vol_columns)
    soil_vol_columns =  ['Year', 'Soil Sequestration TPA (MAX VALUE)', 'Soil Sequestration TPA (MIN VALUE)', 'Soil Sequestration TPA (MEDIAN VALUE)',
                        'Soil Sequestration TPA (MAX INDEX)', 'Soil Sequestration TPA (MIN INDEX)', 'Soil Sequestration TPA (MEDIAN INDEX)']
    df_soil_vol = pd.DataFrame(columns=soil_vol_columns)
    n2o_vol_columns = ['Year', 'Soil N2O TPA (MAX VALUE)', 'Soil N2O TPA (MIN VALUE)', 'Soil N2O TPA (MEDIAN VALUE)',
                        'Soil N2O TPA (MAX INDEX)', 'Soil N2O TPA (MIN INDEX)', 'Soil N2O TPA (MEDIAN INDEX)']
    df_n2o_vol = pd.DataFrame(columns=n2o_vol_columns)
    ghg_vol_columns = ['Year', 'Total GHG TPA (MAX VALUE)', 'Total GHG TPA (MIN VALUE)', 'Total GHG TPA (MEDIAN VALUE)',
                        'Total GHG TPA (MAX INDEX)', 'Total GHG TPA (MIN INDEX)', 'Total GHG TPA (MEDIAN INDEX)']
    df_ghg_vol = pd.DataFrame(columns=ghg_vol_columns)
    fert_rev_columns = ['Year', 'Fertilizer Displacement TPA Revenue ($/Year) (MAX VALUE)', 'Fertilizer Displacement TPA Revenue ($/Year) (MIN VALUE)', 'Fertilizer Displacement TPA Revenue ($/Year) (MEDIAN VALUE)',
                        'Fertilizer Displacement TPA Revenue ($/Year) (MAX INDEX)', 'Fertilizer Displacement TPA Revenue ($/Year) (MIN INDEX)', 'Fertilizer Displacement TPA Revenue ($/Year) (MEDIAN INDEX)']
    df_fert_rev = pd.DataFrame(columns=fert_rev_columns)
    waste_rev_columns = ['Year', 'Waste Diversion TPA Revenue ($/Year) (MAX VALUE)', 'Waste Diversion TPA Revenue ($/Year) (MIN VALUE)', 'Waste Diversion TPA Revenue ($/Year) (MEDIAN VALUE)',
                        'Waste Diversion TPA Revenue ($/Year) (MAX INDEX)', 'Waste Diversion TPA Revenue ($/Year) (MIN INDEX)', 'Waste Diversion TPA Revenue ($/Year) (MEDIAN INDEX)']
    df_waste_rev = pd.DataFrame(columns=waste_rev_columns)
    soil_rev_columns = ['Year', 'Soil Sequestration TPA Revenue ($/Year) (MAX VALUE)', 'Soil Sequestration TPA Revenue ($/Year) (MIN VALUE)', 'Soil Sequestration TPA Revenue ($/Year) (MEDIAN VALUE)',
                        'Soil Sequestration TPA Revenue ($/Year) (MAX INDEX)', 'Soil Sequestration TPA Revenue ($/Year) (MIN INDEX)', 'Soil Sequestration TPA Revenue ($/Year) (MEDIAN INDEX)']
    df_soil_rev = pd.DataFrame(columns=soil_rev_columns)
    n2o_rev_columns = ['Year', 'Soil N2O TPA Revenue ($/Year) (MAX VALUE)', 'Soil N2O TPA Revenue ($/Year) (MIN VALUE)', 'Soil N2O TPA Revenue ($/Year) (MEDIAN VALUE)',
                        'Soil N2O TPA Revenue ($/Year) (MAX INDEX)', 'Soil N2O TPA Revenue ($/Year) (MIN INDEX)', 'Soil N2O TPA Revenue ($/Year) (MEDIAN INDEX)']
    df_n2o_rev = pd.DataFrame(columns=n2o_rev_columns)
    trans_cost_columns = ['Year', 'Transaction Cost ($/Year) (MAX VALUE)', 'Transaction Cost ($/Year) (MIN VALUE)', 'Transaction Cost ($/Year) (MEDIAN VALUE)',
                        'Transaction Cost ($/Year) (MAX INDEX)', 'Transaction Cost ($/Year) (MIN INDEX)', 'Transaction Cost ($/Year) (MEDIAN INDEX)']
    df_trans_cost = pd.DataFrame(columns=trans_cost_columns)
    npv_columns = ['Year', 'NPV from GHG ($/Year) (MAX VALUE)', 'NPV from GHG ($/Year) (MIN VALUE)', 'NPV from GHG ($/Year) (MEDIAN VALUE)',
                        'NPV from GHG ($/Year) (MAX INDEX)', 'NPV from GHG ($/Year) (MIN INDEX)', 'NPV from GHG ($/Year) (MEDIAN INDEX)']
    df_npv = pd.DataFrame(columns=npv_columns)
    npv_tonnes_columns = ['Year', 'NPV from GHG per Tonne ($/Year) (MAX VALUE)', 'NPV from GHG per Tonne ($/Year) (MIN VALUE)', 'NPV from GHG per Tonne ($/Year) (MEDIAN VALUE)',
                        'NPV from GHG per Tonne ($/Year) (MAX INDEX)', 'NPV from GHG per Tonne ($/Year) (MIN INDEX)', 'NPV from GHG per Tonne ($/Year) (MEDIAN INDEX)']
    df_npv_tonnes = pd.DataFrame(columns=npv_tonnes_columns)

    # Check for scenario data and prepare output
    valid_yearly_scenario(df_scenario)
    max_year = len(df_scenario)
    output_folder = create_output_folder(f_string)
    yearly_produciton = []
    years = []
    
    # Loop through each year in the scenario data    
    for year in range(0, max_year):
        # Get scenario values for the year
        n2o_present, production, fap, epp = get_scenario(df_scenario,year)
        valid_scenario(n2o_present, production, fap, epp)

        # Store Values for Plotting
        yearly_produciton.append(production)
        years.append(year+1)
    
        # Calculate Fertilizer Displacement For 100000 TPA Production
        df_ag['Fertilizer Displacement TPA']=df_ag.apply(lambda x : get_emissions_short(x['Product Made'], x['Product Displaced'], production, fap, epp, df_nutriant) , axis=1)
    
        # Calculate Standard Volumes Discount
        df_ag['Fertilizer Displacement TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Fertilizer Displacement TPA']
        df_ag['Waste Diversion TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Waste Diversion TPA'] * df_ag.apply(lambda x : get_discount(x['Feedstock'], x['Baseline'], x['Standard'], df_discvol) , axis=1)
        df_ag['Soil Sequestration TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Soil Sequestration TPA'] * df_ag.apply(lambda x : get_discount('Land Use', 'All', x['Standard'], df_discvol) , axis=1)
        if(n2o_present == 'Yes'):
            df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] = df_ag['Soil N2O TPA'] * df_ag.apply(lambda x : get_discount('Land Use', 'All', x['Standard'], df_discvol) , axis=1)
        else:
            df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] = 0
    
        # Calculate Yearly Volumes Adjusted for Production Volumes
        df_ag['Fertilizer Displacement TPA (Yearly Adjusted Volumes)'] = df_ag['Fertilizer Displacement TPA (Adjusted for Standard Volumes Discount)'] * production / 100000
        df_ag['Waste Diversion TPA (Yearly Adjusted Volumes)'] = df_ag['Waste Diversion TPA (Adjusted for Standard Volumes Discount)'] * production / 100000
        df_ag['Soil Sequestration TPA (Yearly Adjusted Volumes)'] = df_ag['Soil Sequestration TPA (Adjusted for Standard Volumes Discount)'] * production / 100000
        df_ag['Soil N2O TPA (Yearly Adjusted Volumes)'] = df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] * production / 100000
        df_ag['Total GHG TPA'] = df_ag['Fertilizer Displacement TPA (Yearly Adjusted Volumes)'] + df_ag['Waste Diversion TPA (Yearly Adjusted Volumes)'] + df_ag['Soil Sequestration TPA (Yearly Adjusted Volumes)'] + df_ag['Soil N2O TPA (Yearly Adjusted Volumes)']
    
        # Calculate Yearly Prices
        standard_prices = get_standard_prices(df_pricing)
        cash_per_tonnes_short = get_cash_per_tonnes_short('5', 'AS', production, fap, epp, df_nutriant)

        df_ag['Fertilizer Displacement TPA Revenue ($/Year)'] = round(df_ag['Fertilizer Displacement TPA (Adjusted for Standard Volumes Discount)'] * cash_per_tonnes_short,2)
        df_ag['Waste Diversion TPA Revenue ($/Year)'] = round(df_ag['Waste Diversion TPA (Adjusted for Standard Volumes Discount)'] * df_ag.apply(lambda x : get_pricing('Waste',x['Standard'], standard_prices) , axis=1),2)
        df_ag['Soil Sequestration TPA Revenue ($/Year)'] = round(df_ag['Soil Sequestration TPA (Adjusted for Standard Volumes Discount)'] * df_ag.apply(lambda x : get_pricing('Land Use',x['Standard'], standard_prices) , axis=1),2)
        df_ag['Soil N2O TPA Revenue ($/Year)'] = round(df_ag['Soil N2O TPA (Adjusted for Standard Volumes Discount)'] * df_ag.apply(lambda x : get_pricing('N2O (industrial)',x['Standard'], standard_prices) , axis=1),2)

        df_ag['Transaction Cost ($/Year)'] = round(production * TRANSACTION_COST,2)
        df_ag['NPV from GHG ($/Year)'] = round(df_ag['Fertilizer Displacement TPA Revenue ($/Year)'] + df_ag['Waste Diversion TPA Revenue ($/Year)'] + df_ag['Soil Sequestration TPA Revenue ($/Year)'] + df_ag['Soil N2O TPA Revenue ($/Year)'] - df_ag['Transaction Cost ($/Year)'],2)
        df_ag['NPV from GHG per Tonne ($/Year)'] = round(df_ag['NPV from GHG ($/Year)'] / production,2)
    
        # Get Statistics
        df_fert_vol = add_stats_to_df(df_fert_vol, df_ag['Fertilizer Displacement TPA (Yearly Adjusted Volumes)'], year)
        df_waste_vol = add_stats_to_df(df_waste_vol, df_ag['Waste Diversion TPA (Yearly Adjusted Volumes)'], year)
        df_soil_vol = add_stats_to_df(df_soil_vol, df_ag['Soil Sequestration TPA (Yearly Adjusted Volumes)'], year)
        df_n2o_vol = add_stats_to_df(df_n2o_vol, df_ag['Soil N2O TPA (Yearly Adjusted Volumes)'], year)
        df_ghg_vol = add_stats_to_df(df_ghg_vol, df_ag['Total GHG TPA'], year)
        df_fert_rev = add_stats_to_df(df_fert_rev, df_ag['Fertilizer Displacement TPA Revenue ($/Year)'], year)
        df_waste_rev = add_stats_to_df(df_waste_rev, df_ag['Waste Diversion TPA Revenue ($/Year)'], year)
        df_soil_rev = add_stats_to_df(df_soil_rev, df_ag['Soil Sequestration TPA Revenue ($/Year)'], year)
        df_n2o_rev = add_stats_to_df(df_n2o_rev, df_ag['Soil N2O TPA Revenue ($/Year)'], year)
        df_trans_cost = add_stats_to_df(df_trans_cost, df_ag['Transaction Cost ($/Year)'], year)
        df_npv = add_stats_to_df(df_npv, df_ag['NPV from GHG ($/Year)'], year)
        df_npv_tonnes = add_stats_to_df(df_npv_tonnes, df_ag['NPV from GHG per Tonne ($/Year)'], year)
    
        # Print Yearly Results to File
        with open(f'{output_folder}/{f_string}_Results_Year{year+1}.txt', 'w') as f:
            print('Volume Scenarios', file=f)
            print('----------------------------------------------------------------', file=f)
            print_results(df_ag,df_fert_vol, fert_vol_columns, year, f)
            print_results(df_ag,df_waste_vol, waste_vol_columns, year, f)
            print_results(df_ag,df_soil_vol, soil_vol_columns, year, f)
            print_results(df_ag,df_n2o_vol, n2o_vol_columns, year, f)
            print_results(df_ag,df_ghg_vol, ghg_vol_columns, year, f)
        
            print('Revenue Scenarios', file=f)
            print('----------------------------------------------------------------', file=f)
            print_results(df_ag,df_fert_rev, fert_rev_columns, year, f)
            print_results(df_ag,df_waste_rev, waste_rev_columns, year, f)
            print_results(df_ag,df_soil_rev, soil_rev_columns, year, f)
            print_results(df_ag,df_n2o_rev, n2o_rev_columns, year, f)
            print_results(df_ag,df_trans_cost, trans_cost_columns, year,f)
            print_results(df_ag,df_npv, npv_columns, year, f)
            print_results(df_ag,df_npv_tonnes, npv_tonnes_columns, year, f)

    # Print Overall NPV Results to File
    max_npv = df_npv['NPV from GHG ($/Year) (MAX VALUE)'].to_list()
    min_npv = df_npv['NPV from GHG ($/Year) (MIN VALUE)'].to_list()
    median_npv = df_npv['NPV from GHG ($/Year) (MEDIAN VALUE)'].to_list()    
    with open(f'{output_folder}/{f_string}_NPV_Results.txt', 'w') as f:
        print(f'Overall NPV Results (rate = {npv})', file=f)
        print('----------------------------------------------------------------', file=f)
        print_npv_results(npv, max_npv, yearly_produciton, output_folder, 'MAX', f)
        print_npv_results(npv, min_npv, yearly_produciton, output_folder, 'MIN', f)
        print_npv_results(npv, median_npv, yearly_produciton, output_folder, 'MEDIAN', f)
    
    # Plot Yearly GHG and NPV Scenarios
    max_total_ghg = df_ghg_vol['Total GHG TPA (MAX VALUE)'].to_list()
    min_total_ghg = df_ghg_vol['Total GHG TPA (MIN VALUE)'].to_list()
    median_total_ghg = df_ghg_vol['Total GHG TPA (MEDIAN VALUE)'].to_list()

    plot_graphs(years, max_npv, min_npv, median_npv, output_folder, 'NPV', f_string)
    plot_graphs(years, max_total_ghg, min_total_ghg, median_total_ghg, output_folder, 'GHG', f_string)

    print(f"Scenario Results saved to {output_folder}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feedstock', type=str, choices = ['wood','Ag'], default='All', help='Feedstock filter: ("wood", "Ag")')
    parser.add_argument('-p', '--product', type=str, choices = ['AS','AN','U','UN'], default='All', help='Product Made Filter: ("AS", "AN", "U", "UN")')
    parser.add_argument('-s', '--standard', type=str, choices = ['Gold','Verra'], default='All', help='Standard filter: ("Gold", "Verra")')
    parser.add_argument('-n', '--npv', type=float, default=0.1, help='NPV rate (0 <= NPV <= 1)')
    args = parser.parse_args()
    main(f_filter=args.feedstock, p_filter=args.product, s_filter=args.standard, npv = args.npv)
    