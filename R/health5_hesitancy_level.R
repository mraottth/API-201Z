# Set up blank dataframe with columns and dtypes
df_health5 <- data.frame(
           state=character(),
           svi_level=character(),
           def_will=numeric(), 
           prob_will=numeric(), 
           unsure=numeric(),
           prob_wont=numeric(),
           def_wont=numeric(),
           stringsAsFactors=TRUE
         ) 

# Loop through 50 state tabs + DC in pulse excel, select value for each hesitancy level, add to right column & row
for (i in 2:52) {
    
  df_health5[i-1,'def_will'] <- as.numeric(suppressMessages(read_excel('health5_week33.xlsx', sheet = i)[8, 8]))
  df_health5[i-1,'prob_will'] <- as.numeric(suppressMessages(read_excel('health5_week33.xlsx', sheet = i)[8, 9]))
  df_health5[i-1,'unsure'] <- as.numeric(suppressMessages(read_excel('health5_week33.xlsx', sheet = i)[8, 10]))
  df_health5[i-1,'prob_wont'] <- as.numeric(suppressMessages(read_excel('health5_week33.xlsx', sheet = i)[8, 11]))
  df_health5[i-1,'def_wont'] <- as.numeric(suppressMessages(read_excel('health5_week33.xlsx',  sheet = i)[8, 12]))

}

# Get state name and svi level and add to dataframe
state_info <- read.csv('state_svi.csv')[,c(2:3)]
df_health5['state'] <- state_info['abbrev']
df_health5['svi_level'] <- state_info['svi_level']


# Collapse to svi level
low_svi <- colSums(subset(df_health5, svi_level == 'Very Low to Low')[-c(1:2)])
# mid_svi <- colSums(subset(df_health5, svi_level == 'Moderate')[-c(1:2)])
high_svi <- colSums(subset(df_health5, svi_level == 'High to Very High')[-c(1:2)])

# Combine into dataframe for chi square
combined_svi <- rbind(low_svi, high_svi)
combined_svi <- data.frame(combined_svi)

# Run chi square
chisq.test(combined_svi)
