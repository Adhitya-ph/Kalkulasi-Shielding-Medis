from gooey import Gooey, GooeyParser
from math import log10 as log

@Gooey(program_name="Program Kalkulasi Shielding", navigation="TABBED")
def main():
    parser = GooeyParser(description="Program yang mengkalkulasi ketebalan beton yang diperlukan dari fasilitas medis")
    parser.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    parser.add_argument("jumlahPasien", action="store", help="Jumlah pasien dalam sehari (8 jam kerja)", metavar="Jumlah Pasien")
    parser.add_argument("dosisPasien", action="store", help="Dosis yang diterima tiap pasien (Gy)", metavar="Dosis Pasien")
    parser.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari LINAC")
    parser.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    parser.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    parser.add_argument("pilvLinac", choices=["4 MV", "6 MV", "10 MV", "15 MV", "18 MV", "20 MV", "24 MV"], help="Pilih tegangan LINAC", metavar="Tegangan LINAC")
    
    args = parser.parse_args()
    
    jumlahPasien = float(args.jumlahPasien)
    dosisPasien = float(args.dosisPasien)
    dc = float(args.dc)
    U = float(args.U)
    pilvLinac = args.pilvLinac
    pengguna = args.Pengguna
    
    if pengguna == "Shielding Petugas Radiasi":
        T = 1.0
        P = float(400e-6) / 2      # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif pengguna == "Shielding Publik":
        T = float(args.T)
        P = float(20e-6) / 2       # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    
    SAD = 1             # Jarak dari sumber ke isosentris (SAD) (m)
    W = jumlahPasien * 5 * dosisPasien
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("\nAtenuasi B = %g" %B)
    
    n = log(1/B)
    print("Tenth Value Layer (TVL) yang diperlukan =", n)
    if pilvLinac == "4 MV":
        tvl = 290
        print("\nBesar tegangan LINAC: 4 MV")
    if pilvLinac == "6 MV":
        tvl = 343
        print("\nBesar tegangan LINAC: 6 MV")
    if pilvLinac == "10 MV":
        tvl = 389
        print("\nBesar tegangan LINAC: 10 MV")
    if pilvLinac == "15 MV":
        tvl = 432
        print("\nBesar tegangan LINAC: 15 MV")
    if pilvLinac == "18 MV":
        tvl = 445
        print("\nBesar tegangan LINAC: 18 MV")
    if pilvLinac == "20 MV":
        tvl = 457
        print("\nBesar tegangan LINAC: 20 MV")
    if pilvLinac == "24 MV":
        tvl = 470
        print("\nBesar tegangan LINAC: 24 MV")
    l = n * tvl / 10
    print("Ketebalan beton yang diperlukan = %g cm" %l)

if __name__ == "__main__":
    main()