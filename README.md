### 📌 **TaskAI: Task Manager with Smart AI Recommendations**  

TaskAI adalah aplikasi manajemen tugas dengan fitur AI yang membantu mengatur urutan tugas berdasarkan prioritas.  

## **🚀 Fitur Utama**  
✔️ Tambah, edit, hapus tugas dengan mudah  
✔️ AI merekomendasikan urutan tugas berdasarkan prioritas menggunakan **sentence-transformers**  
✔️ Penyimpanan data menggunakan **SQLite**  
✔️ API berbasis **FastAPI** untuk kinerja cepat dan ringan  
✔️ (Opsional) UI berbasis **SvelteKit**  

## **📂 Struktur Folder**  
```
TaskAI/
│── backend/               # Backend menggunakan FastAPI
│   ├── main.py            # Entry point FastAPI
│   ├── models.py          # ORM Model untuk SQLite
│   ├── ai.py              # Model AI untuk rekomendasi tugas
│   ├── database.py        # Koneksi database SQLite
│── frontend/              # (Opsional) Frontend menggunakan SvelteKit
│── requirements.txt       # Dependensi Python
│── README.md              # Dokumentasi proyek
```

## **⚡ Instalasi & Menjalankan Backend**  
Pastikan **Python 3.9+** sudah terinstal.  

1️⃣ **Clone repo ini**  
```bash
git clone https://github.com/Ajax-Z01/TaskAI.git
cd TaskAI/backend
```

2️⃣ **Buat virtual environment (opsional, tapi direkomendasikan)**  
```bash
python -m venv venv
source venv/bin/activate  # Untuk Mac/Linux
venv\Scripts\activate     # Untuk Windows
```

3️⃣ **Instal dependensi**  
```bash
pip install -r requirements.txt
```

4️⃣ **Jalankan server FastAPI**  
```bash
uvicorn main:app --reload
```

API akan berjalan di `http://127.0.0.1:8000`  

## **🌍 Rencana Pengembangan**  
- [x] Backend API dengan FastAPI  
- [x] AI rekomendasi tugas menggunakan `sentence-transformers`  
- [ ] Frontend dashboard dengan SvelteKit  
- [ ] Autentikasi pengguna  

## **📜 Lisensi**  
MIT License  

---