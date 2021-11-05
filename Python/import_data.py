# Read in state-level cases & deaths data from NYT GitHub
states_cases = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
df_states = pd.read_csv(states_cases, parse_dates=['date'])


# Read in state-level vaccine data from CDC
state_vax = 'https://data.cdc.gov/api/views/unsk-b7fc/rows.csv?accessType=DOWNLOAD'
cols = ['Date','Location','Recip_Administered', 'Administered_Dose1_Recip','Administered_Dose1_Pop_Pct','Series_Complete_Yes','Series_Complete_Pop_Pct']
df_vax = pd.read_csv(state_vax, parse_dates=['Date'])[cols]


# Read in csv of state abbreviations and names. Use to join to df_vax to prep for merging with cases
states = pd.read_csv('/Users/mattroth/Desktop/HKS/MPP1/Fall 2021/API-201 Quant/Final Project Charts/states.csv')


# Read in state population table to calculate size of unvaccinated pool
state_pop = 'https://github.com/jakevdp/data-USstates/raw/master/state-population.csv'
df_state_pop = pd.read_csv(state_pop).query('ages == "total" & year == 2012').drop(['ages','year'], axis=1)


# Read in election data 
election = pd.read_csv('/Users/mattroth/Desktop/HKS/MPP1/Fall 2021/API-201 Quant/Final Project Charts/2020 results.csv')
df_joined_cases = pd.merge(df_joined_cases, election, on='state').query('`WoW_%_cases` >= 0 & `WoW_%_vax` >= 0')


# Read in SVI data (from CDC county level). Will need to group by state and take weighted avg by population later
svi_url = 'https://data.cdc.gov/api/views/q9mh-h2tw/rows.csv?accessType=DOWNLOAD'
df_svi = pd.read_csv(svi_url)[['State Code', 'County Name', 'Social Vulnerability Index (SVI)']]


# Read in county population data to weight SVI 
county_pop = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
df_county_pop = pd.read_csv(county_pop, encoding = "ISO-8859-1")[['STNAME','CTYNAME','POPESTIMATE2019']]
