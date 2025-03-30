export const API_URL = "http://127.0.0.1:8000";

export async function fetchTasks() {
    const res = await fetch(`${API_URL}/tasks/`);
    if (!res.ok) {
        throw new Error("Failed to fetch tasks");
    }
    return res.json();
}

export async function fetchTaskById(id: string) {
    const res = await fetch(`http://127.0.0.1:8000/tasks/${id}`);
    if (!res.ok) {
        throw new Error("Failed to fetch task details");
    }
    return await res.json();
}

export async function createTask(task: { title: string; description: string; priority: number, status: string, progress: number }) {
    const res = await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task),
    });
    if (!res.ok) {
        throw new Error("Failed to create task");
    }
    return res.json();
}

export async function getAIRecommendations(mode: string = "urgent") {
    const res = await fetch(`${API_URL}/tasks/recommendations/?mode=${mode}`);
    if (!res.ok) {
        throw new Error("Failed to fetch recommendations");
    }
    return res.json();
}
