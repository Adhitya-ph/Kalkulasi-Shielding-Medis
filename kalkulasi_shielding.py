# Program kalkulasi shielding
from math import log10 as log
def menu():
    print("Selamat Datang di Program Untuk Kalkulasi Shielding")
    print("---------------------------------------------------")
    print("Fasilitas radiasi kesehatan:")
    print("1. Linear Accelerator (LINAC)")
    print("2. Telecobalt-60")
    pilihFasilitas = float(input("Masukkan opsi pilihan : "))
    if pilihFasilitas == 1:
        Linac()
    elif pilihFasilitas == 2:
        telecobalt()
    else:
        print("Pilihan salah")

def Linac():
    print("\nMenu LINAC: Masukkan data-data yang dibutuhkan:")
    opsiPegawai = float(input("Pilih 1 untuk shielding petugas radiasi, 2 untuk shielding publik: "))
    if opsiPegawai == 1:
        P = float(400e-6) / 2      # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif opsiPegawai == 2:
        P = float(20e-6) / 2       # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    jumlahPasien = float(input("Masukkan jumlah pasien per hari (8 jam kerja): "))
    dosisPasien = float(input("Masukkan jumlah dosis per pasien (Gy): "))
    dc = float(input("Masukkan jarak dari isosentris ke titik yang ingin dicari(m) : "))
    SAD = 1                        # Jarak dari sumber ke isosentris (SAD) (m)
    U = float(input("Masukkan use factor : "))
    if opsiPegawai == 1:
        T = 1
    else:
        T = float(input("Masukkan occupancy factor : "))
    W = jumlahPasien * 5 * dosisPasien
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("\nAtenuasi B = %g" %B)
    n = log(1/B)
    print("Tenth Value Layer (TVL) yang diperlukan = %g" %n)

    def menuLINAC():
        while True:
            print("\nMau menghitung apa?")
            print("1. Ketebalan beton yang diperlukan")
            print("2. Dosis maksimal pada jam tertentu")
            print("0. Keluar")
            pilihan = int(input("Masukkan opsi pilihan: "))
            if pilihan == 1:
                primBarrier()
            elif pilihan == 2:
                TADR()
            elif pilihan == 0:
                break
            else:
                print("Pilihan tidak valid. Silakan pilih kembali.")

    def primBarrier():
        print("\nOpsi tegangan LINAC:")
        print("1. 4 MV")
        print("2. 6 MV")
        print("3. 10 MV")
        print("4. 15 MV")
        print("5. 18 MV")
        print("6. 20 MV")
        print("7. 24 MV")
        pilvLinac = float(input("Pilih opsi besar tegangan LINAC: "))
        if pilvLinac == 1:
            tvl = 290
            print("\nBesar tegangan LINAC: 4 MV")
        if pilvLinac == 2:
            tvl = 343
            print("\nBesar tegangan LINAC: 6 MV")
        if pilvLinac == 3:
            tvl = 389
            print("\nBesar tegangan LINAC: 10 MV")
        if pilvLinac == 4:
            tvl = 432
            print("\nBesar tegangan LINAC: 15 MV")
        if pilvLinac == 5:
            tvl = 445
            print("\nBesar tegangan LINAC: 18 MV")
        if pilvLinac == 6:
            tvl = 457
            print("\nBesar tegangan LINAC: 20 MV")
        if pilvLinac == 7:
            tvl = 470
            print("\nBesar tegangan LINAC: 24 MV")
        l = n * tvl / 10
        print("Ketebalan beton yang diperlukan = %g cm" %l)

    def TADR():
        dosisMax = float(input("Masukkan laju dosis maksimum akselerator di isosentris (Gy/min): "))
        pasienMax = float(input("Masukkan jumlah maksimal pasien yang dapat ditangani dalam satu jam: "))
        IDR = dosisMax * 60 * B / (dc+SAD)**2
        print("\nPerkiraan laju dosis (IDR) = %g Gy/h" %IDR)
        Rh = IDR * pasienMax * dosisPasien * U / (dosisMax * 60)
        print("Dosis maksimal pada satu jam tertentu (TADR (Rh)) = %g Sv" %Rh)
        if Rh < 20e-6:
            print("Dosis maksimal tersebut tidak melebihi batas 20 uSv tiap jamnya")
        elif Rh >= 20e-6:
            print("Dosis maksimal tersebut tidak melebihi batas 20 uSv tiap jamnya")

    menuLINAC()

def telecobalt():
    print("\nMenu Telecobalt: Masukkan data-data yang dibutuhkan:")
    opsiPegawai = float(input("Pilih 1 untuk shielding petugas radiasi, 2 untuk shielding publik: "))
    if opsiPegawai == 1:
        P = float(400e-6) / 2  # Batas dosis perminggu untuk petugas radiasi (20 mSv / 50 minggu = 400 uSv) dibagi 2 karena batas PerKa
    elif opsiPegawai == 2:
        P = float(20e-6) / 2   # Batas dosis perminggu untuk publik (1 mSv / 50 minggu = 20 uSv), dibagi 2 karena batas PerKa
    jumlahPasien = float(input("Masukkan jumlah pasien per hari (8 jam kerja): "))
    dosisPasien = float(input("Masukkan jumlah dosis per pasien (Gy): "))
    dc = float(input("Masukkan jarak dari isosentris ke titik yang ingin dicari(m) : "))
    SAD = float(input("Masukkan jarak dari sumber ke isosentris (SAD) (m) : "))
    U = float(input("Masukkan use factor : "))
    if opsiPegawai == 1:
        T = 1
    else:
        T = float(input("Masukkan occupancy factor : "))
    W = jumlahPasien * 5 * dosisPasien
    B = P * (dc+SAD)**2 / ((W*SAD**2) * U * T)
    print("\nAtenuasi B = %g" %B)

    def menuTelecobalt():
        while True:
            print("\nMau menghitung apa?")
            print("1. Ketebalan beton yang diperlukan")
            print("2. Dosis rerata pada satu jam (TADR)")
            print("0. Keluar")
            pilihan = int(input("Masukkan opsi pilihan: "))
            if pilihan == 1:
                primBarrier()
            elif pilihan == 2:
                TADR()
            elif pilihan == 0:
                break
            else:
                print("Pilihan tidak valid. Silakan pilih kembali.")

    def primBarrier():
        n = log(1/B)
        print("\nTenth Value Layer (TVL) yang diperlukan =", n)
        tvl = 218
        l = n * tvl / 10
        print("Ketebalan beton yang diperlukan = %g cm" %l)
        
    def TADR():
        paparanSumber = float(input("Masukkan laju paparan sumber pada jarak 1 meter (Gy/min): "))
        IDR = paparanSumber * 60 * 10e6 * B / (dc+SAD)**2
        print("\nPerkiraan laju dosis (IDR) = %g uSv/h" %IDR)
        TADR = IDR * (jumlahPasien*dosisPasien/(paparanSumber*(1/SAD)**2*60)) * U / 8
        print("Dosis rerata selama satu jam (TADR) = %g uSv" %TADR)

    menuTelecobalt()
    
# Program Utama
menu()

input()