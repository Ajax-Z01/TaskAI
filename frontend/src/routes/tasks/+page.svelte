<script lang="ts">
    import { onMount } from "svelte";
    import { fetchTasks, createTask, getAIRecommendations } from "$lib/api/tasks";
    import type { Task } from "$lib/types/task";
    import TaskCard from "$lib/components/TaskCard.svelte";
	import TaskRecommendation from "$lib/components/TaskRecommendation.svelte";
    
    let tasks: Task[] = [];
    let recommendations: Task[] = [];
    let showModal = false;
    let title = "";
    let description = "";
    let priority = 1;

    async function addTask() {
        try {
            await createTask({ title, description, priority });
            tasks = await fetchTasks();
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

    onMount(async () => {
        try {
            tasks = await fetchTasks();
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    });
</script>

<section class="p-6 max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">Tasks</h2>
    <div class="grid gap-4">
        {#each tasks as task}
            <TaskCard {task} />
        {/each}
    </div>
</section>

<section class="p-6 max-w-3xl mx-auto">
    <h2 class="text-xl font-semibold mb-4">Add Task</h2>
    <form class="space-y-4 bg-white p-4 rounded-lg shadow-md" on:submit|preventDefault={addTask}>
        <input type="text" bind:value={title} placeholder="Title" class="w-full p-2 border rounded" required />
        <input type="text" bind:value={description} placeholder="Description" class="w-full p-2 border rounded" required />
        <input type="number" bind:value={priority} min="1" max="3" class="w-full p-2 border rounded" required />
        <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Add Task</button>
    </form>
</section>

<TaskRecommendation 
	showModal={showModal} 
	recommendations={recommendations} 
	on:fetchRecommendations={fetchRecommendations} 
	on:addTask={(e) => addRecommendedTask(e.detail)} 
	on:close={() => showModal = false} 
/>
