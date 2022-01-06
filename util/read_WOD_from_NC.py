import numpy as np
import numpy.ma as ma
import netCDF4 as nc

class metaData(object):
    def __init__(self):
        pass

def read_variables(f):
    import numpy as np
    import netCDF4 as nc
    temp=f.variables['Temperature'][:]
    temp = ma.array(temp, mask=np.isnan(temp.data))
    depth=f.variables['z'][:]
    depth = ma.array(depth, mask=np.isnan(depth.data))

    meta=metaData() #class
    meta.levels=len(depth)
    # meta.obsdepth=depth[~depth.mask][-1]  #只访问有效元素

    data_type=f.variables['dataset'][:]
    try:
        meta.typ3=str(nc.chartostring(data_type))
    except:
        meta.typ3='UNKNOWN'

    lat=f.variables['lat'][:]
    lat=lat.reshape(-1)
    meta.lat = lat[0]
    lon=f.variables['lon'][:]
    lon=lon.reshape(-1)
    lon=lon[0]
    if(lon>180 and lon<=360):
        lon=lon-360
    meta.lon = lon

    time_var=f.variables['time']
    dtime = nc.num2date(time_var[-1],time_var.units)
    # print(dtime)
    meta.year=dtime.year
    meta.month=dtime.month
    meta.day=dtime.day

    #查看类的属性 meta.__dict__.keys()
    return temp,depth,meta

def read_WOD(file):
    f = nc.Dataset(file, 'a')
    [tem, depth, meta]=read_variables(f)
    return f,tem, depth, meta

if __name__ == '__main__':
    file='E:\\11\\wod_002052715O.nc'
    [f,tem, depth, meta]=read_WOD(file)
    #查看类的属性 meta.__dict__.keys()