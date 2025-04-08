import requests

BASE_URL = "http://127.0.0.1:8000"
TASKS_URL = f"{BASE_URL}/tasks/"
USERS_URL = f"{BASE_URL}/users/"
HEADERS = {"Content-Type": "application/json"}

users = [
    {"username": "user1", "email": "user@example.com"},
    {"username": "luna", "email": "luna@example.com"},
    {"username": "kevin", "email": "kevin@example.com"},
    {"username": "rina", "email": "rina@example.com"},
    {"username": "mika", "email": "mika@example.com"}
]

user_ids = []

print("📌 Menambahkan dummy users...")
for user in users:
    response = requests.post(USERS_URL, json=user, headers=HEADERS)
    if response.status_code == 200:
        user_id = response.json()["id"]
        user_ids.append(user_id)
        print(f"✅ User {user_id} ditambahkan: {user['username']}")
    else:
        print(f"❌ Gagal menambahkan user: {user['username']}", response.text)

# Menampilkan hasil semua user
print("\n📌 Mengambil semua users...")
response = requests.get(USERS_URL)
if response.status_code == 200:
    all_users = response.json()
    for user in all_users:
        print(f"🔹 {user['id']}: {user['username']} ({user['email']})")
else:
    print("❌ Gagal mengambil daftar user")

tasks = [
    {
        "title": "Desain halaman Task Detail",
        "description": "Buat layout halaman detail tugas menggunakan Svelte + Flowbite-Svelte",
        "priority": 2,
        "status": "In Progress",
        "progress": 60
    },
    {
        "title": "Implementasi fitur komentar",
        "description": "Tambahkan fitur komentar untuk setiap task, terhubung ke user",
        "priority": 1,
        "status": "Completed",
        "progress": 100
    },
    {
        "title": "Fitur upload lampiran",
        "description": "Pengguna dapat mengunggah file pada halaman detail task",
        "priority": 1,
        "status": "Completed",
        "progress": 100
    },
    {
        "title": "Halaman Settings",
        "description": "Desain UI halaman pengaturan seperti tema, bahasa, dan akun",
        "priority": 3,
        "status": "Pending",
        "progress": 0
    },
    {
        "title": "Laporan Statistik Tugas",
        "description": "Tampilkan grafik tren, jumlah tugas per status, dan tugas terbaru",
        "priority": 2,
        "status": "In Progress",
        "progress": 40
    },
    {
        "title": "Integrasi backend FastAPI",
        "description": "Hubungkan frontend dengan API FastAPI untuk mengambil data task",
        "priority": 1,
        "status": "Completed",
        "progress": 100
    },
    {
        "title": "Model User dan relasi komentar",
        "description": "Tambahkan model User di backend dan hubungkan ke komentar",
        "priority": 2,
        "status": "Completed",
        "progress": 100
    },
    {
        "title": "Optimasi performa API",
        "description": "Tambahkan pagination dan filter di endpoint tasks",
        "priority": 3,
        "status": "Pending",
        "progress": 0
    },
    {
        "title": "Autentikasi User",
        "description": "Tambahkan autentikasi berbasis token JWT di backend",
        "priority": 1,
        "status": "In Progress",
        "progress": 30
    },
    {
        "title": "Deploy TaskAI ke server",
        "description": "Siapkan deployment untuk backend dan frontend TaskAI",
        "priority": 2,
        "status": "Pending",
        "progress": 0
    }
]

task_ids = []

print("📌 Menambahkan tugas...")
for task in tasks:
    response = requests.post(TASKS_URL, json=task, headers=HEADERS)
    if response.status_code == 200:
        task_id = response.json()["id"]
        task_ids.append(task_id)
        print(f"✅ Task {task_id} ditambahkan: {task['title']}")
    else:
        print(f"❌ Gagal menambahkan task: {task['title']}", response.text)

print("\n📌 Mengambil semua tugas...")
response = requests.get(TASKS_URL)
if response.status_code == 200:
    all_tasks = response.json()
    for task in all_tasks:
        print(f"🔹 {task['id']}: {task['title']} - {task['status']}")
else:
    print("❌ Gagal mengambil daftar tugas")

if task_ids and user_ids:
    first_task_id = task_ids[0]
    COMMENT_URL = f"{BASE_URL}/tasks/{first_task_id}/comments/"
    comment_data = {
        "task_id": first_task_id,
        "author_id": user_ids[0],
        "content": "Ini adalah komentar pertama untuk tugas ini!"
    }

    print(f"\n📌 Menambahkan komentar ke Task {first_task_id}...")
    response = requests.post(COMMENT_URL, json=comment_data, headers=HEADERS)
    if response.status_code == 200:
        print("✅ Komentar berhasil ditambahkan!")
    else:
        print("❌ Gagal menambahkan komentar", response.text)

if task_ids:
    first_task_id = task_ids[0]
    ATTACHMENT_URL = f"{BASE_URL}/tasks/{first_task_id}/attachments/"
    file_path = "test_folder/test_file.txt"

    with open(file_path, "w") as f:
        f.write("Ini adalah file lampiran untuk tugas ini.")

    print(f"\n📌 Mengunggah lampiran ke Task {first_task_id}...")
    with open(file_path, "rb") as file:
        response = requests.post(ATTACHMENT_URL, files={"file": file})

    if response.status_code == 200:
        print("✅ Lampiran berhasil diunggah!")
    else:
        print("❌ Gagal mengunggah lampiran", response.text)
