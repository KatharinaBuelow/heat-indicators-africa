# Heat Indicators Africa

This repository documents the procedure, how the maps of climate heat indicator for africa on the basis of [CORDEX AFR-22](https://cordex.org/experiment-guidelines/cordex-cmip5/cordex-core/cordex-core-simulations/) data got developed.

## [Environment](ENVIRONMENT.md)


## Different heat indicators got calculated:

* Number of Heatdays for different temperature thresholds
* Heatwave frequency, maximum length and number of days in heatwaves
* Warm spell duration index

For the calculation [index_calculator](https://github.com/climate-service-center/index_calculator) is used. This is using [xclim](https://github.com/Ouranosinc/xclim)

### Time slices

Reference time period is 1981-2010.
	 

### Plotting:

If you like to plot the horizontal differences to the reference periode
use
	Notebooks/horiplot-heat-indicator-diff-robust.ipynb
	Notebooks/plotting_tools_africa.py



## Area mean plots

Starting with implementing the [region](REGION.md) in climate fact data.
After calculation the area mean of the region,
you can plot with the following Notebboks:

timeseries_TG_WASCAL_for_bulletin.ipynb



# Specialties:

### Humidex

Humidex is calculate using xclim some information from xclim/indices_conversion.py

The humidex indicates how hot the air feels to an average person, accounting for the effect of humidity. It
    can be loosely interpreted as the equivalent perceived temperature when the air is dry.
    
The humidex *comfort scale* :cite:p:`canada_glossary_2011` can be interpreted as follows:

    - 20 to 29 : no discomfort;
    - 30 to 39 : some discomfort;
    - 40 to 45 : great discomfort, avoid exertion;
    - 46 and over : dangerous, possible heat stroke;


References can be found in the sub directory literature



Humidex is made for houly input, we used daily mean tas and hurs


