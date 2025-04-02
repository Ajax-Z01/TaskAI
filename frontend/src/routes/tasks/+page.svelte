<script lang="ts">
	import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    import { fetchTasks, createTask, getAIRecommendations } from "$lib/api/tasks";
    import type { Task } from "$lib/types/task";
    import { Input, Label, Modal, Progressbar, Select } from 'flowbite-svelte';
    import TaskRecommendation from "$lib/components/TaskRecommendation.svelte";
    import { CirclePlusSolid } from "flowbite-svelte-icons";
	import ViewDetailsButton from "$lib/components/ViewDetailsButton.svelte";
    
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
    let priorities = [
        { value: 1, name: "Low" },
        { value: 2, name: "Medium" },
        { value: 3, name: "High" }
    ];

    let statuses = [
        { value: "Pending", name: "Pending" },
        { value: "In Progress", name: "In Progress" },
        { value: "Completed", name: "Completed" }
    ];
    
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
                class="p-2 text-sm text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 duration-200 ease-in-out rounded-lg shadow-md cursor-pointer transition w-full sm:w-auto">
                {sortOrder === "asc" ? "▲ Asc" : "▼ Desc"}
            </button>

            <button class="flex justify-center p-2 text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer w-full sm:w-auto" on:click={() => showModal = true}>
                <CirclePlusSolid class="w-5 h-5 mt-1 mr-1"/> 
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
                <div class="relative p-4 bg-white dark:bg-gray-900 shadow-md rounded-lg flex flex-col gap-3 transition hover:shadow-lg hover:-translate-y-1">
                    <!-- Priority Label -->
                    <span 
                        class="absolute top-4 right-4 px-3 py-1 text-white text-xs font-semibold rounded-full"
                        class:bg-red-500={task.priority === 1}
                        class:bg-yellow-500={task.priority === 2}
                        class:bg-green-500={task.priority === 3}>
                        {task.priority === 1 ? "High" : task.priority === 2 ? "Medium" : "Low"}
                    </span>

                    <!-- Task Title -->
                    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">{task.title}</h3>
                    <p class="text-gray-600 dark:text-gray-300 text-sm">{task.description}</p>

                    <!-- Status & Progress -->
                    <div class="flex items-center gap-3">
                        <span 
                            class="px-3 py-1 rounded-full text-white text-xs font-medium whitespace-nowrap"
                            class:bg-green-500={task.status === 'Completed'}
                            class:bg-blue-500={task.status === 'In Progress'}
                            class:bg-yellow-500={task.status === 'Pending'}>
                            {task.status}
                        </span>

                        <Progressbar progress={task.progress} size="h-4" class="w-full" />
                    </div>

                    <!-- View Details Button -->
                    <div class="flex justify-end">
                        <ViewDetailsButton taskId={task.id} />
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</section>

<Modal bind:open={showModal} autoclose outsideclose >
    <div>
        <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-200">Add New Task</h2>
        <form class="space-y-4 mt-4" on:submit|preventDefault={addTask}>
            <Label>Title
                <Input type="text" bind:value={title} placeholder="Title" class="mt-2 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white" required />
            </Label>

            <Label>Description
                <Input type="text" bind:value={description} placeholder="Description" class="mt-2 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white" required />
            </Label>

            <Label>Priority
                <Select bind:value={priority} items={priorities} class="mt-2 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white"/>
            </Label>

            <Label>Status
                <Select bind:value={status} items={statuses} class="mt-2 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white"/>
            </Label>

            <div class="relative mb-8">
                <Label>Progress: {progress}%
                    <input type="range" min="0" max="100" step="1" bind:value={progress} 
                    class="mt-2 w-full cursor-pointer accent-primary-600" />
                </Label>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-0 -bottom-6">0%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-1/4 -translate-x-1/4 rtl:translate-x-1/2 -bottom-6">25%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-1/2 -translate-x-1/2 rtl:translate-x-1/2 -bottom-6">50%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-3/4 -translate-x-1/2 rtl:translate-x-1/4 -bottom-6">75%</span>
                <span class="text-sm text-gray-500 dark:text-gray-400 absolute end-0 -bottom-6">100%</span>
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

