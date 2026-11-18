# =====================================================================
# jalankan_semua.ps1
# ---------------------------------------------------------------------
# Mengompilasi seluruh program C++ jawaban, menjalankan setiap skenario
# uji, menyimpan keluaran ke folder hasil/, lalu menjalankan skrip
# verifikasi Python (CFG, V(G), cakupan, DU-path).
#
# Pemakaian (dari folder kode/):
#   powershell -ExecutionPolicy Bypass -File .\jalankan_semua.ps1
# =====================================================================
$ErrorActionPreference = "Stop"

$root   = Split-Path -Parent $MyInvocation.MyCommand.Path
$build  = Join-Path $root "build"
$hasil  = Join-Path $root "hasil"
$gpp    = "g++"

New-Item -ItemType Directory -Force -Path $build, $hasil | Out-Null

$daftar = @(
    @{ nama = "soal02_nilai";        src = "soal02_nilai.cpp" },
    @{ nama = "soal03_coverage";     src = "soal03_coverage.cpp" },
    @{ nama = "soal04_kompleksitas"; src = "soal04_kompleksitas.cpp" },
    @{ nama = "soal05_infeasible";   src = "soal05_infeasible.cpp" },
    @{ nama = "soal06_diskon";       src = "soal06_diskon.cpp" },
    @{ nama = "soal08_aliran_data";  src = "soal08_aliran_data.cpp" },
    @{ nama = "soal09_kriteria";     src = "soal09_kriteria.cpp" },
    @{ nama = "soal10_krs";          src = "soal10_krs.cpp" }
)

Write-Host "=== 1. Kompilasi ===" -ForegroundColor Cyan
$logKompilasi = @()
foreach ($p in $daftar) {
    $exe = Join-Path $build ($p.nama + ".exe")
    $out = & $gpp -std=c++17 -Wall -Wextra -O0 -o $exe (Join-Path $root $p.src) 2>&1
    if ($LASTEXITCODE -ne 0) {
        $out | ForEach-Object { Write-Host $_ -ForegroundColor Red }
        throw "Kompilasi gagal: $($p.src)"
    }
    $pesan = if ($out) { ($out -join "`n") } else { "OK (tanpa peringatan)" }
    Write-Host ("  [OK] {0,-24} {1}" -f $p.src, $pesan)
    $logKompilasi += ("{0,-24} : {1}" -f $p.src, $pesan)
}

# Menjalankan satu program dan menyimpan keluarannya ke hasil/<nama>.txt
function Jalankan-Skenario {
    param(
        [string]$NamaFile,
        [string]$Exe,
        [string[]]$Argumen = @()
    )
    $jalurExe = Join-Path $build ($Exe + ".exe")
    $keluaran = & $jalurExe @Argumen 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "Program $Exe keluar dengan kode $LASTEXITCODE" }
    $tujuan = Join-Path $hasil ($NamaFile + ".txt")
    Set-Content -Path $tujuan -Value $keluaran -Encoding utf8
    Write-Host ("  -> hasil\{0}.txt" -f $NamaFile)
    return $keluaran
}

Write-Host "`n=== 2. Eksekusi skenario uji ===" -ForegroundColor Cyan
$skenario = [ordered]@{}
$skenario["soal02_input_75"]      = Jalankan-Skenario "soal02_input_75" "soal02_nilai" @("75")
$skenario["soal02_input_50"]      = Jalankan-Skenario "soal02_input_50" "soal02_nilai" @("50")
$skenario["soal03_satu_kasus_80"] = Jalankan-Skenario "soal03_satu_kasus_80" "soal03_coverage" @("80")
$skenario["soal03_dua_kasus"]     = Jalankan-Skenario "soal03_dua_kasus" "soal03_coverage" @("80", "40")
$skenario["soal04_kompleksitas"]  = Jalankan-Skenario "soal04_kompleksitas" "soal04_kompleksitas"
$skenario["soal05_infeasible"]    = Jalankan-Skenario "soal05_infeasible" "soal05_infeasible"
$skenario["soal06_tabel_batas"]   = Jalankan-Skenario "soal06_tabel_batas" "soal06_diskon"
$skenario["soal08_aliran_data"]   = Jalankan-Skenario "soal08_aliran_data" "soal08_aliran_data"
$skenario["soal09_dua_kasus"]     = Jalankan-Skenario "soal09_dua_kasus" "soal09_kriteria"
$skenario["soal10_asli"]          = Jalankan-Skenario "soal10_asli" "soal10_krs"
$skenario["soal10_status_1"]      = Jalankan-Skenario "soal10_status_1" "soal10_krs" @("1")
$skenario["soal10_status_0"]      = Jalankan-Skenario "soal10_status_0" "soal10_krs" @("0")

Write-Host "`n=== 3. Verifikasi Python (CFG / cakupan / aliran data) ===" -ForegroundColor Cyan
$alat = Join-Path $root "alat\verifikasi_tugas.py"
& python $alat
if ($LASTEXITCODE -ne 0) { throw "Verifikasi Python gagal" }
$verifikasi = Get-Content -Path (Join-Path $hasil "laporan_verifikasi.txt") -Raw

Write-Host "`n=== 4. Menyusun laporan eksekusi lengkap ===" -ForegroundColor Cyan
$laporan = @()
$laporan += "LAPORAN EKSEKUSI DAN VERIFIKASI"
$laporan += "Tugas Bab 4 - Software Structural Testing (CFT & DFT)"
$laporan += "Dihasilkan otomatis oleh kode/jalankan_semua.ps1"
$laporan += ("Tanggal: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
$laporan += ""
$laporan += "1. KOMPILASI (g++ -std=c++17 -Wall -Wextra)"
$laporan += "---------------------------------------------------------------"
$laporan += $logKompilasi
$laporan += ""
$laporan += "2. KELUARAN SETIAP SKENARIO UJI"
$laporan += "---------------------------------------------------------------"
foreach ($k in $skenario.Keys) {
    $laporan += ""
    $laporan += ("### " + $k)
    $laporan += $skenario[$k].TrimEnd()
}
$laporan += ""
$laporan += "3. VERIFIKASI MODEL CFG, CAKUPAN, DAN ALIRAN DATA"
$laporan += "---------------------------------------------------------------"
$laporan += $verifikasi
$tujuanLaporan = Join-Path $hasil "laporan_eksekusi.txt"
Set-Content -Path $tujuanLaporan -Value ($laporan -join "`r`n") -Encoding utf8

Write-Host "`nSelesai. Laporan lengkap: $tujuanLaporan" -ForegroundColor Green
