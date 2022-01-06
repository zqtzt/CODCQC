#global gradient check
'''
This check identifies temperature observations for which its vertical temperature gradient exceeds the overall depth-dependent gradient climatological range
The gradient ranges are deﬁned on the basis of the depth–gradient histograms.
Both observations are ﬂagged when the vertical gradient falls outside the range.
'''
import numpy as np
import numpy.ma as ma
from COMSQC.util import aqc_constant as const

def movmean(T, m):
    assert (m <= T.shape[0])
    n = T.shape[0]

    sums = np.zeros(n - m + 1)
    sums[0] = np.sum(T[0:m])

    cumsum = np.cumsum(T)
    cumsum = np.insert(cumsum, 0, 0) 

    sums = cumsum[m:] - cumsum[:-m]
    return sums / m

def global_gradient_check(depth,tem,meta):
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth=ma.array(depth,mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
        
    levels=meta.levels

    kflagt=np.zeros(levels,int)
    if (levels < 3):
        descrption = '<3 levels,no gradient check'
        return kflagt

    index=np.logical_or(tem <= const.parminover, tem >= const.parmaxover)
    kflagt[index]=1

    gradient=np.diff(tem) / np.diff(depth)  #gradient calculation
    zedg=movmean(depth,2)  #zedg=0.5*(depth[i]+depth[i+1])
    zedg[zedg<1]=1

    # The gradient ranges are deﬁned on the basis of the depth–gradient histograms.
    gradmin = -150.0 / zedg - 0.010
    gradmin[gradmin<-4]=-4.0
    gradmax = 100.0 / zedg + 0.015
    gradmax[gradmax>1.5]=1.5

    index=np.logical_or(gradient < gradmin,gradient > gradmax)
    index=np.insert(index,0,False)
    kflagt[index]=1
    index2=np.where(index==True)[0]-1
    kflagt[index2]=1   #set valiedatoion flags kflagt8 = 1 at levels k and k+1

    return kflagt






