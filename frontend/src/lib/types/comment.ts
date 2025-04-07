import type { User } from '$lib/types/user';

export type Comment = {
	id: number;
	content: string;
	author: User;
	task_id: number;
	created_at: string;
};