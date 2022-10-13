import numpy as np
from CODCQC.util import CODCQC_constant as const


def combine_flag(kflagt_all):
    levels=len(kflagt_all[0])
    myflagt=np.zeros(levels,int)

    # set final level flag as the minimum flag at each observed level  合并每一层的标记，如果一个观测点有多个标记，取最小的那个值（除了0）
    all_flag=kflagt_all[0]
    for i,kflagt in enumerate(kflagt_all):
        if(i==0):
            continue
        all_flag=np.vstack([all_flag,kflagt])
    flag_bool=np.any(all_flag,0)
    all_flag[np.where(all_flag==0)]=99
    flag_value=np.nanmin(all_flag,0)
    myflagt[flag_bool]=flag_value[flag_bool]

    ## set excessive percentage of flagged levels >=75%
    if(levels>=5):
        nflagged=np.sum(myflagt!=0)
        perbad=100.0*nflagged/levels #perbad=precentage of bad data
        if(perbad >= const.perlimbad):
            myflagt[:]=1  #整层标记

    return myflagt






