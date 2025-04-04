<script lang="ts">
    import { Progressbar } from "flowbite-svelte";
    export let description: string;
    export let priority: number;
    export let status: string;
    export let progress: number;
    export let created_at: string;
    export let updated_at: string;
</script>

<p class="text-gray-700 dark:text-gray-300 mb-2">{description}</p>

<div class="mb-4">
    <Progressbar progress={progress} />
    <p class="text-sm text-gray-500 dark:text-gray-400">{progress}% completed</p>
</div>

<div class="grid grid-cols-2 gap-4 mb-4">
    <div>
        <strong class="text-gray-900 dark:text-white">Priority:</strong>
        <span class="px-2 py-1 text-xs font-semibold text-white rounded-full"
            class:bg-red-500={priority === 1}
            class:bg-yellow-500={priority === 2}
            class:bg-green-500={priority === 3}>
            {priority === 1 ? "High" : priority === 2 ? "Medium" : "Low"}
        </span>
    </div>
    <div>
        <strong class="text-gray-900 dark:text-white">Status:</strong>
        <span class="px-2 py-1 text-xs font-semibold text-white rounded-full"
            class:bg-blue-500={status === "In Progress"}
            class:bg-gray-500={status === "Pending"}
            class:bg-green-500={status === "Completed"}>
            {status}
        </span>
    </div>
    <div class="text-gray-900 dark:text-white"><strong>Created:</strong> {new Date(created_at).toLocaleDateString()}</div>
    <div class="text-gray-900 dark:text-white"><strong>Updated:</strong> {new Date(updated_at).toLocaleDateString()}</div>
</div>
