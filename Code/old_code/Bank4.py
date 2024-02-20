import ERReval as ERR

ChannelList = []

#Channel 0
state0 = [3.3, 4.4, 2.0]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.45, 3.55, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.45, 3.55, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 3.0, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.4, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 1
state0 = [2.6, 3.5, 2.5]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.4, 3.6, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.4, 3.6, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.9, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.5, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 2
state0 = [2.3, 3.2, 2.7]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.35, 3.65, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.35, 3.65, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.8, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.6, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 3
state0 = [1.7, 2.5, 3.1]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.3, 3.7, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.3, 3.7, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.7, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.7, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)


#Channel 4
state0 = [1.5, 2.0, 3.3]
mask=[]
ERR.addwindow(mask, 'S11', '<', -20, 3.25, 3.75, 20)
ERR.addwindow(mask, 'S21', '>',  -3, 3.25, 3.75, 20)
ERR.addwindow(mask, 'S21', '<', -15, 1.0, 2.6, 1)
ERR.addwindow(mask, 'S21', '<', -15, 4.8, 5.5, 1)

Channel=[]
Channel.append({'State0': state0,
                'Mask': mask})

ChannelList.append(Channel)



