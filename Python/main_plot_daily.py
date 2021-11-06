from libraries import * # Import libraries from libraries.py
from import_data import * # Import data from import_data.py
from global_variables import * # Import global variables from global_variables.py
from plotting_functions import * # Import plotting functions from plotting_functions.py


# Import df_joined_cases from Outputs folder
df_joined_cases = pd.read_csv(os.getcwd().split('API-201Z')[0] + 'API-201Z/Data Sources/cleaned_joined_states.csv').query('`WoW_%_vax` >= 0')

# Plot correlations between cases and vax split by party controlling for vax level
lm(
    data=df_joined_cases.query('`Population Vax Level` != "Roughly 30.0%" & @START_DATE <= date <= @END_DATE'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    columns='Population Vax Level',
    title=('Controlling for vax-level, how do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.2, 25),
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Plot correlations between cases and vax split by party
lm(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    columns=None,
    title=('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.1, 12),
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Jointplot of cases vs vax split by political party. One point for each state per day
jp(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    title=('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.1, 12), 
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Jointplot of cases vs vax split by political party. Grouped by state with avg rates
jp(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE')\
        .groupby(['state', '2020 Election Winner'])['WoW_%_cases','WoW_%_vax'].mean().reset_index(),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    title=('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is avg per state in DateRange'\
        , 1.1, 12), 
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent',
    s=50,
    alpha=0.8
)

# Plot every state's case change vs vax response
fig, ax = plt.subplots(figsize=(12,8))
for state in df_vax['state'].unique():
    if election[election['state'] == state]['called'].unique() == 'D':
        color = 'blue'
    else:
        color = 'red'
    sns.regplot(
        data=df_joined_cases[(df_joined_cases['state'] == state)].query('@START_DATE <= date <= @END_DATE'), 
        x='WoW_%_cases', 
        y='WoW_%_vax',        
        color=color,
        line_kws={'lw':0.65, 'alpha':0.45},        
        # lowess=True,
        scatter=False 
        )    
    plt.setp(ax.collections[list(df_vax['state'].unique()).index(state)], alpha=0.07)    
ax.grid(True, which='both', axis='both', alpha=0.17)
# Create custom legend
custom_legend = []
for k, v in {'Democrat':'blue', 'Republican':'red'}.items():
    custom_legend.append(Line2D([0], [0], color=v, lw=2))

ax.legend(custom_legend, ['Democrat', 'Republican'], title='2020 Election Winner')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
plt.xlabel("Rate of case growth (week-over-week % change)")
plt.ylabel('% of remaining unvaxed pop. receiving jab in past week')
plt.title('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE, fontsize=18)
if SAVE_IMAGES == True:
    plt.savefig('/Users/mattroth/Desktop/HKS/MPP1/Fall 2021/API-201 Quant/Final Project Charts/unvax change/REG'\
            + 'How_do_unvaccinated_people_respond_to_increasing_in-state_caseloads_party.jpeg',            
            bbox_inches = "tight", dpi=150)


# Plot every state's case change vs vax response by SVI
fig, ax = plt.subplots(figsize=(12,8))
for state in df_vax['state'].unique():
    if df_joined_cases[df_joined_cases['state'] == state]['SVI Bucket'].unique() == 'Very Low to Low':
        color = 'green'
    elif df_joined_cases[df_joined_cases['state'] == state]['SVI Bucket'].unique() == 'Moderate':
        color = 'gold'
    else:
        color = 'red'
    sns.regplot(
        data=df_joined_cases[(df_joined_cases['state'] == state)].query('@START_DATE <= date <= @END_DATE'), 
        x='WoW_%_cases', 
        y='WoW_%_vax',        
        color=color,
        line_kws={'lw':0.65, 'alpha':0.45},        
        # lowess=True,
        scatter=False 
        )    
    plt.setp(ax.collections[list(df_vax['state'].unique()).index(state)], alpha=0.07)    
ax.grid(True, which='both', axis='both', alpha=0.17)
# Create custom legend
custom_legend = []
for k, v in {'Very Low to Low':'green', 'Moderate':'gold', 'High to Very High':'red'}.items():
    custom_legend.append(Line2D([0], [0], color=v, lw=2))
ax.legend(custom_legend, ['Very Low to Low', 'Moderate', 'High to Very High'])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
plt.xlabel("Rate of case growth (week-over-week % change)")
plt.ylabel('% of remaining unvaxed pop. receiving jab in past week')
plt.title('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE, fontsize=18)
if SAVE_IMAGES == True:
    plt.savefig('/Users/mattroth/Desktop/HKS/MPP1/Fall 2021/API-201 Quant/Final Project Charts/unvax change/REG'\
            + 'How_do_unvaccinated_people_respond_to_increasing_in-state_caseloads_SVI.jpeg',            
            bbox_inches = "tight", dpi=150)

# Jointplot of cases vs vax by SVI level grouped by state
jp(    
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE')\
        .groupby(['state', 'SVI Bucket'])['WoW_%_cases','WoW_%_vax'].mean().reset_index(),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='SVI Bucket',
    hue_levels={'Very Low to Low':'green', 'Moderate':'gold', 'High to Very High':'red'},
    title=('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.1, 12), 
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent',
    s=50,
    alpha=0.8
)

# Jointplot of cases vs vax by SVI level one point per state per day
jp( 
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='SVI Bucket',
    hue_levels={'Very Low to Low':'green', 'Moderate':'gold', 'High to Very High':'red'},
    title=('How do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is avg per state in DateRange'\
        , 1.1, 12), 
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Plot correlations between cases and vax for Rep and Dem split by SVI
lm(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    columns='SVI Bucket',
    col_order=['Very Low to Low','Moderate','High to Very High'],
    title=('Controlling for SVI, how do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.2, 25),
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Plot correlations between cases and vax for Rep and Dem split by SVI
lm(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE & `Population Vax Level` != "Roughly 30.0%"'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='SVI Bucket',
    hue_levels={'Very Low to Low':'green', 'Moderate':'gold', 'High to Very High':'red'},
    columns='Population Vax Level',    
    title=('Controlling for vax-level, how do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.2, 25),
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Plot correlations between cases and vax by SVI split by party
lm(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE & `Population Vax Level` != "Roughly 30.0%"'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='SVI Bucket',
    hue_levels={'Very Low to Low':'green', 'Moderate':'gold', 'High to Very High':'red'},
    columns='2020 Election Winner',    
    title=('Controlling for party, how do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.2, 17),
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)

# Plot correlations between cases and vax by SVI split by party controlling for vax level
lm(
    data=df_joined_cases.query('@START_DATE <= date <= @END_DATE & `Population Vax Level` != "Roughly 30.0%"'),
    x='WoW_%_cases',
    y='WoW_%_vax',
    hue='SVI Bucket',
    hue_levels={'Very Low to Low':'green', 'Moderate':'gold', 'High to Very High':'red'},
    rows='2020 Election Winner',    
    columns='Population Vax Level',
    title=('Controlling for vax-level and party, how do unvaccinated people respond to increasing in-state caseloads?\nDate range: '\
        + START_DATE + ' to ' + END_DATE + ' -- Each point is one state on one day'\
        , 1.1, 30),
    xlabel='Week-over-week growth in cases (% of cumulative)',
    ylabel='% of remaining unvaxed pop. receiving jab in past week',
    yformat='percent',
    xformat='percent'
)
