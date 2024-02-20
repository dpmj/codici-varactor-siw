import RPi.GPIO as GPIO
import spidev

def initDAC(LDAC,CLR): #Parameters are GPIO ports for LDAC and CLR
    GPIO.setmode(GPIO.BCM)
    #Set a LDAC pulse
    GPIO.setup(LDAC,GPIO.OUT)
    GPIO.output(LDAC,0)
    #Set a CLR level
    GPIO.setup(CLR,GPIO.OUT)
    GPIO.output(CLR,1)

def initSPI(device,freq): #Initializes device SPI connection at freq Hz
    spi = spidev.SpiDev()
    bus = 0
    spi.open(bus,device)
    spi.max_speed_hz = freq
    return spi

def closeSPI(): #Closes SPI connection
    GPIO.cleanup()

def PUregs(spi): #TO-DO registers as parameters
    spi.xfer2([0x70, 0x38])

def PDregs(spi): #TO-DO registers as parameters
    spi.xfer2([0x70, 0x00])

def setV(spi,vector): #TO-DO registers as parameters 
    for j in range(len(vector)):
        if vector[j]<0:
            vector[j] = 0
        elif vector[j]>30:
            vector[j] = 30
        
        Digit = int((vector[j]*4096)//30)
        Byte = (Digit & 0x0FFF)
        Byte = Byte | ((int(j+2)) << 12)
        b=Byte
        a=Byte>>8
        spi.xfer2([a, b])
