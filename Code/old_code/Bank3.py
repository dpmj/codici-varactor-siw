import ERReval as ERR

ChannelList = []

#Channel 0
state0 = [1.7, 2.0, 1.4]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.0, 3.2, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.0, 3.2, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.4, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.2, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 1
state0 = [2.0, 2.9, 1.8]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.2, 3.4, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.2, 3.4, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.6, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.4, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 2
state0 = [2.7, 3.6, 2.3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.4, 3.6, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.4, 3.6, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.8, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.6, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 3
state0 = [3.1, 4.3, 3.4]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.6, 3.8, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.6, 3.8, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.0, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.8, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 4
state0 = [3.4, 4.6, 4.6]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.8, 4.0, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.8, 4.0, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.2, 1)
ERR.addwindow(mask, 'S21', '<', -15, 5.0, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 5
state0 = [4.2, 5.3, 5.3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 4.0, 4.2, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 4.0, 4.2, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.4, 1)
ERR.addwindow(mask, 'S21', '<', -15, 5.2, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


