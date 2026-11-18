// =====================================================================
// Soal 6 - Eksekusi Simbolik & Pemilihan Vektor Input
// ---------------------------------------------------------------------
// Kode:
//   if (totalBelanja >= 500000)
//       cout << "Diskon diberikan";
//   else
//       cout << "Tidak mendapat diskon";
//
// Program menerima total belanja sebagai argumen, mencetak cabang yang
// dijalankan, lalu (bila tanpa argumen) menjalankan tabel kasus uji
// termasuk nilai batas (boundary value) 500000 dan 499999.
//
// Kompilasi : g++ -std=c++17 -o build/soal06_diskon soal06_diskon.cpp
// Pemakaian : build/soal06_diskon 750000
//             build/soal06_diskon          (menjalankan seluruh tabel)
// =====================================================================
#include <iostream>
#include <iomanip>
#include <string>
#include <cstdlib>

using namespace std;

static bool beriDiskon(long long totalBelanja) {
    return totalBelanja >= 500000;      // kondisi simbolik: T >= 500000
}

static void satuKasus(long long totalBelanja, bool cetakJudul = true) {
    if (cetakJudul) cout << "\nInput totalBelanja = " << totalBelanja << "\n";
    if (beriDiskon(totalBelanja)) {
        cout << "  cabang TRUE  -> \"Diskon diberikan\"\n";
    } else {
        cout << "  cabang FALSE -> \"Tidak mendapat diskon\"\n";
    }
}

int main(int argc, char** argv) {
    cout << "=== Soal 6: Eksekusi Simbolik & Vektor Input ===\n";

    cout << "\nSyarat cabang TRUE : C  = (totalBelanja >= 500000)\n";
    cout << "Syarat cabang FALSE: ~C = (totalBelanja < 500000)\n";

    if (argc > 1) {
        satuKasus(atoll(argv[1]), false);
        return 0;
    }

    // Tabel kasus uji: nilai batas dan nilai di sekitar batas.
    struct Kasus { long long nilai; const char* alasan; };
    Kasus daftar[] = {
        {750000, "jauh di atas batas"},
        {500000, "tepat pada batas (boundary)"},
        {499999, "satu di bawah batas (boundary - 1)"},
        {250000, "jauh di bawah batas"},
        {0,      "nilai minimum"},
    };

    cout << "\n" << left << setw(12) << "Input" << setw(40) << "Alasan"
         << "Cabang yang dijalankan\n";
    cout << string(92, '-') << "\n";
    for (const auto& k : daftar) {
        cout << left << setw(12) << k.nilai << setw(40) << k.alasan
             << (beriDiskon(k.nilai) ? "TRUE  (diskon)" : "FALSE (tanpa diskon)")
             << "\n";
    }

    cout << "\nKesimpulan: dua vektor input minimal yang menjamin kedua cabang\n";
    cout << "tercakup adalah (750000) dan (250000); nilai batas 500000/499999\n";
    cout << "ditambahkan untuk menguji ketepatan perbandingan >=.\n";
    return 0;
}
