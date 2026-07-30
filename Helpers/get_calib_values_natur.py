import numpy as np

Data = {}

def read_eeprom(data_in, hex_last2digit, name):
    index = int(hex_last2digit, 16)  # hex string -> int
    print(f"\t \t 0x24{hex_last2digit} \t {name:<18} \t {"eeprom"} \t {data_in[index]:<16} ")
    return data_in[index]


def read_pix_eeprom(data_in, data_name, coord1, coord2, name):
    pixel_index = 16 * coord1 + coord2

    if data_name == "os1":          # 192 x Pixel offset - subpage 1
        os1 = data_in[64:256]
        ret = os1[pixel_index]
        hexindex = 64 + pixel_index -64

    elif data_name == "alpha":      # 192 x Pixel sensitivity - α
        alpha = data_in[256:448]
        ret =  alpha[pixel_index]
        hexindex = 256 + pixel_index - 64

    elif data_name == "ktakv":      # 192 x Kta, Kv (i, j)
        ktakv = data_in[448:640]
        ret =  ktakv[pixel_index]
        hexindex = 448 + pixel_index - 64

    elif data_name == "os2":        # 192 x Pixel offset - subpage 2
        os2 = data_in[640:832]
        ret =  os2[pixel_index]
        hexindex = 640 + pixel_index - 64

    else:
        raise ValueError("---wtf---")

    hexindex += 0x2440
    print(f"{"  xy>"} \t {hex(hexindex)} \t {name:<24} \t {"eeprom"} \t {ret:<16} ")
    return ret


for i in range(1):  # Alapvetően 4!
    ir_num = i + 20
    filename = f"../ir_calib/calib_data/ir{ir_num}ec.txt"

    eeprom_data = np.loadtxt(filename, dtype=str)
    eeprom_data = np.array([int(x, 16) for x in eeprom_data])

    print("")
    print(f"SENSOR: {ir_num} \t ADDRESS \t VAL. NAME \t SOURCE \t VALUE")
    print("========================================================================================================================================================")
    Vdd25 = read_eeprom(eeprom_data, '26', "Vdd25")  # 0x2426
    KVdd = read_eeprom(eeprom_data, '27', "KVdd")  # 0x2427
    PTAT25_1 = read_eeprom(eeprom_data, '28', "PTAT25_1")  # 0x2428
    PTAT25_2 = read_eeprom(eeprom_data, '29', "PTAT25_2")  # 0x2429
    KTPTAT = read_eeprom(eeprom_data, '2a', "KTPTAT")  # 0x242a
    KVPTAT = read_eeprom(eeprom_data, '2b', "KVPTAT")  # 0x242b
    AlphaPTAT = read_eeprom(eeprom_data, '2c', "AlphaPTAT")  # 0x242c
    TGC_ee = read_eeprom(eeprom_data, "33", "TGC_ee")  # EE[0x2433]
    GAIN_EE_1 = read_eeprom(eeprom_data, "24", "GAIN_EE_1")
    GAIN_EE_2 = read_eeprom(eeprom_data, "25", "GAIN_EE_2")
    Pix_os_R1_1 = read_eeprom(eeprom_data, "11", "Pix_os_R1_1")
    Pix_os_R1_2 = read_eeprom(eeprom_data, "12", "Pix_os_R1_2")
    Scale_occ = read_eeprom(eeprom_data, "10", "Scale_occ")
    KTa_avg = read_eeprom(eeprom_data, "15", "KTa_avg")
    KTa_scale = read_eeprom(eeprom_data, "16", "KTa_scale")
    KV_avg = read_eeprom(eeprom_data, "17", "KV_avg")
    KV_scale = read_eeprom(eeprom_data, "18", "KV_scale")
    Emissivity = read_eeprom(eeprom_data, "23", "Emissivity")
    Offset_CP_W1 = read_eeprom(eeprom_data, "2f", "Offset_CP_W1")
    Offset_CP_W2 = read_eeprom(eeprom_data, "30", "Offset_CP_W2")
    KV_CP_scale_ee = read_eeprom(eeprom_data, "32", "KV_CP_scale_ee")
    KTa_CP_scale = read_eeprom(eeprom_data, "31", "KTa_CP_scale")
    row1_max = read_eeprom(eeprom_data, "1c", "row1_max")
    row2_max = read_eeprom(eeprom_data, "1d", "row2_max")
    row3_max = read_eeprom(eeprom_data, "1e", "row3_max")
    row4_max = read_eeprom(eeprom_data, "1f", "row4_max")
    row5_max = read_eeprom(eeprom_data, "20", "row5_max")
    row6_max = read_eeprom(eeprom_data, "21", "row6_max")
    scale_row12 = read_eeprom(eeprom_data, "19", "scale_row12")
    scale_row34 = read_eeprom(eeprom_data, "1a", "scale_row34")
    scale_row56 = read_eeprom(eeprom_data, "1b", "scale_row56")
    KsTo_scale_ee = read_eeprom(eeprom_data, "34", "KsTo_scale_ee")
    KsTo_1_ee = read_eeprom(eeprom_data, "35", "KsTo_1_ee")
    KsTo_2_ee = read_eeprom(eeprom_data, "36", "KsTo_2_ee")
    KsTo_3_ee = read_eeprom(eeprom_data, "37", "KsTo_3_ee")
    KsTo_4_ee = read_eeprom(eeprom_data, "38", "KsTo_4_ee")
    KsTo_5_ee = read_eeprom(eeprom_data, "39", "KsTo_5_ee")
    KsTo_6_ee = read_eeprom(eeprom_data, "3b", "KsTo_6_ee")
    KsTo_7_ee = read_eeprom(eeprom_data, "3d", "KsTo_7_ee")
    KsTo_8_ee = read_eeprom(eeprom_data, "3f", "KsTo_8_ee")
    CT6_ee = read_eeprom(eeprom_data, "3a", "CT6_ee")
    CT7_ee = read_eeprom(eeprom_data, "3c", "CT7_ee")
    CT8_ee = read_eeprom(eeprom_data, "3e", "CT8_ee")
    alpha_cyclops = read_eeprom(eeprom_data, "2d", "alpha_cyclops")
    alpha_cyclop_scale = read_eeprom(eeprom_data, "2e", "alpha_cyclop_scale")
    KsTa_ee = read_eeprom(eeprom_data, "22", "KsTa_ee")

    print("")
    array = []
    for y in range(0, 12):
        for x in range(0, 16):
            Pix_os_SP0_ee = read_pix_eeprom(eeprom_data, "os1", y, x, "Pix_os_SP0_ee")
            Pix_os_SP1_ee = read_pix_eeprom(eeprom_data, "os2", y, x, "Pix_os_SP1_ee")
            KTa_ee = read_pix_eeprom(eeprom_data, "ktakv", y, x, "KTa_ee")
            KV_ee = read_pix_eeprom(eeprom_data, "ktakv", y, x, "KV_ee")
            alpha_pixel_sensitivity = read_pix_eeprom(eeprom_data, "alpha", y, x, "alpha_pixel_sensitivity")

            print("")
            act_act_dict = {
                "Pix_os_SP0_ee" : Pix_os_SP0_ee,
                "Pix_os_SP1_ee" : Pix_os_SP1_ee,
                "KTa_ee" : KTa_ee,
                "KV_ee" : KV_ee,
                "alpha_pixel_sensitivity" : alpha_pixel_sensitivity,
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
        "GAIN_EE_1" : GAIN_EE_1,
        "GAIN_EE_2" : GAIN_EE_2,

        "Pix_os_R1_1" : Pix_os_R1_1,
        "Pix_os_R1_2" : Pix_os_R1_2,
        "Scale_occ" : Scale_occ,

        "KTa_avg" : KTa_avg,
        "KTa_scale" : KTa_scale,

        "KV_scale" : KV_scale,
        "KV_avg" : KV_avg,
        "Emissivity" : Emissivity,

        "Offset_CP_W1" : Offset_CP_W1,
        "Offset_CP_W2" : Offset_CP_W2,
        "KV_CP_scale_ee" : KV_CP_scale_ee,
        "KTa_CP_scale" : KTa_CP_scale,

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
        "xy_fuggo_dolgok": array,
    }


    Data[ir_num] = act_dict

#
# for value in Data.values():
#     for key in value:
#         if key == "xy_fuggo_dolgok":
#             for arr in value[key]:
#                 print(f" \t\t\t{arr}")
#         else:
#             print(f"{key} :\t{value[key]}")
#
#
#     print("========================================================================================================================================================")


