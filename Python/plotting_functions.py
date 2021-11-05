# Import libraries from libraries.py

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
        x=pd.to_datetime(start_date), 
        ymin=min(data[y]), 
        ymax=1.1 * np.nanmax(data[data[y] != np.inf][y]), 
        color='gray', 
        alpha=0.4, 
        linestyle='dashed'
        )
    ax.vlines(
        x=pd.to_datetime(end_date), 
        ymin=min(data[y]), 
        ymax=1.1 * np.nanmax(data[data[y] != np.inf][y]), 
        color='gray', 
        alpha=0.4, 
        linestyle='dashed'
        )
    ax.axvspan(
        pd.to_datetime(start_date), 
        pd.to_datetime(end_date), 
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
    if save_images == True:
        plt.savefig(''\
            + title.replace(' ', '_') + hue_col.replace(' ', '_') + '.jpeg', 
            bbox_inches = "tight", dpi=150)

        
        
        

# Create lmplot function to combine scatterplot & regress
def lm(data, x, y, hue, hue_levels, columns, title, xlabel, ylabel, yformat=None, xformat=None, rows=None, col_order=None, size=2, alpha=0.1, robust=True):    
    
    # Create plot
    g = sns.lmplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        scatter=True,    
        robust=robust,        
        n_boot=100,
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
    if save_images == True:
        plt.savefig(''\
            + title[0].replace(' ', '_') + hue.replace(' ', '_') + '.jpeg', 
            bbox_inches = "tight", dpi=150)


        
        
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
    if save_images == True:
        plt.savefig('Output'\
            + title[0].replace(' ', '_') + hue.replace(' ', '_') + '.jpeg', 
            bbox_inches = "tight", dpi=150)
        
