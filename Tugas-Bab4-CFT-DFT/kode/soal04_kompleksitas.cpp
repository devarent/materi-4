// =====================================================================
// Soal 4 - Kompleksitas Siklomatis (Cyclomatic Complexity)
// ---------------------------------------------------------------------
// Menghitung V(G) dengan tiga rumus yang ekuivalen untuk CFG terhubung:
//   1. V(G) = E - N + 2
//   2. V(G) = P + 1            (P = jumlah predicate / titik keputusan)
//   3. V(G) = jumlah region    (bidang tertutup + 1 bidang luar)
//
// Program juga memverifikasi hasil untuk dua CFG lain yang dipakai
// dalam jawaban (Soal 2 dan Soal 10) sebagai pembanding.
//
// Kompilasi : g++ -std=c++17 -o build/soal04_kompleksitas soal04_kompleksitas.cpp
// Pemakaian : build/soal04_kompleksitas
// =====================================================================
#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct Cfg {
    string nama;
    int jumlahSimpul;
    int jumlahSisi;
    int jumlahPredikat;
    int jumlahRegion;
};

static void analisis(const Cfg& g) {
    int vRumus1 = g.jumlahSisi - g.jumlahSimpul + 2;
    int vRumus2 = g.jumlahPredikat + 1;

    cout << "\nCFG: " << g.nama << "\n";
    cout << "  N (simpul)            = " << g.jumlahSimpul << "\n";
    cout << "  E (sisi)              = " << g.jumlahSisi << "\n";
    cout << "  P (predikat)          = " << g.jumlahPredikat << "\n";
    cout << "  Region (bidang)       = " << g.jumlahRegion << "\n";
    cout << "  V(G) = E - N + 2      = " << g.jumlahSisi << " - "
         << g.jumlahSimpul << " + 2 = " << vRumus1 << "\n";
    cout << "  V(G) = P + 1          = " << g.jumlahPredikat << " + 1 = "
         << vRumus2 << "\n";
    cout << "  V(G) = jumlah region  = " << g.jumlahRegion << "\n";
    cout << "  Konsisten             : "
         << ((vRumus1 == vRumus2 && vRumus2 == g.jumlahRegion) ? "YA" : "TIDAK")
         << "\n";
    cout << "  Arti: " << vRumus1
         << " jalur independen -> minimal " << vRumus1
         << " kasus uji untuk basis path testing.\n";
}

int main() {
    cout << "=== Soal 4: Kompleksitas Siklomatis ===\n";

    // Kasus utama dari soal: E = 10, N = 9, graf terhubung (1 komponen).
    // CFG dengan 2 keputusan (P = 2) dan 3 region.
    Cfg kasusSoal{"Kasus soal (E=10, N=9)", 9, 10, 2, 3};

    // CFG Soal 2: 6 simpul, 6 sisi, 1 keputusan, 2 region.
    Cfg cfgSoal2{"CFG Soal 2 (if-else + merge)", 6, 6, 1, 2};

    // CFG Soal 10: 8 simpul, 9 sisi, 2 keputusan, 3 region.
    Cfg cfgSoal10{"CFG Soal 10 (KRS, dua if berurutan)", 8, 9, 2, 3};

    analisis(kasusSoal);
    analisis(cfgSoal2);
    analisis(cfgSoal10);

    cout << "\nCatatan: V(G) adalah batas atas jumlah jalur independen.\n";
    cout << "Jika ada jalur tak layak (infeasible), jumlah kasus uji yang\n";
    cout << "benar-benar dapat dijalankan bisa lebih kecil dari V(G).\n";
    return 0;
}
