import type { Comment } from "$lib/types/comment";
import { API_URL } from "$lib/config";

export async function getCommentsByTaskId(taskId: string): Promise<Comment[]> {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`);
  if (!res.ok) throw new Error("Failed to fetch comments");
  return res.json();
}

export async function postComment(taskId: string, content: string): Promise<void> {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) throw new Error("Failed to post comment");
}
