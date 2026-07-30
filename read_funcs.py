import numpy as np
from icecream import ic


def read_eeprom(data_in, hex_last2digit):
    index = int(hex_last2digit, 16)  # hex string -> int
    if index < 0 or index > 63:
        raise ValueError("wtf bro...")
    return data_in[index]


def read_raw_block(ir_sensor, block_num, data_name, coord1=None, coord2=None):
    if block_num > 219:
        raise ValueError("block_num must be between 0 and 219!")

    if ir_sensor < 20 or ir_sensor > 23:
        raise ValueError("Sensor number should be between 20 and 23!")

    filename = (f"ir_calib/1329_data/raw_block-n{block_num:03d}-{ir_sensor}.txt")
    img = np.zeros((12, 16))

    with open(filename, "r") as file:
        lines = file.readlines()

    time = lines[0].strip()

    # 12x16 kép
    for i in range(1, 13):
        img[i - 1, :] = np.array([int(x, 16) for x in lines[i].split()])

    # RAM sor
    ram = np.array([int(x, 16) for x in lines[13].split()])

    if data_name == "time":
        return float(time)
    elif data_name == "img":
        # return img[coord1-1, coord2-1]
        return img[coord1, coord2]
    elif data_name == "ram":
        index = int(coord1, 16) - 128
        if index < 0 or index > 47:
            raise ValueError("Address should be between 80 and af (string)!")
        return ram[index]
    else:
        raise ValueError("Invalid data_name")


def read_pix_eeprom(data_in, data_name, coord1, coord2):
    pixel_index = 16 * coord1 + coord2

    if data_name == "os1":
        os1 = data_in[64:256]
        return os1[pixel_index]
    elif data_name == "alpha":
        alpha = data_in[256:448]
        return alpha[pixel_index]
    elif data_name == "ktakv":
        ktakv = data_in[448:640]
        return ktakv[pixel_index]
    elif data_name == "os2":
        os2 = data_in[640:832]
        return os2[pixel_index]
    else:
        raise ValueError("Unknown EEPROM data name")
