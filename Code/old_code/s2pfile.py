#! /usr/bin/env python
# -*- coding: utf-8 -*-

import struct

def raw2mat(Data,NPoints):
    t_Mat = []
    for i in range (9):  # ¿estático? 9 columnas: freq, 2 columnas por S (mag, phase)
        t_Mat.append(struct.unpack_from(">" + "d"*NPoints, Data, i*NPoints*8))
    Mat = list(zip(*t_Mat))
    return Mat

    # probablemente esto pueda hacerse con numpy en un segundo


def mat2file(Mat, Name, IDN):
    new = open (Name + '.s2p', 'w+')
    new.write("!" + IDN + '\n')
    new.write("!File generated by LCAF-GAM-UPV software\n")
    new.write("!josevmart@iteam.upv.es\n")
    new.write("!S2P File: Measurements: S11, S21, S12, S22:\n")
    new.write("# Hz S  dB   R 50\n")
    for i in range (len(Mat)): #TO-DO? dynamic length
        line = str(int(Mat[i][0]))
        for j in range (8):
            line = line + ' {0:2.6e}'.format(Mat[i][j+1])
            
        new.write(line + '\n')

    new.close()

def file2mat(Name):
    mat = []
    file = open (Name + '.s2p', 'r')
    for line in file:
        if line != '\n' and line[0] != '#' and line[0] != '!':
            strvalues = line.split()
            values = []
            values.append(float(strvalues[0]))
            for j in range (8):
                values.append(float(strvalues[j+1]))
            mat.append(values)
    file.close()
    return mat
                
