import os
import re

# 1. Baca teks Hujan
with open("teks_hujan.txt", "r", encoding="utf-8") as f:
    konten = f.read()

# 2. Siapkan folder target
folder_output = "hujan/bab_html"
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

# 3. Pecah teks
bagian = re.split(r'---\s*(halaman_\d+)\.webp\s*---', konten)

daftar_halaman = []
for i in range(1, len(bagian), 2):
    nama = bagian[i]
    isi = bagian[i+1].strip()
    if isi:
        daftar_halaman.append({"nama": nama, "isi": isi})

jumlah_halaman = len(daftar_halaman)

# 4. Proses HTML
for i, hal in enumerate(daftar_halaman):
    nama_halaman = hal["nama"]
    isi_halaman = hal["isi"]
    
    isi_halaman = re.sub(r'\n\s*\n', '<PARAGRAF>', isi_halaman)
    isi_halaman = re.sub(r'<PARAGRAF>\d{1,3}<PARAGRAF>', '<PARAGRAF>', isi_halaman)
    isi_halaman = isi_halaman.replace('\n', ' ')
    isi_halaman = isi_halaman.replace('<PARAGRAF>', '</p>\n\n<p>')
    isi_halaman = f"<p>{isi_halaman}</p>"
    
    # --- LOGIKA MENGUBAH ANGKA URUT (MENGHILANGKAN NOL DI DEPAN) ---
    match_angka = re.search(r'\d+', nama_halaman)
    nomor_asli = int(match_angka.group()) if match_angka else 0
    
    # PENTING: Jika halaman_005 di dalam teksnya adalah halaman 4, artinya ada selisih -1.
    # Jika ingin disamakan dengan teks di dalam buku, ubah angka 0 di bawah ini menjadi -1
    selisih_halaman = 0 
    
    nomor_tampil = nomor_asli + selisih_halaman
    judul_tampil = f"Halaman {nomor_tampil}"
    
    link_prev = "../index.html"
    teks_prev = "← Daftar Isi"
    if i > 0:
        link_prev = f"{daftar_halaman[i-1]['nama']}.html"
        teks_prev = "← Sebelumnya"
        
    link_next = "../index.html"
    teks_next = "Selesai →"
    if i < jumlah_halaman - 1:
        link_next = f"{daftar_halaman[i+1]['nama']}.html"
        teks_next = "Selanjutnya →"
    
    html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../style.css">
    <title>{judul_tampil} - Hujan</title>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Ubah Tema</button>
    
    <script>
        function toggleTheme() {{ document.body.classList.toggle('light-mode'); }}
        
        localStorage.setItem('hujan_last_read', '{nama_halaman}.html');
        let riwayatBaca = JSON.parse(localStorage.getItem('hujan_read_pages') || '[]');
        if (!riwayatBaca.includes('{nama_halaman}.html')) {{
            riwayatBaca.push('{nama_halaman}.html');
            localStorage.setItem('hujan_read_pages', JSON.stringify(riwayatBaca));
        }}
    </script>

    <div class="novel-wrapper">
        <div class="top-nav"><a href="../index.html">← Daftar Isi</a></div>
        <h1>{judul_tampil}</h1>
        {isi_halaman}
        <div class="nav-buttons">
            <a href="{link_prev}">{teks_prev}</a>
            <a href="{link_next}">{teks_next}</a>
        </div>
    </div>
</body>
</html>"""
    
    with open(f"{folder_output}/{nama_halaman}.html", "w", encoding="utf-8") as f:
        f.write(html_template)

print(f"[V] SUKSES! {jumlah_halaman} halaman Hujan berhasil diperbarui dengan nomor urut rapi.")
