# 🤖 TaskAI

TaskAI is a task management application that leverages artificial intelligence to suggest task prioritization. The application is built using **FastAPI** for the backend and **SvelteKit** for the frontend.

## 🚀 Key Features
- **Task Management:** Create, edit, delete, and mark tasks as completed.
- **AI Recommendations:** An AI-powered algorithm suggests task order based on priority.
- **Interactive Dashboard:** A modern UI for easy task management.
- **Comments:** Add comments to tasks for better collaboration.
- **File Attachments:** Attach files to tasks for better context.
- **Flexible Settings:** Dark/light theme, user preferences, and more (coming soon).

## 📂 Project Structure
```
TaskAI/
├── backend/               # Backend using FastAPI
│   ├── main.py            # Main entry point for FastAPI
│   ├── models.py          # ORM model definitions (SQLAlchemy)
│   ├── ai.py              # AI model for task recommendations
│   ├── database.py        # Database connection and configuration
│   └── requirements.txt   # Python dependencies
├── frontend/              # Frontend using SvelteKit
│   ├── src/
│   │   ├── routes/        # Application pages and navigation
│   │   ├── lib/           # Utility functions and shared modules
│   │   ├── styles/        # Global and component-specific styles
│   ├── static/            # Static assets (favicon, images, etc.)
│   ├── package.json       # Project configuration and Node.js dependencies
│   ├── svelte.config.js   # SvelteKit configuration
│   ├── vite.config.js     # Vite configuration
└── README.md              # Project documentation
```

---

## 🔧 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Ajax-Z01/TaskAI.git
cd TaskAI
```

### 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate       # On Unix/Mac
venv\Scripts\activate        # On Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

> Backend will run at `http://localhost:8000`

### 3. Frontend Setup (SvelteKit)

```bash
cd frontend
pnpm install    # or npm install / yarn install
pnpm run dev
```

> Frontend will be available at `http://localhost:5173`

---

## 📡 API Endpoints Overview

### Users
- `POST /users/`
- `GET /users/`

### Tasks
- `GET /tasks/`
- `GET /tasks/{id}`
- `POST /tasks/`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`
- `GET /tasks/recommendations/?mode={urgent|balanced}`

### Comments
- `POST /tasks/{id}/comments/`
- `GET /tasks/{id}/comments/`

### Attachments
- `POST /tasks/{id}/attachments/`
- `GET /tasks/{id}/attachments/`
- `DELETE /attachments/{id}`
- `GET /uploads/{filename}`

---

## 🧠 AI Recommendation Modes

- `urgent`: Prioritize tasks based on urgency and deadlines.
- `daily`: Balance tasks based on daily workload and deadlines.
- `progress`: Focus on tasks that are in progress or need immediate attention.
- `impact`: Prioritize tasks based on their impact and importance.

---

## 📌 Roadmap

- Authentication & User Roles
- Advanced AI Prioritization
- UI/UX Enhancements
- Settings & Customization
- Reports & Analytics
- Mobile Support

---

## 🤝 Contribution

1. Fork the repository  
2. Create your feature branch  
3. Commit your changes  
4. Push and open a Pull Request

---

## 📃 License

This project is licensed under the MIT License.

---

## 🙌 Author

Made with ❤️ by [Ajax-Z01](https://github.com/Ajax-Z01)
