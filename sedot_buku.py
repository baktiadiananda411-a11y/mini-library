import requests
import json
import re
import os

base_url = "https://online.fliphtml5.com/ubdxc/smfj/"
config_url = f"{base_url}javascript/config.js"
folder_simpan = "buku_malioboro"

if not os.path.exists(folder_simpan):
    os.makedirs(folder_simpan)

print("[-] Membuka jalur ke file konfigurasi...")
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(config_url, headers=headers)

match = re.search(r'var\s+htmlConfig\s*=\s*({.*});?', response.text, re.DOTALL)

if match:
    data_json = json.loads(match.group(1))
    halaman_list = data_json.get("fliphtml5_pages", [])
    total_halaman = len(halaman_list)
    print(f"[+] Ditemukan {total_halaman} halaman! Memulai unduhan...\n")
    
    for index, item in enumerate(halaman_list):
        nama_file_hash = item["n"][0]
        url_gambar = f"{base_url}files/large/{nama_file_hash}"
        ekstensi = nama_file_hash.split('.')[-1]
        nama_baru = f"halaman_{str(index + 1).zfill(3)}.{ekstensi}"
        path_simpan = os.path.join(folder_simpan, nama_baru)
        
        print(f"--> Mengunduh [{index+1}/{total_halaman}]: {nama_baru}")
        img_resp = requests.get(url_gambar, headers=headers)
        with open(path_simpan, 'wb') as f:
            f.write(img_resp.content)
    print("\n[V] SELESAI! Semua halaman ada di folder: buku_malioboro")
else:
    print("[X] Gagal menemukan data konfigurasi.")
