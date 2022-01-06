# @author Zhetao Tan (IAP/CAS)
# @version: COMS-AutoQC v1.0
'''
   Here is an example of quality control for WOD temperature profiles
   The netCDF file should include the following variables: Temperature, Depth, time, latitude, longitude, instrument type
   The variables should strictly follow the names below in order to corresponding to the function "read_WOD_from_NC.read_WOD()"
   Temperature:  'Temperature'
   Depth: 'z'
   time: 'time'
   latitutde: 'lat'
   longitude: 'lon'
   Instrument type: 'dataset'  (consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html )

   If your netCDF files do not inlcude these variables name, you can read by yourself instead of using function "read_WOD_from_NC.read_WOD()"
   Or you can manually modify the function "read_WOD_from_NC.read_WOD" to fit your netCDF file
   You should only give 3 input variables to the QC check main function "check_profileQC_main()": depth,tem,meta
    depth,tem: 1-dimension array or list
    meta: a class object with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3
    Example:
    depth=[0.0, 5.598, 7.800, 11.200, 14.000, 16.600, 20.000, 21.299]
    tem=[9.1, 8.7, 8.3, 7.2, 5.9, 5.1, 4.4, 4.5]
    meta.lat=55.466  (degrees_north)
    meta.lon=-60.2   (degrees_east)
    meta.year=1962
    meta.month=8
    meta.day= 9
    meta.typ3= 'MBT'  (consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html )
    if value is missing, you can use np.nan or use 9999 to set it
    More example of Quality Control for single profile (cast), please refer to.........
'''
#import sys
#sys.path.append(r'F:\\QC_science\\QC_code\\Github_package')
import COMSQC
from COMSQC.util import read_WOD_from_NC
from COMSQC.AutoQC_main import check_profileQC_main
from COMSQC.AutoQC_main import depth_Tem_isMatch
from COMSQC.util import aqc_constant as const
from COMSQC.util import read_nc
from COMSQC.util import print_stat
import time
import os
time_start=time.time()


[COMS_PATH,a]=os.path.split(COMSQC.__file__)

#the input folder include WOD18 netCDF file：The example WOD18 netCDF files are also attached ata <COMSQC_location>/tests/WOD18_netCDF_temp_data
path=COMS_PATH+'/tests/WOD18_netCDF_temp_data'  #please set the netCDF folder

# list all the netCDF files
files=read_nc.getFiles(path,'.nc')

myflagt_all=[]
myflagt_checks_all=[]
for file in files:
    print(file)

    #Read variables from WOD18 netCDF file
    #Handle:f tempeature:tem  Depth:depth  metadata:meta
    [f, tem, depth, meta] = read_WOD_from_NC.read_WOD(file)

    #check inconsistent array length between temperature and depth. If falied, skip this profile
    try:
        depth_Tem_isMatch(depth, tem)
    except:
        f.close()
        continue

    #run main function of COMSQC v0.1
    [myflagt,myflagt_checks]=check_profileQC_main(depth,tem,meta)
    print('Final Tempflag is:', myflagt)  #myflagt: Final flag combing all checks at each observed depth level
    print('flag by each check is:', myflagt_checks) #myflagt_checks: flag by each check at each observed depth level
    

    #save the final QCflag
    myflagt_all.append(myflagt)
    myflagt_checks_all.append(myflagt_checks)

    #write Final flag to netCDF file
    f=read_nc.write_nc_tempQC(f, myflagt)

    #close netCDF file
    f.close()

#if you like, you can print the final statsitcal result to the txt file
print_stat.print_flag_txt_list(myflagt_all,myflagt_checks_all)

time_end=time.time()
print('Total number of files = ',len(files))
print('time cost',time_end-time_start,'seconds')
print('time cost',round((time_end-time_start)/60,2),'minutes')

