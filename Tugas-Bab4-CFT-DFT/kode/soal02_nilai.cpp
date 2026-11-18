// =====================================================================
// Soal 2 - Control Flow Graph (CFG) sederhana
// ---------------------------------------------------------------------
// Kode yang dianalisis:
//   int nilai = 75;
//   if (nilai >= 60) { cout << "Lulus"; }
//   else             { cout << "Tidak lulus"; }
//   cout << "Selesai";
//
// Program ini mencetak jejak simpul CFG yang dilalui (B1..B6) supaya
// jalur eksekusi dapat dibandingkan langsung dengan gambar CFG pada
// dokumen jawaban.
//
// Kompilasi : g++ -std=c++17 -o build/soal02_nilai soal02_nilai.cpp
// Pemakaian : build/soal02_nilai 75
//             build/soal02_nilai 50
// =====================================================================
#include <iostream>
#include <string>
#include <cstdlib>

using namespace std;

static void jejak(const string& simpul) {
    cout << "[JEJAK] " << simpul << "\n";
}

int main(int argc, char** argv) {
    int nilai = (argc > 1) ? atoi(argv[1]) : 75;

    cout << "=== Soal 2: CFG nilai kelulusan ===\n";
    cout << "Input nilai = " << nilai << "\n";

    // B1: inisialisasi
    jejak("B1  nilai = " + to_string(nilai));

    // B2: titik keputusan
    jejak("B2  if (nilai >= 60)");
    if (nilai >= 60) {                       // B2 -> B3 (true)
        jejak("B3  cout << \"Lulus\"");
        cout << "Lulus\n";
    } else {                                  // B2 -> B4 (false)
        jejak("B4  cout << \"Tidak lulus\"");
        cout << "Tidak lulus\n";
    }

    // B5: penggabungan (merge)
    jejak("B5  cout << \"Selesai\"");
    cout << "Selesai\n";

    // B6: akhir program
    jejak("B6  return 0");

    return 0;
}
