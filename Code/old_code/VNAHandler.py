import TCPClient as TCP

def identify(host, port):
    IDN = TCP.query('*IDN?',host,port).decode()
    print (IDN)
    return IDN

def setsweep(Fmin, Fmax, NPoints, host, port):
    # sin problemas
    # se puede expresar en GHz, e.g.: 1GHz

    TCP.send('SENS:FREQ:STAR ' + str(Fmin), host, port)
    Fmin1 = TCP.query('SENS:FREQ:STAR?',host,port)
    print ('Fmin set to: ' + Fmin1.decode())

    TCP.send('SENS:FREQ:STOP ' + str(Fmax), host, port)
    Fmax1 = TCP.query('SENS:FREQ:STOP?',host,port)
    print ('Fmax set to: ' + Fmax1.decode())

    TCP.send('SENS:SWE:POIN ' + str(NPoints), host, port)
    NPoints1 = TCP.query('SENS:SWE:POIN?',host,port)
    print ('No. of points set to: ' + NPoints1.decode())

##def settrace(host, port):
##    TCP.send('CALC:PAR:SEL "CH1_S11_1"',host,port)
##    Meas = TCP.query('CALC:PAR:SEL?',host,port)
##    print ('Measure selected: ' + Meas.decode())
##
##    TCP.send('CALC:PAR "CH1_S22_1",S22',host,port)
##    TCP.send('CALC:PAR "CH1_S21_1",S21',host,port)
##    TCP.send('CALC:PAR "CH1_S12_1",S12',host,port)
##    Meas = TCP.query('CALC:PAR:CAT?',host,port)
##    print ('Measure selected: ' + Meas.decode())

def settrace(host, port):
    # NOTA (JUAN): nombres de las trazas parecen diferentes
    # Comando adecuado para ZNB: CALC:PAR:SDEF 'Trc1', 'S11'

    TCP.send('CALC:PAR:SEL "CH1_S11_1"',host,port)  # selección traza CH1_S11_1
    Meas = TCP.query('CALC:PAR:SEL?',host,port)
    print ('Measure selected: ' + Meas.decode())  
    # 'Measure selected: "CH1_S11_1"'

    TCP.send('CALC:PAR "CH1_S33_1",S22',host,port)
    TCP.send('CALC:PAR "CH1_S31_1",S21',host,port)
    TCP.send('CALC:PAR "CH1_S13_1",S12',host,port)
    Meas = TCP.query('CALC:PAR:CAT?',host,port)
    print ('Measure selected: ' + Meas.decode())
    # 'Measure selected: "CH1_S11_1,S11,CH1_S33_1,S22,CH1_S31_1,S21,CH1_S13_1,S12,CH1_S13_5,S13,CH1_S31_6,S31,CH1_S33_7,S33"'
    # en el antiguo VNA este comando seleccionaba qué parámetro medir? no aparece en la documentación del N5227A

def setformat(host, port):
    # NOTA (JUAN): sin problemas aquí, aunque probablemente se puede reducir a 32 b
    # A veces al seleccionar un formato da error al recibir comandos de envío de datos??

    TCP.send('FORM:BORD NORM',host,port)
    Form = TCP.query('FORM:BORD?',host,port)
    print ('Byte order selected: ' + Form.decode())

    TCP.send('FORM REAL,64',host,port)
    Form = TCP.query('FORM:DATA?',host,port)
    print ('Format selected: ' + Form.decode())
