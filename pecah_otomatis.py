import os
import re

# 1. Baca file mentah teks novel
with open("teks_novel.txt", "r", encoding="utf-8") as f:
    konten = f.read()

# 2. Hapus watermark CamScanner
konten = re.sub(r'Dipindai dengan CamScanner', '', konten, flags=re.IGNORECASE)

# 3. Siapkan folder target di rak buku Malioboro
folder_output = "malioboro/bab_html"
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

# 4. Pecah teks berdasarkan penanda halaman asli
bagian = re.split(r'---\s*(halaman_\d+)\.webp\s*---', konten)

# 5. Kumpulkan semua halaman yang valid ke dalam sebuah daftar
daftar_halaman = []
for i in range(1, len(bagian), 2):
    nama = bagian[i]
    isi = bagian[i+1].strip()
    if isi:  # Pastikan halamannya tidak kosong
        daftar_halaman.append({"nama": nama, "isi": isi})

jumlah_halaman = len(daftar_halaman)

# 6. Proses pembuatan HTML dengan format rapi dan semua tombol
for i, hal in enumerate(daftar_halaman):
    nama_halaman = hal["nama"]
    isi_halaman = hal["isi"]
    
    # --- LOGIKA PERAPIAN PARAGRAF ---
    isi_halaman = re.sub(r'\n\s*\n', '<PARAGRAF>', isi_halaman)
    isi_halaman = re.sub(r'<PARAGRAF>\d{1,3}<PARAGRAF>', '<PARAGRAF>', isi_halaman)
    isi_halaman = isi_halaman.replace('\n', ' ')
    isi_halaman = isi_halaman.replace('<PARAGRAF>', '</p>\n\n<p>')
    isi_halaman = f"<p>{isi_halaman}</p>"
    
    judul_tampil = nama_halaman.replace('_', ' ').title()
    
    # --- LOGIKA TOMBOL NAVIGASI BAWAH ---
    link_prev = "../index.html"
    teks_prev = "← Kembali ke Daftar Isi"
    if i > 0:
        link_prev = f"{daftar_halaman[i-1]['nama']}.html"
        teks_prev = "← Sebelumnya"
        
    link_next = "../index.html"
    teks_next = "Selesai (Daftar Isi) →"
    if i < jumlah_halaman - 1:
        link_next = f"{daftar_halaman[i+1]['nama']}.html"
        teks_next = "Selanjutnya →"
    
    # --- TEMPLATE HTML FINAL ---
    html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../style.css">
    <title>{judul_tampil}</title>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Ubah Tema</button>
    
    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
        }}
        
        // 1. Catat untuk tombol pintasan Lanjut Membaca
        localStorage.setItem('malioboro_last_read', '{nama_halaman}.html');

        // 2. SENSOR PENCATAT: Masukkan halaman ini ke daftar riwayat yang sudah dibaca
        let riwayatBaca = JSON.parse(localStorage.getItem('malioboro_read_pages') || '[]');
        if (!riwayatBaca.includes('{nama_halaman}.html')) {{
            riwayatBaca.push('{nama_halaman}.html');
            localStorage.setItem('malioboro_read_pages', JSON.stringify(riwayatBaca));
        }}
    </script>

    <div class="novel-wrapper">
        <div class="top-nav">
            <a href="../index.html">← Daftar Isi</a>
        </div>
        
        <h1>{judul_tampil}</h1>
        {isi_halaman}
        
        <div class="nav-buttons">
            <a href="{link_prev}">{teks_prev}</a>
            <a href="{link_next}">{teks_next}</a>
        </div>
    </div>
</body>
</html>"""
    
    # 7. Tulis ke dalam file HTML masing-masing halaman
    with open(f"{folder_output}/{nama_halaman}.html", "w", encoding="utf-8") as f:
        f.write(html_template)

print(f"[V] SUKSES! {jumlah_halaman} halaman berhasil di-update dengan sensor Mark Read otomatis.")
