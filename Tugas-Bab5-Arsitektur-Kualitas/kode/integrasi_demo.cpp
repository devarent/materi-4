// =====================================================================
// integrasi_demo.cpp
// ---------------------------------------------------------------------
// Demonstrasi Soal 5, 6, dan 7:
//   - dua unit lulus Unit Testing secara terpisah;
//   - integrasi langsung gagal karena ketidakcocokan satuan (meter vs cm);
//   - adapter meter -> cm memperbaiki integrasi;
//   - stub membuat Top-Down "lulus semu" bila stub tidak realistis.
//
// Kompilasi:
//   g++ -std=c++17 -Wall -Wextra -O0 -o build/integrasi_demo integrasi_demo.cpp
// Jalankan:
//   ./build/integrasi_demo
// =====================================================================
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

// --- Modul bawah: sensor jarak, satuan meter -------------------------
class SensorJarak {
public:
    double bacaMeter() const { return 1.25; }
};

// --- Modul atas: layar, satuan sentimeter ----------------------------
class Layar {
public:
    string tampilkan(double cm) const {
        ostringstream oss;
        oss << fixed << setprecision(2) << cm << " cm";
        return oss.str();
    }
};

// --- Adapter: menyelaraskan satuan antar antarmuka -------------------
double meterKeCm(double meter) { return meter * 100.0; }

// --- Stub untuk simulasi Top-Down ------------------------------------
double stubSensorCm() { return 125.0; }

bool hampirSama(double a, double b) { return fabs(a - b) < 1e-9; }

int main() {
    SensorJarak sensor;
    Layar layar;

    const double meter = sensor.bacaMeter();
    const double cm = meterKeCm(meter);
    const string harapan = "125.00 cm";

    cout << "==============================================================\n";
    cout << "DEMO UNIT TEST vs INTEGRATION TEST\n";
    cout << "==============================================================\n";
    cout << "SensorJarak mengirim data dalam METER.\n";
    cout << "Layar membaca data dalam SENTIMETER.\n\n";

    cout << left << setw(30) << "Pemeriksaan"
         << setw(18) << "Hasil" << "Status\n";
    cout << string(60, '-') << "\n";

    // Unit test 1: sensor dalam isolasi
    bool unitSensor = hampirSama(meter, 1.25);
    cout << left << setw(30) << "Unit SensorJarak"
         << setw(18) << (to_string(meter).substr(0, 4) + " m")
         << (unitSensor ? "LULUS" : "GAGAL") << "\n";

    // Unit test 2: layar dalam isolasi
    bool unitLayar = (layar.tampilkan(125.0) == harapan);
    cout << left << setw(30) << "Unit Layar(125.0)"
         << setw(18) << layar.tampilkan(125.0)
         << (unitLayar ? "LULUS" : "GAGAL") << "\n";

    // Integrasi tanpa adapter
    const string tanpaAdapter = layar.tampilkan(meter);
    bool integrasiGagal = (tanpaAdapter != harapan);
    cout << left << setw(30) << "Integrasi tanpa adapter"
         << setw(18) << tanpaAdapter
         << (integrasiGagal ? "GAGAL" : "LULUS") << "\n";

    // Integrasi dengan adapter
    const string denganAdapter = layar.tampilkan(cm);
    bool integrasiLulus = (denganAdapter == harapan);
    cout << left << setw(30) << "Integrasi + adapter"
         << setw(18) << denganAdapter
         << (integrasiLulus ? "LULUS" : "GAGAL") << "\n";

    cout << "\nSimulasi Top-Down dengan stub:\n";
    cout << "  Stub mengembalikan " << stubSensorCm() << " cm -> "
         << layar.tampilkan(stubSensorCm()) << " -> LULUS SEMU\n";
    cout << "  Stub yang tidak realistis menyembunyikan cacat satuan.\n";

    cout << "\nKesimpulan:\n";
    cout << "  1. Unit SensorJarak LULUS dan unit Layar LULUS.\n";
    cout << "  2. Integrasi tanpa adapter GAGAL: 1.25 m dibaca menjadi 1.25 cm.\n";
    cout << "  3. Adapter meter->cm membuat integrasi LULUS.\n";
    cout << "  4. Inilah cacat antarmuka yang tidak ditemukan Unit Testing.\n";
    return 0;
}
