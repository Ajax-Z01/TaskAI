<script lang="ts">
	import '../app.css';
	import '../styles/global.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import ToastHost from '$lib/components/ToastHost.svelte';
</script>

<div class="layout">
	<Navbar />
	<div class="content">
		<Sidebar />
		<main class="page bg-gray-100 dark:bg-gray-800">
			<slot />
		</main>
	</div>
</div>

<ToastHost />
