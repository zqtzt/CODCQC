#########可以让使用者自己存成列表
import numpy as np
from collections import Counter
from CODCQC.util import CODCQC_constant as const
def print_rejection_rate(myflagt_all):
    # 总的myflagt_all
    numlevbad = 0
    numprofbad = 0
    numprofall=len(myflagt_all)
    numlevall=0
    for myflagt_single in myflagt_all:
        myflagt_single=np.array(myflagt_single)
        num = np.sum(myflagt_single ==1)
        numlevall= numlevall + np.sum(myflagt_single >-0.5)
        numlevbad = numlevbad + num
        numprofbad = numprofbad + np.any(myflagt_single>0.1)


    import datetime
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%Y%m%d%H%M%S')
    OuputFilename='./COMS_AutoQC_output_stat_' + time_str + '.txt'
    f3 = open(OuputFilename, 'w')
    print('Data Validation completed',file=f3)
    print('Number of profiles = %i'% numprofall,file=f3)
    print('Number of observations = %i' % numlevall,file=f3)
    per=100.0*numlevbad/numlevall
    print('Percent_flagged_levels = %7.2f%%' % per,file=f3)
    per=100.0*numprofbad/numprofall
    print('Percent_flagged_profiles with at least one flag = %7.2f%%' % per,file=f3)

def cal_flag_number(myflagt_all,myflagt_checks,variable=1):
    ######## the inpurt variable "myflagtall" should be LIST type ############

    ## 计算各种flag的百分比
    numlevbad = 0
    numprofbad = 0
    numprofall=len(myflagt_all)
    numlevall=0
    for myflagt_single in myflagt_all:
        myflagt_single=np.array(myflagt_single)
        num = np.sum(myflagt_single ==1)
        numlevall= numlevall + np.sum(myflagt_single >-0.5)
        numlevbad = numlevbad + num
        numprofbad = numprofbad + np.any(myflagt_single>0.1)

    ################
    if(variable==1):  #temperatureQC
        number_of_checks=len(const.kflagt_T_list)  #14
    elif(variable==2):
        number_of_checks=len(const.kflagt_S_list)  #12
    # outlier_number_levels=np.zeros(number_of_checks,np.int)
    # outlier_number_profiles=np.zeros(number_of_checks,np.int)
    # for m in range(13):
    #     ### for levels 每一个模块，被标记为非0（异常值）的个数统计
    #     single_check=myflagt_checks[:,:,m]
    #     number_lev_bad=[Counter(single_check[i]==1).get(True) for i in range(len(single_check))] #列表推导
    #     number_lev_bad=np.array(number_lev_bad)
    #     outlier_number_levels[m]=np.sum(number_lev_bad[np.where(number_lev_bad != None)])
    #
    #     #for profiles 每一个剖面，至少有一个观测值被标记为非0（异常值）的个数统计
    #     number_prf_bad = [np.any(single_check[i]==1) for i in range(len(single_check))]  # 列表推导
    #     outlier_number_profiles[m]=sum(number_prf_bad)

    outlier_number_levels=np.zeros((number_of_checks,1))
    outlier_number_profiles=np.zeros((number_of_checks,1))
    for m in range(number_of_checks):  #14个检查模块
        for i in range(numprofall):  #N条廓线
            single_check=myflagt_checks[i][m]
            outlier_number_levels[m] = outlier_number_levels[m]+sum(single_check) # 列表推导
            outlier_number_profiles[m]=outlier_number_profiles[m]+any(single_check)


    return numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels,outlier_number_profiles
    # return numlevall,numprofall,numlevbad,numprofbad

def flag_stat_print_T(file, numprofbad, numprofall, numlevall, numlevbad,outlier_number_levels,outlier_number_profiles):

    print('Data Validation completed',file=file)
    print('Number of profiles = %i'% numprofall,file=file)
    print('Number of observations = %i' % numlevall,file=file)
    per=100.0*numlevbad/numlevall
    print('Percent_flagged_levels = %7.2f%%' % per,file=file)
    per=100.0*numprofbad/numprofall
    print('Percent_flagged_profiles with at least one flag = %7.2f%%' % per,file=file)

    print('\n',file=file)
    print('____________For LEVELS___________________________',file=file)
    print('Total Number of observed levels = %i' % numlevall,file=file)
    # print('Total Number of not-dummy T-levels = %i'% levnondumall,file=file_name)

    testch1= 'Failed basic infomation check_________________'
    testch2= 'Failed levels order check_____________________'
    testch3 = 'Failed instrument_type_depth check___________'
    testch4 = 'Failed GEBCO depth check_____________________'
    testch5 = 'Failed crude range check_____________________'
    testch6 = 'Failed freezing point check check____________'
    testch7 = 'Failed local climatology check_______________'
    testch8 = 'Failed constant value check__________________'
    testch9 = 'Failed spike check___________________________'
    testch10= 'Failed density inversion check_______________'
    testch11 = 'Failed temperature extrema check____________'
    testch12 = 'Failed global gradient check________________'
    testch13 = 'Failed local gradient climatology check_____'
    testch14 = 'Failed instrument specific type (XBT) check_'
    testch=[testch1,testch2,testch3,testch4,testch5,testch6,testch7,testch8,testch9,testch10,testch11,testch12,testch13,testch14]

    Percen_levfbad = 100.0* outlier_number_levels / numlevall
    Percen_probad = 100.0* outlier_number_profiles / numprofall

    number_of_checks = len(const.kflagt_T_list)

    for i in range(number_of_checks):
        print('%2i %s %i %10.3f%%' % (i+1,testch[i],outlier_number_levels[i],Percen_levfbad[i]),file=file)

    print('\r\n',file=file)   #换行
    print('_________For PROFILES with at least one flag_________',file=file)
    print('Total number of observed profiles = %i'% numprofall,file=file)
    for i in range(number_of_checks):
        print('%2i %s %i %10.3f%%' % (i+1,testch[i],outlier_number_profiles[i],Percen_probad[i]),file=file)

    return file


def flag_stat_print_S(file, numprofbad, numprofall, numlevall, numlevbad,outlier_number_levels,outlier_number_profiles):

    print('Data Validation completed',file=file)
    print('Number of profiles = %i'% numprofall,file=file)
    print('Number of observations = %i' % numlevall,file=file)
    per=100.0*numlevbad/numlevall
    print('Percent_flagged_levels = %7.2f%%' % per,file=file)
    per=100.0*numprofbad/numprofall
    print('Percent_flagged_profiles with at least one flag = %7.2f%%' % per,file=file)

    print('\n',file=file)
    print('____________For LEVELS___________________________',file=file)
    print('Total Number of observed levels = %i' % numlevall,file=file)
    # print('Total Number of not-dummy T-levels = %i'% levnondumall,file=file_name)

    testch1= 'Failed basic infomation check_________________'
    testch2= 'Failed levels order check_____________________'
    testch3 = 'Failed instrument_type_depth check___________'
    testch4 = 'Failed GEBCO depth check_____________________'
    testch5 = 'Failed salinity crude range check____________'
    testch6 = 'Failed global salinity-bottom check__________'
    testch7 = 'Failed global salinity-density check_________'
    testch8 = 'Failed local climatology check_______________'
    testch9 = 'Failed constant value check__________________'
    testch10 = 'Failed spike check__________________________'
    testch11 = 'Failed salinity extrema check_______________'
    testch12 = 'Failed global gradient check________________'
    testch=[testch1,testch2,testch3,testch4,testch5,testch6,testch7,testch8,testch9,testch10,testch11,testch12]

    Percen_levfbad = 100.0* outlier_number_levels / numlevall
    Percen_probad = 100.0* outlier_number_profiles / numprofall

    number_of_checks = len(const.kflagt_S_list)

    for i in range(number_of_checks):
        print('%2i %s %i %10.3f%%' % (i+1,testch[i],outlier_number_levels[i],Percen_levfbad[i]),file=file)

    print('\r\n',file=file)   #换行
    print('_________For PROFILES with at least one flag_________',file=file)
    print('Total number of observed profiles = %i'% numprofall,file=file)
    for i in range(number_of_checks):
        print('%2i %s %i %10.3f%%' % (i+1,testch[i],outlier_number_profiles[i],Percen_probad[i]),file=file)

    return file
    
def print_T_flag_txt(myflagt_all,kflagt_checks_all=None,OuputFilename=None):
    import os

    myflagt_all = [i for i in myflagt_all if i != []]

    if kflagt_checks_all is None:
        print_rejection_rate(myflagt_all)
        return

    kflagt_checks_all = [i for i in kflagt_checks_all if i != []]

    [numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels,outlier_number_profiles]=cal_flag_number(myflagt_all,kflagt_checks_all,1)

    if OuputFilename is None:
        import datetime
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, '%Y%m%d%H%M%S')
        OuputFilename='./CODC_AutoQC_Temp_output_stat_' + time_str + '.txt'
        f3 = open(OuputFilename, 'w')
    else:
        if (not isinstance(OuputFilename, str)):  #如果输入的不是字符串
            raise('Filename input is not str')
        if(os.path.exists(OuputFilename)):
            (_, filename) = os.path.split(OuputFilename)
            (OuputFilename, _) = os.path.splitext(filename)
            OuputFilename=OuputFilename+'_TempQC.txt'
        f3 = open(OuputFilename, 'w')

    f3=flag_stat_print_T(f3, numprofbad, numprofall, numlevall, numlevbad, outlier_number_levels, outlier_number_profiles)
    f3.close()
    return OuputFilename



def print_S_flag_txt(myflagt_all,kflagt_checks_all=None,OuputFilename=None):
    import os

    myflagt_all=[i for i in myflagt_all if i!=[]]

    if kflagt_checks_all is None:
        print_rejection_rate(myflagt_all)
        return

    kflagt_checks_all=[i for i in kflagt_checks_all if i!=[]]

    [numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels,outlier_number_profiles]=cal_flag_number(myflagt_all,kflagt_checks_all,2)

    if OuputFilename is None:
        import datetime
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, '%Y%m%d%H%M%S')
        OuputFilename='./CODC_AutoQC_Salinity_output_stat_' + time_str + '.txt'
        f3 = open(OuputFilename, 'w')
    else:
        if (not isinstance(OuputFilename, str)):  #如果输入的不是字符串
            raise('Filename input is not str')
        if(os.path.exists(OuputFilename)):
            (_, filename) = os.path.split(OuputFilename)
            (OuputFilename, _) = os.path.splitext(filename)
            OuputFilename=OuputFilename+'_SalinityQC.txt'
        f3 = open(OuputFilename, 'w')

    f3=flag_stat_print_S(f3, numprofbad, numprofall, numlevall, numlevbad, outlier_number_levels, outlier_number_profiles)
    f3.close()
    return OuputFilename