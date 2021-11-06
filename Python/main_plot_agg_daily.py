from libraries import * # Import libraries from libraries.py
from import_data import * # Import data from import_data.py
from global_variables import * # Import global variables from global_variables.py
from plotting_functions import * # Import plotting functions from plotting_functions.py


# Plot aggregatd lms

# full date window no splits
agg_lm(
    data=df_joined_cases,
    groupby=None,
    hue_levels={"Total":'gray'},    
    suptitle='Each point is 1 day aggregated nationally'
)

# Full date window split on party
agg_lm(
    data=df_joined_cases,
    groupby='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    suptitle='Each point is 1 day aggregated by red or blue state'
)

# Full date window split on svi
agg_lm(
    data=df_joined_cases,
    groupby='SVI Bucket',
    hue_levels={'High to Very High':'red', 'Moderate':'gold', 'Very Low to Low':'green'},
    suptitle='Each point is 1 day aggregated by state-level SVI'
)

# Cases rising date window no split
agg_lm(
    data=df_joined_cases,
    groupby=None,
    hue_levels={"Total":'gray'},    
    suptitle='Each point is 1 day aggregated nationally',
    start="2021-07-01",
    end="2021-09-01"
)

# Cases rising date window split on party
agg_lm(
    data=df_joined_cases,
    groupby='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    suptitle='Each point is 1 day aggregated by red or blue state',
    start="2021-07-01",
    end="2021-09-01"
)

# Cases rising date window split on svi
agg_lm(
    data=df_joined_cases,
    groupby='SVI Bucket',
    hue_levels={'High to Very High':'red', 'Moderate':'gold', 'Very Low to Low':'green'},
    suptitle='Each point is 1 day aggregated by state-level SVI',
    start="2021-07-01",
    end="2021-09-01"
)

# Cases falling date window no split
agg_lm(
    data=df_joined_cases,
    groupby=None,
    hue_levels={"Total":'gray'},    
    suptitle='Each point is 1 day aggregated nationally',
    start="2021-09-01",
    end="2021-10-31"
)

# Cases falling date window split on party
agg_lm(
    data=df_joined_cases,
    groupby='2020 Election Winner',
    hue_levels={'Democrat':'blue', 'Republican':'red'},
    suptitle='Each point is 1 day aggregated by red or blue state',
    start="2021-09-01",
    end="2021-10-31"
)

# Cases falling date window split on svi
agg_lm(
    data=df_joined_cases,
    groupby='SVI Bucket',
    hue_levels={'High to Very High':'red', 'Moderate':'gold', 'Very Low to Low':'green'},
    suptitle='Each point is 1 day aggregated by state-level SVI',
    start="2021-09-01",
    end="2021-10-31"
)
