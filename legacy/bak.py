# reset and

vna.write("*RST")  # reset
vna.write("INIT:CONT:ALL OFF")  # disables continuous mode even for new traces
vna.write("CALC:PAR:DEL:ALL")  # delete all traces -- black screen

vna.write("INIT:IMM; *WAI")  # single sweep. Waits until completed before proceeding with next command

# Establishes start, stop and number of points

Fmin = 1e9  # Hz
Fmax = 10e9  # Hz
NPoints = 21  # points

vna.write('SENS:FREQ:STAR ' + str(Fmin))
vna.write('SENS:FREQ:STOP ' + str(Fmax))
vna.write('SENS:SWE:POIN' + str(NPoints))


vna.write("INIT:IMM; *WAI")  # single sweep. Waits until completed before proceeding with next command

# Pag 864: CALCulate<Ch>:PARameter:SELect <TraceName>
# create new traces with defined measurements

# channel 1 -  magnitude, logarithmic (dB) and phases (deg)

vna.write("CALC:PAR:SDEF 'Trc1_mlog', 'S11'")
vna.write("CALC:PAR:SEL 'Trc1_mlog'")
vna.write("CALC:FORM MLOG")  # dB - pag 807

vna.write("CALC:PAR:SDEF 'Trc1_phas', 'S11'")
vna.write("CALC:PAR:SEL 'Trc1_phas'")
vna.write("CALC:FORM PHAS")  # phase -180 to 180 - pag 807

vna.write("CALC:PAR:SDEF 'Trc2_mlog', 'S12'")
vna.write("CALC:PAR:SEL 'Trc2_mlog'")
vna.write("CALC:FORM MLOG")

vna.write("CALC:PAR:SDEF 'Trc2_phas', 'S12'")
vna.write("CALC:PAR:SEL 'Trc2_phas'")
vna.write("CALC:FORM PHAS")

vna.write("CALC:PAR:SDEF 'Trc3_mlog', 'S21'")
vna.write("CALC:PAR:SEL 'Trc3_mlog'")
vna.write("CALC:FORM MLOG")

vna.write("CALC:PAR:SDEF 'Trc3_phas', 'S21'")
vna.write("CALC:PAR:SEL 'Trc3_phas'")
vna.write("CALC:FORM PHAS")

vna.write("CALC:PAR:SDEF 'Trc4_mlog', 'S22'")
vna.write("CALC:PAR:SEL 'Trc4_mlog'")
vna.write("CALC:FORM MLOG")

vna.write("CALC:PAR:SDEF 'Trc4_phas', 'S22'")
vna.write("CALC:PAR:SEL 'Trc4_phas'")
vna.write("CALC:FORM PHAS")

vna.write("INIT:IMM; *WAI")  # single sweep. Waits until completed before proceeding with next command


# display traces on the screen

vna.write("DISP:WIND1:STAT ON")

vna.write("DISP:WIND1:TRAC1:FEED 'Trc1_mlog'")
vna.write("DISP:WIND1:TRAC2:FEED 'Trc2_mlog'")
vna.write("DISP:WIND1:TRAC3:FEED 'Trc3_mlog'")
vna.write("DISP:WIND1:TRAC4:FEED 'Trc4_mlog'")

vna.write("DISP:WIND1:TRAC5:FEED 'Trc1_phas'")
vna.write("DISP:WIND1:TRAC6:FEED 'Trc2_phas'")
vna.write("DISP:WIND1:TRAC7:FEED 'Trc3_phas'")
vna.write("DISP:WIND1:TRAC8:FEED 'Trc4_phas'")


vna.write("INIT:IMM; *WAI")  # single sweep. Waits until completed before proceeding with next command
