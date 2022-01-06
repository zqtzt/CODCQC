## SET FLAGT11 flag: excessive percentage of flagged levels (for non-dummy) --75%
import numpy as np
from COMSQC.util import aqc_constant as const

def combine_flag(kflagt_all):

    levels=len(kflagt_all[0])
    myflagt=np.zeros(levels,np.int)

    ## set excessive percentage of flagged levels >=75%
    perbad=0
    if(levels>=3):
        isnumt=sum(kflagt_all)
        nflagged=np.sum(isnumt!=0)

        # perbad=0
        perbad=100.0*nflagged/levels #perbad=precentage of bad data
        if(perbad >= const.perlimbad):
            myflagt[:]=2  #整层标记

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

    return myflagt

def combine_flag_str(kflagt_all):

    levels=len(kflagt_all[0])
    # num_check=len(kflagt_all)

    myflagt = np.array(kflagt_all)
    myflagt=np.transpose(myflagt)   #7行13列
    myflagt=myflagt.astype(dtype='U20').tolist()

    new_myflagt=np.zeros((levels),str).astype(dtype='U20')
    for i,flag in enumerate(myflagt):
        new_myflagt[i]=''.join(flag)

    return new_myflagt

def combine_flag_int(kflagt_all):

    levels=len(kflagt_all[0])
    # num_check=len(kflagt_all)

    myflagt = np.array(kflagt_all)
    myflagt=np.transpose(myflagt)   #7行13列

    return myflagt



