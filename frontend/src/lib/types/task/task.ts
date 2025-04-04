import type { Attachment } from "./attachment";

export type Task = {
	id: number;
	title: string;
	description: string;
	priority: number;
	status: string;
	progress: number;
	attachments: Attachment[];
	created_at: string;
	updated_at: string;
};

export type NewTask = {
	title: string;
	description: string;
	priority: number;
	status: string;
	progress: number;
  attachments: Attachment[];
};