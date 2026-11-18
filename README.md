# 🚀 Web Portofolio & Sistem Manajemen Proyek (Flask + Supabase)

Portofolio web pribadi interaktif yang dikembangkan menggunakan **Python Flask** sebagai backend, **Supabase (PostgreSQL)** sebagai database cloud, dan dideploy secara live di **Vercel**. Proyek ini dilengkapi dengan panel admin terautentikasi dan fitur multimedia (pemutar musik latar).

---

## 🛠️ Tech Stack & Tools
* **Frontend:** HTML5, CSS3 (Anime Moshoku Thensei), JavaScript (Floating Audio & Volume Slider)
* **Backend:** Python, Flask Framework, Werkzeug Security
* **Database & Storage:** Supabase (PostgreSQL Cloud Tables)
* **Deployment:** Vercel Serverless Platform

---

## 📂 Struktur Direktori Proyek
```text
website_portofolio_new/
│
├── static/
│   ├── assets/        # Kumpulan gambar, poster, dan file backsound (.mp3)
│   └── css/           # File gaya antarmuka (style.css, login.css)
│
├── templates/         # Berkas HTML template Flask
│   ├── indeks.html    # Halaman utama portofolio & widget musik
│   ├── login.html     # Halaman login admin dengan autoplay audio
│   └── admin.html     # Dashboard manajemen konten & proyek
│
├── .env               # Variabel lingkungan rahasia (Supabase URL & Key)
├── main.py            # Berkas utama server backend Flask
├── requirements.txt   # Daftar dependensi pustaka Python
└── vercel.json        # Konfigurasi deployment serverless Vercel

⚙️ Cara Konfigurasi & Koneksi Supabase
1. Buat file .env di direktori root proyek, lalu masukkan kredensial berikut:
SUPABASE_URL=https://<url-proyekmu>.supabase.co
SUPABASE_KEY=<api-key-supabase-kamu>
SECRET_KEY=kunci-rahasia-bebasZ

2. Inisialisasi di main.py:
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


✨ Fitur Unggulan
- Dynamic Content: Data proyek dan profil diambil secara real-time dari tabel database Supabase.
- Admin Dashboard: Manajemen tambah, edit, dan hapus proyek serta pembaruan profil singkat secara dinamis.
- Background Audio Player: Widget pemutar musik melayang interaktif lengkap dengan slider kontrol volume di halaman utama, serta autoplay di halaman login admin.

© 2026 Aditiya Ravi Hendrawan. All Rights Reserved.
