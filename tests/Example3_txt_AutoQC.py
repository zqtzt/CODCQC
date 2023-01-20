# -*- coding：utf-8 -*-
# @author Zhetao Tan (IAP/CAS)
# @version: CODC-AutoQC v1.0
'''
    Here is an example of quality control by using *.txt files as the input method
    You should only give 3 input variables to the QC check main function "check_profileQC_main()": depth,tem,meta
    depth,tem: 1-dimension array or list
    meta: a class object with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3)
    if value is missing, you can use np.nan or use -9999 to set it (The recommended option is setting as NaN value. i.e., np.nan)

    The *.txt input files should have sequential arrangement of each profile(cast). The first line is metadata information, then followed by the observed value with two columns,
    the first column is depth value, the second column is temperature value at each observed depth.
    The example input file is in ./util/Example_txt_inpu.txt
    If you want to use txt file as the input method, Please strictly follow the storage format of the sample TXT file ("./util/Example_txt_inpu.txt") by following below criterias:
    (1) The first line is the meta-data informaiton:
         "HH CTD 2013 3 27 20.495 120.467“
         with the meaning of [Handle identification, instrument type, year, month, day, lat, lon] respectectly.
         NOTE: instrument type is strictly consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html  in three characters
    (2) Begins with the second line: the first column is depth value, the second column is temperature value at each corresponding depth, the third colunms is salinity value (if missing, using -9999 to represent it).
    When observed values are finished, then begins with the second profile.....

    Run this program, you can get the example of how to use TXT files as the input method, then output the quality flag in TXT format.
'''


import CODCQC.CODCQC_main as CODCQC_main
from CODCQC.util import IO_functions
from CODCQC.util import print_stat
from CODCQC.util import CODCQC_constant as const
import os
import numpy as np

makeTemperatureQC=True
makeSalinityQC=False

qc = CODCQC_main.QualityControl()

[COMS_PATH, a] = os.path.split(CODCQC.__file__)

txt_file=COMS_PATH+'/tests/Example3_txt_input.txt'
[depth_all,tem_all,sal_all,meta_list]=IO_functions.read_data_from_TXT(txt_file)

num_prof=len(tem_all)
myflagt_all=[]
kflagt_checks_all=[]

for i in range(num_prof):
    print(i)
    depth=depth_all[i]
    tem=tem_all[i]
    sal=sal_all[i]
    meta=CODCQC_main.metaData()
    meta.typ3=meta_list[i][1]
    meta.year=int(meta_list[i][2])
    meta.month=int(meta_list[i][3])
    meta.day=int(meta_list[i][4])
    meta.lat=float(meta_list[i][5])
    meta.lon=float(meta_list[i][6])
    meta.levels = len(depth)
    meta.gebcodepth = qc.get_gebcodepth(meta)
    #### Now, one profile(cast) has been read
    # print("Depth is:", depth)
    # print("Temperature is:", tem)

    # make CODC-AutoQC v1.0 check;  myflagt is the final QC flag combined with all checks; kflagt_checks is the QC flag for each seperated check
    # make Temperature QC
    if (makeTemperatureQC):
        [myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta,sal)
        myflagt_all.append(myflagt)
        kflagt_checks_all.append(kflagt_T_checks)  ###make statistics



#### write txt file
output_file='./Example3_txt_output.txt'  #create a new file
IO_functions.write_QCflag_to_txt_T(output_file,depth_all,tem_all,meta_list,myflagt_all)
print('WRITING FLAG is finished: '+output_file)

# if you like, you can print the detail statistical results to the txt file
if (makeTemperatureQC == True):
    print_stat.print_T_flag_txt(myflagt_all, kflagt_checks_all)
