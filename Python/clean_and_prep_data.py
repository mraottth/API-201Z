# Import libraries from libraries.py
# Import data from import_data.py
# Import global variables from global_variables.py

####################
# PART 1 CASES DATA 
####################

# Calc WoW rate of growth in cumulative cases 
df_cases['WoW_%'] = (df_cases['cases'] - df_cases.groupby(['state'])['cases'].shift(7)) / df_cases.groupby(['state'])['cases'].shift(7)


####################
# PART 2 VAX DATA 
####################

# Join state names and abbrevs to df_vax to prep for merging with cases
df_vax = pd.merge(
            df_vax, 
            states, 
            left_on='Location', 
            right_on='code'
        )

# Merge state pop to vax and sort by state and date
df_vax = pd.merge(
            df_vax, 
            df_state_pop, 
            left_on='Location', 
            right_on='state/region'
            ).sort_values(['state','Date'], ascending=True)

# Calc number of remaining unvaccinated ppl in each state on each day
df_vax['unvaxxed'] = (1 - (df_vax['Administered_Dose1_Pop_Pct']/100)) * df_vax['population'] 

# Calc percent of remaining unvaxxed ppl who got jab in the last week
df_vax['WoW_%'] = (df_vax.groupby(['state'])['unvaxxed'].shift(7) - df_vax['unvaxxed'] ) / df_vax.groupby(['state'])['unvaxxed'].shift(7)

# Create column for n days ago datestamp. Change global variable n to offset cases and vax timeframes by n days
df_vax['date_minus_n'] = df_vax['Date'] - timedelta(days=n)

# Join df_vax and df_cases into the main joined table
df_joined_cases = pd.merge(
                    df_cases, 
                    df_vax, 
                    how='inner',
                    left_on=['date','state'], 
                    right_on=['date_minus_n','state'], 
                    suffixes=['_cases','_vax']
                )


#############################
# PART 3 ELECTION & SVI DATA 
#############################

# Join election results data to df_joined_cases and filter out negative values
df_joined_cases = pd.merge(df_joined_cases, election, on='state').query('`WoW_%_cases` >= 0 & `WoW_%_vax` >= 0')

# Get rid of everything after comma in CDC SVI data county name field to prep for joining to df_joined_cases
df_svi['County Name'] = df_svi['County Name'].apply(lambda x: x.split(',')[0])

# Join svi to county_pop to weight statewide SVI by population
# First join county pop to states to get abbreviations
df_county_pop = pd.merge(
    df_county_pop, 
    states, 
    left_on='STNAME', 
    right_on='state'
    )
# Join svi to county pop
df_svi = pd.merge(df_svi, df_county_pop, left_on=['State Code','County Name'], right_on=['index','CTYNAME'])

# Create weighted average function 
def wavg(data, avg_name, weight_name):
    d = data[avg_name]
    w = data[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()

# Group df_svi by state and get weighted average by county population for state-level svi 
wavg_svi = pd.DataFrame(
    df_svi.groupby('State Code').apply(wavg, 'Social Vulnerability Index (SVI)', 'POPESTIMATE2019')\
        .reset_index()).rename(columns={0:'w_SVI'}
        )
# Join weighted average back to df_svi on state code
df_svi = pd.merge(df_svi, wavg_svi, on='State Code')

# Create SVI buckets from CDC methodology. Group high and low end together b/c data is sparse at extremes
df_svi['SVI Bucket'] = [
    'Very Low to Low' if (0 <= val < 0.4) # 'Very Low' if (0 <= val < 0.2), 'Low' if (0.2 <= val < 0.4)
    else 'Moderate' if (0.4 <= val < 0.6) # 'Moderate' if (0.4 <= val < 0.6)
    else 'High to Very High' if (0.6 <= val <= 1) # 'High' if (0.6 <= val < 0.8), 'Very High' (0.8 <= val <= 1)
    else np.nan 
    for val in df_svi['w_SVI']
]

# Join df_svi to df_joined_cases
df_joined_cases = pd.merge(
    df_joined_cases, 
    df_svi.groupby('State Code')['w_SVI','SVI Bucket'].max().reset_index(), 
    left_on='Location', 
    right_on='State Code'
    )


#################################
# PART 4 FINAL PREP ON JOINED DF 
#################################

# Round vax rate to nearest 10 for vax level variable
df_joined_cases['vax_level'] = 'Roughly ' + round(df_joined_cases['Administered_Dose1_Pop_Pct'], -1).astype(str) + '%'

# Round electoral results (winning share of vote and republican/dem percent) to nearest 5
df_joined_cases['winning_share_rd'] = 5 * round((df_joined_cases['winning_share']).apply(lambda x: x[0:4]).astype(float)/5)
df_joined_cases['rep_percent_rd'] = 5 * round((df_joined_cases['rep_percent']).apply(lambda x: x[0:4]).astype(float)/5)
df_joined_cases['dem_percent_rd'] = 5 * round((df_joined_cases['dem_percent']).apply(lambda x: x[0:4]).astype(float)/5)

# Rename poorly named columns and drop redundant ones
df_joined_cases = df_joined_cases.drop(['Date','Location','state/region'], axis=1)\
    .rename(columns={
        'Recip_Administered':'n_vaccinated_people',
        'Administered_Dose1_Recip':'n_at_least_one_dose',
        'Administered_Dose1_Pop_Pct':'percent_at_least_one_dose',
        'Series_Complete_Yes':'n_fully_vaccinated',
        'Series_Complete_Pop_Percent':'percent_fully_vaccinated',
        'called':'2020 Election Winner',
        'w_SVI':'SVI',
        'vax_level':'Population Vax Level'
      }
    )

# Rename R and D to republican and democrat for clarity
df_joined_cases['2020 Election Winner'] = ['Democrat' if x == 'D' else 'Republican' if x == 'R' else '' for x in df_joined_cases['2020 Election Winner']]

# Cut everything before start and after end using global variables
df_joined_cases = df_joined_cases[(df_joined_cases['date'] >= start_date) & (df_joined_cases['date'] <= end_date)]

# Remove inf values
df_joined_cases.replace([np.inf, -np.inf], np.nan, inplace=True)

# Create a new dataframe resampled weekly to use for a more smoothed out dataset
df_weekly = df_joined_cases.set_index('date').groupby(['state', '2020 Election Winner', 'SVI Bucket', 'Population Vax Level'])\
    .resample('W')[['WoW_%_cases', 'WoW_%_vax']].mean().reset_index()

# Output df_joined_cases to Output folder

