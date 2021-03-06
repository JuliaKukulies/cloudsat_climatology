
## This script reads in 2B-GEOPROF data and creates CFAD based on radar reflectivity 

import h5py
import numpy as np
import glob 
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors


# -------------------DEFINE FUNCTIONS--------------------

# read in hdf5-files and write to numpy arrays
def read_in_hdf5_files(file):
    dset= h5py.File(file,'r+')
    variable_list = [] # stores profile variables, shape=x*125 
    param_list= [] # stores additional info, shape= x*1
    # choose parameters here
    params= ['Latitude', 'Longitude', 'DEM_elevation']
    variables= ['CPR_Cloud_mask', 'Radar_Reflectivity', 'Height']
    for i in params:
        param_list.append( np.array(dset[str(i)]))
    for v in variables:
        variable_list.append(np.array(dset[str(v)]))

    print(len(np.array(param_list)))

    param_arr= np.array(param_list)  # array which is stores all parameter values in 2D hdf5 file:  nr(params) x nr(datafields)
    variable_arr= np.array(variable_list) # array which stores all variables from cloud profiles with vertical resolution:  nr(variables) x nr(datafields) x 125
    variable_arr=variable_arr.squeeze()
    lats= param_arr[0]
    lons= param_arr[1]
    dem= param_arr[2]
    cpr= variable_arr[0]
    param= variable_arr[1]
    height=variable_arr[2]

    # define fill values for no data 
    param[param == -8888]=np.nan
    param[param > 16000]=np.nan

    return param, height, dem, lats, lons, cpr 

def extract_domain(param,lons,lats,dem, cpr):
    iteration=0
    param_TP=[]
    cpr_TP=[]
    lat1= 27 # change coordinates for different subregions 
    lat2= 30
    lon1= 70
    lon2= 105
    # select smaller domain
    for i,value in enumerate(lons):
        if lats[i] >= lat1 and lats[i] <= lat2 and value >= lon1 and value < lon2 and dem[i] >= 3000:
            iteration=iteration+1
            param_TP.append(param[i])
            cpr_TP.append(cpr[i])

    if iteration==0:
        print(file, "this file does not contain data within the study domain")
        param_TP= -9999

    else:
        param_TP= np.array(param_TP)
        cpr_TP= np.array(cpr_TP)
        print(param_TP.shape)
    return param_TP, cpr_TP



def calculate_cfad(param_TP, cfad, total_nr):
    count_low_radar= 0 
    print(param_TP.shape, 'profile processed')
    for y,profile in enumerate(param_TP):
        for x,val in enumerate(profile):     # loop through bins in profile 
            #print('value', val)
            if val < 0  or val > 0:          # avoid nan and 0 values
                if cpr_TP[y,x] >= 30 and val > -3000:     # include only cloudy profiles
                    total_nr +=1
                    ind= int((val*0.01+30))  # convert value of radar reflectivity into index in cfad matrix
                    if ind >= 12*5:  # set maximum
                        #print(val, 'value larger than 30 dbZ')
                        ind= 11*5
                    if ind < 0:  # set minimum 
                        ind= 0 
                    cfad[x,ind]+= 1    # calculate number of samples in each altitude-reflectivity bin
                else:
                    count_low_radar += 1

    return cfad, total_nr, count_low_radar



def plot_cfad(cfad_matrix, output):
    cfad_matrix= cfad_matrix[::-1]
    plt.figure(figsize=(20, 15))
    cmap= plt.cm.get_cmap('magma_r')
    plt.pcolormesh( cfad_matrix*100, cmap=cmap, vmin= 0.000001, vmax= 0.20)
    cmap.set_under(color='white')
    labels= [0, 2.4, 4.8, 7.2, 9.6, 12.0, 14.4, 16.8, 19.2, 21.6]
    plt.yticks([21, 31,41,51,61,71,81,91,101,111],labels)
    xlabels= np.linspace(-30,30,7)
    xticks= np.arange(7)*2*5
    plt.xticks(xticks,xlabels)
    plt.ylim((21,120))
    levels= np.array([0, 0.05, 0.1, 0.15, 0.2,0.25,  0.3, 0.35, 0.4,0.45,  0.5, 0.55 ])/2.5
    cbar= plt.colorbar(spacing='uniform', orientation= 'vertical', ticks= levels, boundaries= levels, extend= 'max')
    bounds=levels
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors= 256)

    cbar.solids.set_edgecolor('face')
    cbar.set_label('Frequency [%]', fontsize= 40)

    plt.xlabel('Reflectivity [dBZ]')
    plt.ylabel('Height [km]')
    plt.rcParams.update({'font.size': 50}) 
    plt.rcParams.update({'axes.linewidth': 4.0})
    plt.savefig(output)
    plt.close()


#--------------MAIN PROGRAM----------------------

# for all julian days 
days= np.arange(366)+1
days= days.astype(str)

# define output directory 
output= '/home/juli/Desktop/Sverige/Atmospheric_Science/Master_thesis/plots/CLOUDSAT/CFAD/cfad_radar_reflect_monsoondomain_JJA_daytime.png'

cfad= np.zeros((125,12*5))
total_nr= 0

# loop through all files (for all year) 
for d in days:
    path= '/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2B_GEOPROF/????/????_*_*_'+d+'_day.hdf5'
    files_by_day= glob.glob(path)
    for file in files_by_day:
        print(file)
        param, height, dem, lats, lons, cpr= read_in_hdf5_files(file)
        param_TP, cpr_TP= extract_domain(param,lons,lats,dem, cpr)
        if np.nanmean(param_TP) !=  -9999:
            cfad, total_nr, count_low_radar= calculate_cfad(param_TP, cfad, total_nr)
    cfad_matrix= cfad/total_nr

plot_cfad(cfad_matrix, output)














