# Scenario Analysis for Agriculture GHG
This script performs scenario analysis for greenhouse gas (GHG) emissions in the agriculture sector. It calculates various metrics such as fertilizer displacement, waste diversion, soil sequestration, and soil N2O emissions, and adjusts these metrics based on production volumes and standard volume discounts. The script also calculates the net present value (NPV) of GHG emissions and generates statistics and plots for the analysis.

### Requirements
- Python 3.x
- pandas
- numpy_financial
- seaborn
- matplotlib

### Installation
Install the required packages using pip:
```console
pip install pandas numpy_financial seaborn matplotlib`
```

### Usage
Run the script from the command line with the following optional arguments:

`-f`, `--feedstock`: Filter by feedstock type (`wood`, `Ag`). Default is `All`.
`-p`, `--product`: Filter by product made (`AS`, `AN`, `U`, `UN`). Default is `All`.
`-s`, `--standard`: Filter by standard (`Gold`, `Verra`). Default is `All`.
`-n`, `--npv`: NPV rate (0 <= NPV <= 1). Default is 0.1.
Example:
```console
python ag_scenario_analysis.py -f wood -p AS -s Gold -n 0.1
```

### Script Overview
1.  Data Loading and Validation: The script loads data from Excel sheets and validates the data to ensure it contains the required columns and no null values.

2. Filtering Data: The script filters the data based on the provided command line arguments.

3. Calculations: The script performs various calculations including:
    - Adjusting volumes for standard volume discounts.
    - Calculating yearly adjusted volumes for production.
    - Calculating yearly prices and NPV from GHG emissions.
    - Statistics and Plots: The script generates statistics for the calculated metrics and saves the results to text files. It also generates plots for yearly GHG and NPV scenarios.

4. Output: The results are saved to an output folder with a timestamp and filter string.

### Output
The script generates the following output files in the output folder:

- Yearly results for each scenario year (`Results_YearX.txt`).
- Overall NPV results (`NPV_Results.txt`).
- Plots for yearly GHG and NPV scenarios (`NPV_Plot.png`, `GHG_Plot.png`).
Example Output
```console
Scenario Results saved to output/wood_AS_Gold_20250222_123456.
```
This indicates that the results have been saved to the specified output folder.

Notes
Ensure the Excel file `ag_data.xlsx` is present in the data directory with the required sheets (`Data`, `Scenario Input`, `Nutriant Table`, `Discounts to Volume Table`, `Pricing Table`).
The script uses various utility functions from the utils directory for data validation, scenario calculations, and statistics generation.