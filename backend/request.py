import requests

BASE_URL = "http://127.0.0.1:8000"
TASKS_URL = f"{BASE_URL}/tasks/"
HEADERS = {"Content-Type": "application/json"}

tasks = [
    {
        "title": "Submit laporan proyek",
        "description": "Deadline hari ini pukul 23:59",
        "priority": 1,
        "status": "Completed",
        "progress": 100
    },
    {
        "title": "Kerjakan tugas desain UI",
        "description": "Perlu diselesaikan minggu depan",
        "priority": 3,
        "status": "In Progress",
        "progress": 50
    },
    {
        "title": "Update dokumentasi API",
        "description": "Tambahkan endpoint terbaru",
        "priority": 2,
        "status": "Pending",
        "progress": 0
    },
    {
        "title": "Fix bug di backend",
        "description": "Bug di login menyebabkan error 500",
        "priority": 1,
        "status": "In Progress",
        "progress": 75
    },
    {
        "title": "Rapat dengan tim",
        "description": "Diskusi roadmap produk untuk Q2",
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

if task_ids:
    first_task_id = task_ids[0]
    COMMENT_URL = f"{BASE_URL}/tasks/{first_task_id}/comments/"
    comment_data = {
        "task_id": first_task_id,
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
