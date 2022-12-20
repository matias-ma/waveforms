# python3

# Uses the raw FADC of HNLs to make waveforms

from icecube import icetray,dataio,dataclasses, simclasses, recclasses
import os
import numpy as np
from matplotlib import pylab as plt
import matplotlib as mpl

mpl.rcParams['font.size'] = 15
mpl.rcParams['figure.figsize'] = (10,5)

if os.path.exists('/home/mandia/waveform/wf/plots') is True: 
    os.system('rm -r /home/mandia/waveform/wf/plots')
    os.mkdir('/home/mandia/waveform/wf/plots')
else:   
    os.mkdir('/home/mandia/waveform/wf/plots')
# frame = f.pop_daq()
# os.mkdir('/home/mandia/waveform/wf')
wft = np.array([])
for i in range(1,10):
    f = dataio.I3File('/data/ana/BSM/HNL/MC/190607/Ares/IC86.AVG/Det/domeff_0.97/00001-01000/Det_00_11_0000'+str(i)+'.i3.zst')
    os.mkdir('/home/mandia/waveform/wf/plots/event'+str(i))

    for x in range(1,25):
        os.mkdir('/home/mandia/waveform/wf/plots/event'+str(i)+'/frame'+str(x))
        # for z in range(x):
        frame = f.pop_daq()
        # f = dataio.I3File('/data/ana/BSM/HNL/MC/190607/Ares/IC86.AVG/Det/domeff_0.97/00001-01000/Det_00_11_0000'+str(i)+'.i3.zst')
        for q in range(len(frame['InIceRawData'])):
            omkey,domlaunches = frame['InIceRawData'].items()[q]
            for z in range(len(domlaunches)):
                domlaunch = domlaunches[z]
                wf = domlaunch.raw_fadc
                t = domlaunch.time
                # for q in range(len(wf)):
                #     wft = np.append(wft, wf[q]+t)

            # fig, ax = plt.subplots(figsize = (20,5))
                if domlaunch.lc_bit is True:
                    val = np.array(range(len(wf)))
                    plt.plot(val*25,wf, ds = 'steps')
                    plt.title('Simulation '+str(i)+' Event '+str(x)+' %s raw FADC 0' % omkey + ' Start time: '+str(int(t))+' ns')
                    plt.ylabel('Counts')
                    plt.xlabel('Time (ns)')
                    if len(domlaunches)>1:
                        plt.savefig('/home/mandia/waveform/wf/plots/event'+str(i)+'/frame'+str(x)+'/wf'+str(q)+'_'+str(z)+'.png')
                    else:
                        plt.savefig('/home/mandia/waveform/wf/plots/event'+str(i)+'/frame'+str(x)+'/wf'+str(q)+'.png')
                    plt.clf()
                
        
            


