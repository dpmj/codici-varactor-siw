import DACHandler as DAC
import ERReval as ERR
import s2pfile as s2p
import OPTHandler as OPT
import TCPClient as TCP
import VNAHandler as VNA
from Source import BankList
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


#Init LDAC and CLR
LDAC = 25
CLR = 5
DAC.initDAC(LDAC,CLR)

#Init SPI
device = 1
freq = 16000000
SPI1=DAC.initSPI(device,freq)

#Power-Up registers B, C & D
DAC.PUregs(SPI1)


step0=(30/4096)*64
maxiter=500


# BankList: lista de bancos de pruebas. 
# Cada banco contiene listas de canales.
# ChannelList: lista de canales 

#Measurement loop

for j in range(len(BankList)):

    ChannelList = BankList[j]

    for i in range(len(ChannelList)):

        with open('./logs/Bank{:d}/Channel{:d}_Optimization_log.txt'.format(j+1,i), 'w') as f:
            with redirect_stdout(f):

                print ('Channel{:d} Optimization log\n'.format(i))
            
                Channel = ChannelList[i] #TO-DO lo pilla como lista con 1 solo item
                state0 = Channel[0]['State0']
                mask = Channel[0]['Mask']

                [result, state, Mat] = OPT.Optimize(SPI1, state0, NPoints, mask, step0, maxiter, host, port)

        # Write an .s2p file
        s2p.mat2file(Mat,'./s2p_files/Bank{:d}/Channel{:d}'.format(j+1,i) , IDN)  

    print('Chanel{:d} done with result: '.format(i) + result)
    
# Turndown DAC and SPI
DAC.PDregs(SPI1)
DAC.closeSPI()



