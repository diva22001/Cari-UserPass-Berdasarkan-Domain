import os
import re
from tqdm import tqdm

def cari_file_password(file_path, target_domain, existing_userpass):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        matches = re.finditer(r'URL:(.*?)\nUsername:(.*?)\nPassword:(.*?)\n(.*?)===============', file_content, re.DOTALL)
        
        count_userpass = 0  # Menambah variabel untuk menghitung username dan password

        for match in matches:
            url = match.group(1).strip()
            username = match.group(2).strip()
            password = match.group(3).strip()

            # Hanya menyimpan baris yang mengandung domain yang diinginkan, memiliki username dan password tanpa spasi
            if target_domain in url and username and password and ' ' not in username and ' ' not in password:
                # Menghapus baris yang mengandung 'UNKNOWN'
                if 'UNKNOWN' not in username and 'UNKNOWN' not in password:
                    # Menghapus karakter Cyrillic
                    username = ''.join(char for char in username if ord(char) < 128)
                    password = ''.join(char for char in password if ord(char) < 128)

                    gabung_data = f"{username}:{password}"

                    # Menambah baris ke set
                    existing_userpass.add(gabung_data)
                    count_userpass += 1  # Menambah jumlah username dan password

    except Exception as e:
        # Jangan menampilkan pesan kesalahan jika gagal membaca file
        pass

    return count_userpass  # Mengembalikan jumlah username dan password

def cari_folder_password(root_folder, target_domain):
    total_userpass = 0  # Menambah variabel total_userpass
    existing_userpass = set()  # Membuat set untuk melacak baris yang sudah ada

    # Menggunakan tqdm untuk menunjukkan progres dalam persen
    for folder_path, _, files in tqdm(os.walk(root_folder), desc='Pencarian File Password', unit='folder', dynamic_ncols=True):
        for file_name in files:
            if file_name.lower() == 'passwords.txt':
                file_path = os.path.join(folder_path, file_name)
                total_userpass += cari_file_password(file_path, target_domain, existing_userpass)

    # Menulis ke satu file output setelah mencari di semua folder
    try:
        new_output_file = f'{target_domain}_{total_userpass}x.txt'
        with open(new_output_file, 'w', encoding='utf-8') as output_file:
            for userpass in existing_userpass:
                output_file.write(userpass + '\n')
    except Exception as e:
        # Jangan menampilkan pesan kesalahan jika gagal menyimpan
        pass

    if total_userpass > 0:
        print(f"Total {total_userpass} username dan password yang ditemukan (tanpa duplikat, tanpa spasi, dan tanpa baris kosong) untuk domain {target_domain}.")
        print(f"File output disimpan sebagai {new_output_file}")
    else:
        print(f"Tidak ada username dan password yang ditemukan untuk domain {target_domain}.")

# Meminta pengguna memasukkan path folder utama
path_ke_folder_utama = input("Masukkan path folder utama: ")

# Meminta pengguna memasukkan domain yang ingin dicari (contoh: facebook.com)
target_domain = input("Masukkan domain yang ingin dicari (contoh: facebook.com): ")

cari_folder_password(path_ke_folder_utama, target_domain)
