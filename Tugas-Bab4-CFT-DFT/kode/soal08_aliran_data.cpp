// =====================================================================
// Soal 8 - Anomali Aliran Data (dead assignment / DDU)
// ---------------------------------------------------------------------
// Kode:
//   int nilai;      // deklarasi (belum ada nilai)
//   nilai = 70;     // d1  (definisi pertama)
//   nilai = 85;     // d2  (definisi ulang tanpa membaca d1)
//   cout << nilai;  // u1  (penggunaan)
//
// Program mencetak jejak peristiwa def/use dan hasil keluaran, sehingga
// terlihat bahwa nilai 70 tidak pernah digunakan (dead assignment).
//
// Kompilasi : g++ -std=c++17 -o build/soal08_aliran_data soal08_aliran_data.cpp
// Pemakaian : build/soal08_aliran_data
// =====================================================================
#include <iostream>
#include <string>

using namespace std;

int main() {
    cout << "=== Soal 8: Anomali Aliran Data ===\n";

    cout << "\nJejak peristiwa data:\n";

    // Deklarasi tanpa inisialisasi: belum ada definisi yang bernilai.
    int nilai;
    cout << "  [1] deklarasi  : int nilai;            (belum ada nilai)\n";

    nilai = 70;
    cout << "  [2] definisi   : nilai = 70            (d1)\n";

    nilai = 85;
    cout << "  [3] definisi   : nilai = 85            (d2, d1 ditimpa)\n";

    cout << "  [4] penggunaan : cout << nilai         (u1 membaca d2)\n";
    cout << "\nKeluaran program: " << nilai << "\n";

    cout << "\nAnalisis:\n";
    cout << "  - Nilai yang ditampilkan adalah 85 (definisi terakhir sebelum use).\n";
    cout << "  - Nilai 70 adalah dead assignment: didefinisikan lalu langsung\n";
    cout << "    ditimpa tanpa pernah dibaca -> anomali DDU (Definisi-Definisi-\n";
    cout << "    Penggunaan) / definisi tanpa penggunaan.\n";
    cout << "  - Pasangan def-use yang sah: (d2, u1). Pasangan (d1, u1) TIDAK ADA\n";
    cout << "    karena d1 sudah di-kill oleh d2.\n";
    cout << "  - Pada kode asli tanpa inisialisasi, bila d1 dan d2 dihapus maka u1\n";
    cout << "    menjadi use-before-def (nilai tak terdefinisi) -> bug.\n";
    return 0;
}
