<script lang="ts">
	const menuItems = [
		{ name: "Dashboard", path: "/" },
		{ name: "Tasks", path: "/tasks" },
		{ name: "Settings", path: "/settings" }
	];
</script>

<aside class="w-64 bg-gray-900 text-white h-full p-5 shadow-lg">
	<nav class="space-y-2">
		{#each menuItems as item}
			<a href="{item.path}" class="block px-4 py-3 rounded-lg hover:bg-gray-700 transition duration-300">
				{item.name}
			</a>
		{/each}
	</nav>
</aside>
