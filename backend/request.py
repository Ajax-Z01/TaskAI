import requests

url = "http://127.0.0.1:8000/tasks/"
headers = {"Content-Type": "application/json"}

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

for task in tasks:
    response = requests.post(url, json=task, headers=headers)
    print(response.status_code, response.json())
