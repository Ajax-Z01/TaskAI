import { writable } from 'svelte/store';

export type Task = {
	id: number;
	title: string;
	completed: boolean;
};

const initialTasks: Task[] = [
	{ id: 1, title: "Build TaskAI frontend", completed: false },
	{ id: 2, title: "Connect backend API", completed: false }
];

export const taskStore = writable<Task[]>(initialTasks);

export const addTask = (title: string) => {
	taskStore.update(tasks => {
		const newTask = { id: tasks.length + 1, title, completed: false };
		return [...tasks, newTask];
	});
};

export const toggleTaskCompletion = (id: number) => {
	taskStore.update(tasks =>
		tasks.map(task =>
			task.id === id ? { ...task, completed: !task.completed } : task
		)
	);
};

export const removeTask = (id: number) => {
	taskStore.update(tasks => tasks.filter(task => task.id !== id));
};
