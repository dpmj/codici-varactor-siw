import ERReval as ERR

ChannelList = []

#Channel 0
state0 = [3.6, 5, 2.6]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.6, 3.7, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.6, 3.7, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.1, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.5, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 1
state0 = [4.2, 5.3, 3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.7, 3.8, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.7, 3.8, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.2, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.6, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 2
state0 = [4.5, 6.5, 3.3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.8, 3.9, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.8, 3.9, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.3, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.7, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 3
state0 = [4.9, 6.9, 3.8]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.9, 4.0, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.9, 4.0, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.4, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.8, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 4
state0 = [5, 7.5, 4.3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 4.0, 4.1, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 4.0, 4.0, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.5, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.9, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 5
state0 = [6, 8.5, 4.5]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 4.1, 4.2, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 4.1, 4.2, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.6, 1)
ERR.addwindow(mask, 'S21', '<', -15, 5.0, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


