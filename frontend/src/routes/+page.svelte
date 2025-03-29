<script lang="ts">
	import { Card, Progressbar } from 'flowbite-svelte';
	import { ClipboardListSolid, CheckCircleSolid, ClockSolid } from 'flowbite-svelte-icons';
	import TableRecentTasks from '$lib/components/TableRecentTask.svelte';
	import { onMount } from 'svelte';
	import { fetchTasks } from '$lib/api/tasks';

	let title = "Dashboard TaskAI";
	let items = [];

	let totalTasks = 0;
	let completedTasks = 0;
	let pendingTasks = 0;
	let progressPercentage = 0;

	async function loadTasks() {
		try {
			const fetchedItems = await fetchTasks();
			if (!fetchedItems || !Array.isArray(fetchedItems)) {
				throw new Error("Invalid response from API");
			}

			items = [...fetchedItems];

			totalTasks = items.length;
			completedTasks = items.filter(t => t.status === "Completed").length;
			pendingTasks = items.filter(t => t.status === "Pending").length;
			progressPercentage = totalTasks > 0 ? Math.floor((completedTasks / totalTasks) * 100) : 0;

		} catch (error) {
			console.error("Error fetching tasks:", error);
		}
	}

	onMount(loadTasks);
</script>


<section class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 p-4">
	<!-- Title and Message -->
	<div class="col-span-full">
		<h1 class="text-2xl font-bold text-gray-800 dark:text-white">{title}</h1>
		<p class="text-gray-600 dark:text-gray-300">Here is your item overview.</p>
	</div>
	
	<!-- Card Total Tasks -->
	<Card class="shadow-md border border-gray-200 dark:border-gray-700 flex items-center p-4 space-x-4">
		<ClipboardListSolid class="w-10 h-10 text-blue-500 ml-4" />
		<div class="flex flex-col items-center">
			<h5 class="text-lg font-semibold text-blue-500">Total Tasks</h5>
			<p class="text-3xl font-bold text-gray-800 dark:text-white">{totalTasks}</p>
		</div>
	</Card>

	<!-- Card Completed Tasks -->
	<Card class="shadow-md border border-gray-200 dark:border-gray-700 flex items-center p-4 space-x-4">
		<CheckCircleSolid class="w-10 h-10 text-green-500 ml-4" />
		<div class="flex flex-col items-center">
			<h5 class="text-lg font-semibold text-green-500">Completed Tasks</h5>
			<p class="text-3xl font-bold text-gray-800 dark:text-white">{completedTasks}</p>
		</div>
	</Card>

	<!-- Card Pending Tasks -->
	<Card class="shadow-md border border-gray-200 dark:border-gray-700 flex items-center p-4 space-x-4">
		<ClockSolid class="w-10 h-10 text-yellow-500 ml-4" />
		<div class="flex flex-col items-center">
			<h5 class="text-lg font-semibold text-yellow-500">Pending Tasks</h5>
			<p class="text-3xl font-bold text-gray-800 dark:text-white">{pendingTasks}</p>
		</div>
	</Card>

	<!-- Progress Bar -->
	<div class="col-span-full">
		<h3 class="text-lg font-semibold text-gray-800 dark:text-white">Overall Progress</h3>
		<Progressbar progress={progressPercentage} />
		<p class="text-sm text-gray-600 dark:text-gray-300 mt-2">{progressPercentage}% completed</p>
	</div>

	<!-- Tasks Table -->
	<div class="col-span-full">
		<h3 class="text-lg font-semibold mb-3 text-gray-800 dark:text-white">Recent Tasks</h3>
		<TableRecentTasks />
	</div>
</section>