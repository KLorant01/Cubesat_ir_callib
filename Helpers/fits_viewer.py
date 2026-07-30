import tkinter as tk
from tkinter import filedialog

from astropy.io import fits
import matplotlib.pyplot as plt

# Elrejti a fő tkinter ablakot
root = tk.Tk()
root.withdraw()

# FITS fájl kiválasztása
filename = filedialog.askopenfilename(
    title="Válassz egy FITS fájlt",
    filetypes=[("FITS fájlok", "*.fits *.fit *.fts")]
)

if not filename:
    exit()

# FITS fájl megnyitása
with fits.open(filename) as hdul:
    hdul.info()  # Kiírja a HDU-kat

    # Megkeresi az első képet tartalmazó HDU-t
    image = None
    for hdu in hdul:
        if hdu.data is not None:
            image = hdu.data
            break

if image is None:
    print("Nem található képadat a fájlban.")
    exit()

# Ha több dimenziós (pl. (1, ny, nx)), akkor az első szeletet veszi
while image.ndim > 2:
    image = image[0]

plt.imshow(image[::-1], origin='lower', cmap='gray')    # Tökrözés x-re
plt.show()