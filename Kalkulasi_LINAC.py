from gooey import Gooey, GooeyParser
from math import sqrt, log10 as log

def linac_prim(P, pilvLinac, dc, U, T, dn, jp_3DCRT, jp_IMRT, jp_SRS_SBRT, jp_RapidArc, jp_QA):
    dsca = 1                        # Jarak dari sumber ke isosentris (Dsca) (m)
    dp_3DCRT = 4.0 
    dp_IMRT = 4.0
    dp_srs_sbrt = 4.0
    dp_RapidArc = 4.0
    dp_QA = 6.0
    W = ((jp_3DCRT * dp_3DCRT) + (jp_IMRT * dp_IMRT) + (jp_SRS_SBRT * dp_srs_sbrt) + (jp_RapidArc * dp_RapidArc) + (jp_QA * dp_QA)) * 5

    if W*dsca**2 * U * T == 0:
        print("Value Error: Pastikan input jumlah pasien sudah benar.")
        return
    B = P * (dc+dsca)**2 / ((W*dsca**2) * U * T)
    print("---------------------------------------------------------------------------------------------------------")
    print("Perhitungan Shielding LINAC")
    print("\nBesar tegangan LINAC: 6 MV")
    print("\nBeban kerja total (primer): %g Gy / minggu" %W)

    n = log(1/B)
    
    if pilvLinac == "6 MV":
        print("\nBesar tegangan LINAC: 6 MV")
        tvl = 343
    elif pilvLinac == "10 MV":
        print("\nBesar tegangan LINAC: 10 MV")
        tvl = 389
    
    l = n * tvl / 10
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (primary barrier) = %g cm" %l)
    
    bw = 0.4 * sqrt(2) * (dn) + 0.6
    print("Primary Barrier Width = %g m" %bw)
    print("---------------------------------------------------------------------------------------------------------\n")
    
def linac_sec(P, pilvLinac, W, W_leak, U, T, dsca, dsec, dw, dr, ds, F, A, angle):
    print("---------------------------------------------------------------------------------------------------------")
        
    if pilvLinac == "6 MV":
        print("\nBesar tegangan LINAC: 6 MV")
        tvl = 343
        tvl_leak = 279
        if angle == 30:
            alpha = 2.77e-3
            tvl_scatter = 261
        elif angle == 45:
            alpha = 1.39e-3
            tvl_scatter = 229
        elif angle == 60:
            alpha = 8.24e-4
            tvl_scatter = 205
        elif angle == 90:
            alpha = 4.26e-4
            tvl_scatter = 171
        elif angle == 135:
            alpha = 3e-4
            tvl_scatter = 144
    if pilvLinac == "10 MV":
        print("\nBesar tegangan LINAC: 10 MV")
        tvl = 389
        tvl_leak = 305
        if angle == 30:
            alpha = 3.18e-3
            tvl_scatter = 275
        elif angle == 45:
            alpha = 1.35e-3
            tvl_scatter = 233
        elif angle == 60:
            alpha = 7.46e-4
            tvl_scatter = 209
        elif angle == 90:
            alpha = 3.81e-4
            tvl_scatter = 173
        elif angle == 135:
            alpha = 3.02e-4
            tvl_scatter = 144
        
    b_patient= P * dsca**2 * dsec**2 / (alpha * (W*dsca**2) * T * F/400)   # P * (dsca**2 * dsec**2) / (alpha * A * (W) * U * T)    
    n_patient = log(1/b_patient)
    l_patient = n_patient * tvl_scatter / 10
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (patient scatter barrier) = %g cm" %l_patient)
    
    b_wall = P * dw**2 * dr**2 / (alpha * A * (W_leak*dsca**2) * U * T)   # P * (dw**2 * dr**2) / (alpha * A * (W) * U * T)
    n_wall = log(1/b_wall)
    l_wall = n_wall * tvl_scatter / 10
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (wall scatter barrier) = %g cm" %l_wall)
    
    b_leak = 1000 * P * ds**2 / ((W_leak*dsca**2) * T)
    n_leak = log(1/b_leak)
    l_leak = n_leak * tvl_leak / 10
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (leakage barrier) = %g cm" %l_leak)
    print("---------------------------------------------------------------------------------------------------------")

@Gooey(program_name="Program Kalkulasi Shielding",
       navigation="TABBED",
       show_success_modal=False,
       clear_before_run=True,
       default_size=(700, 600),
       image_dir= 'C:/Users/asusf/Downloads',
       header_bg_color = '',
       menu=[{'name': 'Help', 
              'items': [{'type': 'Link', 
                         'menuTitle': 'Panduan Penggunaan',
                         'url': 'https://drive.google.com/file/d/1V7WRIG7CglBrZYNZsrNOPpK_sBzX7gjS/view?usp=sharing'},
                        {'type': 'Link', 
                         'menuTitle': 'Acuan Perhitungan',
                         'url': 'https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1223_web.pdf'}
                        ]},
             {'name': 'About', 
              'items': [{'type': 'MessageDialog', 
                         'menuTitle': 'Informasi Program',
                         'message': 'Kalkulator Shielding Fasilitas Medis\n\nProgram ini dibuat untuk memudahkan petugas dalam menghitung ketebalan shielding yang diperlukan dari fasilitas medis.'
                         '\nProgram ini dibuat menggunakan bahasa Python, dan menggunakan bantuan GUI yaitu library Gooey.'
                         '\n \nProgram ini dibuat oleh:\n- Adhitya Pryazada Hadi\n \nJika ada kritik dan saran terhadap program ini, silahkan hubungi nomor WA:\n0878 5502 0870',
                         'caption': 'Informasi Program'},
                        {'type': 'Link', 
                         'menuTitle': 'Source Code',
                         'url': 'https://github.com/Adhitya-ph/Kalkulasi-Shielding-Medis.git'}
                        ]}]
       )

def main(): 
    parser = GooeyParser(description='Program yang mengkalkulasi ketebalan beton yang diperlukan dari fasilitas medis\nMasukkan parameter yang diperlukan, jika desimal gunakan titik (".")')
    subparsers = parser.add_subparsers(help='commands', dest='command')
    
    # Primary barrier parser
    prim_parser = subparsers.add_parser('Primary_Barrier', help='Primary Barrier Calculation')
    spec_fasilitas = prim_parser.add_argument_group("Spesifikasi Fasilitas LINAC")
    jumlah_pasien = prim_parser.add_argument_group("Jumlah Pasien LINAC")
    
    spec_fasilitas.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    spec_fasilitas.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari LINAC")
    spec_fasilitas.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    spec_fasilitas.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    spec_fasilitas.add_argument("Dn", action="store", help="Masukkan jarak ke dinding primer (barrier width) (m)", metavar="Jarak ke Dinding Primer (Barrier Width)")
    spec_fasilitas.add_argument("pilvLinac", choices=["6 MV", "10 MV"], help="Pilih tegangan LINAC dari opsi yang tersedia", metavar="Tegangan LINAC")
    
    jumlah_pasien.add_argument("--jp_3DCRT", action="store", default=0, help="Rerata pasien untuk 3DCRT dalam sehari (8 jam kerja)", metavar="Pasien 3DCRT")
    jumlah_pasien.add_argument("--jp_IMRT", action="store", default=0, help="Rerata pasien untuk IMRT dalam sehari (8 jam kerja)", metavar="Pasien IMRT")
    jumlah_pasien.add_argument("--jp_SRS_SBRT", action="store", default=0, help="Rerata pasien untuk SRS/SBRT dalam sehari (8 jam kerja)", metavar="Pasien SRS/SBRT")
    jumlah_pasien.add_argument("--jp_RapidArc", action="store", default=0, help="Rerata pasien untuk RapidArc dalam sehari (8 jam kerja)", metavar="Pasien RapidArc")
    jumlah_pasien.add_argument("--jp_QA", action="store", default=0, help="Rerata beam untuk QA dalam sehari (8 jam kerja)", metavar="Pasien QA")
    
    # Secondary barrier parser
    sec_parser = subparsers.add_parser('Secondary_Barrier', help='Secondary Barrier Calculation')
    sec_parser.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    sec_parser.add_argument("pilvLinac", choices=["6 MV", "10 MV"], help="Pilih tegangan LINAC dari opsi yang tersedia", metavar="Tegangan LINAC")
    sec_parser.add_argument("W", action="store", help="Masukkan beban kerja total (Gy/minggu)", metavar="Beban Kerja Total")
    sec_parser.add_argument("W_leak", action="store", help="Masukkan beban kerja leakage (Gy/minggu)", metavar="Beban Kerja Leakage")
    sec_parser.add_argument("dsec", action="store", help="Jarak dari pasien ke titik yang ingin dicari (m)", metavar="Dsec")
    sec_parser.add_argument("dw", action="store", help="Jarak dari LINAC ke dinding sebaran (m)", metavar="Dw")
    sec_parser.add_argument("dr", action="store", help="Jarak dari dinding sebaran ke titik target (m)", metavar="Dr")
    sec_parser.add_argument("dc", action="store", help="Jarak dari isosentris ke titik target (m)", metavar="Dc")
    sec_parser.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    sec_parser.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    sec_parser.add_argument("F", action="store", help="Area kolimator (cm^2)", metavar="Area Kolimator")
    sec_parser.add_argument("A", action="store", help="Area dinding sebaran (wall scattering) (m^2)", metavar="Area Dinding Sebaran")
    sec_parser.add_argument("angle", choices=["30", "45", "60", "90", "135"], help="Sudut sebaran (scatter angle) (derajat)", metavar="Sudut Scatter")
    
    args = parser.parse_args()
    
    pengguna = args.Pengguna
    pilvLinac = args.pilvLinac
    U = float(args.U)
    T = float(args.T)
    
    if pengguna == "Shielding Petugas Radiasi":
        T = 1.0
        P = float(400e-6) / 2      # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif pengguna == "Shielding Publik":
        P = float(20e-6) / 2       # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    
    if args.command == 'Primary_Barrier':
        # Call primary barrier function
        dc = float(args.dc)
        jp_3DCRT = float(args.jp_3DCRT)
        jp_IMRT = float(args.jp_IMRT)
        jp_SRS_SBRT = float(args.jp_SRS_SBRT)
        jp_RapidArc = float(args.jp_RapidArc)
        jp_QA = float(args.jp_QA)
        dn = float(args.Dn)
        
        linac_prim(P, pilvLinac, dc, U, T, dn, jp_3DCRT, jp_IMRT, jp_SRS_SBRT, jp_RapidArc, jp_QA)
        
    elif args.command == 'Secondary_Barrier':
        # Call secondary barrier function
        W = float(args.W)
        W_leak = float(args.W_leak)
        dsca = float(args.dsca)
        dsec = float(args.dsec)
        dw = float(args.dw)
        dr = float(args.dr)
        dc = float(args.dc)
        F = float(args.F)
        angle = float(args.angle)
        A = float(args.A)
        
        linac_sec(P, pilvLinac, W, W_leak, U, T, dsca, dsec, dw, dr, dc, F, A, angle)
    
if __name__ == "__main__":
    main()