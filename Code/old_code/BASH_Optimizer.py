import TCPClient as TCP
import s2pfile as s2p
import VNAHandler as VNA
import DACHandler as DAC
import OPTHandler as OPT
##import socket
##import struct

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
VNA.setformat(host, port)


#Init LDAC and CLR in device 1
LDAC = 25
CLR = 5
DAC.initDAC(LDAC,CLR)

#Init SPI for device 1
device = 1
freq = 16000000
DAC.initSPI(device,freq)

#Power-Up registers B, C & D
DAC.PUregs()


#Make a dot matrix list [TO-DO create vector-mask list]
Vlist = []
Vlist.append([4.0, 6.3, 12])
Vlist.append([3.2, 4.9, 9.0])
Vlist.append([2.4, 3.7, 4.5])
Vlist.append([1.7, 2.5, 2.4])
Vlist.append([1.0, 1.2, 1.3])
            

#Measurement loop
for i in range(len(Vlist)):
    #Get optimum state
    [result, state, Mat] = OPT.Optimize(Vlist[i], mask[i], step0, maxiter, host, port)
    
    #Write an .s2p file
    s2p.mat2file(Mat,'Mehdi_{0:2.2f}_{1:2.2f}_{2:2.2f}'.format(*vector) , IDN)

    
#Power-Down AD
DAC.PDregs()
#Close SPI
DAC.closeSPI()
