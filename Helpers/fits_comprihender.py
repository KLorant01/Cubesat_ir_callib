from astropy.io import fits
import numpy as np
from time import time

root = tk.Tk()
root.withdraw()

filename = filedialog.askopenfilename(
    title="Válassz egy FITS fájlt",
    filetypes=[("FITS fájlok", "*.fits *.fit *.fts")]
)