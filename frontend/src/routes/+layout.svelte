<script lang="ts">
	import '../app.css';
	import '../styles/global.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
</script>

<div class="layout">
	<Navbar />
	<div class="content">
		<Sidebar />
		<main class="page">
			<slot />
		</main>
	</div>
</div>

<style>
	.layout {
		display: flex;
		flex-direction: column;
		height: 100vh;
	}

	.content {
		display: flex;
		flex: 1;
	}

	.page {
		flex: 1;
		padding: 1rem;
		overflow-y: auto;
	}
</style>
