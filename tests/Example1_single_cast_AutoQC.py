# @author Zhetao Tan (IAP/CAS)
# @version: COMS-AutoQC v0.1.1
'''
    Here is an example of how to run the COMS AutoQC program manually with a single oceanic observation profile (Now only temperature profile is available)
    You should only give 3 input variables to the QC check main function "check_profileQC_main()": depth,tem,meta
    depth,tem: 1-dimension array or list
    meta: a class object with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3)
    if value is missing, you can use np.nan or use 9999 to set it (The recommended option is setting as NaN value. i.e., np.nan)
    please see below
'''
import COMSQC
from COMSQC.AutoQC_main import check_profileQC_main
from COMSQC.AutoQC_main import depth_Tem_isMatch
import numpy as np


depth = [0.0, 5.598, 7.800, 11.200, 14.000, 16.600, 20.000, 21.299]    #1-dimension array or list for depth value
tem = [9.1, 8.7, 8.3, 7.2, np.nan , 5.1, 4.4, 4.5]  #1-dimension array or list for temperature
print("Depth is:",depth)
print("Temperature is:",tem)

#check inconsistent array length between temperature and depth
depth_Tem_isMatch(depth, tem)

#create object
meta=COMSQC.metaData()
#put metadata attributes into the meta object
meta.lat = 55.466  #(degrees_north)
meta.lon = -60.2   #(degrees_east)
meta.year = 1962
meta.month = 8
meta.day = 9
meta.levels=len(depth)
meta.typ3= 'XBT'  #consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html

# make COMS-AutoQC v1.0 check
#### it will return two variables: myflagt and myflagt_checks
#myflagt: the final flag combing all checks at each observed depth. 0 denotes accpeted value, 1 denotes rejected values
#myflagt_checks:  the flag of each AQC check at each observed epth. 0 denotes accpeted value, 1 denotes rejected values
[myflagt,myflagt_checks] = check_profileQC_main(depth, tem, meta)

#print the result
print('QC result of each check is:',myflagt_checks)
print('QC final result is:',myflagt)



