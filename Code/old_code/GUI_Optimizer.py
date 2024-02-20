#Para tkinter
from tkinter import *
import tkinter as tk
import tkinter.font
#Librerias propias
import ERReval as ERR
import s2pfile as s2p

nlr = 2 #NewLineRow

def addmaskline():
        global nlr
        print(nlr-2)
        Button(mask_frame,text="+",state="disabled").grid(row=nlr,column=0)
        
        sp_dropmenu.append(OptionMenu(mask_frame, "Sij", "S11","S22"))
        ud_dropmenu.append(OptionMenu(mask_frame, "><", ">", "<"))
        flo_entry.append(Entry(mask_frame, width=5))
        fhi_entry.append(Entry(mask_frame, width=5))
        val_entry.append(Entry(mask_frame, width=8))
        wei_entry.append(Entry(mask_frame, width=8))

        sp_dropmenu[nlr-2].grid(row=nlr,column=1)
        ud_dropmenu[nlr-2].grid(row=nlr,column=2)
        flo_entry[nlr-2].grid(row=nlr,column=3)
        fhi_entry[nlr-2].grid(row=nlr,column=4)
        val_entry[nlr-2].grid(row=nlr,column=5)
        wei_entry[nlr-2].grid(row=nlr,column=6)

        nlr=nlr+1

        add_button.grid(row=nlr,column=0)

        return nlr

def exitProgram():
        ##GPIO.cleanup()
        win.quit()

#GUI
win=tk.Tk()
win.title("Optimizer")
win.geometry('{}x{}'.format(640,480))

#Create Containers
mask_frame = Frame (win, bg='red', width=420, height=440, padx=3, pady=3)
VNA_frame = Frame (win, bg='black', width=210, height=440, padx=3, pady=3)
exit_frame = Frame (win, bg='blue', width=630, height=10, padx=3, pady=3)

#Layout Containers
win.grid_rowconfigure(0,weight=20)
win.grid_rowconfigure(1,weight=1)
win.grid_columnconfigure(0,weight=1)
win.grid_columnconfigure(1,weight=1)

mask_frame.grid(row=0,column=0,sticky="ns")
VNA_frame.grid(row=0,column=1,sticky="ns")
exit_frame.grid(row=1,columnspan=2,sticky="nsew")

#Create Widgets for Mask Frame
cond_label = Label(mask_frame,text="Set Conditions")
sp_label = Label(mask_frame,text="Sp")
ud_label = Label(mask_frame,text="><")
flo_label = Label(mask_frame,text="Flo")
fhi_label = Label(mask_frame,text="Fhi")
val_label = Label(mask_frame,text="Value")
wei_label = Label(mask_frame,text="Weight")

add_button = Button(mask_frame,text="+",command=addmaskline)

sp_dropmenu = []
ud_dropmenu = []
flo_entry = []
fhi_entry = []
val_entry = []
wei_entry = []

#Layout widgets in Mask Frame
cond_label.grid(row=0, columnspan=7)
             
sp_label.grid(row=1,column=1,sticky="w")
ud_label.grid(row=1,column=2,sticky="w")
flo_label.grid(row=1,column=3,sticky="w")
fhi_label.grid(row=1,column=4,sticky="w")
val_label.grid(row=1,column=5,sticky="w")
wei_label.grid(row=1,column=6,sticky="w")

add_button.grid(row=2,column=0)

#Create sub-containers in VNA frame
sweep_frame = Frame (VNA_frame, bg='green', width=210, height=150, pady=3)
fresp_frame = Frame (VNA_frame, bg='yellow', width=310, height=290, pady=3)

#layout sub-containers
VNA_frame.grid_rowconfigure(0,weight=1)
VNA_frame.grid_rowconfigure(1,weight=3)

sweep_frame.grid(row=0,column=0)
fresp_frame.grid(row=1,column=0,sticky='ns')

#Create Widgets for VNA frame
#Create Widgets for sweep frame
sweep_label = tk.Label(sweep_frame,text="Set Sweep Parameters")

start_label = Label(sweep_frame,text="Start")
stop_label = Label(sweep_frame,text="Stop")
point_label = Label(sweep_frame,text="NPoints")

start_entry = Entry(sweep_frame, width=8)
stop_entry = Entry(sweep_frame, width=8)
point_entry = Entry(sweep_frame, width=8)

#Create Widgets for fresp frame
fresp_label = tk.Label(fresp_frame,text="Frequency Response")

#Layout widgets in VNA Frame
#Layout widgets in sweep Frame
sweep_label.grid(row=0, columnspan=3)

start_label.grid(row=1,column=0,sticky="w")
stop_label.grid(row=2,column=0,sticky="w")
point_label.grid(row=3,column=0,sticky="w")

start_entry.grid(row=1,column=1)
stop_entry.grid(row=2,column=1)
point_entry.grid(row=3,column=1)

Label(sweep_frame,text="GHz").grid(row=1,column=2)
Label(sweep_frame,text="GHz").grid(row=2,column=2)

#Layout widgets in fresp Frame
fresp_label.grid(row=0, columnspan=1)


button = Button (exit_frame, text="Exit Program", command=exitProgram)
button.pack(anchor=CENTER)

tk.mainloop()



##mask = []
##
##ERR.addwindow(mask,'S11','<',-10,1.45,1.55,10)
##ERR.addwindow(mask,'S21','>',-3,1.45,1.55,1)
##
##print ('Parameter 1 is ' + mask[0]['Parameter'])
##print ('Orientation 2 is ' + mask[1]['Orientation'])
##
##Mat = s2p.file2mat('Mehdi_4.00_6.30_12.00')
##
##print ('Frequency 1 is ' + str(Mat[0][0]))
##print ('Frequency 2 is ' + str(Mat[1][0]))
##
##error = ERR.evalerror(Mat,mask)
