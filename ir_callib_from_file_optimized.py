from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from time import time
from read_funcs import read_pix_eeprom, read_raw_block
import json

# TODO hardcode data !!!

ir_num = 21
block_num = 0
To_image = np.zeros((12, 16), dtype=float)
OS_image = np.zeros((12, 16), dtype=float)

img = fits.getdata(f"1329/raw_block-n{block_num:03d}-{ir_num}.fits")
filename = f"ir_calib/calib_data/ir{ir_num}ec.txt"

tic = time()
VBE =    read_raw_block(ir_num, block_num, 'ram', '80') # 0x0580
VPTAT =  read_raw_block(ir_num, block_num, 'ram', 'a0') # 0x05A0
VDDpix = read_raw_block(ir_num, block_num, 'ram', 'aa') # 0x05AA


VDDpix = float(VDDpix)
if VDDpix > 32767:
    VDDpix = VDDpix - 65536

deltaV = float((VDDpix - Vdd25) / KVdd)

VPTAT = float(VPTAT)
VBE = float(VBE)

if VPTAT > 32767:
    VPTAT = VPTAT - 65536
if VBE > 32767:
    VBE = VBE - 65536

VPTATart = float( VPTAT / (VPTAT * AlphaPTAT + VBE) ) * (2**18)

# Ta
Ta = ( ((VPTATart / (1 + KVPTAT * deltaV)) - VPTAT25) / KTPTAT ) + 25
Vdd = (Resolution_corr * VDDpix - Vdd25) / KVdd + 3.3

GAIN_RAM = read_raw_block(ir_num, block_num,"ram","8a")
GAIN_RAM = float(GAIN_RAM)

if GAIN_RAM > 32767:
    GAIN_RAM = GAIN_RAM - 65536

K_gain = GAIN / GAIN_RAM

CP = float(read_raw_block(ir_num, block_num, "ram", "88"))
if CP > 32767:
    CP = CP - 65536

CP_pix_gain = CP * K_gainTGC_ee

CP_pix_OS = float(CP_pix_gain - pix_OS_ref_CP * (1 + KTa_CP * (Ta - 25)) * (1 + KV_CP * (Vdd - 3.3)))

for y in range(0, 12):
    for x in range(0, 16):

        pix_val = read_raw_block(ir_num, block_num, "img", y, x)
        pix_val = float(pix_val)
        if pix_val > 32767:
            pix_val = pix_val - 65536

        pix_gain = pix_val * K_gain

        # KTa =======================================

        KTa = (KTa_ee * 2 ** KTa_scale_2 + KTa_avg) / 2 ** KTa_scale_1

        # KV ============================

        # Compensation ==============================

        pix_OS_SP0 = round(pix_gain - pix_OS_ref_SP0 * (1 + KTa * (Ta - 25)) * (1 + KV * (Vdd - 3.3)))
        pix_OS_SP1 = round(pix_gain - pix_OS_ref_SP1 * (1 + KTa * (Ta - 25)) * (1 + KV * (Vdd - 3.3)))

        OS_image[y, x] = pix_OS_SP0

        # IR data gradient compensation
        TGC_ee = float(int(TGC_ee) & 0x01ff)
        if TGC_ee > 255:
            TGC_ee = TGC_ee - 512

        TGC = float(TGC_ee / (2 ** 6))
        V_IR_compensated = round((pix_OS_SP0 - TGC * CP_pix_OS) / Emissivity)

        KsTo_scale = float(int(KsTo_scale_ee) & 0x07ff)

        KsTo_3 = float(int(KsTo_3_ee) & 0x07ff)

        if KsTo_3 > 1023:
            KsTo_3 = KsTo_3 - 2048

        KsTo_3 = KsTo_3 / (2 ** KsTo_scale)
        Tr = Ta - 5

        Ta_K4 = (Ta + 273.15) ** 4
        Tr_K4 = (Tr + 273.15) ** 4

        Ta_r = Tr_K4 - (Tr_K4 - Ta_K4) / Emissivity
        Sx_under_root = alpha_comp ** 3 * V_IR_compensated + alpha_comp ** 4 * Ta_r

        if Sx_under_root > 0:
            Sx = KsTo_3 * np.sqrt(np.sqrt(Sx_under_root))
            To = np.sqrt(np.sqrt(V_IR_compensated / (alpha_comp * (1 - KsTo_3 * 273.15) + Sx) + Ta_r)) - 273.15
        else:
            To = 0
        To_image[y, x] = To

print(f"Exec time: {time() - tic}")



variables = {}

for name, value in list(globals().items()):
    if name.startswith("_"):
        continue
    if isinstance(value, (int, float, bool, str)):
        variables[name] = value
    elif isinstance(value, np.ndarray):
        variables[name] = value.tolist()
    elif isinstance(value, np.generic):
        variables[name] = value.item()

with open("Helpers/numeric_variables.json", "w") as f:
    json.dump(variables, f, indent=4)


plt.imshow(To_image, cmap="gray", vmin=-100, vmax=80)
plt.show()
