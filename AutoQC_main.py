""" Apply Auto-Quality Control of temperature profiles
"""
import numpy as np
import numpy.ma as ma
from COMSQC.util.aqc_constant import kflagt_list
from COMSQC.qc_models import check_aqc_01 as check01
from COMSQC.qc_models import check_aqc_02 as check02
from COMSQC.qc_models import check_aqc_03 as check03
from COMSQC.qc_models import check_aqc_04 as check04
from COMSQC.qc_models import check_aqc_05 as check05
from COMSQC.qc_models import check_aqc_06 as check06
from COMSQC.qc_models import check_aqc_07 as check07
from COMSQC.qc_models import check_aqc_08 as check08
from COMSQC.qc_models import check_aqc_09 as check09
from COMSQC.qc_models import check_aqc_10 as check10
from COMSQC.qc_models import check_aqc_11 as check11
from COMSQC.qc_models import check_aqc_12 as check12
from COMSQC.qc_models import check_aqc_13 as check13
from COMSQC.util import aqc_combine_flags


def check_profileQC_main(depth,tem,meta):
    if(not ma.isMaskedArray(depth)):
        depth=ma.array(depth,mask=np.isnan(depth))
    if(not ma.isMaskedArray(tem)):
        tem = ma.array(tem, mask=np.isnan(tem))
    
    kflagt1 = check01.basic_information_check(depth, tem, meta)

    [kflagt2, depth, tem] = check02.levels_order(depth, tem, meta)

    kflagt3 = check03.instrument_type_depth(depth, tem, meta)

    kflagt4 = check04.gebo_check(depth, tem, meta)

    kflagt5 = check05.crude_range(depth, tem, meta)

    kflagt6 = check06.freezing_point_check(depth, tem, meta)

    [kflagt7, _, _] = check07.climatology_check(depth, tem, meta)

    kflagt8 = check08.constant_value(depth, tem, meta)

    kflagt9 = check09.spike_check(depth, tem, meta)

    kflagt10 = check10.number_of_temperature_extrema(depth, tem, meta)

    kflagt11 = check11.global_gradient_check(depth, tem, meta)

    [kflagt12, _, _, _] = check12.gradient_climatology_check(depth, tem, meta)

    kflagt13 = check13.instrument_specific_check_XBT(depth, meta, kflagt12)

    #检combine flag
    kflagt_all = []
    for key in kflagt_list:
        kflagt_all.append(eval(key))
    myflagt_checks = aqc_combine_flags.combine_flag_int(kflagt_all)
    myflagt = np.sum(myflagt_checks, 1)
    myflagt[np.logical_and(myflagt > 0.5, myflagt < 98)] = 1

    return myflagt,myflagt_checks


def depth_Tem_isMatch(depth,tem):
    if(len(depth) == len(tem)):
        return
    else:
        raise('Inconsistent array length!!')