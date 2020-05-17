import numpy as np
from matplotlib.pyplot import step, show, plot
from itertools import chain

## 1. Draw waveform of sequence 011100101 using NRZI, Manchester, Differential Manchester

message = tuple(int(i) for i in '011100101')

# NRZI, invert on 1
nrzi_out = [message[0],]
for i,c in enumerate(message[1:]):
    if c:
        nrzi_out.append(int(not nrzi_out[i]))
    else:
        nrzi_out.append(nrzi_out[i])
nrzi_out.append(nrzi_out[-1]) # add the same last bit for plotting purpose

# Manchester, mid-bit transition, high to low is 0 and low to high is 1
manch_out = list(chain.from_iterable([[0,1] if x else [1,0] for x in message]))
manch_out.append(manch_out[-1]) # add the same last bit for plotting purpose

# Differential Manchester, start of bit transition on 0, mid-bit clocking transition
dmanch_start_bit_transitions = [int(not i) for i in message]
dmanch_out = []
prev_level = 1
for t in dmanch_start_bit_transitions:
    if t:
        dmanch_out.append(int(not prev_level))
        dmanch_out.append(prev_level)
    else:
        dmanch_out.append(prev_level)
        prev_level = int(not prev_level)
        dmanch_out.append(prev_level)
dmanch_out.append(dmanch_out[-1]) # add the same last bit for plotting purpose
        
to_plot = [
    np.transpose([(i*2,c+3) for i,c in enumerate(nrzi_out)]),
      np.transpose([(i,c+1.5) for i,c in enumerate(manch_out)]),
      np.transpose([(i,c) for i,c in enumerate(dmanch_out)])]

for data in to_plot:
    step(*data, where="post")
show()

## 2. Encode 101011010 into ASK, BFSK, BPSK

message = tuple(int(i) for i in '101011010')
resol = 50; ticks = len(message)*resol
freq = np.pi*4; freq0 = np.pi*2
x = np.linspace(0,len(message),ticks)
y_ask = np.zeros(ticks); y_bfsk = np.zeros(ticks); y_bpsk = np.zeros(ticks)
# ask
for i,c in enumerate(message):
    if c:
        y_ask[i*resol:(i+1)*resol] = np.sin(freq*x[i*resol:(i+1)*resol])
# bfsk
for i,c in enumerate(message):
    if c:
        y_bfsk[i*resol:(i+1)*resol] = np.sin(freq*x[i*resol:(i+1)*resol])
    else: # use half frequency
        y_bfsk[i*resol:(i+1)*resol] = np.sin(freq0*x[i*resol:(i+1)*resol])
# bpsk
for i,c in enumerate(message):
    if c:
        y_bpsk[i*resol:(i+1)*resol] = np.sin(freq*x[i*resol:(i+1)*resol])
    else: # shift phase by pi
        y_bpsk[i*resol:(i+1)*resol] = np.sin(freq*x[i*resol:(i+1)*resol]+np.pi)
#plot   
plot(x,y_ask+5); plot(x, y_bfsk+2.5); plot(x, y_bpsk); show()
