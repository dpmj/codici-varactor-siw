import DACHandler as DAC
import TCPClient as TCP
import s2pfile as s2p 

#Habra que definir un filtro para compactar todos los parametros que lo definen

def measure(spi, state, NPoints, host, port):
    DAC.setV(spi,state)
    Data = TCP.querydata('CALC:DATA:SNP? 2', host, port)
    Mat = s2p.raw2mat(Data,NPoints)

    return Mat

