// =====================================================================
// Soal 3 - Statement Coverage dan Branch Coverage
// ---------------------------------------------------------------------
// Kode yang diuji (4 pernyataan, 1 keputusan):
//   S1: int nilai = <input>;
//   S2: if (nilai >= 60)
//   S3:     cout << "Lulus";
//   S4: else cout << "Tidak lulus";
//
// Program ini melakukan instrumentasi manual: setiap pernyataan yang
// dieksekusi dan setiap arah cabang (true/false) dicatat, lalu
// persentase cakupan dihitung dan dicetak.
//
// Kompilasi : g++ -std=c++17 -o build/soal03_coverage soal03_coverage.cpp
// Pemakaian : build/soal03_coverage            (skenario: hanya input 80)
//             build/soal03_coverage 80 40      (skenario: dua input)
// =====================================================================
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>

using namespace std;

struct Cakupan {
    bool S[4] = {false, false, false, false};  // S1..S4
    bool cabangTrue  = false;
    bool cabangFalse = false;
};

// Menjalankan kode yang diuji dengan satu nilai input.
// Parameter "cetakJejak" hanya mengatur output, bukan pencatatan cakupan.
static void jalankan(int nilai, Cakupan& c, bool cetakJejak) {
    c.S[0] = true;                       // S1 dieksekusi
    if (cetakJejak) cout << "  S1  nilai = " << nilai << "\n";

    c.S[1] = true;                       // S2: kondisi dievaluasi
    if (nilai >= 60) {                   // cabang TRUE
        c.cabangTrue = true;
        c.S[2] = true;                   // S3 dieksekusi
        if (cetakJejak) cout << "  S2  (true)  -> S3  cout << \"Lulus\"\n";
        cout << "Lulus\n";
    } else {                             // cabang FALSE
        c.cabangFalse = true;
        c.S[3] = true;                   // S4 dieksekusi
        if (cetakJejak) cout << "  S2  (false) -> S4  cout << \"Tidak lulus\"\n";
        cout << "Tidak lulus\n";
    }
}

static void cetakMatriks(const Cakupan& c) {
    const char* nama[4] = {"nilai = <input>", "if (nilai >= 60)",
                           "cout << \"Lulus\"", "cout << \"Tidak lulus\""};
    cout << "\n  Matriks cakupan pernyataan:\n";
    cout << "  +----+------------------------+------------+\n";
    cout << "  | " << left << setw(2) << "ID" << " | " << setw(22) << "Pernyataan"
         << " | " << setw(10) << "Dieksekusi" << " |\n";
    cout << "  +----+------------------------+------------+\n";
    for (int i = 0; i < 4; ++i) {
        cout << "  | " << left << setw(2) << ("S" + to_string(i + 1)) << " | "
             << setw(22) << nama[i] << " | " << setw(10)
             << (c.S[i] ? "YA" : "TIDAK") << " |\n";
    }
    cout << "  +----+------------------------+------------+\n";

    int jmlPernyataan = 0;
    for (int i = 0; i < 4; ++i) if (c.S[i]) ++jmlPernyataan;
    int jmlCabang = (c.cabangTrue ? 1 : 0) + (c.cabangFalse ? 1 : 0);

    cout << fixed << setprecision(1);
    cout << "  Statement coverage = " << jmlPernyataan << "/4 = "
         << (jmlPernyataan * 100.0 / 4.0) << "%\n";
    cout << "  Branch coverage    = " << jmlCabang << "/2 = "
         << (jmlCabang * 100.0 / 2.0) << "%\n";
    cout << "  Cabang true  : " << (c.cabangTrue ? "tercakup" : "BELUM tercakup") << "\n";
    cout << "  Cabang false : " << (c.cabangFalse ? "tercakup" : "BELUM tercakup") << "\n";
}

int main(int argc, char** argv) {
    cout << "=== Soal 3: Statement & Branch Coverage ===\n";

    if (argc > 2) {
        // Skenario lengkap: dua kasus uji (mis. 80 dan 40)
        vector<int> kasus;
        for (int i = 1; i < argc; ++i) kasus.push_back(atoi(argv[i]));

        Cakupan total;
        for (size_t i = 0; i < kasus.size(); ++i) {
            cout << "\nKasus uji " << (i + 1) << " (nilai = " << kasus[i] << "):\n";
            jalankan(kasus[i], total, true);
        }
        cout << "\n--- Rekap seluruh kasus uji ---";
        cetakMatriks(total);
    } else {
        // Skenario soal: penguji hanya memakai nilai 80 (atau nilai dari argumen)
        int nilai = (argc == 2) ? atoi(argv[1]) : 80;
        cout << "\nKasus uji tunggal (nilai = " << nilai << "):\n";
        Cakupan c;
        jalankan(nilai, c, true);
        cetakMatriks(c);
        cout << "\nKesimpulan: cakupan belum 100%, perlu kasus uji tambahan "
                "dengan nilai < 60 (mis. 40).\n";
    }
    return 0;
}
