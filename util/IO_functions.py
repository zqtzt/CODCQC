# -*- coding：utf-8 -*-
#读取单个nc文件的数据，并且最后以追加的方式写入
import numpy as np
import netCDF4 as nc
import numpy.ma as ma

def getFiles(dir, suffix): # 查找的根目录dir，文件后缀，例如'.nc'
    import os
    file_path = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename) # =>文件名,文件后缀
            if suf == suffix:
                file_path.append(os.path.join(root, filename)) # =>吧一串字符串组合成路径
    return file_path

def add_parameters(params,**kwargs):
    return params.update(kwargs)


def write_MATLAB(filename,**kwargs):
    import os
    import scipy.io as scio

    filepath, filename = os.path.split(filename)
    OuputFilename, _ = os.path.splitext(filename)

    mdic={}
    for k,value in kwargs.items():
        print(k)
        mdic[k]=value
        # value = value.astype(dtype=int)
        # value[value < -100] = 99
        # value = value.astype(dtype=np.int8)  # 99是 NaN
        #exec('mdic=add_parameters(mdic,'+k+'='+value+')')

    # mdic = {'CODCQC_myflagt': myflagt_final_all, 'CODCQC_myflagt_checks': myflagt_final_checks}

    strings = filepath + 'CODCQCflag_' + OuputFilename + '.mat'
    scio.savemat(strings, mdic,do_compression=True)

def write_MATLAB_T(filename,myflagt_final_all,myflagt_final_checks):
    import os
    import scipy.io as scio

    filepath, filename = os.path.split(filename)
    OuputFilename, _ = os.path.splitext(filename)


    myflagt_final_checks = myflagt_final_checks.astype(dtype=int)
    myflagt_final_checks[myflagt_final_checks < -100] = 99
    myflagt_final_checks = myflagt_final_checks.astype(dtype=np.int8)  # 99是 NaN

    myflagt_final_all = myflagt_final_all.astype(dtype=int)
    myflagt_final_all[myflagt_final_all < -100] = 99
    myflagt_final_all = myflagt_final_all.astype(dtype=np.int8)  # 99是 NaN

    mdic = {'CODCQC_myflagt': myflagt_final_all, 'CODCQC_myflagt_checks': myflagt_final_checks}

    strings = filepath + '/CODCQCflag/CODCQCflag_' + OuputFilename + '.mat'
    scio.savemat(strings, mdic,do_compression=True)

# read input data from *.txt file
def read_data_from_TXT(txt_file):
    missing_value=-9999
    flag = 0
    meta_list = []
    depth_all = []
    tem_all = []
    sal_all=[]
    for line in open(txt_file, "r"):
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        if 'HH' in line:
            if (flag == 1):
                depth_all.append(depth)
                tem_all.append(tem)
                sal_all.append(sal)
                flag = 0
            if (flag == 0):
                depth = []
                tem = []
                sal=[]
                handle = line.split(' ')
                while '' in handle:
                    handle.remove('')
                meta_list.append(handle)
                flag = 1
        else:
            data = line.strip('\n').split(' ')
            while '' in data:
                data.remove('')
            #print(data)
            depth_sample, tem_sample,sal_sample = [float(x) for x in data[:3]]  #[float(data[0]),float(data[1]),int(data[2])]
            if(np.abs(depth_sample-missing_value)<0.1):
                depth_sample=np.nan
            if(np.abs(tem_sample-missing_value)<0.1):
                tem_sample=np.nan
            if (np.abs(sal_sample - missing_value) < 0.1):
                sal_sample = np.nan
            depth.append(depth_sample)
            tem.append(tem_sample)
            sal.append(sal_sample)

    depth_all.append(depth)
    tem_all.append(tem)
    sal_all.append(sal)

    return depth_all,tem_all,sal_all,meta_list

def write_nc_tempQC(f,temp_QC):
    #create variables
    try:
        Temperature_CASflag = f.createVariable("Temperature_CASflag", 'i4', ("z"))
    except:   #如果变量已经存在的话,读取变量，修改变量的值
        Temperature_CASflag = f.variables['Temperature_CASflag']
        Temperature_CASflag[:]=temp_QC[:]
        Temperature_CASflag.long_name = "Tempature quality control flagged by Ocean Data Center, Chinese Academy of Sciences (CAS-ODC)"
        Temperature_CASflag.comment = "0: accepeted value; 1: bad value (outlier)"
        Temperature_CASflag.QC_version = "v1.0"
        Temperature_CASflag.processing_centers = "CAS-Ocean Data Center; IAP/CAS"
        return f

    #######create attriubutes
    Temperature_CASflag.long_name = "Tempature quality control flagged by Ocean Data Center, Chinese Academy of Sciences (CAS-ODC)"
    Temperature_CASflag.comment = "0: accepeted value; 1: bad value (outlier)"
    Temperature_CASflag.QC_version = "v1.0"
    Temperature_CASflag.creator_name = "Zhetao Tan"
    Temperature_CASflag.creator_email= "tanzhetao19@mails.ucas.ac.cn"
    Temperature_CASflag.processing_centers = "CAS-Ocean Data Center; IAP/CAS"

    #######put data into variables
    Temperature_CASflag[:] = temp_QC

    return f


def write_nc_salinityQC(f,salnity_QC):
    #create variables
    try:
        Salinity_CASflag = f.createVariable("Salinity_CASflag", 'i4', ("z"))
    except:   #如果变量已经存在的话,读取变量，修改变量的值
        Salinity_CASflag = f.variables['Salinity_CASflag']
        Salinity_CASflag[:]=salnity_QC[:]
        Salinity_CASflag.long_name = "Salinity quality control flagged by Ocean Data Center, Chinese Academy of Sciences (CODC)"
        Salinity_CASflag.comment = "0: accepeted value; 1: bad value (outlier)"
        Salinity_CASflag.QC_version = "v1.0"
        Salinity_CASflag.processing_centers = "CAS-Ocean Data Center; IAP/CAS"
        return f

    #######create attriubutes
    Salinity_CASflag.long_name = "Salinity quality control flagged by Ocean Data Center, Chinese Academy of Sciences (CODC)"
    Salinity_CASflag.comment = "0: accepeted value; 1: bad value (outlier)"
    Salinity_CASflag.QC_version = "v1.0"
    Salinity_CASflag.creator_name = "Zhetao Tan"
    Salinity_CASflag.creator_email= "tanzhetao19@mails.ucas.ac.cn"
    Salinity_CASflag.processing_centers = "CAS-Ocean Data Center; IAP/CAS"

    #######put data into variables
    Salinity_CASflag[:] = salnity_QC
    return f
    
def change_nc_variables(f,oldname,new_name):
    # from netCDF4 import Dataset

    oldname_variable = f.variables[oldname]
    # mytemperature=f.variables['temp_remove_flag']
    # GTSPP_temperature=f.varables['temperature']
    newname_variable = f.variables[new_name]
    newname_variable[:] = oldname_variable[:]

    return f


# def write_QCflag_to_txt(output_file,depth_all,tem_all,meta_list,myflagt_all):
def write_QCflag_to_txt(output_file,depth_all,tem_all,sal_all,meta_list,myflagt_all,myflags_all):
    f_write = open(output_file, 'w')
    for i in range(len(myflagt_all)):
        f_write.writelines(' '.join(meta_list[i]))
        f_write.write('\n')
        depth = depth_all[i]
        tem = tem_all[i]
        myflagt = myflagt_all[i]
        myflags = myflags_all[i]
        sal = sal_all[i]
        if(myflags==[]):  #没有盐度记录
            for j in range(len(depth)):
                print('%-8.3f %-8.3f %i' % (depth[j], tem[j], myflagt[j]), file=f_write)
        else:  #有盐度记录
            for j in range(len(depth)):
                if(np.isnan(sal[j])):
                    print('%-8.3f %-8.3f %i %-8d %i' % (depth[j], tem[j], myflagt[j], -9999,myflags[j]), file=f_write)
                else:
                    print('%-8.3f %-8.3f %i %-8.4f %i' % (depth[j], tem[j], myflagt[j], sal[j], myflags[j]), file=f_write)
    f_write.close()

def write_QCflag_to_txt_T(output_file,depth_all,tem_all,meta_list,myflagt_all):
    f_write = open(output_file, 'w')
    for i in range(len(myflagt_all)):
        f_write.writelines(' '.join(meta_list[i]))
        f_write.write('\n')
        depth = depth_all[i]
        tem = tem_all[i]
        myflagt = myflagt_all[i]

        for j in range(len(depth)):
            print('%-8.3f %-8.3f %i' % (depth[j], tem[j], myflagt[j]), file=f_write)
    f_write.close()

class metaData(object):
    def __init__(self):
        pass

def read_variables(f):
    temp=f.variables['Temperature'][:]
    temp=np.reshape(temp,-1)
    temp = ma.array(temp, mask=np.isnan(temp.data))
    depth=f.variables['z'][:]
    depth=np.reshape(depth,-1)
    # if(type(depth) is not np.ndarray):
        # depth=np.array(depth)
    depth = ma.array(depth, mask=np.isnan(depth.data))

    try:
        sal=f.variables['Salinity'][:]
        sal=np.reshape(sal,-1)
        sal = ma.array(sal, mask=np.isnan(sal.data))
    except:
        sal=np.full((len(depth),1),np.nan)
    
    meta=metaData() #class
    meta.levels=len(depth)
    # meta.obsdepth=depth[~depth.mask][-1]  #只访问有效元素

    data_type=f.variables['dataset'][:]
    try:
        meta.typ3=str(nc.chartostring(data_type))
    except:
        meta.typ3='UNKNOWN'

    lat=f.variables['lat'][:]
    lat=lat.reshape(-1)
    meta.lat = lat[0]
    lon=f.variables['lon'][:]
    lon=lon.reshape(-1)
    lon=lon[0]
    if(lon>180 and lon<=360):
        lon=lon-360
    meta.lon = lon

    time_var=f.variables['time']
    dtime = nc.num2date(time_var[-1],time_var.units)
    # print(dtime)
    meta.year=dtime.year
    meta.month=dtime.month
    meta.day=dtime.day

    #查看类的属性 meta.__dict__.keys()
    return temp,sal,depth,meta

def read_WOD(file):
    f = nc.Dataset(file, 'a')
    [tem, sal,depth, meta]=read_variables(f)
    
    if meta.levels>=3:
        if(depth[0]==0):
            depth[np.where(depth==0)]=np.nan
            depth[0]=0
        else:
            depth[np.where(depth==0)]=np.nan
    depth = ma.array(depth, mask=np.isnan(depth.data))
    
    return f,tem, sal, depth, meta