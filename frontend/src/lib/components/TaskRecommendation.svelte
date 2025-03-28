<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import type { Task } from "$lib/types/task";
	import { Modal, Button } from "flowbite-svelte";

	export let showModal: boolean;
	export let recommendations: Task[] = [];

	const dispatch = createEventDispatcher();

	function fetchRecommendations() {
		dispatch("fetchRecommendations");
	}

	function addRecommendedTask(task: Task) {
		dispatch("addTask", task);
	}

	function closeModal() {
		dispatch("close");
	}
</script>

<div class="text-center my-6">
	<Button color="green" on:click={fetchRecommendations}>
		Get AI Recommendations
	</Button>
</div>

<Modal bind:open={showModal} on:close={closeModal}>
	<h3 slot="header" class="text-lg font-bold">AI Recommendations</h3>

	{#if recommendations.length > 0}
		<div class="space-y-4">
			{#each recommendations as task}
				<div class="p-4 border rounded-lg bg-gray-100">
					<p class="font-semibold">{task.title}</p>
					<p class="text-sm text-gray-600">{task.description}</p>
					<Button color="blue" class="mt-2" on:click={() => addRecommendedTask(task)}>
						Add to Tasks
					</Button>
				</div>
			{/each}
		</div>
	{:else}
		<p class="text-center text-gray-500">No recommendations available.</p>
	{/if}

	<div slot="footer" class="flex justify-end">
		<Button color="red" on:click={closeModal}>Close</Button>
	</div>
</Modal>
