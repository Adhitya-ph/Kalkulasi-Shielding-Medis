from gooey import Gooey, GooeyParser
from math import sqrt, log10 as log

def linac(P, dc, U, T, pilvLinac, jp_3DCRT, jp_IMRT, jp_SRS_SBRT, jp_RapidArc, jp_QA, dw, dr, F, A, angle):
    SAD = 1                        # Jarak dari sumber ke isosentris (SAD) (m)
    dp_3DCRT = 4.0 
    dp_IMRT = 4.0
    f_imrt = 3
    dp_srs_sbrt = 4.0
    f_srs_sbrt = 15
    dp_RapidArc = 4.0
    f_rapidarc = 4.5
    dp_QA = 6.0
    W = ((jp_3DCRT * dp_3DCRT) + (jp_IMRT * dp_IMRT) + (jp_SRS_SBRT * dp_srs_sbrt) + (jp_RapidArc * dp_RapidArc) + (jp_QA * dp_QA)) * 5
    W_leak = ((jp_3DCRT*dp_3DCRT) + (jp_IMRT*dp_IMRT*f_imrt) + (jp_SRS_SBRT*dp_srs_sbrt*f_srs_sbrt) + (jp_RapidArc*dp_RapidArc*f_rapidarc) + (jp_QA*dp_QA)) * 5

    if W*SAD**2 * U * T == 0:
        print("Value Error: Pastikan input jumlah pasien sudah benar.")
        return
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    B_leak = 1000 * P * dc**2 / ((W_leak*SAD**2) * T)
    print("---------------------------------------------------------------------------------------------------------")
    print("Perhitungan Shielding LINAC")
    print("Beban kerja total (primer): %g Gy / minggu" %W)
    print("Beban kerja total (leakage): %g Gy / minggu" %W_leak)

    n = log(1/B)
    n_leak = log(1/B_leak)
    
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
    l = n * tvl / 10
    print("\nKetebalan beton agar memenuhi batas laju dosis yang ditetapkan (primary barrier) = %g cm" %l)
    
    bw = 0.4 * sqrt(2) * (dc+SAD) + 0.6
    print("Primary Barrier Width = %g m" %bw)
    
    l_leak = n_leak * tvl_leak / 10
    print("\nKetebalan beton agar memenuhi batas laju dosis yang ditetapkan (leakage) = %g cm" %l_leak)
    
    b_patient = P * dc**2 / ((alpha * W_leak * T) * (F/400))
    n_patient = log(1/b_patient)
    
    b_wall = P * dw**2 * dr**2 / (alpha * A * (W_leak*SAD**2) * U * T)   # P * (dw**2 * dr**2) / (alpha * A * (W) * U * T)
    n_wall = log(1/b_wall)
    if abs(n_patient - n_wall) > 1:
        n_scatter = max(n_patient, n_wall)
    elif abs(n_patient - n_wall) <= 1:
        n_scatter = max(n_patient, n_wall) + 0.301    # HVL = 0.301 TVL
    l_scatter = (n_scatter * tvl_scatter) / 10
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (scatter) = %g cm" %l_scatter)
    
    if abs(l_scatter-l_leak) > tvl_leak / 10:
        l_secondary = max(l_scatter, l_leak)
    elif abs(l_scatter-l_leak) <= tvl_leak / 10:
        l_secondary = max(l_scatter, l_leak) + (0.301 * tvl_leak / 10)
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (secondary barrier) = %g cm" %l_secondary)
    print("---------------------------------------------------------------------------------------------------------\n")
    
def telecobalt(P, dc, SAD, U, T, jumlahPasien, dosisPasien, ds, angle, F):
    W = jumlahPasien * dosisPasien * 5
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    B_leak = 1000 * P * ds**2 / ((W*SAD**2) * T)
    print("---------------------------------------------------------------------------------------------------------")
    print("Perhitungan Shielding Telecobalt")
        
    n = log(1/B)
    n_leak = log(1/B_leak)
    print("\nJumlah Tenth Value Layer (TVL) yang diperlukan = %g" %n)
    tvl = 218
    tvl_leak = 218
    
    if angle == 30:
        alpha = 6e-3
        tvl_scatter = 213
    elif angle == 45:
        alpha = 3.7e-3
        tvl_scatter = 197
    elif angle == 60:
        alpha = 2.2e-3
        tvl_scatter = 189
    elif angle == 90:
        alpha = 9.1e-4
        tvl_scatter = 151
    elif angle == 135:
        alpha = 5.4e-4
        tvl_scatter = 128
    
    l = n * tvl / 10
    print("\nKetebalan beton agar memenuhi batas laju dosis yang ditetapkan (primary wall) = %g cm" %l)
    l_leak = n_leak * tvl_leak / 10
    print("\nKetebalan beton agar memenuhi batas laju dosis yang ditetapkan (leakage) = %g cm" %l_leak)
    b_patient = P * dc**2 / ((alpha * (W*SAD**2) * T) * (F/400))
    n_patient = log(1/b_patient)
    l_scatter = (n_patient * tvl_scatter) / 10
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (scatter) = %g cm" %l_scatter)
    if abs(l_scatter-l_leak) > tvl_leak / 10:
        l_secondary = max(l_scatter, l_leak)
    elif abs(l_scatter-l_leak) <= tvl_leak / 10:
        l_secondary = max(l_scatter, l_leak) + (0.301 * tvl_leak / 10)
    print("Ketebalan beton agar memenuhi batas laju dosis yang ditetapkan (secondary barrier) = %g cm" %l_secondary)
    print("---------------------------------------------------------------------------------------------------------\n")

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
                        ]},
             ]
       )

def main(): 
    parser = GooeyParser(description='Program yang mengkalkulasi ketebalan beton yang diperlukan dari fasilitas medis\nMasukkan parameter yang diperlukan, jika desimal gunakan titik (".")')
    subparsers = parser.add_subparsers(help='commands', dest='command')
    
    # Linac parser
    linac_parser = subparsers.add_parser('LINAC', help='Linac calculation')
    spec_fasilitas = linac_parser.add_argument_group("Spesifikasi Fasilitas LINAC")
    jumlah_pasien = linac_parser.add_argument_group("Jumlah Pasien LINAC")
    leak_scatter = linac_parser.add_argument_group("Faktor Leak dan Scattering")
    
    spec_fasilitas.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    spec_fasilitas.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari LINAC")
    spec_fasilitas.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    spec_fasilitas.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    spec_fasilitas.add_argument("pilvLinac", choices=["6 MV", "10 MV"], help="Pilih tegangan LINAC dari opsi yang tersedia", metavar="Tegangan LINAC")
    
    jumlah_pasien.add_argument("--jp_3DCRT", action="store", default=0, help="Rerata pasien untuk 3DCRT dalam sehari (8 jam kerja)", metavar="Pasien 3DCRT")
    jumlah_pasien.add_argument("--jp_IMRT", action="store", default=0, help="Rerata pasien untuk IMRT dalam sehari (8 jam kerja)", metavar="Pasien IMRT")
    jumlah_pasien.add_argument("--jp_SRS_SBRT", action="store", default=0, help="Rerata pasien untuk SRS/SBRT dalam sehari (8 jam kerja)", metavar="Pasien SRS/SBRT")
    jumlah_pasien.add_argument("--jp_RapidArc", action="store", default=0, help="Rerata pasien untuk RapidArc dalam sehari (8 jam kerja)", metavar="Pasien RapidArc")
    jumlah_pasien.add_argument("--jp_QA", action="store", default=0, help="Rerata beam untuk QA dalam sehari (8 jam kerja)", metavar="Pasien QA")
    
    leak_scatter.add_argument("dw", action="store", help="Jarak dari sumber ke dinding sebaran (m)", metavar="Dw")
    leak_scatter.add_argument("dr", action="store", help="Jarak dari dinding sebaran ke titik yang ingin dicari (m)", metavar="Dr")
    leak_scatter.add_argument("F", action="store", help="Field area incident di pasien (cm^2)", metavar="Field Area Incident")
    leak_scatter.add_argument("A", action="store", help="Area dinding sebaran (wall scattering) (m^2)", metavar="Area Dinding Sebaran")
    leak_scatter.add_argument("angle", choices=["30", "45", "60", "90", "135"], help="Sudut sebaran (scatter angle) (derajat)", metavar="Sudut Scatter")
    
    # Telecobalt parser
    telecobalt_parser = subparsers.add_parser('Telecobalt', help='Telecobalt calculation')
    spec_fasilitas = telecobalt_parser.add_argument_group("Spesifikasi Fasilitas Telecobalt")
    leak_scatter = telecobalt_parser.add_argument_group("Faktor Leak dan Scattering")
    
    spec_fasilitas.add_argument("Pengguna", choices=["Shielding Petugas Radiasi", "Shielding Publik"], help="Pilih target shielding", metavar="Target Shielding")
    spec_fasilitas.add_argument("dc", action="store", help="Jarak dari isosentris ke titik yang ingin dicari (m)", metavar="Jarak dari Telecobalt")
    spec_fasilitas.add_argument("SAD", action="store", help="Jarak dari sumber ke isosentris (m)", metavar="SAD")
    spec_fasilitas.add_argument("U", action="store", help="Masukkan use factor (0-1)", metavar="Use Factor")
    spec_fasilitas.add_argument("T", action="store", help="Masukkan occupancy factor (0-1)\n*(1 untuk petugas radiasi)", metavar="Occupancy Factor")
    spec_fasilitas.add_argument("jumlahPasien", action="store", help="Masukkan jumlah pasien per hari (8 jam kerja)", metavar="Jumlah Pasien")
    spec_fasilitas.add_argument("dosisPasien", action="store", default=3, help="Masukkan jumlah dosis per pasien (Gy)", metavar="Dosis Pasien")
    
    leak_scatter.add_argument("ds", action="store", help="Jarak dari isosentris ke permukaan luar secondary barrier (m)", metavar="Ds")
    leak_scatter.add_argument("F", action="store", help="Field area incident di pasien (cm^2)", metavar="Field Area Incident")
    leak_scatter.add_argument("angle", choices=["30", "45", "60", "90", "135"], help="Sudut sebaran (scatter angle) (derajat)", metavar="Sudut Scatter")
    
    args = parser.parse_args()
    
    pengguna = args.Pengguna
    dc = float(args.dc)
    U = float(args.U)
    T = float(args.T)
    F = float(args.F)
    angle = float(args.angle)
    
    if pengguna == "Shielding Petugas Radiasi":
        T = 1.0
        P = float(400e-6) / 2      # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif pengguna == "Shielding Publik":
        P = float(20e-6) / 2       # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    
    if args.command == 'LINAC':
        # Call linac function
        pilvLinac = args.pilvLinac
        jp_3DCRT = float(args.jp_3DCRT)
        jp_IMRT = float(args.jp_IMRT)
        jp_SRS_SBRT = float(args.jp_SRS_SBRT)
        jp_RapidArc = float(args.jp_RapidArc)
        jp_QA = float(args.jp_QA)
        dw = float(args.dw)
        dr = float(args.dr)
        A = float(args.A)
        
        linac(P, dc, U, T, pilvLinac, jp_3DCRT, jp_IMRT, jp_SRS_SBRT, jp_RapidArc, jp_QA, dw, dr, F, A, angle)
        
    elif args.command == 'Telecobalt':
        # Call telecobalt function
        SAD = float(args.SAD)
        jumlahPasien = float(args.jumlahPasien)
        dosisPasien = float(args.dosisPasien)
        ds = float(args.ds)
        
        telecobalt(P, dc, SAD, U, T, jumlahPasien, dosisPasien, ds, angle, F)
    
if __name__ == "__main__":
    main()