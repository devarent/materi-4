// =====================================================================
// Soal 5 - Jalur Layak (feasible) dan Jalur Tak Layak (infeasible)
// ---------------------------------------------------------------------
// Kode:
//   if (x > 10) {
//       if (x < 5) {
//           cout << "Proses A";
//       }
//   }
//
// Untuk mencapai "Proses A", jalur harus memenuhi konjungsi:
//   C = (x > 10) AND (x < 5)
//
// Program membuktikan dua hal:
//   1. Secara logika interval, irisan (10, +inf) dan (-inf, 5) kosong.
//   2. Secara empiris, tidak ada satu pun nilai x pada rentang uji yang
//      sangat lebar yang dapat mencapai "Proses A".
//
// Kompilasi : g++ -std=c++17 -o build/soal05_infeasible soal05_infeasible.cpp
// Pemakaian : build/soal05_infeasible
// =====================================================================
#include <iostream>
#include <climits>
#include <string>

using namespace std;

int main() {
    cout << "=== Soal 5: Analisis Jalur Tak Layak ===\n";

    cout << "\n1) Analisis simbolik (tanpa eksekusi)\n";
    cout << "   Syarat simpul B3 (cout \"Proses A\"):\n";
    cout << "     c1: x > 10\n";
    cout << "     c2: x < 5\n";
    cout << "   Gabungan: x > 10 DAN x < 5\n";
    cout << "   Interval c1 = (10, +inf), interval c2 = (-inf, 5)\n";
    cout << "   Irisan    = kosong (empty set)\n";
    cout << "   Kesimpulan: jalur B1->B2->B3->B4 TIDAK LAYAK (infeasible).\n";

    // 2) Pembuktian empiris dengan menyisir rentang bilangan yang lebar.
    long long batasBawah = -1000000;
    long long batasAtas  =  1000000;
    long long jumlahMasuk = 0;
    long long contohX = 0;

    for (long long x = batasBawah; x <= batasAtas; ++x) {
        bool luar = (x > 10);
        if (luar) {
            bool dalam = (x < 5);
            if (dalam) {                 // hanya tercapai jika kedua syarat benar
                ++jumlahMasuk;
                contohX = x;
                break;
            }
        }
    }

    cout << "\n2) Pembuktian empiris (brute force)\n";
    cout << "   Rentang x yang disisir : [" << batasBawah << ", " << batasAtas << "]\n";
    cout << "   Jumlah x yang mencapai \"Proses A\" : " << jumlahMasuk << "\n";
    if (jumlahMasuk == 0)
        cout << "   Tidak ada input yang dapat mengeksekusi B3.\n";
    else
        cout << "   Contoh x = " << contohX << "\n";

    cout << "\n3) Jalur yang LAYAK pada CFG tersebut\n";
    cout << "   P1: B1->B2(true)->B3(false)->B4   (x > 10, x >= 5)\n";
    cout << "   P2: B1->B2(false)->B4             (x <= 10)\n";
    cout << "   P3: B1->B2(true)->B3(true)->...   (TIDAK LAYAK)\n";

    cout << "\n4) Implikasi pengujian\n";
    cout << "   - Jangan buang waktu mencari input untuk P3.\n";
    cout << "   - Dokumentasikan P3 sebagai infeasible beserta alasannya.\n";
    cout << "   - Perbaiki struktur kondisi bila memang ada maksud logika lain\n";
    cout << "     (mis. x > 10 && x < 5 kemungkinan salah tulis).\n";
    return 0;
}
