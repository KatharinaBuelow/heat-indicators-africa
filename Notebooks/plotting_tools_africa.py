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

def get_variable(data,var):
    '''Change the variable of absolute Temperature and unit for plotting'''
    
    if var =='TG':
        data_variable = data[var]-273.15

        data[var].attrs['units']='degree Celsius'
    else:
        data_variable = data[var]

    return data_variable
   

def plot_4diff(
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
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    
    levels=level_steps_diff
    colors=color_steps_diff
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})
        
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
        }

    if westafrica is True:
        height=5.5
    else:
        height=7.5

    # Create subplots
    fig, axes = plt.subplots(
            ncols=2, nrows=2, figsize=(7,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
       
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

             #west Afrika
            #lon : -25.87 to 20 by 0.11 degrees
            #lat : -0.75 to 27.3 by 0.11 degrees
            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
                # Space between rows:
                fig.subplots_adjust(hspace=0.03)
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])

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
                 x=0.5,
                 position=(0.5, 0.99),
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

        axes[0, i].set_title(f'RCP26: {file.split("_")[4]}-{file.split("_")[5]}',fontsize=12)

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
        axes[1, i].set_title(f'RCP85: {file.split("_")[4]}-{file.split("_")[5]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_diff-robust_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return


def plot_6absolut(
        sims_rcp26,
        sims_rcp85,
        level_steps, 
        color_steps,    
        plotdir,
        title="",
        var="",
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels=level_steps
    colors=color_steps
    
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
    }

    if westafrica is True:
        height=5
    else:
        height=7

    
    # Create subplots
    fig, axes = plt.subplots(
            ncols=3, nrows=2, figsize=(10,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
  
    
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
            
            #west Afrika
            #lon : -25.87 to 20 by 0.11 degrees
            #lat : -0.75 to 27.3 by 0.11 degrees
            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data for rcp26
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        #cha_var(data,var)
        data_variable=get_variable(data,var)
        #data_variable = data[var]
    
        # Select labels // Units frome metadata
        # Set title of plot
        varname=data[var].long_name

        add_unit(data,var)
        unit=data[var].units
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.99)
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )

        axes[0, i].set_title(f'RCP26: {file.split("_")[4]}-{file.split("_")[5]}',fontsize=12)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        #cha_var(data,var)
        #data_variable = data[var]
        data_variable=get_variable(data,var)
        
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
        
        axes[1, i].set_title(f'RCP85: {file.split("_")[4]}-{file.split("_")[5]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_absolut_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi)
    return



def plot_3absolut(
        sim_era5,
        sim_evaluation,
        sim_historical,
        level_steps,
        color_steps,
        plotdir,
        title="",
        var="",
        ):
    from cartopy import crs as ccrs
    import cartopy.feature as cf

    # Some graphical features:
    # set the colors:

    levels = level_steps
    colors = color_steps

    font = {
        'family': 'sans-serif',
        'weight': 'normal',
    }

    # Create subplots
    fig, axes = plt.subplots(
        ncols=3, nrows=1, figsize=(10, 3), subplot_kw={'projection': ccrs.PlateCarree()})
    #all of Africa
        #ncols=3, nrows=1, figsize=(10, 3.5), subplot_kw={'projection': ccrs.PlateCarree()})

    for ax in axes:
        ax.gridlines(
            draw_labels={"bottom": "x", "left": "y"},
            dms=True,
            x_inline=False,
            y_inline=False,
            linewidth=0.5,
        )
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        #ax.set_extent([-20, 60, -35, 35])
        #west Afrika
        #lon : -25.87 to 20 by 0.11 degrees
        #lat : -0.75 to 27.3 by 0.11 degrees
        ax.set_extent([-25, 20, -0.75, 27.3])

    # Plot era5 data
    data = xr.open_dataset(sim_era5,decode_timedelta=False)
    
    # Select labels // Units frome metadata
    # Set title of plot
    varname=data[var].long_name

    if var =='TG':
        data_variable = data[var]-273.15
        unit='degree Celsius'
    else:
        data_variable = data[var]
        unit=data[var].units
        add_unit(data,var)
      
    s = "{} {}".format(title,varname)
    
    fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5
                 )  
    
    im = data_variable.plot(ax=axes[0],
                       levels=levels,
                       colors=colors,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                       )
    axes[0].set_title(f'ERA5:',fontsize=12)

# Plot evaluation data
    data = xr.open_dataset(sim_evaluation,decode_timedelta=False)
        
    if var =='TG':
        data_variable = data[var]-273.15
    else:
        print('nothing to do')
        
    im = data_variable.plot(ax=axes[1],
                       levels=levels,
                       colors=colors,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                       )
    axes[1].set_title(f'Evaluation:',fontsize=12)

# Plot historical data
    data = xr.open_dataset(sim_historical,decode_timedelta=False)
        
    if var =='TG':
        data_variable = data[var]-273.15
    else:
        print('nothing to do')
        
    im = data_variable.plot(ax=axes[2],
                       levels=levels,
                       colors=colors,
                       transform=ccrs.PlateCarree(),
                       extend="both",#"neither",
                       add_colorbar=False,
                       )
    axes[2].set_title(f'historical:',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.05])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_change.png".format(plotdir, var)

    savefig(plt, "{}".format(name),300) # dpi should be 1200 for a publication
    
    return