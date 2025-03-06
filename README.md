# Heat Indicators Africa

This repository documents the procedure, how the maps of climate heat indicator for africa on the basis of [CORDEX AFR-22](https://cordex.org/experiment-guidelines/cordex-cmip5/cordex-core/cordex-core-simulations/) data got developed.


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




