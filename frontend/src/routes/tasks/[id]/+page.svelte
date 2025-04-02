<script lang="ts">
    import { onMount } from "svelte";
    import { fetchTaskById, updateTask, deleteTask } from "$lib/api/tasks";
    import { showToast } from "$lib/stores/toast";
    import { Button, Label, Input, Textarea, Progressbar, Modal, Select, Range } from "flowbite-svelte";
    import type { Task } from "$lib/types/task";
    import { page } from "$app/stores";
	import { CaretLeftSolid } from "flowbite-svelte-icons";

    let task: Task | null = null;
    let editedTask: Task | null = null;
    let isEditing = false;
    let isDeleting = false;
    let isLoading = true;
    let taskId = "";
    $: taskId = $page.params.id;
    $: {
        if (editedTask) {
            if (editedTask.progress === 100) {
                editedTask.status = "Completed";
            } else if (editedTask.progress > 0) {
                editedTask.status = "In Progress";
            } else {
                editedTask.status = "Pending";
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
    
    function startEditing() {
        if (!task) return;
        editedTask = { ...task };
        isEditing = true;
    }

    async function saveTask() {
        if (!editedTask) return;
        try {
            await updateTask(editedTask.id, editedTask);
            isEditing = false;
            showToast("Task updated successfully", "success");
            loadTask();
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
            <div class="h-8 bg-gray-300 dark:bg-gray-700 rounded w-1/4"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-full"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-1/3"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-1/3"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-full"></div>
        </div>
    {:else if task}
        <div class="mb-6">
            <a href="/tasks" class="flex items-center gap-2 md:w-1/7 w-1/2 px-4 py-2 text-white bg-blue-600 hover:bg-blue-700  dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">
                <CaretLeftSolid class="w-5 h-5" />
                <span>Back to Tasks</span>
            </a>
        </div>
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{task.title}</h1>
            <Button on:click={startEditing} class="text-white bg-blue-600 hover:bg-blue-700 
            dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Edit</Button>
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
            <Button color="red" on:click={() => isDeleting = true} class="text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Delete Task</Button>
        </div>
    {:else}
        <p class="text-gray-500 dark:text-gray-400 text-center">Task not found</p>
    {/if}

    <!-- Edit Modal -->
    {#if isEditing && editedTask}
    <Modal bind:open={isEditing} autoclose outsideclose title="Edit Task" dialogClass="fixed top-0 start-0 end-0 h-modal md:inset-0 h-full z-50 w-full p-4 flex">
        <div class="space-y-4">
            <Label>Title
                <Input bind:value={editedTask.title} class="mt-2 dark:bg-gray-700 dark:text-white"/>
            </Label>
            <Label>Description
                <Textarea bind:value={editedTask.description} class="mt-2 dark:bg-gray-700 dark:text-white"/>
            </Label>
            <Label>Priority
                <Select bind:value={editedTask.priority} class="mt-2 dark:bg-gray-700 dark:text-white" placeholder="Select Priority">
                    <option value="1">High</option>
                    <option value="2">Medium</option>
                    <option value="3">Low</option>
                </Select>
            </Label>
            <Label>Status
                <Input bind:value={editedTask.status} class="mt-2 dark:bg-gray-700 dark:text-white cursor-not-allowed" readonly/>
            </Label>
            <div class="relative mb-8">
                <Label>Progress = {editedTask.progress}%
                    <input type="range" min="0" max="100" step="1" bind:value={editedTask.progress} class="w-full mt-2 cursor-pointer accent-primary-600" />
                </Label>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-0 -bottom-6">0%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-1/4 -translate-x-1/4 rtl:translate-x-1/2 -bottom-6">25%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-1/2 -translate-x-1/2 rtl:translate-x-1/2 -bottom-6">50%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-3/4 -translate-x-1/2 rtl:translate-x-1/4 -bottom-6">75%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute end-0 -bottom-6">100%</span>
            </div>
        </div>
        <svelte:fragment slot="footer">
            <div class="w-full flex justify-end gap-2">
                <Button on:click={saveTask} class="text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Save</Button>
                <Button color="dark" on:click={() => isEditing = false} class="text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Cancel</Button>
            </div>
        </svelte:fragment>
    </Modal>
    {/if}

    <!-- Delete Confirmation Modal -->
    {#if isDeleting}
    <Modal bind:open={isDeleting} autoclose outsideclose title="Confirm Delete" dialogClass="fixed top-0 start-0 end-0 h-modal md:inset-0 h-full z-50 w-full p-4 flex">
        <p class="text-gray-700 dark:text-gray-300">Are you sure you want to delete this task?</p>
        <div class="flex justify-end gap-2 mt-4">
            <Button color="red" on:click={removeTask} class="text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Yes, Delete</Button>
            <Button on:click={() => isDeleting = false} class="text-white bg-gray-600 hover:bg-gray-700 dark:bg-gray-500 dark:hover:bg-gray-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Cancel</Button>
        </div>
    </Modal>
    {/if}
</section>
