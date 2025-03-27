<script lang="ts">
    import type { Task } from "$lib/types/task";

    export let task: Task;
</script>

<div class="task-card">
    <h3>{task.title}</h3>
    <p>{task.description}</p>
    <span class="priority">Priority: {task.priority}</span>
    <a href="/tasks/{task.id}" class="details-link">View Details</a>
</div>

<style>
    .task-card {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 8px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    h3 {
        margin: 0;
        font-size: 1.2rem;
    }

    p {
        margin: 0.5rem 0;
        color: #555;
    }

    .priority {
        font-size: 0.9rem;
        font-weight: bold;
        color: #ff5722;
    }

    .details-link {
        display: block;
        margin-top: 0.5rem;
        color: #007bff;
        text-decoration: none;
    }

    .details-link:hover {
        text-decoration: underline;
    }
</style>
