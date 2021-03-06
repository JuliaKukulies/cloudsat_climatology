## This creates new HDF5 files containing the profiles within the TP domain for the CLoudSat product 2C- ICE 

from pyhdf.HDF import *
from pyhdf.VS import *
from pyhdf.SD import *
import pprint
import glob 
import numpy as np


#---------- Read HDF Files (VD data) ----------#


# use glob in loop for open all files in directory
days= np.arange(135)+232
days= days.astype(str)

# add zeros to day names 
for idx, d in enumerate(days):
    if int(d) < 100:
        days[idx]= '0'+d
    if int(d) < 10:
        days[idx]= '00'+d


for day in days:
    data= "/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2C-ICE/2009/2009*"+day+"????????????_CS_2C-ICE_GRANULE_P1_R04_E??.hdf"
    all_files= glob.glob(data)

    for file in all_files:
        f = HDF(file)
        print(file)

        # getting vdata 
        vs = f.vstart()
        Latitude = vs.attach('Latitude')
        Longitude = vs.attach('Longitude')
        Profile_time = vs.attach('Profile_time')
        UTC_start = vs.attach('UTC_start')
        DEM_elevation = vs.attach('DEM_elevation')

        Optical_depth= vs.attach('optical_depth')
        Ice_water_path= vs.attach('ice_water_path')
        Optical_depth_unc= vs.attach('optical_depth_uncertainty')
        Ice_water_path_unc= vs.attach('ice_water_path_uncertainty')

        lats = Latitude[:]
        lons = Longitude[:]
        profile_time= Profile_time[:]
        utc_start= UTC_start[:]
        dem= DEM_elevation[:]

        optical_depth= Optical_depth[:]
        ice_water_path= Ice_water_path[:]
        optical_depth_uncertainty= Optical_depth_unc[:]
        ice_water_path_uncertainty= Ice_water_path_unc[:]

        Latitude.detach() # "close" the vdata
        Longitude.detach() # "close" the vdata
        Profile_time.detach()
        UTC_start.detach()
        DEM_elevation.detach()

        Optical_depth.detach()
        Optical_depth_unc.detach()
        Ice_water_path.detach()
        Ice_water_path_unc.detach()

        vs.end() # terminate the vdata interface
        f.close()

        # obtain data from all datasets and write to numpy arrays
        dataset = SD(file,SDC.READ )

        # print info about dataset
        print(dataset.info())
        # print names of SDS (scientific datasets)
        datasets_dic= dataset.datasets()

        # 2C-ICE VARIABLES 
        height_data=dataset.select('Height')
        height= height_data.get()

        temp_data= dataset.select('Temperature')
        temp= temp_data.get()

        iwc_data= dataset.select('IWC')
        iwc= iwc_data.get()
        EXT_coef_data= dataset.select('EXT_coef')
        EXT_coef= EXT_coef_data.get()
        re_data= dataset.select('re')
        re= re_data.get()

        iwc_data_uncertainty= dataset.select('IWC_uncertainty')
        iwc_uncertainty= iwc_data_uncertainty.get()
        EXT_coef_data_uncertainty= dataset.select('EXT_coef_uncertainty')
        EXT_coef_uncertainty= EXT_coef_data_uncertainty.get()
        re_data_uncertainty= dataset.select('re_uncertainty')
        re_uncertainty= re_data.get()


        # Extract data for TP domain -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        latitudes=[]
        longitudes=[]
        dem_TP=[]
        temp_TP=[]
        profile_time_TP= []
        utc_start_TP= []


        height_TP=[]
        iwc_TP=[]
        EXT_coef_TP=[]
        ice_water_path_TP=[]
        re_TP=[]
        optical_depth_TP=[]

        iwc_uncertainty_TP=[]
        EXT_coef_uncertainty_TP=[]
        ice_water_path_uncertainty_TP=[]
        re_uncertainty_TP=[]
        optical_depth_uncertainty_TP=[]


        for i,value in enumerate(lons):
            if value < -180:
                lons[i]= np.nan
            if value >= 70 and value <= 110:
                if lats[i] >= 20 and lats[i] <= 45:
                    latitudes.append(lats[i])
                    longitudes.append(value)
                    dem_TP.append(dem[i])
                    temp_TP.append(temp[i])
                    profile_time_TP.append(profile_time[i])


                    height_TP.append(height[i])
                    iwc_TP.append(iwc[i])
                    EXT_coef_TP.append(EXT_coef[i])
                    ice_water_path_TP.append(ice_water_path[i])
                    re_TP.append(re[i])
                    optical_depth_TP.append(optical_depth[i])


                    iwc_uncertainty_TP.append(iwc_uncertainty[i])
                    EXT_coef_uncertainty_TP.append(EXT_coef_uncertainty[i])
                    ice_water_path_uncertainty_TP.append(ice_water_path_uncertainty[i])
                    re_uncertainty_TP.append(re_uncertainty[i])
                    optical_depth_uncertainty_TP.append(optical_depth_uncertainty[i])


        # arrays with lats and lons and variable values within TP 

        latitudes= np.array(latitudes)
        longitudes= np.array(longitudes)
        dem_TP= np.array(dem_TP)
        temp_TP= np.array(temp_TP)
        profile_time_TP= np.array(profile_time_TP)
        utc_start_TP= np.array(utc_start_TP)

        height_TP= np.array(height_TP)
        iwc_TP= np.array(iwc_TP)
        EXT_coef_TP= np.array(EXT_coef_TP)
        ice_water_path_TP= np.array(ice_water_path_TP)
        re_TP= np.array(re_TP)
        optical_depth_TP= np.array(optical_depth_TP)


        iwc_uncertainty_TP= np.array(iwc_uncertainty_TP)
        EXT_coef_uncertainty_TP= np.array(EXT_coef_uncertainty_TP)
        ice_water_path_uncertainty_TP= np.array(ice_water_path_uncertainty_TP)
        re_uncertainty_TP= np.array(re_uncertainty_TP)
        optical_depth_uncertainty_TP= np.array(optical_depth_uncertainty_TP)


        # set output dimension and write only new file 
        output_dim= iwc_TP.shape  # = normal profile with 125 bins 
        output_dim_vdata= latitudes.shape   # vdata, no vertical dimension, only one cell per vdatainate pair 
        output_dim_utc= utc_start_TP.shape  # one single cell 

        if output_dim[0] > 0:


            # test whether HDF5 file for same day already exists 
            from pathlib import Path
            import h5py

            day_file = Path('/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2C-ICE/2009/2009_'+day+'_night.hdf5')
            if day_file.is_file():

                # read in existing HDF5 file

                existing_file= h5py.File('/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2C-ICE/2009/2009_'+day+'_night.hdf5', 'r+')

                # read in datasets
      
                latitudes0= existing_file["Latitude"]
                height0= existing_file["Height"]
                iwc0= existing_file["IWC"]
                EXT_coef0= existing_file["EXT_coef"]
                ice_water_path0= existing_file["ice_water_path"]
                re0= existing_file["re"]
                optical_depth0= existing_file["optical_depth"]

                iwc_uncertainty0= existing_file["IWC_uncertainty"]
                EXT_coef_uncertainty0= existing_file["EXT_coef_uncertainty"]
                ice_water_path_uncertainty0= existing_file["ice_water_path_uncertainty"]
                re_uncertainty0= existing_file["re_uncertainty"]
                optical_depth_uncertainty0= existing_file["optical_depth_uncertainty"]

                longitudes0= existing_file["Longitude"]
                dem0= existing_file["DEM_elevation"]
                profile_time0= existing_file["Profile_time"]
                utc_start0= existing_file["UTC_start"]
                temp0= existing_file["Temperature"]


                # concatenate new datasets and old datasets vertically (x rows, 125 columns)

                latitudes1= np.concatenate((latitudes0, latitudes), axis = 0 )
                longitudes1= np.concatenate((longitudes0, longitudes), axis = 0)
                dem1= np.concatenate((dem0, dem_TP), axis = 0)
                profile_time1= np.concatenate((profile_time0, profile_time_TP), axis = 0)
                temp1= np.concatenate((temp0, temp_TP), axis = 0 )
                utc_start1= np.concatenate((utc_start0, utc_start_TP), axis = 0)

                iwc1= np.concatenate((iwc0, iwc_TP), axis = 0)
                height1= np.concatenate((height0, height_TP), axis = 0)
                EXT_coef1= np.concatenate((EXT_coef0, EXT_coef_TP), axis = 0)
                ice_water_path1= np.concatenate((ice_water_path0, ice_water_path_TP), axis = 0)
                re1= np.concatenate((re0, re_TP), axis = 0)
                optical_depth1= np.concatenate((optical_depth0, optical_depth_TP), axis = 0)


                iwc_uncertainty1= np.concatenate((iwc_uncertainty0, iwc_uncertainty_TP), axis = 0)
                EXT_coef_uncertainty1= np.concatenate((EXT_coef_uncertainty0, EXT_coef_uncertainty_TP), axis = 0)
                ice_water_path_uncertainty1= np.concatenate((ice_water_path_uncertainty0, ice_water_path_uncertainty_TP), axis = 0)
                re_uncertainty1= np.concatenate((re_uncertainty0, re_uncertainty_TP), axis = 0)
                optical_depth_uncertainty1= np.concatenate((optical_depth_uncertainty0, optical_depth_uncertainty_TP), axis = 0)

                # save data from numpy arrays to HDF5 datasets and replacing the old datasets

                dim_vdata= latitudes1.shape # 1 column only 
                dim= iwc1.shape # 125 columns
                dim_utc= utc_start1.shape # 1x1 = start time for orbit
  
                del existing_file["Latitude"]
                latitude= existing_file.create_dataset("Latitude", dim_vdata)
                latitude[...]= latitudes1

                del existing_file["Longitude"]
                longitude= existing_file.create_dataset("Longitude", dim_vdata)
                longitude[...]= longitudes1


                del existing_file["DEM_elevation"]
                dem= existing_file.create_dataset("DEM_elevation", dim_vdata)
                dem[...]= dem1

                del existing_file["Temperature"]
                temp= existing_file.create_dataset("Temperature", dim)
                temp[...]= temp1

                del existing_file["Profile_time"]
                profile_time= existing_file.create_dataset("Profile_time", dim_vdata)
                profile_time[...]= profile_time1

                del existing_file["UTC_start"]
                utc_start= existing_file.create_dataset("UTC_start", dim_utc)
                utc_start[...]= utc_start1


                del existing_file["IWC"]
                iwc= existing_file.create_dataset("IWC", dim)
                iwc[...]= iwc1

                del existing_file["Height"]
                height= existing_file.create_dataset("Height", dim)
                height[...]= height1


                del existing_file["EXT_coef"]
                EXT_coef= existing_file.create_dataset("EXT_coef", dim)
                EXT_coef[...]= EXT_coef1


                del existing_file["ice_water_path"]
                ice_water_path= existing_file.create_dataset("ice_water_path", dim_vdata)
                ice_water_path[...]= ice_water_path1

                del existing_file["re"]
                re= existing_file.create_dataset("re", dim)
                re[...]= re1


                del existing_file["optical_depth"]
                optical_depth= existing_file.create_dataset("optical_depth", dim_vdata)
                optical_depth[...]= optical_depth1


                del existing_file["IWC_uncertainty"]
                iwc_uncertainty= existing_file.create_dataset("IWC_uncertainty", dim)
                iwc[...]= iwc1

                del existing_file["EXT_coef_uncertainty"]
                EXT_coef_uncertainty= existing_file.create_dataset("EXT_coef_uncertainty", dim)
                EXT_coef_uncertainty[...]= EXT_coef1

                del existing_file["ice_water_path_uncertainty"]
                ice_water_path_uncertainty= existing_file.create_dataset("ice_water_path_uncertainty", dim_vdata)
                ice_water_path_uncertainty[...]= ice_water_path1

                del existing_file["re"]
                re= existing_file.create_dataset("re", dim)
                re[...]= re1

                del existing_file["optical_depth_uncertainty"]
                optical_depth= existing_file.create_dataset("optical_depth_uncertainty", dim_vdata)
                optical_depth[...]= optical_depth1


                existing_file.close()
          

            else:
            # create new SD based variable values for extracted lons and lats 

                #output_nr= str(iterations) # use iterator for different output names 

                # create new HDF5 file containing the datasets within the TP

                import h5py

                f= h5py.File('/media/juli/Elements/masterthesis_JK/CLOUDSAT_TP/2C-ICE/2009/2009_'+day+'_night.hdf5', "w")

                dset= f.create_dataset("Height", output_dim)
                dset[...]= height_TP

                dset= f.create_dataset("IWC",  output_dim)
                dset[...]= iwc_TP

                dset= f.create_dataset("EXT_coef",  output_dim)
                dset[...]= EXT_coef_TP

                dset= f.create_dataset("ice_water_path",  output_dim_vdata)
                dset[...]= ice_water_path_TP


                dset= f.create_dataset("re",  output_dim)
                dset[...]= re_TP

                dset= f.create_dataset("optical_depth",  output_dim_vdata)
                dset[...]= optical_depth_TP



                dset= f.create_dataset("IWC_uncertainty",  output_dim)
                dset[...]= iwc_uncertainty_TP

                dset= f.create_dataset("EXT_coef_uncertainty",  output_dim)
                dset[...]= EXT_coef_uncertainty_TP

                dset= f.create_dataset("ice_water_path_uncertainty",  output_dim_vdata)
                dset[...]= ice_water_path_uncertainty_TP


                dset= f.create_dataset("re_uncertainty",  output_dim)
                dset[...]= re_TP

                dset= f.create_dataset("optical_depth_uncertainty",  output_dim_vdata)
                dset[...]= optical_depth_uncertainty_TP


                dset= f.create_dataset("Latitude", output_dim_vdata)
                dset[...]= latitudes

                dset= f.create_dataset("Longitude", output_dim_vdata)
                dset[...]= longitudes


                dset= f.create_dataset("DEM_elevation", output_dim_vdata)
                dset[...]= dem_TP

                dset= f.create_dataset("Profile_time", output_dim_vdata)
                dset[...]= profile_time_TP

                dset= f.create_dataset("UTC_start", output_dim_utc)
                dset[...]= utc_start_TP

                dset= f.create_dataset("Temperature", output_dim)
                dset[...]= temp_TP

                f.close()

        else:
            print('This orbit did NOT cross the TP!')

#extract subdomain (westerly-dominated: 35-40 N, 70-105 E; transition zone: 30-35 N, 70-105 E, monsoon-dominated: 27-30 N, 70-105 E)

def extract_domain(param,lons,lats,dem):
    iteration=0
    lat1= 27 # change here coordinates to extract subregion! 
    lat2= 30
    lon1= 70
    lon2= 105
    param_TP=[]
    # select smaller domain
    for i,value in enumerate(lons):
        if lats[i] >= lat1  and lats[i] <= lat2 and value >= lon1 and value < lon2 and dem[i] >= 3000:
            iteration=iteration+1
            param_TP.append(param[i])

    if iteration==0:
        print(file, "this file does not contain data within the study domain")
        param_TP= -9999

    else:
        param_TP= np.array(param_TP)
    return param_TP

