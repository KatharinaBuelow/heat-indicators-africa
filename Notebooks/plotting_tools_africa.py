#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr

def savefig(plot, name, dpi):
    plot.savefig(name, dpi=dpi, bbox_inches='tight')
    print('plot ist saved in : ', name)

def directory_available(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def add_unit(data,var):
     
    '''Some indices do not have a unit,
    for example number of Heatwave, Hotspell'''

    if var in ['HSf','HWf']:
        data[var].attrs['units'] = 'Number'
    else:
        print('nothing to do, unit exists')
    return


def plot_6diff(
        sims_rcp26,
        sims_rcp85,
        robust_rcp26,
        robust_rcp85,
        level_steps_diff, 
        color_steps_diff,
        what,
        robust,
        plotdir,
        title="",
        var="",
        robustness=None,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    
    # Some graphical features:
    # set the colors:
    
    levels=level_steps_diff
    colors=color_steps_diff
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})
    
    #from matplotlib.colors import ListedColormap
    #colors = ListedColormap(color_steps_diff)
    #colors.set_bad(color="green")
    #colors.set_under(color="white")
    #vmin=0.5
    
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
}

    # Create subplots
    fig, axes = plt.subplots(
            ncols=3, nrows=2, figsize=(10,7), subplot_kw={'projection': ccrs.PlateCarree()}) 
    # Space between rows:
    #fig.subplots_adjust(hspace=0.3)
   
    for row in axes:
        for ax in row:
            ax.gridlines(
                draw_labels={"bottom": "x", "left": "y"}, 
                dms=True,
                x_inline=False, 
                y_inline=False,
                linewidth=0.5,
            )
            ax.coastlines(resolution="50m", color="black", linewidth=1)
            ax.add_feature(cf.BORDERS)
            ax.set_extent([-20,60,-35,35])

    # Plot data for rcp26
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
    
        # Select labels // Units frome metadata
        # Set title of plot
        varname=data[var].long_name
        add_unit(data,var)
        unit=data[var].units
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        if robustness is True:
            robust_rcp26=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp26)
            datar_variable = datar[var]  
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                        ax=axes[0,i],
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )

        axes[0, i].set_title(f'RCP26: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        
        data_variable = data[var]
        
        #data_variable = data['SU35'].dt.days
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        
        if robustness is True:
            robust_rcp85=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp85)
            datar_variable = datar[var]
            #datar_variable = datar['SU35']
            #plt.rcParams.update({'hatch.color': hatchcolor})
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                    ax=axes[1,i],
                    levels=[-.5, .5],
                    colors='none',
                    hatches=[ None,None,"//", ],
                    add_colorbar=False,
                    extend='both',
                    transform=ccrs.PlateCarree()
            )
        axes[1, i].set_title(f'RCP85: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_change.png".format(plotdir, var)

    savefig(plt, "{}".format(name),300) # dpi should be 1200 for a publication
    return
