// =====================================================================
// Soal 9 - Kriteria All-Defs, All-Uses, All-DU-Paths (contoh 1)
// ---------------------------------------------------------------------
// Kode:
//   1  int harga = <input>;        // d1(harga)
//   2  int diskon = 0;             // d2(diskon)
//   3  if (harga > 50000)          // u1(p-use harga)
//   4      diskon = 10;            // d3(diskon), mematikan d2
//   5  int total = harga - diskon;  // u2(c-use harga), u3(c-use diskon), d4(total)
//   6  cout << total;              // u4(c-use total)
//
// Program mencatat peristiwa def/use yang benar-benar terjadi pada satu
// eksekusi. Dengan menjalankan dua harga (100000 dan 30000) seluruh
// definisi dan seluruh pasangan def-use yang layak dapat tercakup.
//
// Kompilasi : g++ -std=c++17 -o build/soal09_kriteria soal09_kriteria.cpp
// Pemakaian : build/soal09_kriteria            (dua kasus uji)
//             build/soal09_kriteria 100000
// =====================================================================
#include <iostream>
#include <set>
#include <string>
#include <cstdlib>

using namespace std;

int main(int argc, char** argv) {
    cout << "=== Soal 9: Kriteria Cakupan Aliran Data ===\n";

    long long daftarHarga[2] = {100000, 30000};
    int jumlahKasus = (argc > 1) ? 1 : 2;

    set<string> peristiwa;
    set<string> pasangan;

    for (int k = 0; k < jumlahKasus; ++k) {
        long long harga = (argc > 1) ? atoll(argv[1]) : daftarHarga[k];
        int diskon = 0;

        cout << "\nKasus uji " << (k + 1) << ": harga = " << harga << "\n";
        cout << "  d1: harga  = " << harga << "\n";
        peristiwa.insert("d1");
        cout << "  d2: diskon = 0\n";
        peristiwa.insert("d2");

        cout << "  u1: p-use harga pada kondisi (harga > 50000) -> ";
        peristiwa.insert("u1");
        if (harga > 50000) {
            cout << "TRUE\n";
            diskon = 10;
            cout << "  d3: diskon = 10 (d2 ditimpa)\n";
            peristiwa.insert("d3");
            pasangan.insert("d3->u3");
        } else {
            cout << "FALSE\n";
            // d2 tetap hidup sampai digunakan di baris total
            pasangan.insert("d2->u3");
        }

        long long total = harga - diskon;
        cout << "  u2: c-use harga -> total = " << harga << " - " << diskon
             << " = " << total << "\n";
        cout << "  u3: c-use diskon (nilai " << diskon << ")\n";
        cout << "  d4: total = " << total << "\n";
        peristiwa.insert("u2");
        peristiwa.insert("u3");
        peristiwa.insert("d4");

        pasangan.insert("d1->u1");
        pasangan.insert("d1->u2");
        pasangan.insert("d4->u4");

        cout << "  u4: c-use total -> " << total << "\n";
        peristiwa.insert("u4");
    }

    cout << "\n--- Rekap ---\n";
    cout << "Peristiwa tercakup : ";
    for (const auto& p : peristiwa) cout << p << " ";
    cout << "\nPasangan def-use  : ";
    for (const auto& p : pasangan) cout << p << " ";
    cout << "\n\nCakupan All-Defs  : d1, d2, d3, d4 masing-masing mencapai use\n";
    cout << "Cakupan All-Uses  : 5 pasangan layak -> butuh 2 kasus uji\n";
    cout << "All-DU-Paths      : d1->u2 memiliki 2 jalur berbeda (true/false)\n";
    return 0;
}
