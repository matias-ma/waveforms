#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

# Uses the raw ATWD of HNLs to make waveforms

from icecube import icetray,dataio,dataclasses, simclasses, recclasses
import os
import numpy as np
from matplotlib import pylab as plt
import matplotlib as mpl
import scipy 
from scipy.spatial import distance

mpl.rcParams['font.size'] = 15
mpl.rcParams['figure.figsize'] = (10,5)

if os.path.exists('/home/mandia/waveform/wf/plots') is True: 
    os.system('rm -r /home/mandia/waveform/wf/plots')
    os.mkdir('/home/mandia/waveform/wf/plots')
else:   
    os.mkdir('/home/mandia/waveform/wf/plots')


g_f = dataio.I3File('/data/ana/BSM/HNL/GCD/GeoCalibDetectorStatus_IC86.AVG_Pass2_SF0.99.i3.gz')
g_frame = g_f.pop_frame()
g_frame = g_f.pop_frame()
g_frame = g_f.pop_frame()
g_frame = g_f.pop_frame()
geo = g_frame['I3Geometry']


for i in range(1,10):
    f = dataio.I3File('/data/ana/BSM/HNL/MC/190607/Ares/IC86.AVG/Det/domeff_0.97/00001-01000/Det_00_11_0000'+str(i)+'.i3.zst')
    os.mkdir('/home/mandia/waveform/wf/plots/event'+str(i))

    for x in range(1,25):
        os.mkdir('/home/mandia/waveform/wf/plots/event'+str(i)+'/frame'+str(x))
        # for z in range(x):
        frame = f.pop_daq()
        
        try:
            both_casc = np.loadtxt('/home/mandia/waveform/wf/pos/pos'+str(i)+'_'+str(x)+'.txt')
        except:
            pass

        casc0 = np.array([])
        casc0 = np.append(casc0, both_casc[0,])

        for q in range(len(frame['InIceRawData'])):
            omkey,domlaunches = frame['InIceRawData'].items()[q]
            for z in range(len(domlaunches)):
                domlaunch = domlaunches[z]
                wf = domlaunch.raw_atwd[0]
                t = domlaunch.time

                # bandaid to get real time
                pos = np.array([])
                arr = np.array([omkey])
                first = int(arr[:,0])
                second = int(arr[:,1])
                third = int(arr[:,2])
                om = getattr(icetray, 'OMKey')(first, second, third)
                position = geo.omgeo[om].position
                pos = np.append(pos, position)
                dist0 = distance.euclidean(casc0,pos)
                time0 = dist0/dataclasses.I3Constants.c_ice
                try:
                    old_t = np.loadtxt('/home/mandia/waveform/wf/time/time'+str(i)+'_'+str(x)+'.txt')
                    bandaid_time0 = time0 + old_t[0]
                except:
                    pass
                    
                for g in range(len(frame['MCPESeriesMap']))
                    mcpe = frame['MCPESeriesMape'].items(g)
                
                if domlaunch.lc_bit is True:
                    
                    val = np.array(range(len(wf)))
                    plt.plot(val*3.3,wf, ds = 'steps')
                    # plt.title('Simulation '+str(i)+' Event '+str(x)+' %s raw ATWD 0' % omkey + ' Start time: '+str(int(t))+' ns')
                    plt.title('Simulation '+str(i)+' Event '+str(x)+' %s raw ATWD 0' % omkey + ' Start time: '+str(int(bandaid_time0))+' ns')
                    plt.ylabel('Counts')
                    plt.xlabel('Time (ns)')
                    if len(domlaunches)>1:
                        plt.savefig('/home/mandia/waveform/wf/plots/event'+str(i)+'/frame'+str(x)+'/wf'+str(q)+'_'+str(z)+'.png')
                    else:
                        plt.savefig('/home/mandia/waveform/wf/plots/event'+str(i)+'/frame'+str(x)+'/wf'+str(q)+'.png')
                    plt.clf()
                        

        


