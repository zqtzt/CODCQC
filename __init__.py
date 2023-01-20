# -*- coding: utf-8 -*-
name='CODCQC'
__author__ = 'Zhetao Tan (IAP/CAS), Lijing Cheng (IAP/CAS)'
__email__ = 'tanzhetao@mail.iap.ac.cn'
__version__ = '1.0'
import os
import CODCQC

class metaData(object):
    def __init__(self):
        pass

[COMS_PATH, a] = os.path.split(CODCQC.__file__)
### check external files exists or not

file1=COMS_PATH+'/background_field/gebco_2021_15arcsecond.npz'
if(not os.path.exists(file1)):
    print('The external file [ebco_2021_15arcsecond.npz] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
    print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')


file2=COMS_PATH+'/background_field/IAP_T_range.mat'
if(not os.path.exists(file2)):
    print('The external file [IAP_T_range.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
    print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')

file2=COMS_PATH+'/background_field/IAP_T_range_kmax_kmin.mat'
if(not os.path.exists(file2)):
    print('The external file [IAP_T_range_kmax_kmin.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
    print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')


file2=COMS_PATH+'/background_field/IAP_TG_range.mat'
if(not os.path.exists(file2)):
    print('The external file [IAP_TG_range.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
    print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')


file2=COMS_PATH+'/background_field/climatology_Savg_IAP41_1955_2020.mat'
if(not os.path.exists(file2)):
    print('The external file [climatology_Savg_IAP41_1955_2020.mat] does not exist in this package, please download the file with the same name in this link [http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/]')
    print('And then please put this file in a folder named [background_field] under the installed path of CODCQC package')

