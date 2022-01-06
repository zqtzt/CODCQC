# -*- coding：utf-8 -*-
#读取单个nc文件的数据，并且最后以追加的方式写入

def getFiles(dir, suffix): # 查找的根目录dir，文件后缀，例如'.nc'
    import os
    file_path = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename) # =>文件名,文件后缀
            if suf == suffix:
                file_path.append(os.path.join(root, filename)) # =>吧一串字符串组合成路径
    return file_path


def write_nc_tempQC(f,temp_QC):

    #create variables
    try:
        temp_QC_COMS = f.createVariable("temp_QC_COMS", 'i4', ("z"))
    except:   #如果变量已经存在的话,读取变量，修改变量的值
        temp_QC_COMS = f.variables['temp_QC_COMS']
        temp_QC_COMS[:]=temp_QC[:]
        return f

    #######create attriubutes
    temp_QC_COMS.long_name = "Tempature QC flag by Center for Ocean Mega-Science, Chinese Academy of Sciences "
    temp_QC_COMS.comment = "0 for good value; 1 failed date/location check; 2 failed range check; 3 failed local maximum depth check; 4 failed constant value check; ..." \
                           "5 failed spike check; 6 failed global gradient check; 7 failed instrument type check; 8 failed local climatology check; 9 failed local gradient climatology check"
    temp_QC_COMS.QC_version = "V1.0"
    temp_QC_COMS.creator_name = "Zhetao Tan"
    temp_QC_COMS.creator_email= "tanzhetao19@mails.ucas.ac.cn"
    temp_QC_COMS.processing_centers = "MSDC/IOCAS; ICCES/IAP"

    #######put data into variables
    temp_QC_COMS[:] = temp_QC

    return f


def change_nc_variables(f,oldname,new_name):
    # from netCDF4 import Dataset

    oldname_variable = f.variables[oldname]
    # mytemperature=f.variables['temp_remove_flag']
    # GTSPP_temperature=f.varables['temperature']
    newname_variable = f.variables[new_name]
    newname_variable[:] = oldname_variable[:]

    return f


def write_QCflag_to_txt(output_file,depth_all,tem_all,meta_list,myflagt_all):
    f_write = open(output_file, 'w')
    for i in range(len(myflagt_all)):
        f_write.writelines(' '.join(meta_list[i]))
        f_write.write('\n')
        depth = depth_all[i]
        tem = tem_all[i]
        myflagt = myflagt_all[i]
        for j in range(len(depth_all[i])):
            print('%-8.3f %-8.3f %i' % (depth[j], tem[j], myflagt[j]), file=f_write)
    f_write.close()

