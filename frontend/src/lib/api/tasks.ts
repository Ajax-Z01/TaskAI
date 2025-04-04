import { API_URL } from "$lib/config";
import type { Task, NewTask } from "$lib/types/task/task";

// Get all tasks
export async function fetchTasks(): Promise<Task[]> {
    const res = await fetch(`${API_URL}/tasks/`);
    if (!res.ok) throw new Error("Failed to fetch tasks");
    return res.json();
}

// Get single task
export async function fetchTaskById(id: string): Promise<Task> {
    const res = await fetch(`${API_URL}/tasks/${id}`);
    if (!res.ok) throw new Error("Failed to fetch task details");
    return res.json();
}

// Create a new task
export async function createTask(task: NewTask): Promise<Task> {
    const res = await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task),
    });
    if (!res.ok) throw new Error("Failed to create task");
    return res.json();
}


// Update a task
export async function updateTask(id: number, updates: Partial<Omit<Task, "id" | "createdAt" | "updatedAt">>): Promise<Task> {
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error("Failed to update task");
    return res.json();
}

// Delete a task
export async function deleteTask(id: number): Promise<{ success: boolean }> {
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE"
    });
    if (!res.ok) throw new Error("Failed to delete task");
    return { success: true };
}

// Get AI Recommendations
export async function getAIRecommendations(mode: string = "urgent"): Promise<Task[]> {
    const res = await fetch(`${API_URL}/tasks/recommendations/?mode=${mode}`);
    if (!res.ok) throw new Error("Failed to fetch recommendations");
    return res.json();
}
