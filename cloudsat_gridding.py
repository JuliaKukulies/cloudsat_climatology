
## This script reads in a specified CloudSat data product (file format:HDF5) and creates monthly gridded datasets from profile samples

import h5py
import numpy as np
import glob

# ----------------------------------------------------------------------DEFINE FUNCTIONS-----------------------------------------------------------------------------------------------


# define empty grid: means=  25 (lats) x 40 (lons) x 125 vertical

def empty_grid():
    means=np.zeros((25,40,125))
    means[ means == 0 ]= np.nan
    bin_counts= np.zeros((25,40, 125))   # counts number of valid bin in profile 
    prof_count= np.zeros((25,40)) # counts number of profiles in grid point 
    return means, bin_counts, prof_count


# method to convert original coordinates of CPR/CALIOP footprint into new grid point coordinates and corresponding index new grid matrix 
def convert_coordinates(lats,lons):
    lats_ind=np.linspace(20,44,25)
    new_lats=np.zeros(lats.shape)
    for i,e in enumerate(lats):
        new_coord= round(float(e),0) # round coordinate to only one decimal
        if new_coord > e or new_coord == 45.0:
            new_coord= round (new_coord - 1, 0)
        cond= np.isclose(lats_ind, [new_coord])
        new_lats[i]=int(np.where(cond == True)[0]) # convert coordinate to corresponding row index in output grid
        new_lats= new_lats.astype(int)

    lons_ind=np.linspace(70, 109, 40 )
    new_lons=np.zeros(lons.shape)
    for j,v in enumerate(lons):
        new_coord= round(float(v),0) 
        if new_coord > v or new_coord == 110.0 :
            new_coord= round (new_coord - 1, 0)
        cond= np.isclose(lons_ind, [new_coord])
        new_lons[j]=int(np.where(cond == True)[0]) # convert coordinate to corresponding column index in output grid
        new_lons= new_lons.astype(int)

    return new_lats, new_lons, lats_ind, lons_ind

# create sum of two arrays where single nan occurence treated as 0 and double nan occurence treated as nan (to control distinction between 0 and nan values in output grid)
def sum_nan_arrays(a,b):
    ma = np.isnan(a)
    mb = np.isnan(b)
    return np.where(ma&mb, np.nan, np.where(ma,0,a) + np.where(mb,0,b))


# read in hdf5-files and write to numpy arrays
def read_in_hdf5_files(path):
    dset= h5py.File(file,'r+')
    variable_list = [] # stores profile variables, shape=x*125 
    param_list= [] # stores additional info, shape= x*1
    # choose parameters here
    params= ['Latitude', 'Longitude', 'DEM_elevation' ]
    variables= ['CPR_Cloud_mask']
    for i in params:
        param_list.append( np.array(dset[str(i)]))
    for v in variables:
        variable_list.append(np.array(dset[str(v)]))

    param_arr= np.array(param_list)  # array which is stores all variables values in 2D hdf5 file:  nr(params) x nr(datafields)
    variable_arr= np.array(variable_list)
    variable_arr=variable_arr.squeeze()
    variable_arr[variable_arr < 0 ]= np.nan # define nan values (-9999 in original HDF files)
    lats= param_arr[0]
    lons= param_arr[1]
    dem= param_arr[2]
    param= variable_arr[0]
    # define more profile parameters, if data products contains more than one that is needed 
    return variable_arr, lats, lons, dem, param






#loop through all profiles and calculate means for new grid 
def gridcell_means(param,new_lats,new_lons, bin_counts, prof_count):
    print('param shape ', param.shape)
    for ind,p in enumerate(param):
        means[int(new_lats[ind]),int(new_lons[ind]) ] = sum_nan_arrays( means[int(new_lats[ind]),int(new_lons[ind]) ],  param[ind])
        if np.isnan(param[ind])[np.isnan(param[ind]) == True].size != 125:
            #prof_count counts only valid profiles for one grid point
            prof_count[int(new_lats[ind]), int(new_lons[ind]) ] += 1
        for cell in np.arange(125):
            if param[ind, cell] > 0:
                bin_counts[int(new_lats[ind]), int(new_lons[ind]), cell] += 1

        return bin_counts, prof_count

        # uncomment for gridding of columnintegrated parameters (e.g. cloud occurrence frequency)
        # for  ind,p in enumerate(param):
        #     counts[int(new_lats[ind]),int(new_lons[ind]) ]  += 1
        #     if np.nanmean(p) > 0:
        #         means[int(new_lats[ind]),int(new_lons[ind]) ] += 1


def create_grid(means,bin_counts):
    rows= 25
    columns= 40
    bins= 125

    for i in range(rows):
       for j in range(columns):
           for b in range(bins):
               if  bin_counts[i,j,b] != 0:  # avoid 0-divide 
                   means[i, j, b]= means[i,j, b]/ bin_counts[i,j,b]
    print('new matrix shape', means.shape)
    return means


def write_newfile(m, means):
    # change output path 
    f= h5py.File('/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2B_GEOPROF/gridded_data/2B_GEOPROF_month'+m+'_grid.hdf5', "w")
    dset= f.create_dataset("CloudFraction_CPR", ((25,40, 125)))
    dset[...]= means

    dset.dims[0].label = 'lat'
    dset.dims[1].label = 'lon'
    dset.dims[2].label = 'height'

    f.close()
    print('new file for month ',m, '  created.')

    
#--------------------------------------------------------------------------------------------MAIN PROGRAM ---------------------------------------------- ---------------------------------------------------

month= np.arange(12)+1
month= month.astype(str)

for m in month:
    path= '/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2B_GEOPROF/????/????_*_'+m+'_*.hdf5' # define path to respective data product (file names: yyyy_mm_dd_day/night.hdf5)
    means, bin_counts, prof_count= empty_grid()
    files_by_month= glob.glob(path)
    for file in files_by_month:
        print(file)
        param,lats,lons,dem,variables_arr= read_in_hdf5_files(path)
        new_lats,new_lons, lats_ind, lons_ind =convert_coordinates(lats,lons)
        bin_counts,prof_count=gridcell_means(param,new_lats,new_lons,bin_counts,prof_count)
    means=create_grid(means,bin_counts)
    write_newfile(m, means)


































