import os
import re

folder_bab = "hujan/bab_html"
file_index = "hujan/index.html"

files = [f for f in os.listdir(folder_bab) if f.endswith('.html')]

def ambil_angka(nama_file):
    match = re.search(r'\d+', nama_file)
    return int(match.group()) if match else 0

files_urut = sorted(files, key=ambil_angka)

html_links = ""
for file in files_urut:
    # --- SINKRONISASI ANGKA URUT DENGAN KODE SEBELUMNYA ---
    nomor_asli = ambil_angka(file)
    
    # Pastikan nilai selisih_halaman ini SAMA dengan yang ada di pecah_hujan.py
    selisih_halaman = 0 
    
    nomor_tampil = nomor_asli + selisih_halaman
    label = f"Halaman {nomor_tampil}"
    
    html_links += f'                <li><a href="bab_html/{file}">{label}</a></li>\n'

html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Hujan - Daftar Isi</title>
    <style>
        .btn-kembali {{ display: block; text-align: center; color: #bb86fc; text-decoration: none; font-size: 14px; margin-bottom: 25px; font-weight: bold; }}
        .grid-daftar {{ margin-top: 30px; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; }}
        .grid-daftar a {{ color: #bb86fc; text-decoration: none; background: #2c2c2c; padding: 12px 8px; display: block; text-align: center; border-radius: 6px; font-size: 14px; font-weight: bold; position: relative; border: 1px solid #3d3d3d; }}
        .grid-daftar a.sudah-dibaca::after {{ content: ""; position: absolute; top: 6px; right: 6px; width: 8px; height: 8px; background-color: #ff4c4c; border-radius: 50%; box-shadow: 0 0 5px #ff4c4c; }}
        .btn-lanjut {{ display: none; background: #bb86fc; color: #121212; text-align: center; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; margin: 20px auto; max-width: 250px; }}
        body.light-mode .grid-daftar a {{ background: #eeeeee; color: #5e35b1; border: 1px solid #ddd; }}
        body.light-mode .btn-lanjut {{ background: #5e35b1; color: #fff; }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Ubah Tema</button>

    <div class="novel-wrapper">
        <a href="../index.html" class="btn-kembali">← Kembali ke Library Utama</a>
        <h1 style="margin-bottom: 5px; text-align: center;">Hujan</h1>
        <p style="text-align: center; font-style: italic; color: #aaa; margin-top: 0;">Karya Tere Liye</p>
        
        <a href="#" id="btnLanjut" class="btn-lanjut">📖 Lanjut Membaca</a>
        <hr style="border: 0; border-top: 1px solid #3d3d3d; margin: 20px 0;">
        <ul class="grid-daftar">
{html_links}
        </ul>
    </div>

    <script>
        function toggleTheme() {{ document.body.classList.toggle('light-mode'); }}
        document.addEventListener("DOMContentLoaded", function() {{
            let lastRead = localStorage.getItem('hujan_last_read');
            if (lastRead) {{
                let btn = document.getElementById('btnLanjut');
                btn.href = "bab_html/" + lastRead;
                btn.style.display = "block";
            }}
            let riwayatBaca = JSON.parse(localStorage.getItem('hujan_read_pages') || '[]');
            riwayatBaca.forEach(function(pageFile) {{
                let kotakLink = document.querySelector('.grid-daftar a[href="bab_html/' + pageFile + '"]');
                if (kotakLink) kotakLink.classList.add('sudah-dibaca');
            }});
        }});
    </script>
</body>
</html>"""

with open(file_index, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"[V] SUKSES! Daftar Isi Hujan berhasil diperbarui dengan nomor urut rapi.")
