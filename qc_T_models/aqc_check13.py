import numpy as np
import numpy.ma as ma
from CODCQC.util import CODCQC_constant as const

def gradient_climatology_check(qc_object,depth, tem, meta):
    levels = meta.levels
    kflagt = np.zeros(levels, int)
    typ3 = meta.typ3
    if (levels <= 3):  # not check for few levels profiles
        kflagt = np.zeros(levels, int)
        _ = np.nan
        return kflagt, _, _, _
  
    if ('MRB' in typ3 or 'moored buoy' in typ3 or 'mrb' in typ3 or 'SUR' in typ3):  # MRB是定点观测，不做梯度检查
        kflagt = np.zeros(levels, int)
        _ = np.nan
        return kflagt, _, _, _
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth = ma.array(depth, mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    rlat = meta.lat
    rlon = meta.lon
    month = meta.month 
    if (np.nanmax(depth)<=150):  #no check for upper 150m
        kflagt = np.zeros(levels, int)
        _ = np.nan
        return kflagt, _, _, _      
        
    #central difference to get the profile gradient in different interval levels
    t1 = np.diff(tem)
    t_left = t1[0:-1]
    t_right = t1[1:]
    d1 = np.diff(depth)
    d_left = d1[0:-1]
    d_right = d1[1:]
    distance_3points = d_left + d_right
    distance_3points = np.concatenate(([0], distance_3points, [d1[-1]]))
    dtdz = (t_left + t_right) / (d_left + d_right)
    dtdz = np.concatenate(([np.nan], dtdz, [t1[-1] / d1[-1]]))
    makeMean_gradient = np.zeros(levels, int)
    makeMean_gradient[distance_3points < 10] = 1  # distance inside three points，mean gradient
    dtdz_makeMeangradient = profile_mean_gradient_QC(meta, tem, depth, makeMean_gradient)
    dtdz[np.logical_and(makeMean_gradient == 1, ~np.isnan(dtdz_makeMeangradient))] = dtdz_makeMeangradient[
        np.logical_and(makeMean_gradient == 1, ~np.isnan(dtdz_makeMeangradient))]

    ###对distance_3points 进行分类识别，标记1，2，3，4，然后后面找对应的气候态
    distance_3points = np.round(distance_3points)
    distance_flag = distance_3points - 10 + 1
    # print(type(distance_flag))
    distance_flag[distance_flag >= 151] = np.nan  # no checks for distance greater than 160m (low resolution profile)
    distance_flag[distance_flag < 0] = 1
    distance_flag[makeMean_gradient == 1] = 1  # 小于10m的都用mean_gradient_clj 变到10m的间隔去算梯度

    # find grid-index for MIN/MAX-fields from lat/lon values
    try:
        jy = np.where(np.logical_and(rlat > qc_object.Grad_lat_bound[0, :], rlat <= qc_object.Grad_lat_bound[1, :]))[0][
            0]  # latitude
        ix = np.where(np.logical_and(rlon > qc_object.Grad_lon_bound[0, :], rlon <= qc_object.Grad_lon_bound[1, :]))[0][
            0]  # longitude
    except:
        kflagt = np.zeros(levels, int)
        _ = np.nan
        return kflagt, _, _, _

    # find depth-index for MIN/MAX-fields from depth values
    depth_index = []
    for k in range(levels):
        if (~isData[k]):
            depth_index.append(np.nan)
            continue
        try:
            depth_index.append(np.where(np.logical_and(depth[k] >= qc_object.Grad_std_depth_bound[0, :],
                                                       depth[k] < qc_object.Grad_std_depth_bound[1, :]))[0][0])
        except:
            depth_index.append(np.nan)
    Q05_grid_interp = climatology_horzional_interp(qc_object.Gradmin, ix, jy, qc_object.interp_grid, month)
    Q995_grid_interp = climatology_horzional_interp(qc_object.Gradmax, ix, jy, qc_object.interp_grid, month)


    depth_index = np.array(depth_index)
    index_NaN = np.logical_or(np.isnan(depth_index), np.isnan(distance_flag))
    depth_index = depth_index.astype(int)
    depth_index[index_NaN] = 0
    distance_flag = distance_flag.astype(int)
    distance_flag[index_NaN] = 1
    Gradmin_array = Q05_grid_interp[depth_index, distance_flag - 1]
    Gradmax_array = Q995_grid_interp[depth_index, distance_flag - 1]
    Gradmin_array[index_NaN] = const.DTDZminover
    Gradmax_array[index_NaN] = const.DTDZmaxover
    Gradmax_array[Gradmax_array > const.DTDZmaxover] = const.DTDZmaxover
    Gradmin_array[Gradmin_array < const.DTDZminover] = const.DTDZminover
    Gradmin_array[np.isnan(Gradmin_array)] = const.DTDZminover
    Gradmax_array[np.isnan(Gradmax_array)] = const.DTDZmaxover

    # input torlerance and start flagging
    type_advanced = ['CTD', 'CT', 'CU', 'ctd', 'PFL', 'pfl', 'profiling', 'DRB', 'Drifting','GLD','glider','Argo','argo']
    if (typ3 in type_advanced):
        # for PFL, CTD and GLD, gibe tolerance for the threshold
        index2 = depth < (np.nanmax(depth) - 10)
        index3 = depth <= 2000
        index4 = makeMean_gradient == 1
        index1 = np.logical_and.reduce([index2, index3, index4])  
        if ('GLD' in typ3):
            flag_noSignleSide = np.logical_or(
                (dtdz[index1 == 0] < Gradmin_array[index1 == 0] - np.abs(Gradmin_array[index1 == 0]) * 0.01),
                (dtdz[index1 == 0] > Gradmax_array[index1 == 0] + np.abs(Gradmax_array[index1 == 0]) * 0.01))
            flag_SignleSide = np.logical_or(
                (dtdz[index1 == 1] < Gradmin_array[index1 == 1] - np.abs(Gradmin_array[index1 == 1]) * 0.15),
                (dtdz[index1 == 1] > Gradmax_array[index1 == 1] + np.abs(Gradmax_array[index1 == 1]) * 0.15))
        else:
            flag_noSignleSide = np.logical_or(
                (dtdz[index1 == 0] < Gradmin_array[index1 == 0] - np.abs(Gradmin_array[index1 == 0]) * 0.1),
                (dtdz[index1 == 0] > Gradmax_array[index1 == 0] + np.abs(Gradmax_array[index1 == 0]) * 0.1))
            flag_SignleSide = np.logical_or(
                (dtdz[index1 == 1] < Gradmin_array[index1 == 1] - np.abs(Gradmin_array[index1 == 1]) * 0.2),
                (dtdz[index1 == 1] > Gradmax_array[index1 == 1] + np.abs(Gradmax_array[index1 == 1]) * 0.2))
        kflagt[index1 == 0] = flag_noSignleSide
        kflagt[index1 == 1] = flag_SignleSide
    elif ('XBT' in typ3 or 'xbt' in typ3):
        index1 = depth > 1000
        flag_upper1000 = np.logical_or(
            (dtdz[index1 == 0] < Gradmin_array[index1 == 0] - np.abs(Gradmin_array[index1 == 0]) * 0.01),
            (dtdz[index1 == 0] > Gradmax_array[index1 == 0] + np.abs(Gradmax_array[index1 == 0]) * 0.01))
        kflagt[index1 == 0] = flag_upper1000
        flag_T5 = np.logical_or(
            (dtdz[index1 == 1] < Gradmin_array[index1 == 1] - np.abs(Gradmin_array[index1 == 1]) * 0.3),
            (dtdz[index1 == 1] > Gradmax_array[index1 == 1] + np.abs(Gradmax_array[index1 == 1]) * 0.3))
        kflagt[index1 == 1] = flag_T5
    else:
        index2 = depth > (np.nanmax(depth) - 10)
        index3 = depth <= 2000
        index4 = makeMean_gradient
        index1 = np.logical_and.reduce([index2, index3, index4])  
        flag_noSignleSide = np.logical_or(
            (dtdz[index1 == 0] < Gradmin_array[index1 == 0] - np.abs(Gradmin_array[index1 == 0]) * 0.01),
            (dtdz[index1 == 0] > Gradmax_array[index1 == 0] + np.abs(Gradmax_array[index1 == 0]) * 0.01))
        flag_SignleSide = np.logical_or(
            (dtdz[index1 == 1] < Gradmin_array[index1 == 1] - np.abs(Gradmin_array[index1 == 1]) * 0.2),
            (dtdz[index1 == 1] > Gradmax_array[index1 == 1] + np.abs(Gradmax_array[index1 == 1]) * 0.2))
        kflagt[index1 == 0] = flag_noSignleSide
        kflagt[index1 == 1] = flag_SignleSide
    if (not ('XBT' in typ3 or 'xbt' in typ3)):  
        kflagt[depth < 10] = 0
    
    kflagt[depth <= 150] = 0  #no check for upper 150m 

    return kflagt, dtdz, Gradmin_array, Gradmax_array



def profile_mean_gradient_QC(meta,tem,depth,makeMean_gradient,depth_interval_left=10,depth_interval_right=12.5):
    dtdz=np.full(meta.levels,np.nan)
    dz=np.concatenate(([0],np.diff(depth)))
    isData = np.logical_and(depth.mask == False, tem.mask == False)
    
    for k in range(1,meta.levels):
        if(~isData[k]):
            continue
        if(makeMean_gradient[k]):
            index=k
            #找出左右的位置索引
            i=1
            flag=1   ##右1左2
            depth_inteval=0
            loop_time=1
            left_index,right_index=np.nan,np.nan

            if(depth[-1]-depth[k]>=10):
                while(depth_inteval<depth_interval_right):
                    if(loop_time==1):
                        depth_inteval=dz[index]
                        left_index=index-1
                        right_index=index
                    elif(flag==1):
                        try:
                            depth_inteval=depth_inteval+dz[index+i]
                        except:
                            break
                        flag=2  #回到左侧
                        right_index=right_index+1
                    else:
                        try:
                            depth_inteval = depth_inteval + dz[index - i]
                        except:
                            break
                        flag=1  #下一个循环回到右侧
                        left_index=left_index-1
                        i=i+1
                    loop_time=loop_time+1
                    if(depth_inteval>depth_interval_left):
                        break

                if(left_index<0):
                    left_index=0
                if(right_index>=meta.levels-1):
                    right_index=meta.levels-1

                ###对找出的位置做中央差分，然后求mean gradient
                if(depth_inteval<=7):  ##不够10m，一条廓线，特别是最开始的几个点 和最后的几个点，depth_interval前后不够位置差分，导致算出来的梯度很大
                    #采用单边差分补足5m
                    if(right_index==meta.levels-1):  #廓线最后几个点，往左边补足5m
                        while((depth[k]-depth[left_index])<5):
                            left_index=left_index-1
                        depth_inteval=depth[right_index]-depth[left_index]
                    else:
                        dtdz[k]=np.nan

                #把温度插值到前后5m，1m一个网格点的位置上，对齐到depth_interval的深度，或者对齐到10m的深度所在的温度
                temp_select=tem[left_index:right_index+1]
                depth_select=depth[left_index:right_index+1]
                depth_interp=np.arange(depth[k]-5,depth[k]+6)
                try:
                    # f = interp1d(depth_select, temp_select, kind='linear', bounds_error=False)
                    # tem_interp = f(depth_interp)
                    tem_interp = np.interp(depth_interp, depth_select, temp_select, left=np.nan, right=np.nan,
                                          period=None)
                except:  #深度有重复值，插值不了
                    temp_left=np.nanmean(tem[left_index:k+1])
                    temp_right=np.nanmean(tem[k+1:right_index+1])
                    dtdz[k]=(temp_right-temp_left)/depth_inteval
                    continue
                temp_left=np.nanmean(tem_interp[:6])
                temp_right=np.nanmean(tem_interp[6:])
                dtdz[k]=(temp_right-temp_left)/10
            else:  #廓线最后10m，采用往左边单边5m差分
                if(meta.levels>=10):
                    right_index=k
                    left_index=right_index-1
                    while((depth[k]-depth[left_index])<5):
                        if(left_index==0):
                            break
                        left_index=left_index-1
                    depth_inteval=depth[right_index]-depth[left_index]
                    temp_right=tem[right_index]                    
                    temp_left=np.nanmean(tem[left_index:right_index])
                    dtdz[k]=(temp_right-temp_left)/depth_inteval

    return dtdz

def climatology_horzional_interp(data_5D,ix,jy,interp_grid,month):
    horzional_interval = np.array([10, 20, 40, 60, 100, 160])
    horizonal_interval_interp = np.arange(10,161)
    data_grid=np.squeeze(data_5D[ix,jy,:,month-1,:])
    data_grid_interp=np.full((79,len(horizonal_interval_interp)),int)
    for k in range(79):
        # f = interp1d(horzional_interval, np.squeeze(data_grid[k,:]), kind='linear', bounds_error=False)
        # data_grid_interp[k]=f(horizonal_interval_interp)
        data_grid_interp[k] = np.interp(horizonal_interval_interp, horzional_interval, np.squeeze(data_grid[k,:]), left=np.nan, right=np.nan,
                               period=None)
    data_grid_interp[np.isnan(interp_grid)]=np.nan
    data_grid_interp=data_grid_interp.astype(np.float32)
    return data_grid_interp