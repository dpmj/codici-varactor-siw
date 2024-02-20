import ERReval as ERR

ChannelList = []

#Channel 0
state0 = [1.8, 2.5, 1.1]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3, 3.1, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3, 3.1, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1, 2.5, 1)
ERR.addwindow(mask, 'S21', '<', -15, 3.9, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


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


