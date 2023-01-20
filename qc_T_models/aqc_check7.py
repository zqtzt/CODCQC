import numpy as np
import numpy.ma as ma
from CODCQC.util import CODCQC_constant as const

def climatology_check(qc_object,depth, tem, meta):
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth = ma.array(depth, mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    levels = meta.levels
    rlat = meta.lat
    rlon = meta.lon
    month = meta.month
    iyear=meta.year

    tmin_array = []
    tmax_array = []
    kflagt = np.zeros(levels, np.int)
    if (levels == 0):
        return kflagt, tmin_array, tmax_array

    # find grid-index for MIN/MAX-fields from lat/lon values
    try:
        jy = np.where(np.logical_and(rlat > qc_object.lat_bound[0, :], rlat <= qc_object.lat_bound[1, :]))[0][0]  # 纬度
        ix = np.where(np.logical_and(rlon > qc_object.lon_bound[0, :], rlon <= qc_object.lon_bound[1, :]))[0][0]  # 经度
    except:
        return kflagt, tmin_array, tmax_array

    if ((ix < 0 or ix > 361) or (jy < 0 or jy > 181)):
        descrption = 'no find ix,jy,no climatology check'
        # print(descrption)
        return kflagt, tmin_array, tmax_array

    # find depth-index for MIN/MAX-fields from depth values
    depth_index = []
    for k in range(levels):
        if (~isData[k]):
            depth_index.append(np.nan)
            continue
        try:
            depth_index.append(np.where(
                np.logical_and(depth[k] >= qc_object.Std_depth_bound[0, :], depth[k] < qc_object.Std_depth_bound[1, :]))[0][0])
        except:
            depth_index.append(np.nan)

    for i in range(levels):
        if (np.isnan(depth_index[i])):
            tmin_array.append(const.parminover_T)
            tmax_array.append(const.parmaxover_T)
            continue
        if (depth_index[i] < 79):  # has monthly climatological range data
            tmina = qc_object.tmin[ix, jy, depth_index[i], month - 1]
            tmaxa = qc_object.tmax[ix, jy, depth_index[i], month - 1]
            ##########2022.10.3 time-varying IAP-T-range
            T_clim_year=1981
            # give tolerant for the threshold
            year_diff = iyear - T_clim_year
            if(year_diff>0):
                coeff_Tmax = qc_object.kmax_T[ix, jy, depth_index[i], month-1]
                if(coeff_Tmax<0):  # 系数k小于0，不缩小最大值范围，就保留原状
                    coeff_Tmax=np.nan
                coeff_Tmin = qc_object.kmin_T[ix, jy, depth_index[i], month-1]
                if(coeff_Tmin>0): #系数k大于0，不缩小最小孩范围，就保留原状
                    coeff_Tmin=np.nan
                if (not np.isnan(year_diff * coeff_Tmax)):
                    tmaxa = tmaxa + year_diff * np.abs(coeff_Tmax)
                if (not np.isnan(year_diff * coeff_Tmin)):
                    tmina = tmina - year_diff * np.abs(coeff_Tmin)
            elif(year_diff<0): #年份在左侧
                year_diff = np.abs(year_diff)
                coeff_Tmin = qc_object.kmin_T[ix, jy, depth_index[i], month-1]
                if(coeff_Tmin<0):
                    coeff_Tmin=np.nan
                coeff_Tmax = qc_object.kmax_T[ix, jy, depth_index[i], month-1]
                if(coeff_Tmax>0):
                    coeff_Tmax=np.nan
                if (not np.isnan(year_diff * coeff_Tmin)):
                    tmina = tmina - year_diff * np.abs(coeff_Tmin)
                if (not np.isnan(year_diff * coeff_Tmax)):
                    tmaxa = tmaxa + year_diff * np.abs(coeff_Tmax)
            if (tmina <= const.parminover_T or np.isnan(tmina)):
                tmina = const.parminover_T
            if (tmaxa >= const.parmaxover_T or np.isnan(tmaxa)):
                tmaxa = const.parmaxover_T
        elif (depth_index[i] >= 79 and depth_index[i] <= 98):  # 2000m-4000m: seasonal climatological threshold
            # 判断是哪个季节，12，1，2为冬天
            if month in [3, 4, 5]:
                imonth = 14
            elif month in [6, 7, 8]:
                imonth = 15
            elif month in [9, 10, 11]:
                imonth = 16
            elif month in [12, 1, 2]:
                imonth = 13
            tmina = qc_object.tmin[ix, jy, depth_index[i] - 79, imonth - 1]
            tmaxa = qc_object.tmax[ix, jy, depth_index[i] - 79, imonth - 1]
            if (tmina <= const.parminover_T or np.isnan(tmina)):
                tmina = const.parminover_T
            if (tmaxa >= const.parmaxover_T or np.isnan(tmaxa)):
                tmaxa = const.parmaxover_T
        elif (depth_index[i] > 98):  # 4000m-6000m 'all years' climatological
            tmina = qc_object.tmin[ix, jy, depth_index[i] - 99, 16]
            tmaxa = qc_object.tmax[ix, jy, depth_index[i] - 99, 16]
            if (tmina <= const.parminover_T or np.isnan(tmina)):
                tmina = const.parminover_T
            if (tmaxa >= const.parmaxover_T or np.isnan(
                    tmaxa)): 
                tmaxa = const.parmaxover_T
        tmin_array.append(tmina)
        tmax_array.append(tmaxa)

    # input torlerance and start flagging
    type_advanced = ['CTD', 'CT', 'CU', 'ctd', 'PFL', 'pfl', 'profiling', 'DRB', 'Drifting']
    if (meta.typ3 in type_advanced):
        tmin_array = np.array(tmin_array)
        tmin_array = tmin_array - np.abs(tmin_array) * 0.04
        tmax_array = np.array(tmax_array)
        tmax_array = tmax_array + np.abs(tmax_array) * 0.04
        kflagt[np.logical_or(tem < tmin_array, tem > tmax_array)] = 1
    else:
        tmin_array = np.array(tmin_array)
        tmin_array = tmin_array - np.abs(tmin_array) * 0.01
        tmax_array = np.array(tmax_array)
        tmax_array = tmax_array + np.abs(tmax_array) * 0.01
        kflagt[np.logical_or(tem < tmin_array, tem > tmax_array)] = 1

    if ('DRB' in meta.typ3 or 'Drifting' in meta.typ3):  # no checks for DRB greater than 760m
        kflagt[depth > 760] = 0

    return kflagt, tmin_array, tmax_array