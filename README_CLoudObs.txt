This document briefly describes the processed satellite cloud data for the TP and downstream regions that can be found in following: subdirectories

Updated May 2021, Contact: julia.kukulies@gu.se 

*ISCCP 

Monthly gridded cloud parameters from ISCCP H Series 
Domain: 20-60 N, 70-125 E 
Time period: 1983 – 2017 
Webpage: https://www.ncdc.noaa.gov/isccp
Downloaded from:https://www.ncei.noaa.gov/thredds/catalog/cdr/isccp_hgm_agg/files/catalog.html 

Variables: 
cldamt = Mean cloud amount 
pc = Mean cloud pressure 
tau = Mean cloud cloud optical depth (TAU) 
wp = Mean cloud water path 
tc = Mean cloud temperature 
snoice = Mean snow/ice amount 

*CloudSat

Processed cloud profiles based on data product 2B-GEOPROF-LIDAR (http://www.cloudsat.cira.colostate.edu/data-products/level-2b/2b-geoprof-lidar)

lidar_cloud_fraction: cloud fraction detected by CALIPSO (lidar sensor)
height-latitude profiles averaged over longitudes (80-90E)
height-longitude profiles averaged over latitudes (33-36N)

Processed cloud profiles based on data product 2B-GEOPROF (http://www.cloudsat.cira.colostate.edu/data-products/level-2b/2b-geoprof)

radar_reflectivity: signal detected by CPR (radar sensor)
height-latitude profiles averaged over longitudes (80-90E)
height-longitude profiles averaged over latitudes (33-36N)

*DARDAR

Processed cloud profiles based on data product DARDAR (CALIPSO and CloudSat combined product)

Webpage: https://airbornescience.nasa.gov/content/From_CloudSat-CALIPSO_to_EarthCare_Evolution_of_the_DARDAR_cloud_classification_and_its 

Downloaded from: https://www.icare.univ-lille.fr/dardar/ 

ice_water_content (retrieved from radar-lidar combined product)
height-latitude profiles averaged over longitudes (80-90E)
height-longitude profiles averaged over latitudes (33- 36N)

cloud_mask (retrieved from radar-lidar combined product)
height-latitude profiles averaged over longitudes (80-90E)
height-longitude profiles averaged over latitudes (33-36N)
