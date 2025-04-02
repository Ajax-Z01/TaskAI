# TaskAI

TaskAI is a task management application that leverages artificial intelligence to suggest task prioritization. The application is built using **FastAPI** for the backend and **SvelteKit** for the frontend.

## 🚀 Key Features
- **Task Management:** Create, edit, delete, and mark tasks as completed.
- **AI Recommendations:** An AI-powered algorithm suggests task order based on priority.
- **Interactive Dashboard:** A modern UI for easy task management.
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

## 🔧 How to Run the Project

### 1. Running the Backend (FastAPI)
```sh
git clone https://github.com/Ajax-Z01/TaskAI.git
cd TaskAI/backend

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
```

### 2. Running the Frontend (SvelteKit)
```sh
cd TaskAI/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at **http://localhost:5173/** (frontend) and **http://localhost:8000/** (backend).

## 📌 Roadmap
- [x] FastAPI backend for CRUD task management
- [x] AI model for task prioritization
- [x] Initial frontend setup with SvelteKit
- [x] Task detail page
- [ ] Application settings (theme, preferences, etc.)
- [ ] UI/UX improvements

## 💡 Contribution
If you would like to contribute, feel free to fork this repository and submit a pull request. All feedback and suggestions are welcome!