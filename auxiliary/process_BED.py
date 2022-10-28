import glob


def get_mean_vertical_profile_from_BED(csv_files, varname, season, min_date = None, max_date = None, delimiter = " "):

    import pandas as pd
    import glob
    import xarray as xr
    import numpy as np

    depths = []
    nsamples = []
    stds = []
    values = []
        
    for csvf in csv_files:

        # read in the csv file
        if delimiter == " ":
            df = pd.read_csv(csvf, delim_whitespace=True)
        else:
            df = pd.read_csv(csvf, delimiter=delimiter)
        
        samples = []
        
        for i, dnr in enumerate(df["Dnr"]): 
        
            date = int(str(df["Year"][i])+str("{month:02d}").format(month = df["Month"][i])+str("{day:02d}").format(day = df["Day"][i]))
            
            #print(date)        
            if min_date is not None and date < min_date:
                continue
                
            if max_date is not None and date > max_date:
                continue
                
            if (season != "") and (str(df["Month"][i]) not in season.replace(" ","").split(",")):
                continue
            
            samples.append(df["Average"][i])

        samples = np.array(samples)
        nsamples.append(samples.size)
        stds.append(samples.std())
        values.append(samples.mean())
        depths.append(float(csvf.split(".")[-2][-3:]))
        
    if not depths:
        return None
    
    ds = xr.Dataset({varname : (("depth"), values),
                     varname+"_STD" : (("depth"), stds),
                     "nsamples" : (("depth"), nsamples)
                    },
                    coords = {"depth" : depths})
    
    return ds

def process_BED(variables, results_dir, from_date, to_date):
    import glob
    for var in variables.keys():
        
        try:
            ref_file_pattern = variables[var]["BED-reference-file-pattern"]
        except:
            print("No BED reference given for variable "+var)
            continue

        seasons = variables[var]["seasons"]
        stations = variables[var]["stations"]

        ref_files = glob.glob(ref_file_pattern)

        for station in stations:

            try:
                station_names = variables[var]["stations"]["alternative-names"]
                for name in station_names:
                    for rf in ref_files:
                        if name in rf:
                            station_name = name
                            break
            except:
                station_name = station
                    
            station_ref_files = [s for s in ref_files if station_name in s]

            if not station_ref_files:
                print("No reference files found for variable "+var+" and station "+station)
                continue

            for season in seasons.keys():
                bed_data = get_mean_vertical_profile_from_BED(station_ref_files, var, min_date=from_date, max_date=to_date, season=seasons[season])
                if bed_data is None:
                    continue
                    
                bed_data.to_netcdf(results_dir+"/"+var+"-"+station+"-"+season+".nc")