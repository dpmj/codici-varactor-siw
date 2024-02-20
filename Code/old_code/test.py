import DACHandler as DAC
import ERReval as ERR
import s2pfile as s2p
import OPTHandler as OPT
import TCPClient as TCP
import VNAHandler as VNA
from contextlib import redirect_stdout

with open('./logs/Connection_log.txt', 'w') as f:
    with redirect_stdout(f):
        #Define an instrument 
        host = '192.168.1.105'
        port = 5025

        #Try test connection
        TCP.testconnection(host, port)

        #Get name of the instrument
        IDN = VNA.identify(host, port)

        #Define the frequency sweep
        Fmin = 1000000000
        Fmax = 10000000000
        NPoints = 901
        VNA.setsweep(Fmin, Fmax, NPoints, host, port)

        #Define the format to use
        VNA.settrace(host, port)
        VNA.setformat(host, port)

#DACHandler test
LDAC = 25
CLR = 5
DAC.initDAC(LDAC,CLR)

device = 1
freq = 16000000
SPI1=DAC.initSPI(device,freq)

DAC.PUregs(SPI1)


#OPTHandler test
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3, 3.1, 20)
ERR.addwindow(mask, 'S21', '>',  -2, 3, 3.1, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.5, 1)
ERR.addwindow(mask, 'S21', '<', -15, 3.9, 5.5, 1)

state0=[1.8, 2.5, 1.1]
step0=(30/4096)*64
maxiter=1

[result, state, Mat] = OPT.Optimize(SPI1, state0, NPoints, mask, step0, maxiter, host, port)

s2p.mat2file(Mat,'./s2p_files/100MHz BW/0_tested','josevmart')


#Turndown DAC and SPI
DAC.PDregs(SPI1)

DAC.closeSPI()
