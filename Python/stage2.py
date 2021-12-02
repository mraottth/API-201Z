# See plotting_functions.py for function def
# See mraottth/API-201Z/Python for other data importation, cleaning, and plotting modules
vax_cases_and_correlation(
    data=df_joined_cases, 
    groupby='SVI Bucket', 
    hue_levels={'High to Very High':'red', 'Moderate':'gold', 'Very Low to Low':'green'},
    start="2021-07-12", 
    end="2021-10-28"
) 
