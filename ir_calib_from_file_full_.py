from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from time import time
from read_funcs import read_eeprom, read_pix_eeprom, read_raw_block
import json

# TODO hardcode data !!!

ir_num = 21
block_num = 1
To_image = np.zeros((12, 16), dtype=float)
OS_image = np.zeros((12, 16), dtype=float)

img = fits.getdata(f"1329/raw_block-n{block_num:03d}-{ir_num}.fits")
filename = f"ir_calib/calib_data/ir{ir_num}ec.txt"

eeprom_data = np.loadtxt(filename, dtype=str)
eeprom_data = np.array([int(x, 16) for x in eeprom_data])

tic = time()

Vdd25 =     read_eeprom(eeprom_data, '26')  # 0x2426
KVdd =      read_eeprom(eeprom_data, '27')  # 0x2427
PTAT25_1 =  read_eeprom(eeprom_data, '28')  # 0x2428
PTAT25_2 =  read_eeprom(eeprom_data, '29')  # 0x2429
KTPTAT =    read_eeprom(eeprom_data, '2a')  # 0x242a
KVPTAT =    read_eeprom(eeprom_data, '2b')  # 0x242b
AlphaPTAT = read_eeprom(eeprom_data, '2c')  # 0x242c

VBE =    read_raw_block(ir_num, block_num, 'ram', '80') # 0x0580
VPTAT =  read_raw_block(ir_num, block_num, 'ram', 'a0') # 0x05A0
VDDpix = read_raw_block(ir_num, block_num, 'ram', 'aa') # 0x05AA

# KVPTAT
KVPTAT = float(KVPTAT & 0x07ff)
if KVPTAT > 1023:
    KVPTAT = KVPTAT - 2048
KVPTAT = KVPTAT / (2**12)

# KTPTAT
KTPTAT = float(KTPTAT & 0x07ff)
if KTPTAT > 1023:
    KTPTAT = KTPTAT - 2048
KTPTAT = KTPTAT / (2**3)

# deltaV
Vdd25 = float(Vdd25 & 0x07ff)
KVdd = float(KVdd & 0x07ff)
VDDpix = float(VDDpix)
if VDDpix > 32767:
    VDDpix = VDDpix - 65536
if Vdd25 > 1023:
    Vdd25 = Vdd25 - 2048

Vdd25 = Vdd25 * (2**5)

if KVdd > 1023:
    KVdd = KVdd - 2048

KVdd = KVdd * (2**5)
deltaV = float((VDDpix - Vdd25) / KVdd)

# VPTAT25
PTAT25_1 = float(PTAT25_1 & 0x07ff)
PTAT25_2 = float(PTAT25_2 & 0x07ff)
VPTAT25 = 32 * PTAT25_1 + PTAT25_2

# VPTATart
AlphaPTAT = float(AlphaPTAT & 0x07ff)
VPTAT = float(VPTAT)
VBE = float(VBE)

if VPTAT > 32767:
    VPTAT = VPTAT - 65536
if VBE > 32767:
    VBE = VBE - 65536

AlphaPTAT = AlphaPTAT / (2**7)
VPTATart = float( VPTAT / (VPTAT * AlphaPTAT + VBE) ) * (2**18)

# Ta
Ta = ( ((VPTATart / (1 + KVPTAT * deltaV)) - VPTAT25) / KTPTAT ) + 25

# Vdd =======================================

TGC_ee = read_eeprom(eeprom_data, "33")   # EE[0x2433]
Control_register = 0x1901

# resolution
Resolution_EE = float(TGC_ee & 0x0600)
Resolution_EE = Resolution_EE / (2**9)
Resolution_REG = float(Control_register & 0x0c00)
Resolution_REG = Resolution_REG / (2**10)
Resolution_corr = (2**Resolution_EE) / (2**Resolution_REG)

Vdd = (Resolution_corr * VDDpix - Vdd25) / KVdd + 3.3

GAIN_RAM = read_raw_block(ir_num, block_num,"ram","8a")
GAIN_EE_1 = read_eeprom(eeprom_data, "24")
GAIN_EE_2 = read_eeprom(eeprom_data, "25")
GAIN_RAM = float(GAIN_RAM)

if GAIN_RAM > 32767:
    GAIN_RAM = GAIN_RAM - 65536

GAIN = float( 32 * (GAIN_EE_1 & 0x07ff) + (GAIN_EE_2 & 0x07ff))
K_gain = GAIN / GAIN_RAM

# Offset
Pix_os_R1_1 = read_eeprom(eeprom_data, "11")
Pix_os_R1_2 = read_eeprom(eeprom_data, "12")
Scale_occ = read_eeprom(eeprom_data, "10")

Offset_average = float(32 * (int(Pix_os_R1_1) & 0x07ff) + (int(Pix_os_R1_2) & 0x07ff))
if Offset_average > 32767:
    Offset_average = Offset_average - 65536

Offset_scale = float(int(Scale_occ) & 0x07e0)
Offset_scale = Offset_scale / (2 ** 5)

KTa_avg = read_eeprom(eeprom_data, "15")
KTa_scale = read_eeprom(eeprom_data, "16")

KTa_avg = float(int(KTa_avg) & 0x07ff)
if KTa_avg > 1023:
    KTa_avg = KTa_avg - 2048

KTa_scale_1 = float(int(KTa_scale) & 0x07e0)
KTa_scale_1 = KTa_scale_1 / (2 ** 5)
KTa_scale_2 = float(int(KTa_scale) & 0x001f)

KV_avg = read_eeprom(eeprom_data, "17")
KV_scale = read_eeprom(eeprom_data, "18")

KV_avg = float(int(KV_avg) & 0x07ff)
if KV_avg > 1023:
    KV_avg = KV_avg - 2048

KV_scale_1 = float(int(KV_scale) & 0x07e0)
KV_scale_1 = KV_scale_1 / (2 ** 5)
KV_scale_2 = float(int(KV_scale) & 0x001f)

# IR data emissivity ==========================
Emissivity = read_eeprom(eeprom_data, "23")
Emissivity = float(int(Emissivity) & 0x07ff)
if Emissivity > 1023:
    Emissivity = Emissivity - 2048

Emissivity = Emissivity / (2 ** 9)

CP = float(read_raw_block(ir_num, block_num, "ram", "88"))
if CP > 32767:
    CP = CP - 65536

CP_pix_gain = CP * K_gain

# offset compensation

Offset_CP_W1 = read_eeprom(eeprom_data, "2f")
Offset_CP_W2 = read_eeprom(eeprom_data, "30")
KV_CP_scale_ee = read_eeprom(eeprom_data, "32")
KTa_CP_scale = read_eeprom(eeprom_data, "31")

pix_OS_ref_CP = float(32 * (int(Offset_CP_W1) & 0x07ff) + (int(Offset_CP_W2) & 0x07ff))
if pix_OS_ref_CP > 32767:
    pix_OS_ref_CP = pix_OS_ref_CP - 65536

KV_CP_scale = float(int(KV_CP_scale_ee) & 0x07c0)
KV_CP_scale = KV_CP_scale / (2 ** 6)

KV_CP_ee = float(int(KV_CP_scale_ee) & 0x003f)
if KV_CP_ee > 31:
    KV_CP_ee = KV_CP_ee - 64

KV_CP = KV_CP_ee / (2 ** KV_CP_scale)

KTa_CP_ee = float(int(KTa_CP_scale) & 0x003f)
if KTa_CP_ee > 31:
    KTa_CP_ee = KTa_CP_ee - 64

KTa_CP_scale_1 = float(int(KTa_CP_scale) & 0x07c0)
KTa_CP_scale_1 = KTa_CP_scale_1 / (2 ** 6)
KTa_CP = KTa_CP_ee / (2 ** KTa_CP_scale_1)
CP_pix_OS = float(CP_pix_gain - pix_OS_ref_CP * (1 + KTa_CP * (Ta - 25)) * (1 + KV_CP * (Vdd - 3.3)))

# Normalizing to sensitivity
row1_max = read_eeprom(eeprom_data, "1c")
row2_max = read_eeprom(eeprom_data, "1d")
row3_max = read_eeprom(eeprom_data, "1e")
row4_max = read_eeprom(eeprom_data, "1f")
row5_max = read_eeprom(eeprom_data, "20")
row6_max = read_eeprom(eeprom_data, "21")

scale_row12 = read_eeprom(eeprom_data, "19")
scale_row34 = read_eeprom(eeprom_data, "1a")
scale_row56 = read_eeprom(eeprom_data, "1b")

# Calculating To basic range [0..80 °C] - range 3
KsTo_scale_ee = read_eeprom(eeprom_data, "34")
KsTo_1_ee = read_eeprom(eeprom_data, "35")
KsTo_2_ee = read_eeprom(eeprom_data, "36")
KsTo_3_ee = read_eeprom(eeprom_data, "37")
KsTo_4_ee = read_eeprom(eeprom_data, "38")
KsTo_5_ee = read_eeprom(eeprom_data, "39")
KsTo_6_ee = read_eeprom(eeprom_data, "3b")
KsTo_7_ee = read_eeprom(eeprom_data, "3d")
KsTo_8_ee = read_eeprom(eeprom_data, "3f")

CT6_ee = read_eeprom(eeprom_data, "3a")
CT7_ee = read_eeprom(eeprom_data, "3c")
CT8_ee = read_eeprom(eeprom_data, "3e")

alpha_cyclops = read_eeprom(eeprom_data, "2d")
alpha_cyclop_scale = read_eeprom(eeprom_data, "2e")
KsTa_ee = read_eeprom(eeprom_data, "22")

alpha_scale_row1 = float(int(scale_row12) & 0x07e0) / (2 ** 5) + 20
alpha_scale_row2 = float(int(scale_row12) & 0x001f) / (2 ** 5) + 20
alpha_scale_row3 = float(int(scale_row34) & 0x07e0) / (2 ** 5) + 20
alpha_scale_row4 = float(int(scale_row34) & 0x001f) / (2 ** 5) + 20
alpha_scale_row5 = float(int(scale_row56) & 0x07e0) / (2 ** 5) + 20
alpha_scale_row6 = float(int(scale_row56) & 0x001f) / (2 ** 5) + 20

alpha_reference_row1 = float(int(row1_max) & 0x07ff) / (2 ** alpha_scale_row1)
alpha_reference_row2 = float(int(row2_max) & 0x07ff) / (2 ** alpha_scale_row2)
alpha_reference_row3 = float(int(row3_max) & 0x07ff) / (2 ** alpha_scale_row3)
alpha_reference_row4 = float(int(row4_max) & 0x07ff) / (2 ** alpha_scale_row4)
alpha_reference_row5 = float(int(row5_max) & 0x07ff) / (2 ** alpha_scale_row5)
alpha_reference_row6 = float(int(row6_max) & 0x07ff) / (2 ** alpha_scale_row6)

print(alpha_reference_row1)
print(alpha_reference_row2)
print(alpha_reference_row3)
print(alpha_reference_row4)
print(alpha_reference_row5)
print(alpha_reference_row6)


alpha_scale_CP = float(int(alpha_cyclop_scale) & 0x07ff)
alpha_CP = float(int(alpha_cyclops) & 0x07ff)
alpha_CP = alpha_CP / (2 ** alpha_scale_CP)

for y in range(0, 12):
    for x in range(0, 16):

        pix_val = read_raw_block(ir_num, block_num, "img", y, x)
        pix_val = float(pix_val)
        if pix_val > 32767:
            pix_val = pix_val - 65536

        pix_gain = pix_val * K_gain

        Pix_os_SP0_ee = read_pix_eeprom(eeprom_data, "os1", y, x)
        Pix_os_SP1_ee = read_pix_eeprom(eeprom_data, "os2", y, x)

        Offset_SP0 = float(int(Pix_os_SP0_ee) & 0x07ff)
        if Offset_SP0 > 1023:
            Offset_SP0 = Offset_SP0 - 2048

        Offset_SP1 = float(int(Pix_os_SP1_ee) & 0x07ff)
        if Offset_SP1 > 1023:
            Offset_SP1 = Offset_SP1 - 2048

        pix_OS_ref_SP0 = Offset_average + Offset_SP0 * 2 ** Offset_scale
        pix_OS_ref_SP1 = Offset_average + Offset_SP1 * 2 ** Offset_scale

        # KTa =======================================

        KTa_ee = read_pix_eeprom(eeprom_data, "ktakv", y, x)
        KTa_ee = float(int(KTa_ee) & 0x07e0)
        KTa_ee = KTa_ee / (2 ** 5)
        if KTa_ee > 31:
            KTa_ee = KTa_ee - 64

        KTa = (KTa_ee * 2 ** KTa_scale_2 + KTa_avg) / 2 ** KTa_scale_1

        # KV ============================

        KV_ee = read_pix_eeprom(eeprom_data, "ktakv", y, x)
        KV_ee = float(int(KV_ee) & 0x001f)
        if KV_ee > 15:
            KV_ee = KV_ee - 32

        KV = (KV_ee * 2 ** KV_scale_2 + KV_avg) / 2 ** KV_scale_1

        # Compensation ==============================

        pix_OS_SP0 = round(pix_gain - pix_OS_ref_SP0 * (1 + KTa * (Ta - 25)) * (1 + KV * (Vdd - 3.3)))
        pix_OS_SP1 = round(pix_gain - pix_OS_ref_SP1 * (1 + KTa * (Ta - 25)) * (1 + KV * (Vdd - 3.3)))

        current_subpage = y % 2
        pix_OS = pix_OS_SP0 if current_subpage == 0 else pix_OS_SP1
        # pix_OS = pix_OS_SP0

        OS_image[y, x] = pix_OS

        # IR data gradient compensation
        TGC_ee = float(int(TGC_ee) & 0x01ff)
        if TGC_ee > 255:
            TGC_ee = TGC_ee - 512

        TGC = float(TGC_ee / (2 ** 6))
        V_IR_compensated = round((pix_OS - TGC * CP_pix_OS) / Emissivity)

        alpha_pixel_sensitivity = read_pix_eeprom(eeprom_data, "alpha", y, x)
        alpha_pixel = float(int(alpha_pixel_sensitivity) & 0x07ff)

        KsTa = float(int(KsTa_ee) & 0x07ff)
        if KsTa > 1023:
            KsTa = KsTa - 2048

        KsTa = KsTa / (2 ** 15)
        alpha = (alpha_pixel / (2 ** 11 - 1)) * alpha_reference_row3
        alpha_comp = (alpha - TGC * alpha_CP) * (1 + KsTa * (Ta - 25))

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

        print("==============================")
        print(f"alpha_pixel raw: {alpha_pixel}")
        print(f"alpha: {alpha}")
        print(f"alpha_comp: {alpha_comp}")
        print(f"Sx_under_root: {Sx_under_root}")

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
