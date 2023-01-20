# @author Zhetao Tan (IAP/CAS)
# @version: CODC-AutoQC v1.0
'''
    Here is an example of how to make the CODC AutoQC program manually with a single oceanic observation profile (Now only Temperature are available)
    You should only give 3 input variables to the QC check main function "check_profileQC_main()": depth,tem,meta
    depth,tem: 1-dimension array or list
    meta: a class object with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3)
    if value is missing, you can use np.nan or use 9999 to set it (The recommended option is setting as NaN value. i.e., np.nan)
    please see the interperation below
'''

import CODCQC
from CODCQC import CODCQC_main
from CODCQC.util import CODCQC_constant as const
import numpy as np

qc = CODCQC_main.QualityControl()  #create a quality control object

depth = [0.0, 5.598, 7.800, 11.200, 14.000, 16.600, 20.000, 21.299]    #1-dimension array or list for depth value
tem = [9.1, 8.7, 8.3, 7.2, np.nan , 5.1, 4.4, 4.5]  #1-dimension array or list for temperature
print("Depth is:",depth)
print("Temperature is:",tem)


#create object to set metadata of a profile(cast)
meta=CODCQC.metaData()
#put metadata attributes into the meta object
meta.lat = 55.466  #(degrees_north)
meta.lon = -60.2   #(degrees_east)
meta.year = 1962
meta.month = 8
meta.day = 9
meta.levels=len(depth)
meta.typ3= 'CTD'  #consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html
meta.gebcodepth=qc.get_gebcodepth(meta)

# make CODC-QC v1.0 check
[myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta)


# print the temperature QC result
print('Temperature QC result is:',myflagt)
print('QC result of each check is:')
for i,name in enumerate(const.QCcheck_T_name):
    print(name+' is: ',kflagt_T_checks[i])


