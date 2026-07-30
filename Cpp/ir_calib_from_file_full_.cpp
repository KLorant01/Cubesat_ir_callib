#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <fitsio.h> // CFITSIO könyvtár (astropy.io.fits helyett)

int main() {
    int ir_num = 21;
    int block_num = 200;

    // 1. Mátrixok inicializálása nullákkal (12 sor, 16 oszlop)
    std::vector<std::vector<double>> To_image(12, std::vector<double>(16, 0.0));
    std::vector<std::vector<double>> OS_image(12, std::vector<double>(16, 0.0));

    // 2. Fájlnevek összeállítása formázott sztringként (Python f-string megfelelője)
    std::ostringstream fits_ss;
    fits_ss << "1329/raw_block-n" << std::setw(3) << std::setfill('0') << block_num 
            << "-" << ir_num << ".fits";
    std::string fits_filename = fits_ss.str();

    std::ostringstream txt_ss;
    txt_ss << "ir_calib/calib_data/ir" << ir_num << "ec.txt";
    std::string txt_filename = txt_ss.str();

    // 3. FITS fájl beolvasása CFITSIO-val
    fitsfile *fptr;
    int status = 0; // A CFITSIO a hibakódokat ezen a változón keresztül adja vissza

    // FITS fájl megnyitása olvasásra
    fits_open_file(&fptr, fits_filename.c_str(), READONLY, &status);

    // Képadat tároló (12 * 16 elemű lapos tömb)
    std::vector<double> img_data(12 * 16);
    long fpixel = 1;
    long nelements = 12 * 16;
    int anynul = 0;

    // Képadatok beolvasása a tömbbe
    fits_read_img(fptr, TDOUBLE, fpixel, nelements, NULL, img_data.data(), &anynul, &status);
    fits_close_file(fptr, &status);

    if (status != 0) {
        fits_report_error(stderr, status); // Hiba kiírása, ha nem sikerült az olvasás
    }

    // 4. Hexadecimális adatok beolvasása és konvertálása TXT-ből
    std::vector<int> eeprom_data;
    std::ifstream txt_file(txt_filename);
    std::string hex_str;

    if (txt_file.is_open()) {
        while (txt_file >> hex_str) {
            // Hexadecimális string konvertálása 10-es számrendszerbeli int-té (Python: int(x, 16))
            int value = std::stoi(hex_str, nullptr, 16);
            eeprom_data.push_back(value);
        }
        txt_file.close();
    } else {
        std::cerr << "Nem sikerült megnyitni a TXT fájlt: " << txt_filename << std::endl;
    }

    // 5. Időmérés kezdete
    auto tic = std::chrono::high_resolution_clock::now();

    return 0;
}
