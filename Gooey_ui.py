from gooey import Gooey, GooeyParser
from math import log10 as log

@Gooey(program_name="Program Kalkulasi Shielding", navigation="TABBED")
def main():
    parser = GooeyParser(description="Program yang mengkalkulasi ketebalan beton yang diperlukan dari fasilitas medis")
    
    group = parser.add_mutually_exclusive_group("selection")
    group.add_argument("--Shielding_Pegawai", action="store_true", help="Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa")
    group.add_argument("--Shielding_Publik", action="store_true", help="Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa")
                    
    parser.add_argument("jumlahPasien", action="store", help="Jumlah pasien dalam sehari (8 jam kerja)", metavar="Jumlah Pasien")
    parser.add_argument("dosisPasien", action="store", help="Dosis yang diterima tiap pasien (Gy)", metavar="Dosis Pasien")
    parser.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari(m)", metavar="Jarak dari LINAC")
    parser.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    parser.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)", metavar="Occupancy Factor")
    
    args = parser.parse_args()
    
    jumlahPasien = float(args.jumlahPasien)
    dosisPasien = float(args.dosisPasien)
    dc = float(args.dc)
    U = float(args.U)
    
    pilihan_1 = args.Shielding_Pegawai
    pilihan_2 = args.Shielding_Publik
    
    if pilihan_1:
        T = 1.0
        P = float(400e-6) / 2      # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif pilihan_2:
        T = float(args.T)
        P = float(20e-6) / 2       # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    
    SAD = 1             # Jarak dari sumber ke isosentris (SAD) (m)
    W = jumlahPasien * 5 * dosisPasien
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("\nAtenuasi B = %g" %B)
    

    n = log(1/B)
    print("\nTenth Value Layer (TVL) yang diperlukan =", n)
    tvl = 218
    l = n * tvl / 10
    print("Ketebalan beton yang diperlukan = %g cm" %l)

if __name__ == "__main__":
    main()