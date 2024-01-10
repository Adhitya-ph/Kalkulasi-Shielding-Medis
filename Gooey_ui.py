from gooey import Gooey, GooeyParser
from math import log10 as log

@Gooey(program_name="Program Kalkulasi Shielding", navigation="TABBED", show_success_modal=False, clear_before_run=True)
def main():
    parser = GooeyParser(description="Program yang mengkalkulasi ketebalan beton yang diperlukan dari fasilitas medis")
    wajib = parser.add_argument_group('Parameter yang harus diisi (Desimal dalam format titik ".")', gooey_options={'show_border': True})
    
    wajib.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    wajib.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari LINAC")
    wajib.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    wajib.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    wajib.add_argument("pilvLinac", choices=["4 MV", "6 MV", "10 MV", "15 MV", "18 MV", "20 MV", "24 MV"], help="Pilih tegangan LINAC dari opsi yang tersedia", metavar="Tegangan LINAC")
    
    jmlPasien = parser.add_argument_group("Jumlah pasien", gooey_options={'show_border': True}) 
    jmlPasien.add_argument("--jp_3DCRT", action="store", default=0, help="Rerata pasien untuk 3DCRT dalam sehari (8 jam kerja)", metavar="Pasien 3DCRT")
    jmlPasien.add_argument("--jp_IMRT", action="store", default=0, help="Rerata pasien untuk IMRT dalam sehari (8 jam kerja)", metavar="Pasien IMRT")
    jmlPasien.add_argument("--jp_SRS_SBRT", action="store", default=0, help="Rerata pasien untuk SRS/SBRT dalam sehari (8 jam kerja)", metavar="Pasien SRS/SBRT")
    jmlPasien.add_argument("--jp_RapidArc", action="store", default=0, help="Rerata pasien untuk RapidArc dalam sehari (8 jam kerja)", metavar="Pasien RapidArc")
    jmlPasien.add_argument("--jp_QA", action="store", default=0, help="Rerata beam untuk QA dalam sehari (8 jam kerja)", metavar="Pasien QA")
    
    args = parser.parse_args()
    
    jp_3DCRT = float(args.jp_3DCRT)
    dp_3DCRT = 4.0 
    jp_IMRT = float(args.jp_IMRT)
    dp_IMRT = 4.0
    jp_SRS_SBRT = float(args.jp_SRS_SBRT)
    dp_srs_sbrt = 4.0
    jp_RapidArc = float(args.jp_RapidArc)
    dp_RapidArc = 4.0
    jp_QA = float(args.jp_QA)
    dp_QA = 6.0
    
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
    W = (jp_3DCRT * dp_3DCRT * 5) + (jp_IMRT * dp_IMRT * 5) + (jp_SRS_SBRT * dp_srs_sbrt * 5) + (jp_RapidArc * dp_RapidArc * 5) + (jp_QA * dp_QA * 5)
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("------------------------------------------------------")
    print("Atenuasi B = %g" %B)
    
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
    print("------------------------------------------------------\n")

if __name__ == "__main__":
    main()