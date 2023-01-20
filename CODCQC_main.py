""" Apply Auto-Quality Control of temperature profiles
"""
import CODCQC
import numpy as np
import numpy.ma as ma
import scipy.io as scio
import os
import gsw
from CODCQC.util import CODCQC_constant as const
from CODCQC.util import util_functions
from CODCQC.qc_T_models import aqc_check1 as check01_T
from CODCQC.qc_T_models import aqc_check2 as check02_T
from CODCQC.qc_T_models import aqc_check3 as check03_T
from CODCQC.qc_T_models import aqc_check4 as check04_T
from CODCQC.qc_T_models import aqc_check5 as check05_T
from CODCQC.qc_T_models import aqc_check6 as check06_T
from CODCQC.qc_T_models import aqc_check7 as check07_T
from CODCQC.qc_T_models import aqc_check8 as check08_T
from CODCQC.qc_T_models import aqc_check9 as check09_T
from CODCQC.qc_T_models import aqc_check10 as check10_T
from CODCQC.qc_T_models import aqc_check11 as check11_T
from CODCQC.qc_T_models import aqc_check12 as check12_T
from CODCQC.qc_T_models import aqc_check13 as check13_T
from CODCQC.qc_T_models import aqc_check14 as check14_T



class metaData(object):
    def __init__(self):
        pass

class QualityControl(object):
    def __init__(self):
        ######自动导入外部数据库
        [COMS_PATH, a] = os.path.split(CODCQC.__file__)
        ##  GEBCO_2021_15arc-seconds data
        print('start reading GEBCO depth file')
        if(not os.path.exists(COMS_PATH+'/background_field/gebco_2021_15arcsecond.npz')):
            print('The external file [ebco_2021_15arcsecond.npz] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
            print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')
            raise('Error')
        data = np.load(COMS_PATH+'/background_field/gebco_2021_15arcsecond.npz')
        self.elevation = data['elevation']
        self.gebco_lat_bnd = data['lat_bnd']
        self.gebco_lon_bnd = data['lon_bnd']
        del data

        # Temperature 1 degree-climatology field (constant IAP-T-range)
        from scipy import io
        print('start reading temperature climatology field')
        if(not os.path.exists(COMS_PATH+'/background_field/IAP_T_range.mat')):
            print('The external file [IAP_T_range.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
            print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')
            raise('Error')        
        mat = io.loadmat(COMS_PATH+'/background_field/IAP_T_range.mat')
        self.tmin = mat['T_min']
        self.tmax = mat['T_max']
        Std_depth = mat['Std_depth']
        self.Std_depth = np.transpose(Std_depth)[0]
        lat = np.linspace(-89, 90, 180)
        lon = np.linspace(-179, 180, 360)
        self.lon_bound = np.array([lon - 0.5,lon + 0.5])
        self.lat_bound = np.array([lat - 0.5, lat + 0.5])
        self.lat_bound[0, 0] = -90.0
        self.lon_bound[0, 0] = -180.0
        depth_left = self.Std_depth[1:] - np.diff(self.Std_depth) / 2
        depth_left = np.insert(depth_left, 0, 0)
        depth_right = np.hstack((depth_left[1:], 100000))
        self.Std_depth_bound = np.array([depth_left, depth_right])
        del mat

        # Temperature: k_min k_max linear coefficient for time-varying IAP-T-range
        from scipy import io
        print('start reading linear coefficient for time-varying IAP-T-range')
        if(not os.path.exists(COMS_PATH+'/background_field/IAP_T_range_kmax_kmin.mat')):
            print('The external file [IAP_T_range_kmax_kmin.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
            print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')
            raise('Error') 
        mat = io.loadmat(COMS_PATH+'/background_field/IAP_T_range_kmax_kmin.mat')
        self.kmin_T = mat['T_min_linear_coeff']
        self.kmax_T = mat['T_max_linear_coeff']
        del mat


        ## T-gradient climatology field (IAP-TG-range)
        print('start reading temperature gradient climatology field')
        if(not os.path.exists(COMS_PATH+'/background_field/IAP_TG_range.mat')):
            print('The external file [IAP_TG_range.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
            print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')
            raise('Error')         
        mat = io.loadmat(COMS_PATH+'/background_field/IAP_TG_range.mat')
        self.Gradmin = mat['Gmin_all'][:]  # (360,180,79,12,6)
        self.Gradmax = mat['Gmax_all'][:]
        self.interp_grid = mat['interp_grid'][:]
        Grad_lon = np.squeeze(mat['lon'][:])
        Grad_lat = np.squeeze(mat['lat'][:])
        Grad_std_depth = np.squeeze(mat['Std_depth'][:])
        self.Grad_lon_bound = np.array([Grad_lon - 0.5, Grad_lon + 0.5])
        self.Grad_lat_bound = np.array([Grad_lat - 0.5, Grad_lat + 0.5])
        depth_left = Grad_std_depth[1:] - np.diff(Grad_std_depth) / 2
        depth_left = np.insert(depth_left, 0, 0)
        depth_right = np.hstack((depth_left[1:], 2050))
        self.Grad_std_depth_bound = np.array([depth_left, depth_right])
        del mat

        ###### IAP41 salinity climatology files
        print('start reading salinity climatology field')
        if(not os.path.exists(COMS_PATH+'/background_field/climatology_Savg_IAP41_1955_2020.mat')):
            print('The external file [climatology_Savg_IAP41_1955_2020.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
            print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')
            raise('Error')          
        mat = io.loadmat(COMS_PATH+'/background_field/climatology_Savg_IAP41_1955_2020.mat')
        self.Savg = mat['S_avg']
        Std_depth_41 = mat['Std_depth_41']
        Std_depth_41 = np.transpose(Std_depth_41)[0]
        depth_left = Std_depth_41[1:] - np.diff(Std_depth_41) / 2
        depth_left = np.insert(depth_left, 0, 0)
        depth_right = np.hstack((depth_left[1:], 2050))
        self.Std_depth_41_bound = np.array([depth_left, depth_right])
        del mat
        
        pass

    def __del__(self):
        pass

    def get_gebcodepth(self,meta):
        rlat = meta.lat
        rlon = meta.lon
        if(rlon > 180 and rlon <=360):
            rlon=rlon-360
        # #计算gebco
        try:
            jy = np.where(np.logical_and(rlat > self.gebco_lat_bnd[:, 0], rlat <= self.gebco_lat_bnd[:, 1]))[0][
                0]  # 纬度
            ix = np.where(np.logical_and(rlon > self.gebco_lon_bnd[:, 0], rlon <= self.gebco_lon_bnd[:, 1]))[0][
                0]  # 经度
        except:
            gebcodepth=np.nan
            return gebcodepth
        if ((ix < 0 or ix > 86400) or (jy < 0 or jy > 43200)):
            gebcodepth= np.nan
            return gebcodepth
        gebcodepth = self.elevation[ix][jy]
        gebcodepth = -(gebcodepth)  # ocean: negative value
        
        # GEBCP-DEPTH with tolerance  
        if (meta.lat > -60):
            if gebcodepth < 15:
                gebcodepth = gebcodepth + 35.0 + gebcodepth * 0.087
            elif (gebcodepth < 1000):
                gebcodepth = gebcodepth + 30 + gebcodepth * 0.087
            else:
                gebcodepth = gebcodepth + 80
        else:
            if (gebcodepth < 600):
                gebcodepth = gebcodepth + 270 - gebcodepth * 0.037
            else:
                gebcodepth = gebcodepth + 80
        return gebcodepth
    
    def check_T_main(self,tem,depth,meta,sal=[]):
        if (not ma.isMaskedArray(depth)):
            depth = ma.array(depth, mask=np.isnan(depth))
        if (not ma.isMaskedArray(tem)):
            tem = ma.array(tem, mask=np.isnan(tem))
        #if (not ma.isMaskedArray(sal)):
        #    sal = ma.array(sal, mask=np.isnan(sal))
        

        [kflagt1, discard_flag,meta] = check01_T.basic_information_check(self,depth, tem, meta)

        [kflagt2, depth, tem] = check02_T.levels_order(self,depth, tem, meta)
        # kflagt2=np.zeros(meta.levels,np.int)

        kflagt3 = check03_T.instrument_type_depth(self,depth, tem, meta)
        # kflagt3 = np.zeros(meta.levels, np.int)

        kflagt4 = check04_T.gebo_check(self,depth, tem, meta)
        # kflagt4 = np.zeros(meta.levels, np.int)

        kflagt5 = check05_T.crude_range(self,depth, tem, meta)
        # kflagt5 = np.zeros(meta.levels, np.int)

        kflagt6 = check06_T.freezing_point_check(self,depth, tem, meta)

        [kflagt7, _, _] = check07_T.climatology_check(self,depth, tem, meta)
        # kflagt7 = np.zeros(meta.levels, np.int)

        kflagt8 = check08_T.constant_value(self,depth, tem, meta)
        # kflagt8 = np.zeros(meta.levels, np.int)

        kflagt9 = check09_T.spike_check(self,depth, tem, meta)
        # kflagt9 = np.zeros(meta.levels, np.int)

        kflagt10 = check10_T.density_inversion_check(self,depth,tem,meta,sal)

        kflagt11 = check11_T.number_of_temperature_extrema(self,depth, tem, meta)
        # kflagt10 = np.zeros(meta.levels, np.int)

        kflagt12 = check12_T.global_gradient_check(self,depth, tem, meta)

        ####### 11 local gradient climatology check
        [kflagt13, _, _, _] = check13_T.gradient_climatology_check(self,depth, tem, meta)
        # kflagt13 = np.zeros(meta.levels, np.int)

        kflagt14 = check14_T.instrument_specific_check_XBT(self,depth, kflagt13, meta)
        # kflagt14 = np.zeros(meta.levels, np.int)

        kflagt_checks = []
        for key in const.kflagt_T_list:
            kflagt_checks.append(list(eval(key)))

        myflagt = util_functions.combine_flag(kflagt_checks).tolist()
        return myflagt,kflagt_checks



if __name__ == '__main__':

    from util import IO_functions
    from util import print_stat

    file_path = 'F:\\QC_science\\QC_code\\COMS_QC\\tests\\\WOD18_netCDF_temp_data\\'

    qc=QualityControl()  #创建类

    # the input folder include WOD18 netCDF file
    files = IO_functions.getFiles(file_path, '.nc')

    myflagt_all = []
    kflagt_checks_all=[]
    for file in files:
        print(file)

        # Read variables from WOD18 netCDF file
        # Handle:f  tempeature:tem Depth:depth  metadata:meta
        [f, tem, depth, meta] = IO_functions.read_WOD(file)

        # make COMS-AutoQC v1.0 check
        [myflagt,kflagt_checks]=qc.check_main(tem,depth,meta)
        # print(myflagt)

        # save the final QCflag
        myflagt_all.append(myflagt)
        kflagt_checks_all.append(kflagt_checks)  ###make statistics

        # write QCflag to netCDF file
        f = IO_functions.write_nc_tempQC(f, myflagt)

        # close netCDF file
        f.close()

    # if you like, you can print the detail statsitcal results to the txt file
    print_stat.print_flag_txt(myflagt_all,kflagt_checks_all)
    # print_stat.print_flag_txt(myflagt_all)
