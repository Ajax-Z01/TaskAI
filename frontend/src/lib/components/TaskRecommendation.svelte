<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import type { Task } from "$lib/types/task";

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
	<button 
		on:click={fetchRecommendations} 
		class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition">
		Get AI Recommendations
	</button>
</div>

{#if showModal}
	<!-- Overlay -->
	<div class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50">
		<!-- Modal -->
		<div class="bg-white p-6 rounded-lg shadow-xl max-w-md w-full transform scale-100 transition ease-out duration-300">
			<h2 class="text-lg font-bold mb-4 text-center">AI Recommendations</h2>

			{#if recommendations.length > 0}
				<div class="space-y-4">
					{#each recommendations as task}
						<div class="p-4 border rounded-lg bg-gray-100">
							<p class="font-semibold">{task.title}</p>
							<p class="text-sm text-gray-600">{task.description}</p>
							<button 
								on:click={() => addRecommendedTask(task)} 
								class="mt-2 bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition">
								Add to Tasks
							</button>
						</div>
					{/each}
				</div>
			{:else}
				<p class="text-center text-gray-500">No recommendations available.</p>
			{/if}

			<button 
				on:click={closeModal} 
				class="mt-4 w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition">
				Close
			</button>
		</div>
	</div>
{/if}
