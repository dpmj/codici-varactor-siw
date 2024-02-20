def addwindow(mask, param, ori, value, flo, fhi, wei):
    mask.append({'Parameter': param,
                 'Orientation': ori,
                 'Value': value,
                 'Flo': flo,
                 'Fhi': fhi,
                 'Weight': wei})

def evalerror(mat, mask):
    NPoints = len(mat)
    error = 0
    ##print ('NPoints is ' + str(NPoints))
    for window in mask:
        winerror = 0
        Flo = window['Flo']*1000000000 #GHz to Hz
        Fhi = window['Fhi']*1000000000
        if Flo > Fhi:
            print('ERROR: Flo cannnot be greater than Fhi')
            print(Flo + ' ' + Fhi)
            return -1

        Findex = 0
        Floindex = None
        #Search Flo index in mat[i][0]
        while Findex < NPoints:
            if mat[Findex][0] > Flo:
                Floindex = Findex
                break
            Findex = Findex+1

        if Floindex is None:
            print('ERROR: Flo cannot be greater than s2p range')
            print(str(Flo) + ' ' + str(mat[-1][0]))
            return -1
        elif Floindex == 0:
            print('WARNING: Flo is lower than s2p range')

        ##print('Floindex is : ' + str(Floindex))

        #Search Fhi index in mat[i][0]
        Fhiindex = None
        while Findex < NPoints:
            if mat[Findex][0] > Fhi:
                Fhiindex = Findex-1
                break
            Findex = Findex+1

        if Fhiindex is None:
            print('WARNING: Fhi is greater than s2p range')
            Fhiindex = NPoints-1
        elif Fhiindex == 0:
            print('ERROR: Fhi cannot be lower than s2p range')
            return -1

        ##print('Fhiindex is : ' + str(Fhiindex))
  

        if window['Parameter'] == 'S11':
            #Column index = 1, mat[i][1]
            Colindex = 1
        elif window['Parameter'] == 'S21':
            #Column index = 3, mat[i][3]
            Colindex = 3
        else:
            print('ERROR: ' + (window['Parameter'] + ' is not a valid parameter'))
            return -1

        #Calculate the error
        value = window['Value']
        weight = window['Weight']
        ##print(window['Parameter'] + window['Orientation'] + str(value))
        if window['Orientation'] == '>':
            for Findex in range (Floindex,Fhiindex):
                freqerror = (value - mat[Findex][Colindex])
                if freqerror > 0:
                    winerror = winerror + freqerror*weight

        elif window['Orientation'] == '<':
            for Findex in range (Floindex,Fhiindex):
                freqerror = (mat[Findex][Colindex] - value)
                if freqerror > 0:
                    winerror = winerror + freqerror*weight
        else:
            print('ERROR : ' + window['Orientation'] + ' is not a valid orientation')
            return -1

        ##print('winerror is :' + str(winerror) + '\n')
        error = error + winerror

    ##print('Total error is :' + str(error))
    return error
