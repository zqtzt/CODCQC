import CODCQC as CODCQC
import CODCQC.CODCQC_main as CODCQC_main
from CODCQC.util import IO_functions
from CODCQC.util import print_stat
import numpy as np

def main(file_path,makeTemperatureQC=True,makeSalinityQC=False):
    qc = CODCQC_main.QualityControl()  # 创建类

    # the input folder include WOD18 netCDF file
    files = IO_functions.getFiles(file_path, '.nc')

    import time
    t1=time.time()
    myflagt_all = []
    kflagt_checks_all = []
    for file in files:
        print(file)

        # Read variables from WOD18 netCDF file
        # Handle:f  tempeature:tem Depth:depth  metadata:meta
        [f, tem, sal, depth, meta] = IO_functions.read_WOD(file)
        meta.gebcodepth=qc.get_gebcodepth(meta)
        
        # make COMS-AutoQC v1.0 check
        # make Temperature QC
        if(makeTemperatureQC==True):
            [myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta)
            # save the final QCflag
            myflagt_all.append(myflagt)
            kflagt_checks_all.append(kflagt_T_checks)  ###make statistics
            # write QCflag to netCDF file
            f = IO_functions.write_nc_tempQC(f, myflagt)
                
        # close netCDF file
        f.close()

    # if you like, you can print the detail statsitcal results to the txt file
    if(makeTemperatureQC==True):
        print_stat.print_T_flag_txt(myflagt_all,kflagt_checks_all)

    t2=time.time()
    print('time cost: '+str(t2-t1))

if __name__ == '__main__':
    filepath='./CODCQC/tests/WOD18_netCDF_temp_data/WOD18_netCDF_temp_data/'
    makeTemperatureQC=True
    makeSalinityQC=False
    main(filepath,makeTemperatureQC,makeSalinityQC)
