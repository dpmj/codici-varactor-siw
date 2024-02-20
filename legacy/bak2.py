DATA2 = np.array([float(item) for item in DATA.split(",")])  # from string to array of floats
DATA3 = DATA2.reshape(8, NPoints)  # Reshape: 8 columns, of NPoints rows.
print(f"Shape = {np.shape(DATA3)}")
DATA3



# plotting to confirm reading works - should be the same as in the screen

import numpy as np
from matplotlib import pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, figsize=[12, 10])

fig.suptitle("Data retrieved from VNA - Magnitude and phase")
ax1.set_title('Data - Magnitude')
# ax1.set_xlabel('Freq (Hz)')
ax1.set_ylabel('Magnitude (dB)')
ax2.set_title('Data - Phase')
ax2.set_xlabel('Freq (Hz)')
ax2.set_ylabel('Phase (º)')

ax1.plot(f, DATA3[0][:], label="Trc1,S11,mlog")
ax1.plot(f, DATA3[2][:], label="Trc2,S21,mlog")
ax1.plot(f, DATA3[4][:], label="Trc3,S12,mlog")
ax1.plot(f, DATA3[6][:], label="Trc4,S22,mlog")

ax1.grid(True, which='major', color='#DDDDDD', linestyle='-', linewidth=0.8)
ax1.grid(True, which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
ax1.minorticks_on()
ax1.legend(loc="center right")


plt.plot(f, DATA3[1][:], label="Trc1,S11,phas")
plt.plot(f, DATA3[3][:], label="Trc2,S21,phas")
plt.plot(f, DATA3[5][:], label="Trc3,S12,phas")
plt.plot(f, DATA3[7][:], label="Trc4,S22,phas")

ax2.grid(True, which='major', color='#DDDDDD', linestyle='-', linewidth=0.8)
ax2.grid(True, which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
ax2.minorticks_on()
ax2.legend(loc="center right")



plt.show()
