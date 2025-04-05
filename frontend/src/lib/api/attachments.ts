import { API_URL } from "$lib/config";

export async function fetchAttachments(taskId: number) {
    const res = await fetch(`${API_URL}/tasks/${taskId}/attachments/`);
    if (!res.ok) {
        throw new Error("Failed to fetch attachments");
    }
    return res.json();
}

export async function uploadAttachment(taskId: number, file: File) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_URL}/tasks/${taskId}/attachments/`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error("Failed to upload attachment");
    }

    return res.json();
}

export async function deleteAttachment(id: number): Promise<{ message: string }> {
	const res = await fetch(`${API_URL}/attachments/${id}`, {
		method: 'DELETE',
	});

	if (!res.ok) {
		const error = await res.json().catch(() => ({}));
		throw new Error(error.detail || 'Failed to delete attachment');
	}

	return res.json();
}

export function getAttachmentUrl(fileName: string): string {
	return `${API_URL}/uploads/${fileName}`;
}