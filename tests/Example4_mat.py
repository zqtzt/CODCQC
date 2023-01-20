import CODCQC
import CODCQC.CODCQC_main as CODCQC_main
from CODCQC.util import IO_functions
from CODCQC.util import print_stat
from CODCQC.util import CODCQC_constant as const
import scipy.io as scio
import h5py
import numpy as np


def QC_MATLAB(filepath,makeTemperatureQC=True,makeSalinityQC=False):
    qc = CODCQC_main.QualityControl()  # 创建类

    # the input folder include WOD18 netCDF file
    files = IO_functions.getFiles(file_path, '.mat')

    for m,filename in enumerate(files):
        print(m)
        print(filename)

        #read matlab file data
        data=scio.loadmat(filename)
        # data=h5py.File(filename,'r')

        Datainfo=data['CAS_info'][:]
        depth_raw=data['depth_raw'][:]
        tem_raw=data['temp_raw'][:]
        sal_raw=data['salinity_raw'][:]

        [levels_max, xbtn] = np.shape(tem_raw)
        print(xbtn)
        if(makeTemperatureQC):
            myflagt_final_checks = np.full((xbtn, levels_max, len(const.kflagt_T_list)), np.nan)
            myflagt_final_all = np.full((xbtn, levels_max), np.nan)

            
        myflagt_all = []
        kflagt_checks_all = []
        for i in range(xbtn):   #loop the profiles
            print(i)
            meta=CODCQC_main.metaData()

            # Read variables from MATLAB file
            try:
                meta.typ3 = const.type_name[int(Datainfo[7][i])]
                meta.year = int(Datainfo[1][i])
                meta.month = int(Datainfo[2][i])
            except:
                continue
            meta.day = int(Datainfo[3][i])
            meta.lat = float(Datainfo[5][i])
            meta.lon = float(Datainfo[6][i])
            meta.gebcodepth=qc.get_gebcodepth(meta)

            # make CODC-AutoQC v1.0 check
            # make Temperature QC
            if(makeTemperatureQC):
                depth = depth_raw[:, i]
                tem=tem_raw[:,i]
                sal=sal_raw[:,i]
                index_isData= ~np.isnan(tem)
                depth = depth[index_isData]
                tem = tem[index_isData]
                sal = sal[index_isData]
                meta.levels = len(depth)
                [myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta,sal)
                # print(myflagt)
                myflagt_all.append(myflagt)
                kflagt_checks_all.append(kflagt_T_checks)  ###make statistics
                # save QCflag to matrix
                myflagt_final_checks[i, index_isData, :] = np.array(kflagt_T_checks).transpose()
                myflagt_final_all[i, index_isData] = np.array(myflagt)

                
        # write and save QCflag to MATLAB file
        IO_functions.write_MATLAB_T(filename, myflagt_final_all,myflagt_final_checks)

        # if you like, you can print the detail statsitcal results to the txt file
        if(makeTemperatureQC==True):
            print_stat.print_T_flag_txt(myflagt_all,kflagt_checks_all,filename)


    print('QC finifhsed!')


if __name__ == '__main__':
    file_path = './CODCQC/tests/WOD18_mat_temp_data/'
    makeTemperatureQC=True
    makeSalinityQC=False
    import time
    t1=time.time()
    QC_MATLAB(file_path,makeTemperatureQC,makeSalinityQC)
    t2=time.time()
    print(t2-t1)