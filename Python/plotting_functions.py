from libraries import * # Import libraries from libraries.py
from global_variables import * # Import global variables


######################
# LINE FOR EACH STATE
#####################

# Create function to plot line for each state 
def line_for_each_state(data, x, y, hue_col, hue_levels, title, xlabel, ylabel, ci=None, yformat=None, xformat=None):

    # Create subplot
    fig, ax = plt.subplots(figsize=(12,8))

    # Iterate through each state
    for state in data['state'].unique():
        
        # Get color from hue_levels by searching for hue_col value
        color = hue_levels[data[data['state'] == state][hue_col].unique()[0]]
        
        # Plot for each state
        sns.lineplot(
            data=data[data['state'] == state], 
            x=x, 
            y=y,        
            color=color,
            lw=1,
            alpha=0.17,
            legend=None,
            ci=ci
            )    
    
    # Window highlighting timebox
    ax.vlines(
        x=pd.to_datetime(START_DATE), 
        ymin=min(data[y]), 
        ymax=1.1 * np.nanmax(data[data[y] != np.inf][y]), 
        color='gray', 
        alpha=0.4, 
        linestyle='dashed'
        )
    ax.vlines(
        x=pd.to_datetime(END_DATE), 
        ymin=min(data[y]), 
        ymax=1.1 * np.nanmax(data[data[y] != np.inf][y]), 
        color='gray', 
        alpha=0.4, 
        linestyle='dashed'
        )
    ax.axvspan(
        pd.to_datetime(START_DATE), 
        pd.to_datetime(END_DATE), 
        alpha=0.08, 
        color='lightgray', 
        zorder=0
        )
    
    # Set chart parameters
    plt.ylim((0, 1.1 * np.nanmax(data[data[y] != np.inf][y])))
    ax.set_title(title, fontsize=21, y=1.02)
    ax.set_ylabel(ylabel, fontsize=14)    
    ax.set_xlabel(xlabel)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    ax.grid(True, which='both', axis='both', alpha=0.15)    

    # Create custom legend
    custom_legend = []
    for k, v in hue_levels.items():
        custom_legend.append(Line2D([0], [0], color=v, lw=2))
    
    ax.legend(custom_legend, list(hue_levels.keys()), title=hue_col)

    # Format axis ticks
    if yformat == 'percent':    
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
    if xformat == 'percent':
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    # Save image to Output folder
    if SAVE_IMAGES == True:
        plt.savefig(os.getcwd().split('API-201Z')[0] + 'API-201Z/Outputs/Plots/line_' +\
            + title.replace(' ', '_') + hue_col.replace(' ', '_') + '.jpeg', 
            bbox_inches = "tight", dpi=150)

        
        
##################
# LMPLOT FUNCTION
#################    

# Create lmplot function to combine scatterplot & regress
def lm(data, x, y, hue, hue_levels, columns, title, xlabel, ylabel, yformat=None, xformat=None, rows=None, col_order=None, size=2, alpha=0.1, robust=False):    
    
    # Create plot
    g = sns.lmplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        scatter=True,    
        robust=robust,        
        hue_order=list(hue_levels.keys()),
        palette=list(hue_levels.values()),
        col=columns,
        col_order=col_order,
        row=rows,                        
        scatter_kws={"alpha": alpha, 's':size},
        legend=None,
        sharex=True,
        sharey=True
    )    
    
    # Set parameters
    g.tight_layout()
    g.set_axis_labels(xlabel, ylabel)
    g.fig.suptitle(title[0], y=title[1], fontsize=title[2])

    # Create custom legend
    custom_legend = []
    for k, v in hue_levels.items():
        custom_legend.append(Line2D([0], [0], color=v, lw=2))
    
    # Iterate through subplots to create gridlines and legend & format axis ticks
    for a in g.axes.flat:
        
        # Create gridlines
        a.grid(True, which='both', axis='both', alpha=0.25)   

        # Add legend
        a.legend(custom_legend, list(hue_levels.keys()), title=hue)

        # Format axis ticks
        if yformat == 'percent':    
            a.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
        if xformat == 'percent':
            a.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))      
    
    # Save to Output folder
    if SAVE_IMAGES == True:
        plt.savefig(os.getcwd().split('API-201Z')[0] + 'API-201Z/Outputs/Plots/lm_' +\
            title[0].replace(' ', '_') + hue.replace(' ', '_') + '.jpeg', 
            bbox_inches = "tight", dpi=150)


######################
# JOINTPLOT FUNCTION
#####################   
        
# Define jointplot function to do scatterplot & distributions with regression line
def jp(data, x, y, hue, hue_levels, title, xlabel, ylabel, yformat=None, xformat=None, s=7, alpha=0.25):    
    g = sns.jointplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        hue_order=list(hue_levels.keys()),
        palette=list(hue_levels.values()),
        alpha=alpha,
        s=s
    )
    # Set chart parameters
    plt.suptitle(title[0], y=title[1], fontsize=title[2])
    g.set_axis_labels(xlabel, ylabel)
    
    # Save to Output folder
    if SAVE_IMAGES == True:
        plt.savefig(os.getcwd().split('API-201Z')[0] + 'API-201Z/Outputs/Plots/jp_' +\
            title[0].replace(' ', '_') + hue.replace(' ', '_') + '.jpeg', 
            bbox_inches = "tight", dpi=150)
        

##################################
# AGGREGATE THEN REGRESSION TABLE
#################################

from stargazer.stargazer import Stargazer
from IPython.core.display import HTML
import statsmodels.api as sm

def regression_table(data, groupby, hue_levels, start, end):
    if groupby == None:
        agg = data.groupby('date')[['cases', 'unvaxxed']].sum().reset_index()
        agg['WoW_%_cases'] = (agg['cases'] - agg['cases'].shift(7)) / agg['cases'].shift(7)
        agg['WoW_%_vax'] = (agg['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg['unvaxxed'].shift(7)
        agg = agg.query('@start <= date <= @end')
    else: # Otherwise group by groupby and re-calculate WoW fields and cut to time window         
        agg = data.groupby(['date', groupby])[['cases', 'unvaxxed']].sum().reset_index()
        agg['WoW_%_cases'] = (agg['cases'] - agg.groupby([groupby])['cases'].shift(7)) / agg.groupby([groupby])['cases'].shift(7)
        agg['WoW_%_vax'] = (agg.groupby([groupby])['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg.groupby([groupby])['unvaxxed'].shift(7)
        agg = agg.query('@start <= date <= @end')

    stats_results = []
    if groupby != None:
        for i in range(len(hue_levels.keys())):
            level = list(hue_levels.keys())[i]  
            y = agg[(agg[groupby] == level) & (agg['date'] >= start) & (agg['date'] < end)].rename(columns={'WoW_%_vax':'Vax Response'})['Vax Response']
            x = sm.add_constant(agg[(agg[groupby] == level) & (agg['date'] >= start) & (agg['date'] < end)].rename(columns={'WoW_%_cases':'Case Growth'})['Case Growth'])      
            stats_results.append(sm.OLS(endog=y, exog=x).fit())
    else: # If groupby argument is empty just run the regression once
        y = agg[(agg['date'] >= start) & (agg['date'] < end)].rename(columns={'WoW_%_vax':'Vax Response'})['Vax Response']
        x = sm.add_constant(agg[(agg['date'] >= start) & (agg['date'] < end)].rename(columns={'WoW_%_cases':'Case Growth'})['Case Growth'])      
        stats_results.append(sm.OLS(endog=y, exog=x).fit())

    stargazer = Stargazer(stats_results)

    if groupby != None:
        stargazer.custom_columns(list(hue_levels.keys()), [1 for i in range(len(list(hue_levels.keys())))])
    stargazer.show_model_numbers(False)

    return HTML(stargazer.render_html())

        
######################
# AGGREGATE THEN LM
#####################        
        
# Create aggregation and lm plot function        
def agg_lm(data, groupby, hue_levels, suptitle, start=START_DATE, end=END_DATE, line_kws=None, legend=False):
    
    # If there's no groupby argument, only aggregate by date. Re-calculate WoW fields and cut to time window
    if groupby == None:
        agg = data.groupby('date')[['cases', 'unvaxxed']].sum().reset_index()
        agg['WoW_%_cases'] = (agg['cases'] - agg['cases'].shift(7)) / agg['cases'].shift(7)
        agg['WoW_%_vax'] = (agg['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg['unvaxxed'].shift(7)
        agg = agg.query('@start <= date <= @end')
        line_kws = {'label':"Linear Reg"}
        legend=True
    else: # Otherwise group by groupby and re-calculate WoW fields and cut to time window         
        agg = data.groupby(['date', groupby])[['cases', 'unvaxxed']].sum().reset_index()
        agg['WoW_%_cases'] = (agg['cases'] - agg.groupby([groupby])['cases'].shift(7)) / agg.groupby([groupby])['cases'].shift(7)
        agg['WoW_%_vax'] = (agg.groupby([groupby])['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg.groupby([groupby])['unvaxxed'].shift(7)
        agg = agg.query('@start <= date <= @end')
    
    # Iterate through levels of hue_levels, run linear regression, store results in stats_results
    stats_results = []
    if groupby != None:
        for i in range(len(hue_levels.keys())):
            level = list(hue_levels.keys())[i]                
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                agg[(agg[groupby] == level) & (agg['date'] >= start) & (agg['date'] < end)]['WoW_%_cases'],
                agg[(agg[groupby] == level) & (agg['date'] >= start) & (agg['date'] < end)]['WoW_%_vax']
                )
            stats_results.append((slope, intercept, r_value, p_value, std_err))
    else: # If groupby argument is empty just run the regression once
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            agg[(agg['date'] >= start) & (agg['date'] < end)]['WoW_%_cases'],
            agg[(agg['date'] >= start) & (agg['date'] < end)]['WoW_%_vax']
            )        
    
    # Set up plot
    g = sns.lmplot(
        data=agg, 
        x='WoW_%_cases', 
        y='WoW_%_vax', 
        robust=False,         
        legend=legend,
        line_kws=line_kws,
        height=5,
        aspect=1.5/1,
        hue=groupby, 
        palette=list(hue_levels.values()),
        scatter_kws={"alpha": 0.55}    
        )

    # Build legend and populate with results from linear reg
    if groupby != None: 
        ax = g.axes[0, 0]
        ax.legend(bbox_to_anchor=(1,0.75), loc='upper left', frameon=False)
        leg = ax.get_legend()
        L_labels = leg.get_texts()
        
        # Unpack results for each tuple in stats_results and put in legend
        for j in range(len(stats_results)):
            level = list(hue_levels.keys())[j]
            mxb = r'y = {0:.3f}x+{1:.3f}'.format(stats_results[j][0], stats_results[j][1])
            r = 'r: ' + '{:0.2}'.format(stats_results[j][2]) + '  -  R^2: ' + '{:0.2}'.format(stats_results[j][2]**2)
            p = 'p: ' + '{:0.3e}'.format(stats_results[j][3])
            L_labels[j].set_text(level + '\n' + mxb + '\n' + r + '\n' + p + '\n')
    else: # If there's no groupby argument no need to loop through stats_results   
        ax = g.axes[0, 0]
        ax.legend(loc=2)
        leg = ax.get_legend()
        L_labels = leg.get_texts()            
        m = r'y = {0:.3f}x+{1:.3f}'.format(slope,intercept, p_value)
        rval = 'r: ' + '{:0.2}'.format(r_value) + '  -  R^2: ' + '{:0.2}'.format(r_value**2)
        pval = 'p: ' + '{:0.3e}'.format(p_value)
        L_labels[0].set_text( m + '\n' + rval + '\n' + pval)

    # Set chart parameters
    plt.title('How do unvaccinated people respond to increasing caseloads?', fontsize=18, y=1.09)
    plt.suptitle('      ' + suptitle + '. Dates: ' + start + ' to ' + end, fontsize=13, y=1.035)
    plt.xlabel('\nCase growth (% growth in cumulative cases in 7-d window)', fontsize=13)
    plt.ylabel('\n% of unvaxxed population jabbed in 7-d window\n', fontsize=13)
    ax.grid(True, which='both', axis='both', alpha=0.25)   
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))      
    plt.ylim(0.75 * agg['WoW_%_vax'].min(), 1.1 * agg['WoW_%_vax'].max())

    # Save to Output folder
    if SAVE_IMAGES == True:
        if groupby == None:
            gb = 'no_grouping'
        else:
            gb = groupby
        plt.savefig(os.getcwd().split('API-201Z')[0] + 'API-201Z/Outputs/Plots/agg_lm_' +\
            gb + start + '_to_' + end + '.jpeg', 
            bbox_inches = "tight", dpi=150)    

    return g, regression_table(data, groupby, hue_levels, start, end)

###########################
# AGGREGATE THEN JOINTPLOT
##########################

def agg_jp(data, groupby, hue_levels, suptitle, start=START_DATE, end=END_DATE):
    
    # If there's no groupby argument, only aggregate by date. Re-calculate WoW fields and cut to time window
    if groupby == None:
        agg = data.groupby('date')[['cases', 'unvaxxed']].sum().reset_index()
        agg['WoW_%_cases'] = (agg['cases'] - agg['cases'].shift(7)) / agg['cases'].shift(7)
        agg['WoW_%_vax'] = (agg['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg['unvaxxed'].shift(7)
        agg = agg.query('@start <= date <= @end')                
    else: # Otherwise group by groupby and re-calculate WoW fields and cut to time window         
        agg = data.groupby(['date', groupby])[['cases', 'unvaxxed']].sum().reset_index()
        agg['WoW_%_cases'] = (agg['cases'] - agg.groupby([groupby])['cases'].shift(7)) / agg.groupby([groupby])['cases'].shift(7)
        agg['WoW_%_vax'] = (agg.groupby([groupby])['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg.groupby([groupby])['unvaxxed'].shift(7)
        agg = agg.query('@start <= date <= @end')

    p = sns.jointplot(
            data=agg, 
            x='WoW_%_cases', 
            y='WoW_%_vax',                   
            hue=groupby, 
            palette=list(hue_levels.values())            
            )
    
    # Set chart parameters    
    plt.title('How do unvaccinated people respond to increasing caseloads?', fontsize=18, y=1.3, x=2.9, ha='right')
    plt.suptitle('      ' + suptitle + '. Dates: ' + start + ' to ' + end, fontsize=13, y=1.035)
    p.set_axis_labels(
        '\nCase growth (% growth in cumulative cases in 7-d window)',
        '\n% of unvaxxed population jabbed in 7-d window\n', fontsize=13
        )    
    plt.ylim(0.75 * agg['WoW_%_vax'].min(), 1.1 * agg['WoW_%_vax'].max())

    # Save to Output folder
    if SAVE_IMAGES == True:
        if groupby == None:
            gb = 'no_grouping'
        else:
            gb = groupby
        plt.savefig(os.getcwd().split('API-201Z')[0] + 'API-201Z/Outputs/Plots/agg_jp_' +\
            gb + start + '_to_' + end + '.jpeg', 
            bbox_inches = "tight", dpi=150)


def case_and_vax_plot(data, hue_col, hue_levels, title, start, end, axs):

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12,8))
    sns.lineplot(
        data=data.query(' @start <= date <= @end'),
        x='date',
        y='WoW_%_cases',
        hue=hue_col,
        palette=list(hue_levels.values()),
        alpha=0.7,
        ax=axs[0]
    )
    sns.lineplot(
        data=data.query(' @start <= date <= @end'),
        x='date',
        y='WoW_%_vax',
        hue=hue_col,
        palette=list(hue_levels.values()),
        alpha=0.7,
        ax=axs[1]
    )
    axs[0].set_title(title, fontsize=16, y=1.08)
    axs[0].set_xlabel(None)
    axs[1].set_xlabel(None)
    axs[0].tick_params(axis='x', rotation=45)
    axs[1].tick_params(axis='x', rotation=45)
    axs[0].set_ylabel('Case growth', fontsize=12)
    axs[1].set_ylabel('Vaxination growth', fontsize=12)
    axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[0].grid(True, which='both', axis='both', alpha=0.25)   
    axs[1].grid(True, which='both', axis='both', alpha=0.25)  
    import matplotlib.ticker as ticker
    axs[0].xaxis.set_major_locator(ticker.MultipleLocator(7))
    axs[1].xaxis.set_major_locator(ticker.MultipleLocator(7))




def vax_cases_and_correlation(data, groupby, hue_levels, start=START_DATE, end=END_DATE):
    
    fig, ax = plt.subplots(figsize=(16,8))

    sub1 = fig.add_subplot(2,2,2) # two rows, two columns, 2nd cell
    sub2 = fig.add_subplot(2,2,4) # two rows, two columns, 4th cell
    sub3 = fig.add_subplot(2,2,(1,3)) # two rows, two colums, combined first and third cell

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.subplots_adjust(wspace=0.2, hspace=0.2)

    # Create aggregation and lm plot function        
    def agg_reg(data, groupby, hue_levels, ax, start=START_DATE, end=END_DATE, line_kws=None, legend=False):    
        
        # If there's no groupby argument, only aggregate by date. Re-calculate WoW fields and cut to time window
        if groupby == None:
            agg = data.groupby('date')[['cases', 'unvaxxed']].sum().reset_index()
            agg['WoW_%_cases'] = (agg['cases'] - agg['cases'].shift(7)) / agg['cases'].shift(7)
            agg['WoW_%_vax'] = (agg['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg['unvaxxed'].shift(7)
            agg = agg.query('@start <= date <= @end')
            line_kws = {'label':"Linear Reg"}
            legend=True
        else: # Otherwise group by groupby and re-calculate WoW fields and cut to time window         
            agg = data.groupby(['date', groupby])[['cases', 'unvaxxed']].sum().reset_index()
            agg['WoW_%_cases'] = (agg['cases'] - agg.groupby([groupby])['cases'].shift(7)) / agg.groupby([groupby])['cases'].shift(7)
            agg['WoW_%_vax'] = (agg.groupby([groupby])['unvaxxed'].shift(7) - agg['unvaxxed'] ) / agg.groupby([groupby])['unvaxxed'].shift(7)
            agg = agg.query('@start <= date <= @end')
        
        # Iterate through levels of hue_levels, run linear regression, store results in stats_results
        stats_results = []
        if groupby != None:
            for i in range(len(hue_levels.keys())):
                level = list(hue_levels.keys())[i]                
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    agg[(agg[groupby] == level) & (agg['date'] >= start) & (agg['date'] < end)]['WoW_%_cases'],
                    agg[(agg[groupby] == level) & (agg['date'] >= start) & (agg['date'] < end)]['WoW_%_vax']
                    )
                stats_results.append((slope, intercept, r_value, p_value, std_err))
        else: # If groupby argument is empty just run the regression once
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                agg[(agg['date'] >= start) & (agg['date'] < end)]['WoW_%_cases'],
                agg[(agg['date'] >= start) & (agg['date'] < end)]['WoW_%_vax']
                )       
            stats_results.append((slope, intercept, r_value, p_value, std_err))

        if groupby != None:
            for level in agg[groupby].unique():
                # Set up plot
                g = sns.regplot(
                    data=agg[agg[groupby] == level], 
                    x='WoW_%_cases', 
                    y='WoW_%_vax', 
                    robust=False,                    
                    color=hue_levels[level],
                    scatter_kws={"alpha": 0.55},
                    ax=ax 
                    )
        else:
            # Set up plot
            g = sns.regplot(
                data=agg, 
                x='WoW_%_cases', 
                y='WoW_%_vax',                 
                robust=False,                    
                color=list(hue_levels.values())[0],
                scatter_kws={"alpha": 0.55},
                line_kws=line_kws,
                ax=ax 
                )
        
        legend_labels = []
        for j in range(len(stats_results)):
            level = list(hue_levels.keys())[j]
            mxb = r'y = {0:.3f}x+{1:.3f}'.format(stats_results[j][0], stats_results[j][1])
            r = 'r: ' + '{:0.2}'.format(stats_results[j][2]) + '  -  R^2: ' + '{:0.2}'.format(stats_results[j][2]**2)
            p = 'p: ' + '{:0.3e}'.format(stats_results[j][3])
            legend_labels.append(level + '\n' + mxb + '\n' + r + '\n' + p + '\n')
        
        ax.grid(True, which='both', axis='both', alpha=0.25)   
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))   
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))     
        plt.xlabel('\nCase growth (% growth in cumulative cases in 7-d window)', fontsize=12)
        plt.ylabel('\n% of unvaxxed population jabbed in 7-d window', fontsize=12)
        plt.title('Correlation Between Cases & Vaccinations', fontsize=16, y=1.04)
        
        return g, legend_labels

    case_and_vax_plot(
        data=data, 
        hue_col=groupby, 
        hue_levels=hue_levels, 
        title='Case and Vaccination Growth: ' + start + ' to ' + end, 
        start=start, 
        end=end,
        axs=(sub1, sub2)
        )
    
    ar = agg_reg(data, groupby, hue_levels, start=start, end=end, ax=sub3)
    ar
    sub3.legend(
        ar[1],
        bbox_to_anchor=(1,0.75), 
        loc='upper left', 
        frameon=False
    )
        
    plt.setp(ax.get_xticklabels(), fontsize=0)
    plt.setp(ax.get_yticklabels(), fontsize=0)
    plt.setp(ax.xaxis.get_ticklines(), 'markersize', 0)
    plt.tight_layout()