from gooey import Gooey, GooeyParser
from math import sqrt, log10 as log

def linac(P, dc, U, T, pilvLinac, jp_3DCRT, jp_IMRT, jp_SRS_SBRT, jp_RapidArc, jp_QA):
    SAD = 1                        # Jarak dari sumber ke isosentris (SAD) (m)
    dp_3DCRT = 4.0 
    dp_IMRT = 4.0
    dp_srs_sbrt = 4.0
    dp_RapidArc = 4.0
    dp_QA = 6.0
    W = ((jp_3DCRT * dp_3DCRT) + (jp_IMRT * dp_IMRT) + (jp_SRS_SBRT * dp_srs_sbrt) + (jp_RapidArc * dp_RapidArc) + (jp_QA * dp_QA)) * 5

    if W*SAD**2 * U * T == 0:
        print("Value Error: Pastikan input jumlah pasien sudah benar.")
        return
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("-------------------------------------------------------------------------------------")
    print("Perhitungan Shielding LINAC")
    print("Beban kerja total: %g Gy / minggu" %W)
    print("Atenuasi B = %g" %B)

    n = log(1/B)
    print("\nJumlah Tenth Value Layer (TVL) yang diperlukan = %g" %n)
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
    print("Tebal beton agar intensitas menjadi 10%% intensitas awalnya (Tebal TVL) = %g mm" %tvl)
    l = n * tvl / 10
    print("\nKetebalan beton agar memenuhi batas laju dosis yang ditetapkan = %g cm" %l)
    bw = 0.4 * sqrt(2) * (dc+SAD) + 0.6
    print("Primary Barrier Width = %g m" %bw)
    print("-------------------------------------------------------------------------------------\n")
    
def telecobalt(P, dc, SAD, U, T, jumlahPasien, dosisPasien):
    W = jumlahPasien * dosisPasien * 5
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("-------------------------------------------------------------------------------------")
    print("Perhitungan Shielding Telecobalt")
    print("Atenuasi B = %g" %B)
        
    n = log(1/B)
    print("\nJumlah Tenth Value Layer (TVL) yang diperlukan = %g" %n)
    tvl = 218
    print("Tebal beton agar intensitas menjadi 10%% intensitas awalnya (Tebal TVL) = %g mm" %tvl)
    l = n * tvl / 10
    print("\nKetebalan beton agar memenuhi batas laju dosis yang ditetapkan = %g cm" %l)
    print("-------------------------------------------------------------------------------------\n")

@Gooey(program_name="Program Kalkulasi Shielding", navigation="TABBED", show_success_modal=False, clear_before_run=True, default_size=(700, 600))
def main():
    parser = GooeyParser(description="Program yang mengkalkulasi ketebalan beton yang diperlukan dari fasilitas medis")
    subparsers = parser.add_subparsers(help='commands', dest='command')
    
    # Linac parser
    linac_parser = subparsers.add_parser('LINAC', help='Linac calculation')
    spec_fasilitas = linac_parser.add_argument_group("Spesifikasi Fasilitas LINAC")
    jumlah_pasien = linac_parser.add_argument_group("Jumlah Pasien LINAC")
    
    spec_fasilitas.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    spec_fasilitas.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari LINAC")
    spec_fasilitas.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    spec_fasilitas.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    spec_fasilitas.add_argument("pilvLinac", choices=["4 MV", "6 MV", "10 MV", "15 MV", "18 MV", "20 MV", "24 MV"], help="Pilih tegangan LINAC dari opsi yang tersedia", metavar="Tegangan LINAC")
    
    jumlah_pasien.add_argument("--jp_3DCRT", action="store", default=0, help="Rerata pasien untuk 3DCRT dalam sehari (8 jam kerja)", metavar="Pasien 3DCRT")
    jumlah_pasien.add_argument("--jp_IMRT", action="store", default=0, help="Rerata pasien untuk IMRT dalam sehari (8 jam kerja)", metavar="Pasien IMRT")
    jumlah_pasien.add_argument("--jp_SRS_SBRT", action="store", default=0, help="Rerata pasien untuk SRS/SBRT dalam sehari (8 jam kerja)", metavar="Pasien SRS/SBRT")
    jumlah_pasien.add_argument("--jp_RapidArc", action="store", default=0, help="Rerata pasien untuk RapidArc dalam sehari (8 jam kerja)", metavar="Pasien RapidArc")
    jumlah_pasien.add_argument("--jp_QA", action="store", default=0, help="Rerata beam untuk QA dalam sehari (8 jam kerja)", metavar="Pasien QA")
    
    telecobalt_parser = subparsers.add_parser('Telecobalt', help='Telecobalt calculation')
    telecobalt_parser.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    telecobalt_parser.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari Telecobalt")
    telecobalt_parser.add_argument("SAD", action="store", help="Jarak dari sumber ke isosentris (m)", metavar="SAD")
    telecobalt_parser.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    telecobalt_parser.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    telecobalt_parser.add_argument("jumlahPasien", action="store", help="Masukkan jumlah pasien per hari (8 jam kerja)", metavar="Jumlah Pasien")
    telecobalt_parser.add_argument("dosisPasien", action="store", default=3, help="Masukkan jumlah dosis per pasien (Gy)", metavar="Dosis Pasien")
    
    args = parser.parse_args()
    
    pengguna = args.Pengguna
    dc = float(args.dc)
    U = float(args.U)
    T = float(args.T)
    if pengguna == "Shielding Petugas Radiasi":
        T = 1.0
        P = float(400e-6) / 2      # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif pengguna == "Shielding Publik":
        T = float(args.T)
        P = float(20e-6) / 2       # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    
    if args.command == 'LINAC':
        # Call linac function
        pilvLinac = args.pilvLinac
        jp_3DCRT = float(args.jp_3DCRT)
        jp_IMRT = float(args.jp_IMRT)
        jp_SRS_SBRT = float(args.jp_SRS_SBRT)
        jp_RapidArc = float(args.jp_RapidArc)
        jp_QA = float(args.jp_QA)
        
        linac(P, dc, U, T, pilvLinac, jp_3DCRT, jp_IMRT, jp_SRS_SBRT, jp_RapidArc, jp_QA)
        
    elif args.command == 'Telecobalt':
        # Call telecobalt function
        SAD = float(args.SAD)
        jumlahPasien = float(args.jumlahPasien)
        dosisPasien = float(args.dosisPasien)
        
        telecobalt(P, dc, SAD, U, T, jumlahPasien, dosisPasien)
    
if __name__ == "__main__":
    main()