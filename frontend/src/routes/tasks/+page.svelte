<script lang="ts">
	import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    import { fetchTasks, createTask, getAIRecommendations } from "$lib/api/tasks";
    import type { Task } from "$lib/types/task";
    import { Modal, Progressbar } from 'flowbite-svelte';
    import TaskRecommendation from "$lib/components/TaskRecommendation.svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    
	const dispatch = createEventDispatcher();

    let tasks: Task[] = [];
    let filteredTasks: Task[] = [];
    let recommendations: Task[] = [];
    
    let sortBy = "title";
    let sortOrder = "asc";
    let filterStatus = "All";

    let showModal = false;
    let showRecommendationModal = false;
    let loadingRecommendations = false;
    let selectedMode = "";
    let title = "";
    let description = "";
    let priority = 1;
    let status = "Pending";
    let progress = 0;
    let loading = true;
    
    async function addTask() {
        try {
            await createTask({ title, description, priority, status, progress });
            tasks = await fetchTasks();
            title = "";
            description = "";
            priority = 1;
            status = "Pending";
            progress = 0;
            applyFilters();
            showModal = false;
        } catch (error) {
            console.error("Error adding task:", error);
        }
    }

    async function fetchRecommendations(event: Event) {
        const customEvent = event as CustomEvent<{ mode: string }>;
        try {
            loadingRecommendations = true;
            selectedMode = customEvent.detail?.mode || "unknown";
            recommendations = await getAIRecommendations(selectedMode);
            showRecommendationModal = true;
        } catch (error) {
            console.error("Error fetching AI recommendations:", error);
        } finally {
            loadingRecommendations = false;
        }

    }

    async function fetchData() {
        try {
            tasks = await fetchTasks();
            applyFilters();
        } catch (error) {
            console.error("Error fetching tasks:", error);
        } finally {
            loading = false;
        }
    }
    
    function closeModal() {
		dispatch("close");
	}

    function applyFilters() {
        let tempTasks = [...tasks];

        if (filterStatus !== "All") {
            tempTasks = tempTasks.filter(task => task.status === filterStatus);
        }

        tempTasks.sort((a, b) => {
            if (sortBy === "title") {
                return sortOrder === "asc"
                    ? a.title.localeCompare(b.title)
                    : b.title.localeCompare(a.title);
            }
            if (sortBy === "priority") {
                return sortOrder === "asc" ? a.priority - b.priority : b.priority - a.priority;
            }
            if (sortBy === "progress") {
                return sortOrder === "asc" ? a.progress - b.progress : b.progress - a.progress;
            }
            return 0;
        });

        filteredTasks = tempTasks;
    }

    onMount(fetchData);
    
    onMount(() => {
        const event = new CustomEvent("recommendations", { 
            detail: { mode: "urgent" } 
        });
        window.dispatchEvent(event);
    });
</script>

<section class="relative grid md:grid-cols-2 lg:grid-cols-3 p-4">
    <div class="col-span-full">
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Task Management</h1>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Manage your tasks efficiently.</p>
    </div>
    
    <TaskRecommendation 
        showRecommendationModal={showRecommendationModal} 
        recommendations={recommendations} 
        on:fetchRecommendations={fetchRecommendations}
        on:close={() => showRecommendationModal = false} 
    />
</section>

{#if loadingRecommendations}
<div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg text-center flex flex-col items-center">
        <p class="text-lg font-semibold text-gray-800 dark:text-white">Fetching AI Recommendations...</p>
        <p class="text-md text-gray-600 dark:text-gray-400 mt-1">Mode: {selectedMode}</p>
        <div class="mt-4 flex justify-center">
            <div class="h-10 w-10 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
    </div>
</div>
{/if}

<section class="p-6 mx-4 bg-white dark:bg-gray-900 shadow-md rounded-lg">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 gap-4">
        <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-200">Manage Tasks</h2>
        
        <div class="flex flex-col sm:flex-row gap-2 sm:gap-4 w-full sm:w-auto">
            <select bind:value={filterStatus} on:change={applyFilters} 
                class="p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white w-full sm:w-auto">
                <option value="All">All</option>
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
            </select>

            <select bind:value={sortBy} on:change={applyFilters} 
                class="p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white w-full sm:w-auto">
                <option value="title">Title</option>
                <option value="priority">Priority</option>
                <option value="progress">Progress</option>
            </select>

            <button on:click={() => { sortOrder = sortOrder === "asc" ? "desc" : "asc"; applyFilters(); }}
                class="p-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition w-full sm:w-auto">
                {sortOrder === "asc" ? "▲ Asc" : "▼ Desc"}
            </button>

            <button class="flex justify-center p-2 text-sm bg-green-500 text-white rounded-lg hover:bg-green-600 transition w-full sm:w-auto" on:click={() => showModal = true}>
                <PlusOutline/> 
                <span>Add Task</span>
            </button>
        </div>
    </div>
</section>

<section class="py-4 mx-4">
    {#if loading}
        <p class="text-center text-gray-500 dark:text-gray-400">Loading tasks...</p>
    {:else if filteredTasks.length === 0}
        <p class="text-center text-gray-500 dark:text-gray-400">No tasks available.</p>
    {:else}
        <div class="grid gap-4">
            {#each filteredTasks as task (task.id)}
                <div class="relative p-4 bg-white dark:bg-gray-900 shadow-md rounded-lg flex flex-col gap-2 transition hover:shadow-lg">
                    <span 
                        class="absolute top-5 right-4 px-3 py-1 text-white text-xs font-semibold rounded-full"
                        class:bg-red-500={task.priority === 1}
                        class:bg-yellow-500={task.priority === 2}
                        class:bg-green-500={task.priority === 3}>
                        {task.priority === 1 ? "High" : task.priority === 2 ? "Medium" : "Low"}
                    </span>

                    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">{task.title}</h3>
                    <p class="text-gray-600 dark:text-gray-300">{task.description}</p>

                    <div class="flex items-center gap-2">
                        <span 
                            class="px-3 py-1 rounded-full text-white text-sm font-medium whitespace-nowrap"
                            class:bg-green-500={task.status === 'Completed'}
                            class:bg-blue-500={task.status === 'In Progress'}
                            class:bg-yellow-500={task.status === 'Pending'}>
                            {task.status}
                        </span>

                        <Progressbar progress={task.progress} size="h-4" class="w-full" />
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</section>

<Modal bind:open={showModal} on:close={closeModal}>
    <div>
        <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-200">Add New Task</h2>
        <form class="space-y-4 mt-4" on:submit|preventDefault={addTask}>
            <input type="text" bind:value={title} placeholder="Title" 
                class="w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white" required />

            <input type="text" bind:value={description} placeholder="Description" 
                class="w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white" required />

            <select bind:value={priority} 
                class="w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                <option value="1">Low</option>
                <option value="2">Medium</option>
                <option value="3">High</option>
            </select>

            <select bind:value={status} 
                class="w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
            </select>

            <div>
                <label class="block text-sm text-gray-600 dark:text-gray-300">Progress: {progress}%
                    <input type="range" min="0" max="100" step="1" bind:value={progress} 
                    class="w-full cursor-pointer accent-blue-500" />
                </label>
            </div>

            <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition">
                Add Task
            </button>
            <button type="button" class="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition"
                on:click={() => showModal = false}>
                Cancel
            </button>
        </form>
    </div>
</Modal>

