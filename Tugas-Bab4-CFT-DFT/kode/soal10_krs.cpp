// =====================================================================
// Soal 10 - Studi Kasus KRS: Integrasi CFT dan DFT
// ---------------------------------------------------------------------
// Kode asli (statusMahasiswa konstan 1):
//   int sks = 0;
//   int statusMahasiswa = 1;
//   if (statusMahasiswa == 1) { sks = 20; }
//   if (sks >= 20) { cout << "Boleh mengambil mata kuliah"; }
//   else           { cout << "Tidak boleh mengambil mata kuliah"; }
//
// Dua mode eksekusi:
//   build/soal10_krs            -> mode "asli": statusMahasiswa = 1 (konstan)
//   build/soal10_krs 0          -> mode "parametrik": status dari argumen
//
// Mode parametrik dipakai untuk membuktikan bahwa cabang "tidak aktif"
// hanya dapat diuji setelah nilai statusMahasiswa dijadikan input.
//
// Kompilasi : g++ -std=c++17 -o build/soal10_krs soal10_krs.cpp
// =====================================================================
#include <iostream>
#include <string>
#include <cstdlib>

using namespace std;

static void jejak(const string& s) { cout << "  [JEJAK] " << s << "\n"; }

static void jalankan(int statusMahasiswa, bool cetakJejak) {
    int sks = 0;                            // d1
    if (cetakJejak) jejak("B1  sks = 0");

    if (cetakJejak) jejak("B2  baca statusMahasiswa = " + to_string(statusMahasiswa));
    if (cetakJejak) jejak("B3  if (statusMahasiswa == 1)");

    if (statusMahasiswa == 1) {             // p-use statusMahasiswa
        sks = 20;                           // d2
        if (cetakJejak) jejak("B4  sks = 20");
    } else {
        if (cetakJejak) jejak("B3  (false) -> B5");
    }

    if (cetakJejak) jejak("B5  if (sks >= 20)");   // p-use sks
    if (sks >= 20) {
        if (cetakJejak) jejak("B6  cout \"Boleh mengambil mata kuliah\"");
        cout << "Boleh mengambil mata kuliah\n";
    } else {
        if (cetakJejak) jejak("B7  cout \"Tidak boleh mengambil mata kuliah\"");
        cout << "Tidak boleh mengambil mata kuliah\n";
    }
    if (cetakJejak) jejak("B8  selesai");
}

int main(int argc, char** argv) {
    cout << "=== Soal 10: KRS - CFT & DFT ===\n";

    if (argc > 1) {
        int status = atoi(argv[1]);
        cout << "\nMode parametrik: statusMahasiswa = " << status << "\n";
        jalankan(status, true);
        return 0;
    }

    // Mode asli: statusMahasiswa dideklarasikan konstan di dalam program.
    cout << "\nMode asli (statusMahasiswa = 1 konstan):\n";
    const int statusMahasiswa = 1;
    jalankan(statusMahasiswa, true);

    cout << "\nCatatan statis:\n";
    cout << "  - Karena statusMahasiswa selalu 1, cabang else pada B3 tidak\n";
    cout << "    mungkin dieksekusi -> jalur B1-B2-B3(false)-B5-B7-B8 tidak layak.\n";
    cout << "  - Cabang B5 false juga tidak layak karena sks pasti 20 setelah B4.\n";
    cout << "  - Agar kedua cabang dapat diuji, statusMahasiswa harus menjadi\n";
    cout << "    parameter/input (lihat mode parametrik).\n";
    return 0;
}
