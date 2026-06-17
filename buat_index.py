import os
import re

folder_bab = "malioboro/bab_html"
file_index = "malioboro/index.html"

if not os.path.exists(folder_bab):
    print(f"[X] Error: Folder '{folder_bab}' tidak ditemukan!")
    exit()

files = [f for f in os.listdir(folder_bab) if f.endswith('.html')]

# Mengurutkan nomor halaman agar rapi
def ambil_angka(nama_file):
    match = re.search(r'\d+', nama_file)
    return int(match.group()) if match else 0

files_urut = sorted(files, key=ambil_angka)

html_links = ""
for file in files_urut:
    label = file.replace('.html', '').replace('_', ' ').title()
    html_links += f'                <li><a href="bab_html/{file}">{label}</a></li>\n'

# Template halaman Daftar Isi lengkap dengan gaya grid, light mode, dan titik merah otomatis
html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Malioboro at Midnight - Daftar Isi</title>
    <style>
        .btn-kembali {{
            display: block; text-align: center; color: #bb86fc; text-decoration: none;
            font-size: 14px; margin-bottom: 25px; font-weight: bold; transition: color 0.2s;
        }}
        .btn-kembali:hover {{ color: #9a67ea; text-decoration: underline; }}
        
        /* Desain Grid Kotak-Kotak */
        .grid-daftar {{
            margin-top: 30px; padding: 0; list-style: none; display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px;
        }}
        .grid-daftar a {{
            color: #bb86fc; text-decoration: none; background: #2c2c2c; padding: 12px 8px;
            display: block; text-align: center; border-radius: 6px; font-size: 14px;
            font-weight: bold; transition: all 0.2s ease; border: 1px solid #3d3d3d;
            position: relative; /* Membuat acuan untuk posisi titik merah di sudut */
        }}
        .grid-daftar a:hover {{
            background: #bb86fc; color: #121212; transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(187, 134, 252, 0.2);
        }}
        
        body.light-mode .grid-daftar a {{ background: #eeeeee; color: #5e35b1; border: 1px solid #ddd; }}
        body.light-mode .grid-daftar a:hover {{ background: #5e35b1; color: #ffffff; box-shadow: 0 4px 8px rgba(94, 53, 177, 0.2); }}
        
        .btn-lanjut {{
            display: none; background: #bb86fc; color: #121212; text-align: center; padding: 12px;
            border-radius: 6px; text-decoration: none; font-weight: bold; margin: 20px auto;
            max-width: 250px; transition: all 0.2s ease;
        }}
        .btn-lanjut:hover {{ background: #9a67ea; transform: translateY(-2px); }}
        body.light-mode .btn-lanjut {{ background: #5e35b1; color: #fff; }}
        body.light-mode .btn-lanjut:hover {{ background: #4527a0; }}
        
        /* --- GAYA ELEMEN TITIK MERAH (SUDUT KANAN ATAS KOTAK) --- */
        .grid-daftar a.sudah-dibaca::after {{
            content: "";
            position: absolute;
            top: 6px;
            right: 6px;
            width: 8px;
            height: 8px;
            background-color: #ff4c4c; /* Merah menyala */
            border-radius: 50%;
            box-shadow: 0 0 5px #ff4c4c; /* Efek glowing tipis */
        }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Ubah Tema</button>

    <div class="novel-wrapper">
        <a href="../index.html" class="btn-kembali">← Kembali ke Library Utama</a>

        <h1 style="margin-bottom: 5px; text-align: center;">Malioboro at Midnight</h1>
        <p style="text-align: center; font-style: italic; color: #aaa; margin-top: 0;">Koleksi Halaman Digital</p>
        
        <a href="#" id="btnLanjut" class="btn-lanjut">📖 Lanjut Membaca</a>
        
        <hr style="border: 0; border-top: 1px solid #3d3d3d; margin: 20px 0;">
        
        <ul class="grid-daftar">
{html_links}
        </ul>
    </div>

    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
        }}
        
        document.addEventListener("DOMContentLoaded", function() {{
            // 1. Logika Tombol Lanjut Membaca
            let lastRead = localStorage.getItem('malioboro_last_read');
            if (lastRead) {{
                let btn = document.getElementById('btnLanjut');
                btn.href = "bab_html/" + lastRead;
                btn.style.display = "block";
            }}
            
            // 2. LOGIKA TITIK MERAH: Ambil semua riwayat halaman yang sudah dibaca
            let riwayatBaca = JSON.parse(localStorage.getItem('malioboro_read_pages') || '[]');
            riwayatBaca.forEach(function(pageFile) {{
                // Cari elemen kotak link yang sesuai dengan nama file
                let kotakLink = document.querySelector('.grid-daftar a[href="bab_html/' + pageFile + '"]');
                if (kotakLink) {{
                    kotakLink.classList.add('sudah-dibaca'); // Tempelkan tanda titik merah
                }}
            }});
        }});
    </script>
</body>
</html>"""

with open(file_index, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"[V] SUKSES! File Daftar Isi diperbarui dengan sistem rendering penanda titik merah otomatis.")
