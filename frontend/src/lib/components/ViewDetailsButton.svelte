<script lang="ts">
    import { goto } from "$app/navigation";
	import { Button } from "flowbite-svelte";
    export let taskId: number;
</script>

<Button color="blue" class="flex items-center gap-2 px-3 py-2 mt-2 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600 transition cursor-pointer"
    on:click={() => goto(`/tasks/${taskId}`)}>
    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m0 0l3-3m-3 3l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    View Details
</Button>