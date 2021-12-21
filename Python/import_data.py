from libraries import * # Import libraries from libraries.py

def import_data():
    # Read in state-level cases & deaths data from NYT GitHub
    states_cases = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
    df_cases = pd.read_csv(states_cases, parse_dates=['date']).query('date >= "2021-02-13"').sort_values(['state','date'], ascending=True)


    # Read in state-level vaccine data from CDC
    state_vax = 'https://data.cdc.gov/api/views/unsk-b7fc/rows.csv?accessType=DOWNLOAD'
    cols = ['Date','Location','Recip_Administered', 'Administered_Dose1_Recip','Administered_Dose1_Pop_Pct','Series_Complete_Yes','Series_Complete_Pop_Pct']
    df_vax = pd.read_csv(state_vax, parse_dates=['Date'], usecols=cols)


    # Read in csv of state abbreviations and names. Use to join to df_vax to prep for merging with cases
    states = pd.read_csv('/Users/mattroth/Desktop/HKS/MPP1/Fall 2021/API-201 Quant/Final Project/Final Project Charts/states.csv')


    # Read in state population table to calculate size of unvaccinated pool
    state_pop = 'https://github.com/jakevdp/data-USstates/raw/master/state-population.csv'
    df_state_pop = pd.read_csv(state_pop).query('ages == "total" & year == 2012').drop(['ages','year'], axis=1)


    # Read in election data 
    election = pd.read_csv('/Users/mattroth/Desktop/HKS/MPP1/Fall 2021/API-201 Quant/Final Project/Final Project Charts/2020 results.csv')


    # Read in SVI data (from CDC county level). Will need to group by state and take weighted avg by population later
    svi_url = 'https://data.cdc.gov/api/views/q9mh-h2tw/rows.csv?accessType=DOWNLOAD'
    df_svi = pd.read_csv(svi_url, usecols=['State Code', 'County Name', 'Social Vulnerability Index (SVI)'])


    # Read in county population data to weight SVI 
    county_pop = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
    df_county_pop = pd.read_csv(county_pop, encoding = "ISO-8859-1", usecols=['STNAME','CTYNAME','POPESTIMATE2019'])


    # Write all of the dataframes to Data Sources folder as csvs
    df_list = [
        ('cases', df_cases),
        ('vax', df_vax),
        ('state_pop', df_state_pop),
        ('election', election),
        ('svi', df_svi),
        ('county_pop', df_county_pop)
        ]

    for name, df in df_list:
        df.to_csv(os.getcwd().split('API-201Z')[0] + 'API-201Z/Data Sources/' + name + '.csv')

