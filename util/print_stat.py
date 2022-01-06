import numpy as np

def cal_stat_list(myflagt_all,myflagt_checks_all):
    ######## the myflagt_all should be LIST type
    numlevall=sum(list(map(len,myflagt_all)))
    numprofall=len(myflagt_all)

    numlevbad=0
    numprofbad=0
    for myflagt in myflagt_all:
        num=np.sum(myflagt!=0)
        numlevbad=numlevbad+num
        numprofbad=numprofbad+np.any(myflagt)

    outlier_number_levels=np.zeros(13,np.int)
    # outlier_number_profiles=np.zeros(13,np.int)
    for m in range(13):
        for myflagt_check in myflagt_checks_all:
            num_bad=np.nansum(myflagt_check[:,m])
            outlier_number_levels[m]=outlier_number_levels[m]+num_bad

    return numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels

def print_flag_txt_list(myflagt_all,myflagt_checks_all,OuputFilename=None):
    [numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels]=cal_stat_list(myflagt_all,myflagt_checks_all)

    if OuputFilename is None:
        import datetime
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, '%Y%m%d%H%M%S')
        OuputFilename='./COMS_AutoQC_output_stat_' + time_str + '.txt'
        f3 = open(OuputFilename, 'w')
    else:
        if (not isinstance(OuputFilename, str)):  #如果输入的不是字符串
            raise('Filename input is not str')
        f3 = open(OuputFilename, 'w')
    f3=flag_stat_print_list(f3, numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels)
    f3.close()
    return OuputFilename

def flag_stat_print_list(file, numlevall,numprofall,numlevbad,numprofbad,outlier_number_levels):

    print(' Data Validation completed',file=file)
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
    testch10 = 'Failed temperature extrema check____________'
    testch11 = 'Failed global gradient check________________'
    testch12 = 'Failed local gradient climatology check_____'
    testch13 = 'Failed instrument specific type (XBT) check_'
    testch=[testch1,testch2,testch3,testch4,testch5,testch6,testch7,testch8,testch9,testch10,testch11,testch12,testch13]

    Percen_levfbad = 100.0* outlier_number_levels / numlevall

    for i in range(13):
        print('%2i %s %i %10.3f%%' % (i+1,testch[i],outlier_number_levels[i],Percen_levfbad[i]),file=file)

    return file