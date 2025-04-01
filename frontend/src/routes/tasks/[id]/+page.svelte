<script lang="ts">
    import { onMount } from "svelte";
    import { fetchTaskById, updateTask, deleteTask } from "$lib/api/tasks";
    import { showToast } from "$lib/stores/toast";
    import { Button, Input, Textarea, Progressbar, Modal } from "flowbite-svelte";
    import type { Task } from "$lib/types/task";
    import { page } from "$app/stores";

    let task: Task | null = null;
    let isEditing = false;
    let isDeleting = false;
    let isLoading = true;
    let taskId = "";
    $: taskId = $page.params.id;
    $: {
        if (task) {
            if (task.progress === 100) {
                task.status = "Completed";
            } else if (task.progress > 0) {
                task.status = "In Progress";
            } else {
                task.status = "Pending";
            }
        }
    }

    async function loadTask() {
        isLoading = true;
        try {
            task = await fetchTaskById(taskId);
        } catch (error) {
            console.error("Failed to load task", error);
        } finally {
            isLoading = false;
        }
    }

    async function saveTask() {
        if (!task) return;
        try {
            await updateTask(task.id, task);
            isEditing = false;
            showToast("Task updated successfully", "success");
        } catch (error) {
            showToast("Failed to update task", "error");
        }
    }

    async function removeTask() {
        if (!task) return;
        try {
            await deleteTask(task.id);
            showToast("Task deleted successfully", "success");
        } catch (error) {
            showToast("Failed to delete task", "error");
        }
    }

    onMount(loadTask);
</script>

<section class="p-6 mx-auto">
    {#if isLoading}
        <!-- Skeleton Loader -->
        <div class="animate-pulse space-y-4">
            <div class="h-8 bg-gray-300 dark:bg-gray-700 rounded w-3/4"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-full"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-5/6"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
        </div>
    {:else if task}
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{task.title}</h1>
            <Button on:click={() => isEditing = true} class="text-white bg-blue-500 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-800">Edit</Button>
        </div>

        <p class="text-gray-700 dark:text-gray-300 mb-2">{task.description}</p>

        <div class="mb-4">
            <Progressbar progress={task.progress} />
            <p class="text-sm text-gray-500 dark:text-gray-400">{task.progress}% completed</p>
        </div>

        <!-- Status & Priority -->
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <strong class="text-gray-900 dark:text-white">Priority:</strong>
                <span class="px-2 py-1 text-xs font-semibold text-white rounded-full"
                    class:bg-red-500={task.priority === 1}
                    class:bg-yellow-500={task.priority === 2}
                    class:bg-green-500={task.priority === 3}>
                    {task.priority === 1 ? "High" : task.priority === 2 ? "Medium" : "Low"}
                </span>
            </div>
            <div>
                <strong class="text-gray-900 dark:text-white">Status:</strong>
                <span class="px-2 py-1 text-xs font-semibold text-white rounded-full"
                    class:bg-blue-500={task.status === "In Progress"}
                    class:bg-gray-500={task.status === "Pending"}
                    class:bg-green-500={task.status === "Completed"} >
                    {task.status}
                </span>
            </div>
            <div class="text-gray-900 dark:text-white"><strong>Created:</strong> {new Date(task.created_at).toLocaleDateString()}</div>
            <div class="text-gray-900 dark:text-white"><strong>Updated:</strong> {new Date(task.updated_at).toLocaleDateString()}</div>
        </div>

        <div class="flex justify-end gap-2">
            <Button color="red" on:click={() => isDeleting = true} class="bg-red-600 hover:bg-red-800 dark:bg-red-700 dark:hover:bg-red-900">Delete Task</Button>
        </div>
    {:else}
        <p class="text-gray-500 dark:text-gray-400 text-center">Task not found</p>
    {/if}

    <!-- Edit Modal -->
    {#if isEditing && task}
    <Modal bind:open={isEditing} title="Edit Task" class="dark:bg-gray-800">
        <div class="space-y-4">
            <label for="title" class="block text-sm font-medium text-gray-900 dark:text-gray-200">Title
                <Input bind:value={task.title} class="mt-1 dark:bg-gray-700 dark:text-white"/>
            </label>
            <label for="description" class="block text-sm font-medium text-gray-900 dark:text-gray-200">Description
                <Textarea bind:value={task.description} class="mt-1 dark:bg-gray-700 dark:text-white"/>
            </label>
            <label for="priority" class="block text-sm font-medium text-gray-900 dark:text-gray-200">Priority
                <select bind:value={task.priority} class="mt-1 dark:bg-gray-700 dark:text-white">
                    <option value="1">High</option>
                    <option value="2">Medium</option>
                    <option value="3">Low</option>
                </select>
            </label>
            <label for="status" class="block text-sm font-medium text-gray-900 dark:text-gray-200">Status
                <select bind:value={task.status} class="mt-1 dark:bg-gray-700 dark:text-white" disabled>
                    <option value="Pending">Pending</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                </select>
            </label>
            <label for="progress" class="block text-sm font-medium text-gray-900 dark:text-gray-200">Progress
                <input type="range" min="0" max="100" step="1" bind:value={task.progress} class="w-full cursor-pointer accent-blue-500" />
            </label>
        </div>
        <div class="flex justify-end gap-2 mt-4">
            <Button on:click={saveTask} class="bg-blue-500 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-800 text-white">Save</Button>
            <Button color="dark" on:click={() => isEditing = false} class="bg-red-500 hover:bg-red-700 dark:bg-red-600 dark:hover:bg-red-800 text-white">Cancel</Button>
        </div>
    </Modal>
    {/if}

    <!-- Delete Confirmation Modal -->
    {#if isDeleting}
        <Modal bind:open={isDeleting} title="Confirm Delete" class="dark:bg-gray-800">
            <p class="text-gray-700 dark:text-gray-300">Are you sure you want to delete this task?</p>
            <div class="flex justify-end gap-2 mt-4">
                <Button color="red" on:click={removeTask} class="bg-red-600 hover:bg-red-800 dark:bg-red-700 dark:hover:bg-red-900 text-white">Yes, Delete</Button>
                <Button on:click={() => isDeleting = false} class="bg-gray-500 hover:bg-gray-700 dark:bg-gray-600 dark:hover:bg-gray-800 text-white">Cancel</Button>
            </div>
        </Modal>
    {/if}
</section>
