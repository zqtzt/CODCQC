import numpy as np
from CODCQC.util import CODCQC_constant as const
import numpy.ma as ma
import gsw

def density_inversion_check(qc_object,depth, tem, meta,salinity=[]):
    levels = meta.levels
    kflagt = np.zeros(levels, int)
    if (levels <= 2):
        return kflagt
    if(np.all(np.isnan(salinity)) or salinity==[]):  #no salinity observation, pass
        return kflagt
    if('MRB' in meta.typ3 or 'mrb' in meta.typ3 or 'buoy' in meta.typ3):
        return kflagt
    rlat = meta.lat
    rlon = meta.lon
    # month = meta.month
    # iyear=meta.year
    # meta.typ3

    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth = ma.array(depth, mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        # salinity = ma.array(salinity,mask=np.isnan(salinity))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
        # isData = np.logical_and(isData.mask==False, salinity.mask==False)

    pressure=gsw.p_from_z(-depth,rlat)
    SA=gsw.SA_from_SP(salinity,pressure,rlon,rlat)
    CT=gsw.CT_from_t(SA,tem,pressure)
    density=gsw.rho(SA,CT,pressure)  #kg/m^3
    density = density/1000  #g/cm^3
    # density[np.logical_or(density>=1053,density<=1002.5)]=np.nan

    #begin QC
    depth_diff=np.diff(depth)
    depth_diff[depth_diff < 1] = np.nan
    depth_diff[depth_diff < 3]= 3
    density_diff = np.diff(density) / depth_diff

    density_diff = np.insert(density_diff, 0, np.nan)

    kflagt[np.logical_and(depth<=30,density_diff<=-3e-5)]=1
    kflagt[np.logical_and(np.logical_and(depth>30,depth<=400),density_diff<=-2e-5)]=1
    kflagt[np.logical_and(depth>400, density_diff<=-1e-6)]=1
    kflagt[depth<=3.01]=0 # surface no perform QC near surface area

    return kflagt