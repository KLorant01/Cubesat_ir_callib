import numpy as np
from read_funcs import read_eeprom, read_pix_eeprom

Data = {}

for i in range(4):
    ir_num = i + 20
    filename = f"../ir_calib/calib_data/ir{ir_num}ec.txt"

    eeprom_data = np.loadtxt(filename, dtype=str)
    eeprom_data = np.array([int(x, 16) for x in eeprom_data])

    Vdd25 = read_eeprom(eeprom_data, '26')  # 0x2426
    KVdd = read_eeprom(eeprom_data, '27')  # 0x2427
    PTAT25_1 = read_eeprom(eeprom_data, '28')  # 0x2428
    PTAT25_2 = read_eeprom(eeprom_data, '29')  # 0x2429
    KTPTAT = read_eeprom(eeprom_data, '2a')  # 0x242a
    KVPTAT = read_eeprom(eeprom_data, '2b')  # 0x242b
    AlphaPTAT = read_eeprom(eeprom_data, '2c')  # 0x242c


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

    if Vdd25 > 1023:
        Vdd25 = Vdd25 - 2048

    Vdd25 = Vdd25 * (2**5)

    if KVdd > 1023:
        KVdd = KVdd - 2048

    KVdd = KVdd * (2**5)

    # VPTAT25
    PTAT25_1 = float(PTAT25_1 & 0x07ff)
    PTAT25_2 = float(PTAT25_2 & 0x07ff)
    VPTAT25 = 32 * PTAT25_1 + PTAT25_2

    # VPTATart
    AlphaPTAT = float(AlphaPTAT & 0x07ff)
    AlphaPTAT = AlphaPTAT / (2**7)

    TGC_ee = read_eeprom(eeprom_data, "33")  # EE[0x2433]
    Control_register = 0x1901

    Resolution_EE = float(TGC_ee & 0x0600)
    Resolution_EE = Resolution_EE / (2 ** 9)
    Resolution_REG = float(Control_register & 0x0c00)
    Resolution_REG = Resolution_REG / (2 ** 10)
    Resolution_corr = (2 ** Resolution_EE) / (2 ** Resolution_REG)

    GAIN_EE_1 = read_eeprom(eeprom_data, "24")
    GAIN_EE_2 = read_eeprom(eeprom_data, "25")
    GAIN = float(32 * (GAIN_EE_1 & 0x07ff) + (GAIN_EE_2 & 0x07ff))

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

    alpha_scale_CP = float(int(alpha_cyclop_scale) & 0x07ff)
    alpha_CP = float(int(alpha_cyclops) & 0x07ff)
    alpha_CP = alpha_CP / (2 ** alpha_scale_CP)


    array = []
    for y in range(0, 12):
        for x in range(0, 16):
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

            KTa_ee = read_pix_eeprom(eeprom_data, "ktakv", y, x)
            KTa_ee = float(int(KTa_ee) & 0x07e0)
            KTa_ee = KTa_ee / (2 ** 5)
            if KTa_ee > 31:
                KTa_ee = KTa_ee - 64

            KV_ee = read_pix_eeprom(eeprom_data, "ktakv", y, x)
            KV_ee = float(int(KV_ee) & 0x001f)
            if KV_ee > 15:
                KV_ee = KV_ee - 32

            KV = (KV_ee * 2 ** KV_scale_2 + KV_avg) / 2 ** KV_scale_1

            alpha_pixel_sensitivity = read_pix_eeprom(eeprom_data, "alpha", y, x)
            alpha_pixel = float(int(alpha_pixel_sensitivity) & 0x07ff)

            KsTa = float(int(KsTa_ee) & 0x07ff)
            if KsTa > 1023:
                KsTa = KsTa - 2048

            KsTa = KsTa / (2 ** 15)
            alpha = (alpha_pixel / (2 ** 11 - 1)) * alpha_reference_row3

            act_act_dict = {
                "Pix_os_SP0_ee" : Pix_os_SP0_ee,
                "Pix_os_SP1_ee" : Pix_os_SP1_ee,
                "Offset_SP0" : Offset_SP0,
                "Offset_SP1" : Offset_SP1,
                "pix_OS_ref_SP0" : pix_OS_ref_SP0,
                "pix_OS_ref_SP1" : pix_OS_ref_SP1,
                "KTa_ee" : KTa_ee,
                "KV_ee" : KV_ee,
                "KV" : KV,
                "alpha_pixel_sensitivity" : alpha_pixel_sensitivity,
                "alpha_pixel" : alpha_pixel,
                "KsTa" : KsTa,
                "alpha" : alpha,
            }
            array.append(act_act_dict)

    act_dict = {
        "Vdd25" : Vdd25,
        "KVdd" : KVdd,
        "PTAT25_1" : PTAT25_1,
        "PTAT25_2" : PTAT25_2,
        "KTPTAT" : KTPTAT,
        "KVPTAT" : KVPTAT,
        "AlphaPTAT" : AlphaPTAT,

        "TGC_ee" : TGC_ee,
        "Resolution_EE" : Resolution_EE,
        "Resolution_REG" : Resolution_REG,
        "Resolution_corr" : Resolution_corr,
        "GAIN_EE_1" : GAIN_EE_1,
        "GAIN_EE_2" : GAIN_EE_2,
        "GAIN" : GAIN,

        "Pix_os_R1_1" : Pix_os_R1_1,
        "Pix_os_R1_2" : Pix_os_R1_2,
        "Scale_occ" : Scale_occ,

        "Offset_average" : Offset_average,
        "Offset_scale" : Offset_scale,
        "KTa_avg" : KTa_avg,
        "KTa_scale" : KTa_scale,

        "KTa_scale_1" : KTa_scale_1,
        "KTa_scale_2" : KTa_scale_2,
        "KV_scale" : KV_scale,
        "KV_avg" : KV_avg,
        "KV_scale_1" : KV_scale_1,
        "KV_scale_2" : KV_scale_2,
        "Emissivity" : Emissivity,

        "Offset_CP_W1" : Offset_CP_W1,
        "Offset_CP_W2" : Offset_CP_W2,
        "KV_CP_scale_ee" : KV_CP_scale_ee,
        "KTa_CP_scale" : KTa_CP_scale,
        "pix_OS_ref_CP" : pix_OS_ref_CP,
        "KV_CP_scale" : KV_CP_scale,
        "KV_CP_ee" : KV_CP_ee,
        "KV_CP" : KV_CP,
        "KTa_CP_ee" : KTa_CP_ee,
        "KTa_CP_scale_1" : KTa_CP_scale_1,
        "KTa_CP" : KTa_CP,

        "row1_max" : row1_max,
        "row2_max" : row2_max,
        "row3_max" : row3_max,
        "row4_max" : row4_max,
        "row5_max" : row5_max,
        "row6_max" : row6_max,
        "scale_row12" : scale_row12,
        "scale_row34" : scale_row34,
        "scale_row56" : scale_row56,
        "KsTo_scale_ee" : KsTo_scale_ee,
        "KsTo_1_ee" : KsTo_1_ee,
        "KsTo_2_ee" : KsTo_2_ee,
        "KsTo_3_ee" : KsTo_3_ee,
        "KsTo_4_ee" : KsTo_4_ee,
        "KsTo_5_ee" : KsTo_5_ee,
        "KsTo_6_ee" : KsTo_6_ee,
        "KsTo_7_ee" : KsTo_7_ee,
        "KsTo_8_ee" : KsTo_8_ee,
        "CT6_ee" : CT6_ee,
        "CT7_ee" : CT7_ee,
        "CT8_ee" : CT8_ee,
        "alpha_cyclops" : alpha_cyclops,
        "alpha_cyclop_scale" : alpha_cyclop_scale,
        "KsTa_ee" : KsTa_ee,
        "alpha_scale_row1" : alpha_scale_row1,
        "alpha_scale_row2" : alpha_scale_row2,
        "alpha_scale_row3" : alpha_scale_row3,
        "alpha_scale_row4" : alpha_scale_row4,
        "alpha_scale_row5" : alpha_scale_row5,
        "alpha_scale_row6" : alpha_scale_row6,
        "alpha_reference_row1" : alpha_reference_row1,
        "alpha_reference_row2" : alpha_reference_row2,
        "alpha_reference_row3" : alpha_reference_row3,
        "alpha_reference_row4" : alpha_reference_row4,
        "alpha_reference_row5" : alpha_reference_row5,
        "alpha_reference_row6" : alpha_reference_row6,
        "alpha_scale_CP" : alpha_scale_CP,
        "alpha_CP" : alpha_CP,
        "xy_fuggo_dolgok": array,
    }


    Data[ir_num] = act_dict

for value in Data.values():
    for key in value:
        if key == "xy_fuggo_dolgok":
            for arr in value[key]:
                print(f" \t\t\t{arr}")
        else:
            print(f"{key} :\t{value[key]}")


    print("========================================================================================================================================================")


