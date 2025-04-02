<script lang="ts">
	import { Progressbar, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
	import type { Task } from "$lib/types/task";
	import { onMount } from "svelte";
	import { fetchTasks } from "$lib/api/tasks";

	let items: Task[] = [];

	async function loadTasks() {
		try {
			const fetchedData = await fetchTasks();
			if (!fetchedData || !Array.isArray(fetchedData)) {
				throw new Error("Invalid response from API");
			}
            
            console.log(fetchedData);

			items = fetchedData.slice(-4).reverse();
		} catch (error) {
			console.error("Error fetching tasks:", error);
		}
	}

	onMount(loadTasks);
</script>

<Table>
    <TableHead>
        <TableHeadCell>Date</TableHeadCell>
        <TableHeadCell>Task</TableHeadCell>
        <TableHeadCell>Priority</TableHeadCell>
        <TableHeadCell>Status</TableHeadCell>
        <TableHeadCell>Progress</TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        {#each items as item (item.id)}
            <TableBodyRow>
                <TableBodyCell class="p-3">{new Date(item.created_at).toLocaleDateString()}</TableBodyCell>
                <TableBodyCell class="p-3">{item.title}</TableBodyCell>
                <TableBodyCell class="p-3">{item.priority === 1 ? "High" : item.priority === 2 ? "Medium" : "Low"}</TableBodyCell>
                <TableBodyCell class="p-3">{item.status}</TableBodyCell>
                <TableBodyCell class="p-3">
                    <Progressbar progress={item.progress} />
                </TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>
