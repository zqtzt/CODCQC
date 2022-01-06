# @author Zhetao Tan (IAP/CAS)
# @version: COMS-AutoQC v1.0
'''
    Here is an example of quality control by using *.txt files as the input method
    You should only give 3 input variables to the QC check main function "check_profileQC_main()": depth,tem,meta
    depth,tem: 1-dimension array or list
    meta: a class object with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3)
    if value is missing, you can use np.nan or use 9999 to set it (The recommended option is setting as NaN value. i.e., np.nan)

    The *.txt input files should have sequential arrangement of each profile(cast). The first line is metadata information, then followed by the observed value with two columns,
    the first column is depth value, the second column is temperature value at each observed depth.
    The example input file is in ./util/Example_txt_inpu.txt
    If you want to use txt file as the input method, Please strictly follow the storage format of the sample TXT file ("./util/Example_txt_inpu.txt") by following below criterias:
    (1) The first line is the meta-data informaiton:
         "HH CTD 2013 3 27 20.495 120.467“
         with the meaning of [Handle identification, instrument type, year, month, day, lat, lon] respectectly.
         NOTE: instrument type is strictly consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html  in three characters
    (2) Begins with the second line: the first column is depth value, the second column is temperature value at each corresponding depth.
    When observed values are finished, then begins with the second profile.....

    Run this program, you can get the example of how to use TXT files as the input method, then output the quality flag in TXT format.
'''
import sys
import os
sys.path.append(r'F:\\QC_science\\QC_code\\Github_package')
from COMSQC.AutoQC_main import check_profileQC_main
from COMSQC.AutoQC_main import depth_Tem_isMatch

import numpy as np
from COMSQC.util import read_data_from_TXT
# a class object to set metadata of a profile(cast)
class metaData(object):
    def __init__(self):
        pass

import COMSQC
[COMS_PATH,a]=os.path.split(COMSQC.__file__)
txt_file=COMS_PATH+'/tests/Example3_txt_input.txt'
[depth_all,tem_all,meta_list]=read_data_from_TXT.data_reading(txt_file)

num_prof=len(depth_all)
myflagt_checks_all=[]
myflagt_all=[]
# myflagt_all=np.full((num_prof, levels_max), np.nan)
# myflagt_final_all = np.full((num_prof, levels_max, len(const.kflagt_list)), np.nan)

# raise ('Error')
for i in range(num_prof):
    depth=depth_all[i]
    tem=tem_all[i]
    meta=metaData()
    meta.typ3=meta_list[i][1]
    meta.year=int(meta_list[i][2])
    meta.month=int(meta_list[i][3])
    meta.day=int(meta_list[i][4])
    meta.lat=float(meta_list[i][5])
    meta.lon=float(meta_list[i][6])

    #### Now, one profile(cast) has been read
    print("Depth is:", depth)
    print("Temperature is:", tem)

    # check inconsistent array length between temperature and depth
    depth_Tem_isMatch(depth, tem)
    meta.levels=len(depth)

    # make COMS-AutoQC v1.0 check
    [myflagt, myflagt_checks] = check_profileQC_main(depth, tem, meta)

    # print the result
    print('QC result of each check is:', myflagt_checks)
    print('QC final result is:', myflagt)

    #save the final QCflag
    myflagt_checks_all.append(myflagt_checks)
    myflagt_all.append(myflagt)


#### write txt file
from COMSQC.util import read_nc
output_file='./test_output.txt'
read_nc.write_QCflag_to_txt(output_file,depth_all,tem_all,meta_list,myflagt_all)
print('WRITING FLAG is finished: '+output_file)

#if you like, you can print the final statsitcal result to the txt file
from COMSQC.util import print_stat
OuputFilename=print_stat.print_flag_txt_list(myflagt_all,myflagt_checks_all)
print('Printing statistical results is finished: '+OuputFilename)