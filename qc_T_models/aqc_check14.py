import numpy as np

def instrument_specific_check_XBT(qc_object,depth, kflagt12, meta):
    levels = meta.levels
    kflagt = np.zeros(levels, int)
    typ3 = meta.typ3
    if (not ('XBT' in typ3 or 'xbt' in typ3 or 'xb' in typ3 or 'XB' in typ3)):
        return kflagt
    if (levels <= 3):  # not check for few levels profiles
        return kflagt
    if (np.nanmax(depth)<=150):  #no check for upper 150m
        return kflagt     
    #central difference to get the profile gradient in different interval levels
    d1 = np.diff(depth)
    d_left = d1[0:-1]
    d_right = d1[1:]
    distance_3points = d_left + d_right
    distance_3points = np.concatenate(([0], distance_3points, [d1[-1]]))
    makeMean_gradient = np.zeros(levels, int)
    makeMean_gradient[distance_3points < 10] = 1 

    #####main check
    if (np.nanmax(depth) <= 650):
        [kflagt, XBT_flag] = check_XBT_T4_T6(depth, makeMean_gradient, kflagt12)
    elif (np.nanmax(depth) <= 1200):
        [kflagt, XBT_flag] = check_XBT_T7_DB(depth, makeMean_gradient, kflagt12)
    
    kflagt[depth <= 150] = 0 
    return kflagt


def groupby(data1D):
    data1D=data1D[~np.isnan(data1D)]
    k=np.diff(np.concatenate(([0], data1D,[0])))
    loc_begin=np.where(k==1)[0]
    num_continue=np.where(k==-1)[0]-loc_begin
    return num_continue,loc_begin

def check_XBT_T4_T6(depth,makeMake_gradient,kflagt):
    begin_depth=150  #从150米往下
    maximum_depth=650
    XBT_flag=0
    if(np.nanmax(depth)<maximum_depth and np.nansum(makeMake_gradient)>10 and np.nansum(kflagt[depth>begin_depth])>10):
        flag_data=kflagt[depth<maximum_depth]
        [num_continue,loc_begin]=groupby(flag_data)
        index3=num_continue>=6
        times=np.nansum(index3)
        if(times>=2):
            weizhi=loc_begin[index3][0]
            flag_data[weizhi:]=1
            kflagt[depth<maximum_depth]=flag_data
            XBT_flag=1
        if(np.nansum(num_continue>=25)):
            weizhi=loc_begin[num_continue>=25][0]
            flag_data[weizhi:]=1
            kflagt[depth<maximum_depth]=flag_data
            XBT_flag=1

        ######400m以下，只要出现一次漂移，漂移之后的点全部标记为错误
        flag_data=kflagt[np.logical_and(depth>400,depth<650)]
        [num_continue, loc_begin] = groupby(flag_data)
        index4=num_continue>=6
        times=np.nansum(index4)
        if(times>=1):
            weizhi=loc_begin[index4][0]
            flag_data[weizhi:]=1
            kflagt[np.logical_and(depth>400,depth<650)]=flag_data
            XBT_flag=1

    return kflagt,XBT_flag

def check_XBT_T7_DB(depth,makeMake_gradient,kflagt):
    begin_depth=400
    maximum_depth=1200
    XBT_flag=0
    if(np.nanmax(depth)<maximum_depth and np.nansum(makeMake_gradient)>20 and np.nansum(kflagt[depth>begin_depth])>15):
        flag_data=kflagt[depth>begin_depth]
        [num_continue,loc_begin]=groupby(flag_data)
        index3=num_continue>=6
        times=np.nansum(index3)
        if(np.nansum(num_continue>=70)):
            weizhi=loc_begin[num_continue>=70][0]
            flag_data[weizhi:]=1
            kflagt[depth>begin_depth]=flag_data
            XBT_flag=1

        if(times>=7):
            weizhi=loc_begin[index3][0]
            flag_data[weizhi:]=1
            kflagt[depth>begin_depth]=flag_data
            XBT_flag=1
        else:
            flag_data=kflagt[depth>700]
            [num_continue, loc_begin] = groupby(flag_data)
            index4=num_continue>=6  #出现连续大于6个点被标记的次数
            times=np.nansum(index4)
            if(times>=3):
                weizhi=loc_begin[index4][0]
                flag_data[weizhi:]=1
                kflagt[depth>700]=flag_data
                XBT_flag=1
            if(np.nansum(num_continue>=35)):
                weizhi=loc_begin[num_continue>=35][0]
                flag_data[weizhi:]=1
                kflagt[depth>700]=flag_data
                XBT_flag=1


        ######800m以下，只要出现一次漂移，漂移之后的点全部标记为错误
        flag_data=kflagt[depth>800]
        [num_continue, loc_begin] = groupby(flag_data)
        index4=num_continue>=5
        times=np.nansum(index4)
        if(times>=1):
            weizhi=loc_begin[index4][0]
            flag_data[weizhi:]=1
            kflagt[depth>800]=flag_data
            XBT_flag=1

    return kflagt,XBT_flag
