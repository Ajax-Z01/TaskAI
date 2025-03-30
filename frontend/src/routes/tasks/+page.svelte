<script lang="ts">
    import { onMount } from "svelte";
    import { fetchTasks, createTask, getAIRecommendations } from "$lib/api/tasks";
    import type { Task } from "$lib/types/task";
    import { Progressbar } from 'flowbite-svelte';
    import TaskRecommendation from "$lib/components/TaskRecommendation.svelte";
    
    let tasks: Task[] = [];
    let filteredTasks: Task[] = [];
    let recommendations: Task[] = [];
    
    let sortBy = "title";
    let sortOrder = "asc";
    let filterStatus = "All";
    
    let showModal = false;
    let title = "";
    let description = "";
    let priority = 1;
    let loading = true;

    async function addTask() {
        try {
            await createTask({ title, description, priority });
            tasks = await fetchTasks();
            title = "";
            description = "";
            priority = 1;
            applyFilters();
        } catch (error) {
            console.error("Error adding task:", error);
        }
    }
    
    async function fetchRecommendations() {
        try {
            recommendations = await getAIRecommendations();
            showModal = true;
        } catch (error) {
            console.error("Error fetching AI recommendations:", error);
        }
    }

    async function addRecommendedTask(task: Task) {
        try {
            await createTask(task);
            tasks = await fetchTasks();
        } catch (error) {
            console.error("Error adding recommended task:", error);
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
</script>

<section class="p-6 max-w-4xl mx-auto text-center">
    <h1 class="text-4xl font-bold text-gray-800 dark:text-white mb-6">Task Management</h1>
</section>

<section class="p-6 max-w-4xl mx-auto bg-white dark:bg-gray-900 shadow-md rounded-lg">
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-200">Manage Tasks</h2>
        
        <div class="flex gap-4">
            <select bind:value={filterStatus} on:change={applyFilters} class="p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                <option value="All">All</option>
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
            </select>

            <select bind:value={sortBy} on:change={applyFilters} class="p-2 border rounded dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                <option value="title">Title</option>
                <option value="priority">Priority</option>
                <option value="progress">Progress</option>
            </select>

            <button on:click={() => { sortOrder = sortOrder === "asc" ? "desc" : "asc"; applyFilters(); }}
                class="p-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
                {sortOrder === "asc" ? "▲ Asc" : "▼ Desc"}
            </button>
        </div>
    </div>
</section>

<section class="max-w-4xl py-4 mx-auto">
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
                        class:bg-red-500={task.priority === 3}
                        class:bg-yellow-500={task.priority === 2}
                        class:bg-green-500={task.priority === 1}>
                        {task.priority === 3 ? "High" : task.priority === 2 ? "Medium" : "Low"}
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


<section class="p-6 max-w-4xl mx-auto bg-white dark:bg-gray-900 shadow-md rounded-lg transition hover:shadow-lg">
    <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-200">Add New Task</h2>
    <form class="space-y-4" on:submit|preventDefault={addTask}>
        <div>
            <label class="block text-gray-600 dark:text-gray-300 text-sm">Title
                <input type="text" bind:value={title} placeholder="Enter title" class="w-full p-2 border rounded focus:ring focus:ring-blue-300 dark:bg-gray-800 dark:border-gray-700 dark:text-white" required />
            </label>
        </div>
        <div>
            <label class="block text-gray-600 dark:text-gray-300 text-sm">Description
                <input type="text" bind:value={description} placeholder="Enter description" class="w-full p-2 border rounded focus:ring focus:ring-blue-300 dark:bg-gray-800 dark:border-gray-700 dark:text-white" required />
            </label>
        </div>
        <div>
            <label class="block text-gray-600 dark:text-gray-300 text-sm">Priority
                <select bind:value={priority} class="w-full p-2 border rounded focus:ring focus:ring-blue-300 dark:bg-gray-800 dark:border-gray-700 dark:text-white">
                    <option value="1">Low</option>
                    <option value="2">Medium</option>
                    <option value="3">High</option>
                </select>
            </label>
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition dark:bg-blue-600 dark:hover:bg-blue-700">Add Task</button>
    </form>
</section>

<TaskRecommendation 
    showModal={showModal} 
    recommendations={recommendations} 
    on:fetchRecommendations={fetchRecommendations} 
    on:addTask={(e) => addRecommendedTask(e.detail)} 
    on:close={() => showModal = false} 
/>