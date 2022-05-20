import glob
import os

import numpy.ma as ma
import pandas as pd
import numpy as np
import pickle
import math 

import matplotlib.pyplot as plt

from tqdm.notebook import tqdm
from datetime import date
import netCDF4 as nc

from scipy.interpolate import make_interp_spline, BSpline
from sklearn.metrics import mean_squared_error

os.getcwd()

##### get radiance (time is 10 may 2022, 12:00)
fn = 'C:/Users/anscha/Ecological Modelling course/Data/sentinel-3a (level 1)/S3A_OL_1_ERR____20220510T113946_20220510T122409_20220511T121916_2663_085_123______PS1_O_NT_002.SEN3/*radiance.nc'
radiances = glob.glob(fn, 
                   recursive = True)[2:6]

##### get radiance
coordinates = 'C:/Users/anscha/Ecological Modelling course/Data/sentinel-3a (level 1)/S3A_OL_1_ERR____20220510T113946_20220510T122409_20220511T121916_2663_085_123______PS1_O_NT_002.SEN3/geo_coordinates.nc'

lat = nc.Dataset(coordinates)['latitude'][:].filled(fill_value=np.nan).round(1)
lon = nc.Dataset(coordinates)['longitude'][:].filled(fill_value=np.nan).round(1)

oa3 = nc.Dataset(radiances[0])['Oa03_radiance'][:].filled(fill_value=np.nan)
oa4 = nc.Dataset(radiances[1])['Oa04_radiance'][:].filled(fill_value=np.nan)
oa5 = nc.Dataset(radiances[2])['Oa05_radiance'][:].filled(fill_value=np.nan)
oa6 = nc.Dataset(radiances[3])['Oa06_radiance'][:].filled(fill_value=np.nan)

data_vars = (lat, lon, oa3, oa4, oa5, oa6)
data = np.stack(data_vars, axis = -1)

### OC4Me algorithm
A0 = 0.450
A1 = -3.259
A2 = 3.522 
A3 = -3.359 
A4 = 0.949

all_lats = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
chl_conc = np.zeros((all_lats.shape[0],))
with tqdm(total=len(all_lats)) as pbar:
    for i, lat1 in enumerate(all_lats):
        idx_lat, idx_lon = np.where((data[:,:,0] == lat1) & (data[:,:,1] == -30.0)) 
        chl_value = 0
        dd = data[idx_lat, idx_lon, :]
        for j in range(dd.shape[0]):
            R = math.log10(np.max([dd[j,2]/dd[j,5], dd[j,3]/dd[j,5], dd[j,4]/dd[j,5]]))
            chl_value += pow(10, A0 + A1*R + A1*pow(R,2) + A1*pow(R,3) + A4*pow(R,4))
        chl_conc[i] = chl_value/dd.shape[0]
        pbar.update(1)

chl_model = pd.read_csv('C:/Users/anscha/Ecological Modelling course/Data/chl_all_coordinates.csv', header = None).to_numpy().reshape(12,10)  ### NUM model chl-a cconcentration

fig, ax = plt.subplots(figsize = (12,12))
for i, chl in enumerate(chl_model[::2]):
    
    # 300 represents number of points to make between T.min and T.max
    xnew = np.linspace(np.arange(0,10).min(), np.arange(0,10).max(), 100) 

    spl = make_interp_spline(np.arange(0,10), chl , k=3)  # type: BSpline
    power_smooth = spl(xnew)

    ax.plot(power_smooth, xnew, label = f'Lat: {all_lats[i*2]}, Lon: -30')
    ax.set_yticklabels(np.arange(-120,0,20))
plt.legend()
plt.xlabel('CHL-a concentration', fontsize = 16)
plt.ylabel('Depth', fontsize = 16)
plt.savefig(f'C:/Users/anscha/Ecological Modelling course/figures/water_column.png', dpi = 300)
plt.show()

#### integrating water column concentration to one chl-a concentration value
k_d = 0.05
#z = np.arange(0,30,10)
z = np.arange(0,100,10)
chl_sim = np.zeros((chl_model.shape[0],))
for i in range(chl_model.shape[0]):
    sum1 = 0
    sum2 = 0
    for j in range(z.shape[0]):
        sum1 += chl_model[i, j]*np.exp(-2*k_d*z[j])
        sum2 += np.exp(-2*k_d*z[j])
    chl_sim[i] = sum1/sum2
    
mean_error = mean_squared_error(chl_sim, chl_conc)

fig, ax = plt.subplots(figsize = (12,12))
fig.canvas.draw()
ax.plot(chl_sim, label = 'NUM model')
ax.plot(chl_conc, label = 'Satellite reading')
#ax.plot(chl_sim - chl_conc, label = 'error')
ax.set_xticklabels(np.append(0,all_lats[::2]))
ax.legend()
plt.show()

