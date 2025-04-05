<script lang="ts">
    import { onMount } from "svelte";
    import { fetchTaskById, updateTask, deleteTask } from "$lib/api/tasks";
    import { showToast } from "$lib/stores/toast";
    import { Button } from "flowbite-svelte";
    import type { Task } from "$lib/types/task/task";
    import { page } from "$app/stores";
	import { CaretLeftSolid } from "flowbite-svelte-icons";
	import TaskInfo from "$lib/components/TaskInfo.svelte";
	import TaskComments from "$lib/components/TaskComments.svelte";
	import TaskEditModal from "$lib/components/TaskEditModal.svelte";
	import DeleteConfirmationModal from "$lib/components/DeleteConfirmationModal.svelte";
    import { goto } from "$app/navigation";
	import TaskAttachmentsList from "$lib/components/TaskAttachmentsList.svelte";
	import TaskAttachmentsModal from "$lib/components/TaskAttachmentsModal.svelte";

    let task: Task | null = null;
    let editedTask: Task | null = null;
    let isEditing = false;
    let isSaving = false;
    let isDeleting = false;
    let isAttachmentModalOpen = false;
    let isLoading = true;
    let attachmentsListRef: InstanceType<typeof TaskAttachmentsList> | null = null;
    let taskId = "";
    $: taskId = $page.params.id;

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
        } finally {
            isSaving = false;
        }
    }

    async function removeTask() {
        if (!task) return;
        try {
            await deleteTask(task.id);
            showToast("Task deleted successfully", "success");
            goto("/tasks");
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
            <div class="flex gap-4">
                <Button on:click={() => isAttachmentModalOpen = true}
                class="text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">➕ Add Attachment </Button>
                <Button on:click={startEditing} class="text-white bg-blue-600 hover:bg-blue-700 
                dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Edit </Button>
            </div>
        </div>
        
        <TaskInfo {...task} />
        
        <TaskAttachmentsList bind:this={attachmentsListRef} taskId={taskId} />
        
        <div class="flex justify-end gap-2">
            <Button color="red" on:click={() => isDeleting = true} class="text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Delete Task</Button>
        </div>
        
        <TaskComments taskId={taskId} />
    {:else}
        <p class="text-gray-500 dark:text-gray-400 text-center">Task not found</p>
    {/if}
    
    <!-- Attachmeent Modal -->
    {#if isAttachmentModalOpen}
        <TaskAttachmentsModal
            taskId={taskId}
            bind:open={isAttachmentModalOpen}
            on:uploaded={() => attachmentsListRef?.reload()}
        />
    {/if}

    <!-- Edit Modal -->
    {#if isEditing && editedTask}
        <TaskEditModal
            bind:open={isEditing}
            editedTask={editedTask}
            on:close={() => isEditing = false}
            onSave={saveTask}
            onCancel={() => isEditing = false}
            isSaving={isSaving}
        />
    {/if}

    <!-- Delete Confirmation Modal -->
    {#if isDeleting}
        <DeleteConfirmationModal 
            bind:open={isDeleting}
            on:close={() => isDeleting = false}
            onConfirm={removeTask}
            onCancel={() => isDeleting = false}
        />
    {/if}
</section>
