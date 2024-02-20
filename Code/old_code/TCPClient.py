import socket
import time

def testconnection(host, port):
    s = socket.socket()
    s.connect((host,port))
    print ('Connected to ' + host)
    s.close

def send(MSG, host, port):
    a = socket.socket()
    a.connect((host,port))
    a.sendall((MSG + "\n").encode())
    print (MSG + ' sent')
    a.close

def query(MSG, host, port):
    a = socket.socket()
    a.connect((host,port))
    a.sendall((MSG + "\n").encode())
    print (MSG + ' sent')
    RESP = a.recv(1024)
    a.close
    return RESP

def querydata(MSG, host, port):
    a = socket.socket()
    a.connect((host, port))
    a.sendall((MSG + "\n").encode())
    #print (MSG + ' sent')

    RESP=a.recv(1).decode()
    #print ('Response detected: ' + RESP)

    DIG=a.recv(1).decode()
    #print ('No of data digits: ' + DIG)

    DSize=int(a.recv(int(DIG)))
    #print ('No of data bytes: ' + str(DSize))

    Data = bytearray(0)
    while DSize:
        time.sleep(0.1) #Da tiempo al VNA a llenar el buffer
        if DSize >= 4096:
            chunk = a.recv(4096)
            #print ('No of bytes received: {0}'.format(len(chunk)))
            Data.extend(chunk)
            DSize = DSize - 4096
        else:
            chunk = a.recv(DSize)
            #print ('No of bytes received: {0}'.format(len(chunk)))
            Data.extend(chunk)
            DSize = 0

    a.close
    return Data

def querytest(MSG, host, port):
    a = socket.socket()
    a.connect((host, port))
    a.sendall((MSG + "\n").encode())
    print (MSG + ' sent')

    word = a.recv(8)
    print(word)
    
    
