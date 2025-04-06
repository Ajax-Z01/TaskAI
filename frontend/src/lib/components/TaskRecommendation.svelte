<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import type { Task } from "$lib/types/task/task";
	import { Modal, Button, Progressbar, Dropdown, DropdownItem } from "flowbite-svelte";
	import { ChevronDownOutline } from 'flowbite-svelte-icons';

	export let showRecommendationModal: boolean;
	export let recommendations: Task[] = [];

	let dropdownOpen = false;
	export let selectedMode = "urgent";
	const dispatch = createEventDispatcher();
	
	const modes = [
        { key: "urgent", label: "🚨 Urgent Tasks" },
        { key: "daily", label: "📅 Daily Planner" },
        { key: "progress", label: "📊 Progress-Based" },
        { key: "impact", label: "🔝 High Impact" }
    ];
	
	function selectMode(modeKey: string) {
        selectedMode = modeKey;
    }

	function fetchRecommendations() {
		dispatch("fetchRecommendations", { mode: selectedMode });
		dropdownOpen = false;
	}

	function closeModal() {
		dispatch("close");
	}
	
	function getStatusColor(status: string) {
		return status === "Completed" ? "bg-green-500 text-white" 
			 : status === "Pending" ? "bg-yellow-500 text-white"
			 : "bg-blue-500 text-white";
	}

	function getPriorityColor(priority: number) {
		return priority === 1 ? "bg-yellow-500 text-white" 
			 : priority === 2 ? "bg-blue-500 text-white"
			 : "bg-green-500 text-white";
	}

	function getProgressColor(progress: number) {
		return progress <= 30 ? "red"
			 : progress <= 70 ? "yellow" 
			 : "green";
	}
</script>

<div class="flex flex-col-reverse sm:flex-row sm:absolute sm:top-6 sm:right-4 gap-2">
    <Button color="primary" class="hover:scale-105 transition cursor-pointer">
        Get AI Recommendations<ChevronDownOutline class="w-6 h-6 ms-2 text-white dark:text-white" />
    </Button>
	<Dropdown bind:open={dropdownOpen}>
		<div slot="header" class="px-2 py-2 text-center">
			<h3 class="text-lg font-bold text-gray-800 dark:text-gray-200">Select AI Mode</h3>
			<p class="text-sm font-semibold text-gray-800 dark:text-gray-200">
				{#each modes as mode}
					{#if mode.key === selectedMode}
						{mode.label}
					{/if}
				{/each}
			</p>
		</div>
        
        {#each modes as mode}
            <DropdownItem on:click={() => selectMode(mode.key) } class="cursor-pointer">
                {mode.label}
            </DropdownItem>
        {/each}
		
		<div slot="footer" class="px-2 py-2">
			<Button onclick={fetchRecommendations} color="green" class="flex items-center gap-2 w-full text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">
				Run AI Recommendations
			</Button>
		</div>
    </Dropdown>
</div>

<Modal bind:open={showRecommendationModal} on:close={closeModal}>
	<h3 slot="header" class="text-lg font-bold text-gray-800 dark:text-gray-200">
		✨ AI Recommendations
	</h3>

	<div class="max-h-[75vh] md:max-h-full overflow-y-auto space-y-4 p-2">
		{#if recommendations.length > 0}
			{#each recommendations as task, i}
				<div class="p-4 border rounded-lg bg-gray-100 dark:bg-gray-800 shadow-md transition hover:scale-[1.02]">
					
					<!-- Nomor Ranking -->
					<div class="flex items-center">
						<span class="px-3 py-1 text-sm font-semibold text-white rounded-lg
							{ i === 0 ? 'bg-yellow-500'
							: i === 1 ? 'bg-gray-400'
							: i === 2 ? 'bg-orange-500'
							: 'bg-primary-800' }"> 
							{i + 1}
						</span>
						<p class="text-lg font-semibold text-gray-900 dark:text-gray-100 ms-2">{task.title}</p>
					</div>

					<p class="text-sm text-gray-600 dark:text-gray-400">{task.description}</p>

					<div class="grid grid-cols-2 gap-2 mt-2">
						<span class="px-3 py-1 text-sm rounded-lg {getPriorityColor(task.priority)}">
							Priority: {task.priority}
						</span>
						<span class="px-3 py-1 text-sm bg-blue-500 text-white rounded-lg {getStatusColor(task.status)}">
							{task.status}
						</span>
					</div>

					<div class="mt-3">
						<Progressbar progress={task.progress} color={getProgressColor(task.progress)} />
					</div>
				</div>
			{/each}
		{:else}
			<p class="text-center text-gray-500">No recommendations available.</p>
		{/if}
	</div>

	<div slot="footer" class="flex justify-end">
		<Button color="red" class="hover:scale-105 transition" on:click={closeModal}>Close</Button>
	</div>
</Modal>
