// =====================================================================
// domain_demo.cpp
// ---------------------------------------------------------------------
// Demonstrasi Soal 2, 3, dan 4:
//   - batas tertutup usia >= 18, titik ON = 18 dan OFF = 17;
//   - closure error  : usia > 18   (tanda batas salah)
//   - shifted error  : usia >= 19  (batas bergeser ke kanan)
//   - shifted error  : usia >= 17  (batas bergeser ke kiri)
//   - computation bug: rumus harga diskon salah, batas benar.
//
// Kompilasi:
//   g++ -std=c++17 -Wall -Wextra -O0 -o build/domain_demo domain_demo.cpp
// Jalankan:
//   ./build/domain_demo
// =====================================================================
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

// --- Aturan pendaftaran: usia minimal 18 tahun (batas tertutup) ------
bool daftarBenar(int usia)        { return usia >= 18; }
bool daftarClosureError(int usia) { return usia > 18; }   // salah tanda
bool daftarShiftKanan(int usia)   { return usia >= 19; }  // bergeser +1
bool daftarShiftKiri(int usia)    { return usia >= 17; }  // bergeser -1

const char* hasil(bool diterima) {
    return diterima ? "DITERIMA" : "DITOLAK";
}

string tanda(bool hasilUji, bool diharapkan) {
    return hasilUji == diharapkan ? "  " : " *";
}

// --- Aturan harga tiket: usia < 12 tahun mendapat harga anak ---------
int hargaBenar(int usia) {
    return (usia < 12) ? 25000 : 50000;
}

int hargaDomainBug(int usia) {
    return (usia <= 12) ? 25000 : 50000;   // batas salah: 12 ikut diskon
}

int hargaKomputasiBug(int usia) {
    return (usia < 12) ? 40000 : 50000;    // rumus salah: harusnya 25000
}

struct KasusDaftar {
    int usia;
    bool diharapkan;
};

struct KasusTiket {
    int usia;
    int diharapkan;
};

int main() {
    cout << "==============================================================\n";
    cout << "DEMO DOMAIN TESTING - PENDAFTARAN USIA >= 18\n";
    cout << "==============================================================\n";
    cout << "Batas     : TERTUTUP (operator >=, nilai 18 termasuk domain sah)\n";
    cout << "Domain    : usia 18, 19, 20, ... diterima; 17, 16, ... ditolak\n";
    cout << "Titik ON  : 18 (tepat di garis batas, di dalam domain)\n";
    cout << "Titik OFF : 17 (tetangga terdekat di luar domain)\n\n";

    vector<KasusDaftar> kasus = {
        {17, false}, {18, true}, {19, true}, {25, true},
    };

    cout << left
         << setw(6)  << "Usia"
         << setw(11) << "Harapan"
         << setw(14) << "Benar(>=18)"
         << setw(15) << "Closure(>18)"
         << setw(16) << "Shift(>=19)"
         << setw(16) << "Shift(>=17)" << "\n";
    cout << string(78, '-') << "\n";

    for (const KasusDaftar& k : kasus) {
        bool b = daftarBenar(k.usia);
        bool c = daftarClosureError(k.usia);
        bool s1 = daftarShiftKanan(k.usia);
        bool s2 = daftarShiftKiri(k.usia);
        cout << left
             << setw(6)  << k.usia
             << setw(11) << hasil(k.diharapkan)
             << setw(14) << (string(hasil(b))  + tanda(b,  k.diharapkan))
             << setw(15) << (string(hasil(c))  + tanda(c,  k.diharapkan))
             << setw(16) << (string(hasil(s1)) + tanda(s1, k.diharapkan))
             << setw(16) << (string(hasil(s2)) + tanda(s2, k.diharapkan))
             << "\n";
    }

    cout << "\nTanda * = hasil menyimpang dari aturan (cacat terdeteksi).\n";
    cout << "Kesimpulan:\n";
    cout << "  1. Closure error (>18) tertangkap oleh titik ON 18.\n";
    cout << "  2. Shift ke kanan (>=19) juga tertangkap oleh 18.\n";
    cout << "  3. Shift ke kiri (>=17) tertangkap oleh titik OFF 17.\n";
    cout << "  4. Uji 19 dan 25 saja TIDAK cukup: keempat versi menerima.\n";

    cout << "\n==============================================================\n";
    cout << "DEMO CACAT KOMPUTASI - HARGA TIKET BIODATA\n";
    cout << "==============================================================\n";
    cout << "Aturan: usia < 12 -> Rp25.000; selain itu -> Rp50.000\n\n";

    vector<KasusTiket> tiket = {
        {10, 25000}, {11, 25000}, {12, 50000}, {18, 50000},
    };

    cout << left
         << setw(6)  << "Usia"
         << setw(14) << "Harga benar"
         << setw(18) << "DomainBug(<=12)"
         << setw(20) << "KomputasiBug(0.8)" << "\n";
    cout << string(60, '-') << "\n";

    for (const KasusTiket& t : tiket) {
        int hb = hargaBenar(t.usia);
        int hd = hargaDomainBug(t.usia);
        int hk = hargaKomputasiBug(t.usia);
        cout << left
             << setw(6)  << t.usia
             << setw(14) << hb
             << setw(18) << (to_string(hd) + (hd == t.diharapkan ? "  " : " *"))
             << setw(20) << (to_string(hk) + (hk == t.diharapkan ? "  " : " *"))
             << "\n";
    }

    cout << "\nTanda * = harga menyimpang dari aturan.\n";
    cout << "Kesimpulan:\n";
    cout << "  1. Domain bug hanya muncul di batas (usia 12).\n";
    cout << "  2. Computation bug muncul di dalam domain (usia 10 dan 11).\n";
    cout << "  3. Karena itu pengujian memerlukan titik batas DAN nilai nominal.\n";
    return 0;
}
