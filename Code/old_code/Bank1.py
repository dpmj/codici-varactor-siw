import ERReval as ERR

ChannelList = []

#Channel 0
state0 = [1.8, 2.5, 1.1]
mask=[]

# state 0: punto de partida?

# mask: lista en la que se append() un diccionario con:
#   param: <parametro S>
#   ori: <orientacion> : sentido de la optimización: mayor que, menor que
#   value: <valor> : valor con el que comparar el parámetro
#   flo: <freq low> : límite inferior de freq a optimizar
#   fhi: <freq high> : límite superior de freq a optimizar
#   wei: <weight>

# parámetros de optimización: está dando instrucciones de qué parámetro optimizar, en qué 
# frecuencia, y cuánto debe valer. Está dando pesos a la optimización para favorecer
# algunos parámetros sobre otros. 

# Err: evaluación del error de optimización
# addwindow simplemente añade en mask el diccionario con los parámetros

ERR.addwindow(mask, 'S11', '<', -20, 3, 3.1, 20)  # Define adaptación en la banda de paso
ERR.addwindow(mask, 'S21', '>',  -3, 3, 3.1, 20)  # Define pérdidas en la banda de paso
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.5, 1)  # Define atenuación en bandas laterales
ERR.addwindow(mask, 'S21', '<', -15, 3.9, 5.5, 1)  # Lo mismo

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)

# el canal es un diccionario de parámetros, que parten de un mismo estado


#Channel 1
state0 = [2, 3, 1.4]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.1, 3.2, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.1, 3.2, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.6, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 2
state0 = [2.2, 3.2, 1.5]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.2, 3.3, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.2, 3.3, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.7, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.1, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 3
state0 = [2.8, 3.5, 1.7]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.3, 3.4, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.3, 3.4, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.8, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.2, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 4
state0 = [3.2, 4, 1.8]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.4, 3.5, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.4, 3.5, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.9, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.3, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 5
state0 = [3.3, 4.4, 2.3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.5, 3.6, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.5, 3.6, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 3, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.4, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


