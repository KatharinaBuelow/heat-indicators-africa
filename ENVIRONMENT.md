# ENVIRONMENT:

## For potting the horizontal plots

I executed the following steps to built my environment by installing e.g. [pyhomogenize](https://github.com/climate-service-center/pyhomogenize)and [py-cordex](https://github.com/euro-cordex/py-cordex):

  conda create --name afrheat python==3.10
  conda activate afrheat
  conda install -c conda-forge py-cordex
  pip install pyhomogenize
  pip install matplotlib
  pip install seaborn
  pip install cartopy





## For calculating the area mean

I need a nice environment to use [climat_fact_data](https://codebase.helmholtz.cloud/gerics_infrastructure/climate_fact_data)

 conda create --name cfworld python==3.10
 conda activate cfworld
 conda install -c conda-forge xesmf
 conda install -c conda-forge cartopy
 pip install xweights
 
Go to [climate_fact_data](https://codebase.helmholtz.cloud/gerics_infrastructure/climate_fact_data/-/tree/main) and create a branch.

..contine with creating a [new region](REGION.md)

 