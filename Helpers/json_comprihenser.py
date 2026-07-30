import tkinter as tk
from tkinter import filedialog
import json
import ast

root = tk.Tk()
root.withdraw()

# FITS fájl kiválasztása
JSON_S = filedialog.askopenfilenames(
    title="Válassz két JSON fájlt",
    filetypes=[("FITS fájlok", "*.json")]
)

if not len(JSON_S) == 2:
    raise Exception("Bro wtf?")

with open(JSON_S[0], "r") as json_1:
    with open(JSON_S[1], "r") as json_2:
        json_1_data = json.load(json_1)
        json_2_data = json.load(json_2)

INDENT  = 24
INDENT_ = 110

print(f"{"KEY":^{INDENT}} || {"JSON 1":^{INDENT_}} || {"JSON 2":^{INDENT_}}")
print(f"{"="*INDENT}=||={"="*INDENT_}=||={"="*INDENT_}")
json_2_keys = json_2_data.keys()
for key in json_1_data:
    if key not in json_2_keys:
        print(f"{str(key):^{INDENT}} || {str(json_1_data[key]):^{INDENT_}} || {"None":^{INDENT_}}")
        continue
    if not json_1_data[key] == json_2_data[key]:

        if isinstance(json_1_data[key], list):
            formated_out_1 = json_1_data[key]
            formated_out_2 = json_2_data[key]

            print(f"{"-" * INDENT}-||-{"-" * INDENT_}-||-{"-" * INDENT_}")
            for num in range(len(formated_out_1)):
                print(f"{" ":^{INDENT}} || {str(formated_out_1[num]):^{INDENT_}} || {str(formated_out_2[num]):^{INDENT}}")
            print(f"{"-" * INDENT}-||-{"-" * INDENT_}-||-{"-" * INDENT_}")

        else:
            print(f"{str(key):^{INDENT}} || {str(json_1_data[key]):^{INDENT_}} || {str(json_2_data[key]):^{INDENT_}}")

while 1:
    pass