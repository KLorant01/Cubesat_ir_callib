from read_funcs import read_eeprom, read_pix_eeprom, read_raw_block
block_num = 200
ir_num = 21



print(float(read_raw_block(ir_num, block_num, "ram", "88")))