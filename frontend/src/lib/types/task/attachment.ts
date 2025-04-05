export type Attachment = {
	id: number;
	original_name: string;
	filename: string;
	url: string;
	task_id: number;
	created_at: string;
};

export type RawAttachment = {
	id: number;
	task_id: number;
	original_name: string;
	file_name: string;
	file_url: string;
	uploaded_at: string;
  };
  