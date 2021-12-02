# Set up blank dataframe with columns and dtypes
df_health6 <- data.frame(
  state=character(),
  svi_level=character(),
  side_effects=numeric(), 
  doubts_efficacy=numeric(), 
  dont_need=numeric(),
  dont_like=numeric(),
  no_doc_rec=numeric(),
  wait_and_see=numeric(), 
  others_need_more=numeric(), 
  cost=numeric(),
  mistrust_vax=numeric(),
  mistrust_gov=numeric(),
  stringsAsFactors=TRUE
) 

# Loop through 50 state tabs + DC in pulse excel, select value for each hesitancy level, add to right column & row
for (i in 2:52) {
  
  df_health6[i-1,'side_effects'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 3]))
  df_health6[i-1,'doubts_efficacy'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 4]))
  df_health6[i-1,'dont_need'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 5]))
  df_health6[i-1,'dont_like'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 6]))
  df_health6[i-1,'no_doc_rec'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 7]))
  df_health6[i-1,'wait_and_see'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 8]))
  df_health6[i-1,'others_need_more'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 9]))
  df_health6[i-1,'cost'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 10]))
  df_health6[i-1,'mistrust_vax'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 11]))
  df_health6[i-1,'mistrust_gov'] <- as.numeric(suppressMessages(read_excel('health6_week33.xlsx', sheet = i)[7, 12]))
  
}

# Get state name and svi level and add to dataframe
state_info <- read.csv('state_svi.csv')[,c(2:3)]
df_health6['state'] <- state_info['abbrev']
df_health6['svi_level'] <- state_info['svi_level']
df_health6[is.na(df_health6)] <- 0

# Collapse to svi level
low_svi <- colSums(subset(df_health6, svi_level == 'Very Low to Low')[-c(1:2)])
# mid_svi <- colSums(subset(df_health6, svi_level == 'Moderate')[-c(1:2)])
high_svi <- colSums(subset(df_health6, svi_level == 'High to Very High')[-c(1:2)])

# Combine into dataframe for chi square
combined_svi <- rbind(low_svi, high_svi)
combined_svi <- data.frame(combined_svi)

# Run chi square
chisq.test(combined_svi)