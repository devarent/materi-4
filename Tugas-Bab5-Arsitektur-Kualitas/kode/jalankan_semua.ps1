# =====================================================================
# jalankan_semua.ps1
# ---------------------------------------------------------------------
# Mengompilasi dua program demo Tugas Bab 5, menjalankan skenarionya,
# menjalankan verifikasi Python, lalu menyusun laporan eksekusi.
#
# Pemakaian (dari folder kode/):
#   powershell -ExecutionPolicy Bypass -File .\jalankan_semua.ps1
# =====================================================================
$ErrorActionPreference = "Stop"

$root  = Split-Path -Parent $MyInvocation.MyCommand.Path
$build = Join-Path $root "build"
$hasil = Join-Path $root "hasil"
$gpp   = "g++"

New-Item -ItemType Directory -Force -Path $build, $hasil | Out-Null

$daftar = @(
    @{ nama = "domain_demo";    src = "domain_demo.cpp" },
    @{ nama = "integrasi_demo"; src = "integrasi_demo.cpp" }
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
    Write-Host ("  [OK] {0,-20} {1}" -f $p.src, $pesan)
    $logKompilasi += ("{0,-20} : {1}" -f $p.src, $pesan)
}

function Jalankan-Skenario {
    param([string]$NamaFile, [string]$Exe)
    $jalurExe = Join-Path $build ($Exe + ".exe")
    $keluaran = & $jalurExe 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "Program $Exe keluar dengan kode $LASTEXITCODE" }
    $tujuan = Join-Path $hasil ($NamaFile + ".txt")
    Set-Content -Path $tujuan -Value $keluaran -Encoding utf8
    Write-Host ("  -> hasil\{0}.txt" -f $NamaFile)
    return $keluaran
}

Write-Host "`n=== 2. Eksekusi demo ===" -ForegroundColor Cyan
$skenario = [ordered]@{}
$skenario["domain_demo"]    = Jalankan-Skenario "domain_demo" "domain_demo"
$skenario["integrasi_demo"] = Jalankan-Skenario "integrasi_demo" "integrasi_demo"

Write-Host "`n=== 3. Verifikasi Python ===" -ForegroundColor Cyan
$alat = Join-Path $root "alat\verifikasi_tugas.py"
$verifikasi = & python $alat 2>&1 | Out-String
if ($LASTEXITCODE -ne 0) { throw "Verifikasi Python gagal" }
$verifikasi | Write-Host
Set-Content -Path (Join-Path $hasil "laporan_verifikasi.txt") -Value $verifikasi -Encoding utf8

Write-Host "`n=== 4. Menyusun laporan eksekusi lengkap ===" -ForegroundColor Cyan
$laporan = @()
$laporan += "LAPORAN EKSEKUSI DAN VERIFIKASI"
$laporan += "Tugas Bab 5 - Arsitektur Kualitas Perangkat Lunak"
$laporan += "Domain Testing & System Integration Testing"
$laporan += "Dihasilkan otomatis oleh kode/jalankan_semua.ps1"
$laporan += ("Tanggal: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
$laporan += ""
$laporan += "1. KOMPILASI (g++ -std=c++17 -Wall -Wextra)"
$laporan += "---------------------------------------------------------------"
$laporan += $logKompilasi
$laporan += ""
$laporan += "2. KELUARAN SETIAP DEMO"
$laporan += "---------------------------------------------------------------"
foreach ($k in $skenario.Keys) {
    $laporan += ""
    $laporan += ("### " + $k)
    $laporan += $skenario[$k].TrimEnd()
}
$laporan += ""
$laporan += "3. VERIFIKASI ANGKA"
$laporan += "---------------------------------------------------------------"
$laporan += $verifikasi.TrimEnd()
$tujuanLaporan = Join-Path $hasil "laporan_eksekusi.txt"
Set-Content -Path $tujuanLaporan -Value ($laporan -join "`r`n") -Encoding utf8

Write-Host "`nSelesai. Laporan lengkap: $tujuanLaporan" -ForegroundColor Green
