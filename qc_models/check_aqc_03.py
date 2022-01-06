#  instrument_type_depth check
'''
Different oceanographic instruments have their nominal maximum sampled depth (e.g., CTD is 8000m, XBT is 2200m). 
If observed depth value falls outside the nomial maximum depth, the temperature values at these depth are flagged as 1.
'''
import numpy as np


def istight(t, thresh=0.1):
    # given a temperature profile, return an array of bools
    # true = this level is within thresh of both its neighbors
    gaps = np.absolute(np.diff(t))
    left = np.append(gaps,0)   
    right = np.insert(gaps,0,0)  
    return (left<thresh) & (right<thresh)

def instrument_type_depth(depth,tem,meta):
    typ3=meta.typ3
    levels=meta.levels
    obsdepth=depth[~depth.mask][-1]

    kflagt4=np.zeros(levels,int)
    if(levels<=3):
        return kflagt4

    type_advanced=['OSD','CTD','CD','CT','CU','MC','XC','XCTD']
    if((typ3 in type_advanced) and obsdepth>=9000.0):  
        kflagt4[np.where(depth > 9000.0)] = 1
    elif(('PFL' in typ3 or 'PF' in typ3 or 'profiling float' in typ3) and obsdepth>=6050.0):
        kflagt4[np.where(depth > 6050.0)] = 1
    elif('APB' in typ3 and obsdepth>=1200.0):
        kflagt4[np.where(depth > 1200.0)] = 1
    elif(('MBT' in typ3 or 'MB' in typ3) and obsdepth>=320.0):
        if(obsdepth>=1900.0):  #### Japanese ship
            kflagt4[np.where(depth > 2020.0)] = 1
        else:  ####normal MBT
            kflagt4[np.where(depth > 320.0)] = 1
    elif(('XBT' in typ3 or 'XB' in typ3) and obsdepth>=2200.0): 
        kflagt4[np.where(depth > 2200.0)] = 1

    if('CTD' in typ3 or 'CD' in typ3 or 'CT' in typ3 or 'CU' in typ3):  #CTD above 2meters are all flagged
        kflagt4[np.where(depth < 2.0)] = 1
    if('XBT' in typ3 or 'XB' in typ3):
        kflagt4[np.where(depth < 3)] = 1

    # For drfiting buoys, checking the last two observed level: if the last two tempearture records are the same, flag the last one
    if('DRB' in typ3 or 'Drifting' in typ3):
        if(np.abs(tem[-1]-tem[-2])<=1e-3):
            kflagt4[np.where(depth==depth[-1])]=1

    kflagt4[kflagt4 == 1] = 1

    return kflagt4


if __name__ == '__main__':
    cc='CN'
    typ3='CTD'
    instrument_type_max_obs_depth(tem,depth,meta)