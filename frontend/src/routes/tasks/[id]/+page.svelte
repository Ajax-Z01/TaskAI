<script lang="ts">
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { fetchTaskById } from "$lib/api/tasks";
    import type { Task } from "$lib/types/task";
    import { goto } from "$app/navigation"; // Import fungsi untuk navigasi

    let taskId = "";
    let task: Task | null = null;

    $: taskId = $page.params.id;

    onMount(async () => {
        if (taskId) {
            try {
                task = await fetchTaskById(taskId);
            } catch (error) {
                console.error("Error fetching task details:", error);
            }
        }
    });

    function goBack() {
        goto("/tasks"); // Navigasi kembali ke halaman daftar tugas
    }
</script>

<section class="task-detail">
    {#if task}
        <h2>{task.title}</h2>
        <p><strong>Description:</strong> {task.description}</p>
        <p><strong>Priority:</strong> {task.priority}</p>
        <button on:click={goBack} class="back-btn">← Back</button>
    {:else}
        <p>Loading task details...</p>
    {/if}
</section>

<style>
    .task-detail {
        padding: 2rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: auto;
        text-align: center;
    }

    h2 {
        margin-bottom: 0.5rem;
    }

    p {
        margin: 0.5rem 0;
    }

    .back-btn {
        margin-top: 1rem;
        padding: 0.5rem 1rem;
        border: none;
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }

    .back-btn:hover {
        background-color: #0056b3;
    }
</style>
