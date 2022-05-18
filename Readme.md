# Purpose, Description

This is the repository for basic postprocess tasks for the individual models. 
The goal is to provide scripts for
 * processing the raw model output into the format "1 file per variable"
 * creating basic plots of seansonal means and time series for 
   * stations (specific coordinates)
   * regions (rectangles)
   * compare to given reference data
 * performing model specific tasks as
   * preparing ocean model's output for Hagen Radtke's validator, 
     see https://openresearchsoftware.metajnl.com/articles/10.5334/jors.259/ 
     and https://github.com/hagenradtke/validator
   * generate forcings for MOM5 from the CCLM output

Each user can add his/her own customized postprocess tasks as described at
https://sven-karsten.github.io/iow_esm/usage/create_postprocess_task.html.


# Authors
    
* SK      (sven.karsten@io-warnemuende.de)


# Versions

## 1.01.02 (in preparation)

| date        | author(s)   | link                                                                            |
|---          |---          |---                                                                              |
| 2022-05-18  | SK          | XXX |   

<details>

### changes
* fixed bug in using the cdo showname operator
* allow for mean over total time period by using empty month list
* committed more general global settings
    
### dependencies
* python environment as anaconda3 or miniconda3
* cdo, nco, (texlive), see load module scripts for your target
  
### known issues
* plotting on HLRN Berlin not yet possible due to missing python module basemap
  * can be circumvented by creating own conda environment via
  ``` bash
  module load anaconda3/2019.10
  conda init bash
  conda create --name plotting
  conda activate plotting
  conda install basemap
  conda install netCDF4
  conda install xarray
  ```
  and adding `conda activate plotting` to your local `load_modules.sh` on blogin
* plotting time series on HLRN Göttingen with calendar "proleptic_gregorian" might be a problem

### tested with
* intensively tested on Berlin's (with workaround) and on Göttingen's HLRN machine on MOM5 and CCLM output
  
</details>

## 1.01.01 (latest release)

| date        | author(s)   | link                                                                            |
|---          |---          |---                                                                              |
| 2022-05-04  | SK          | [1.01.01](https://git.io-warnemuende.de/iow_esm/postprocess/src/branch/1.01.01) |   

<details>

### changes
* fixed bug in using the mppncombine tool in MOM5/mppncombine/mppncombine.py
  * the first IO rectangle was not merged to the others
  * was not visible with 8nm MOM5 setup since this there was no data in this rectangle
    
### dependencies
* python environment as anaconda3 or miniconda3
* cdo, nco, (texlive), see load module scripts for your target
  
### known issues
* plotting on HLRN Berlin not yet possible due to missing python module basemap
  * can be circumvented by creating own conda environment via
  ``` bash
  module load anaconda3/2019.10
  conda init bash
  conda create --name plotting
  conda activate plotting
  conda install basemap
  conda install netCDF4
  conda install xarray
  ```
  and adding `conda activate plotting` to your local `load_modules.sh` on blogin

### tested with
* intensively tested on Berlin's (with workaround) and on Göttingen's HLRN machine on MOM5 and CCLM output
  
</details>

## 1.01.00

| date        | author(s)   | link                                                                            |
|---          |---          |---                                                                              |
| 2022-04-27  | SK          | [1.01.00](https://git.io-warnemuende.de/iow_esm/postprocess/src/branch/1.01.00) |   

<details>

### changes
* added task generate_mom_forcing to CCLM's tasks
  * task creates forcing for the MOM5 ocean model according to transformation given
      Thomas Neumann's scripts
  * splitted process_raw_output task for MOM5
    * mppncombine does merging of MOM's output
    * split_files generates subsequently "1 file per variable" pattern
* fixed file ending .nc in CCLM/process_raw_output for total rain variable
* fixed plotting of standard deviation in time series
* remove results directory when rerunning a task
* if no units are specified, arbitrary units "a.u." appear in the plot
    
### dependencies
* python environment as anaconda3 or miniconda3
* cdo, nco, (texlive), see load module scripts for your target
  
### known issues
* plotting on HLRN Berlin not yet possible due to missing python module basemap
  * can be circumvented by creating own conda environment via
  ``` bash
  module load anaconda3/2019.10
  conda init bash
  conda create --name plotting
  conda activate plotting
  conda install basemap
  conda install netCDF4
  conda install xarray
  ```
  and adding `conda activate plotting` to your local `load_modules.sh` on blogin

### tested with
* intensively tested on Berlin's (with workaround) and on Göttingen's HLRN machine on MOM5 and CCLM output
  
</details>


## 1.00.00 

| date        | author(s)   | link                                                                              |
|---          |---          |---                                                                                |
| 2022-01-31  | SK          | [1.00.00](https://git.io-warnemuende.de/iow_esm/postprocess/src/branch/1.00.00)   |     

<details>

### changes
* initital release
  * configured variables can be plotted and compared to a reference 
    via seasonal means and time series for stations and regions
    
### dependencies
* python environment as anaconda3 or miniconda3
* cdo, nco, (texlive), see load module scripts for your target
  
### known issues
* plotting on HLRN Berlin not yet possible due to missing python module basemap

### tested with
* intensively tested on Göttingen's HLRN machine on MOM5 and CCLM output

</details>