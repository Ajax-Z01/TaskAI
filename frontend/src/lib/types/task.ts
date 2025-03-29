export type Task = {
    id: number;
    title: string;
    description: string;
    priority: number;
    status: string;
    progress: number;
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
  };
  