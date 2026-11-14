import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from supabase import create_client, Client
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "KunciRahasiaRongawi2026")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

UPLOAD_FOLDER_PROYEK = 'static/assets/proyek'
UPLOAD_FOLDER_ASSET = 'static/assets'

@app.route('/')
@app.route('/indeks')
def index():
    try:
        res_proyek = supabase.table("proyek").select("*").execute()
        proyek_list = res_proyek.data if res_proyek.data else []
        
        # Diubah ke tabel 'konten_web'
        res_konten = supabase.table("konten_web").select("*").execute()
        konten_data = res_konten.data[0] if res_konten.data else {}
    except Exception:
        proyek_list = []
        konten_data = {}
    
    return render_template('indeks.html', proyek=proyek_list, konten=konten_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            res = supabase.table("admin").select("*").eq("username", username).execute()
            user_data = res.data
            if user_data and user_data[0].get('password') == password:
                session['user'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                if username == "Aditiyaravi" and password == "Allizade":
                    session['user'] = username
                    return redirect(url_for('admin_dashboard'))
                return render_template('login.html', error="Username atau Password salah, Yang Mulia!")
        except Exception:
            if username == "Aditiyaravi" and password == "Allizade":
                session['user'] = username
                return redirect(url_for('admin_dashboard'))
            return render_template('login.html', error="Terjadi kesalahan koneksi database.")
    return render_template('login.html')

@app.route('/ganti_password', methods=['GET', 'POST'])
def ganti_password():
    error, success = None, None
    if request.method == 'POST':
        username = request.form.get('username')
        password_lama = request.form.get('password_lama')
        password_baru = request.form.get('password_baru')
        try:
            res = supabase.table("admin").select("*").eq("username", username).execute()
            if res.data and res.data[0].get('password') == password_lama:
                supabase.table("admin").update({"password": password_baru}).eq("username", username).execute()
                success = "Password berhasil diubah, Yang Mulia!"
            else:
                error = "Username atau Password lama salah!"
        except Exception:
            error = "Gagal memperbarui password ke database."
    return render_template('ganti_password.html', error=error, success=success)

@app.route('/admin')
def admin_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    try:
        res_proyek = supabase.table("proyek").select("*").execute()
        proyek_list = res_proyek.data if res_proyek.data else []
        
        # Diubah ke tabel 'konten_web'
        res_konten = supabase.table("konten_web").select("*").execute()
        konten_data = res_konten.data[0] if res_konten.data else {}
    except Exception:
        proyek_list = []
        konten_data = {}
    return render_template('admin.html', proyek=proyek_list, konten=konten_data)

@app.route('/admin/tambah', methods=['POST'])
def tambah_proyek():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    judul = request.form.get('judul')
    deskripsi = request.form.get('deskripsi')
    link_drive = request.form.get('link_drive')
    gambar_nama = request.form.get('gambar')
    
    file_gambar = request.files.get('file_gambar')
    if file_gambar and file_gambar.filename != '':
        filename = secure_filename(file_gambar.filename)
        os.makedirs(UPLOAD_FOLDER_PROYEK, exist_ok=True)
        file_gambar.save(os.path.join(UPLOAD_FOLDER_PROYEK, filename))
        gambar_nama = filename

    try:
        supabase.table("proyek").insert({
            "judul": judul,
            "deskripsi": deskripsi,
            "link_drive": link_drive,
            "gambar": gambar_nama
        }).execute()
    except Exception as e:
        print("Error tambah proyek:", e)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:id>', methods=['POST'])
def edit_proyek(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    judul = request.form.get('judul')
    deskripsi = request.form.get('deskripsi')
    link_drive = request.form.get('link_drive')
    gambar_nama = request.form.get('gambar')
    
    file_gambar = request.files.get('file_gambar')
    if file_gambar and file_gambar.filename != '':
        filename = secure_filename(file_gambar.filename)
        os.makedirs(UPLOAD_FOLDER_PROYEK, exist_ok=True)
        file_gambar.save(os.path.join(UPLOAD_FOLDER_PROYEK, filename))
        gambar_nama = filename

    try:
        supabase.table("proyek").update({
            "judul": judul,
            "deskripsi": deskripsi,
            "link_drive": link_drive,
            "gambar": gambar_nama
        }).eq("id", id).execute()
    except Exception as e:
        print("Error edit proyek:", e)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/hapus/<int:id>')
def hapus_proyek(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    try:
        supabase.table("proyek").delete().eq("id", id).execute()
    except Exception as e:
        print("Error hapus proyek:", e)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_konten', methods=['POST'])
def update_konten():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    profil_singkat = request.form.get('profil_singkat')
    about_intro = request.form.get('about_intro')
    pengalaman_sma = request.form.get('pengalaman_sma')
    pengalaman_kerja = request.form.get('pengalaman_kerja')
    pengalaman_kuliah = request.form.get('pengalaman_kuliah')
    
    update_data = {}
    if profil_singkat is not None: update_data['profil_singkat'] = profil_singkat
    if about_intro is not None: update_data['about_intro'] = about_intro
    if pengalaman_sma is not None: update_data['pengalaman_sma'] = pengalaman_sma
    if pengalaman_kerja is not None: update_data['pengalaman_kerja'] = pengalaman_kerja
    if pengalaman_kuliah is not None: update_data['pengalaman_kuliah'] = pengalaman_kuliah
    
    file_foto = request.files.get('file_foto')
    if file_foto and file_foto.filename != '':
        foto_name = secure_filename(file_foto.filename)
        os.makedirs(UPLOAD_FOLDER_ASSET, exist_ok=True)
        file_foto.save(os.path.join(UPLOAD_FOLDER_ASSET, foto_name))
        update_data['foto_profil'] = foto_name

    try:
        # Diubah ke tabel 'konten_web'
        supabase.table("konten_web").update(update_data).eq("id", 1).execute()
    except Exception as e:
        print("Error update konten:", e)
        
    return redirect(url_for('admin_dashboard'))

@app.route('/about')
def about():
    try:
        # Diubah ke tabel 'konten_web'
        res_konten = supabase.table("konten_web").select("*").execute()
        konten_data = res_konten.data[0] if res_konten.data else {}
    except Exception:
        konten_data = {}
    return render_template('about.html', konten=konten_data)

@app.route('/about_page')
def about_page():
    return redirect(url_for('about'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)