<script lang="ts">
	let theme: "light" | "dark" = "light";

	function toggleTheme() {
		theme = theme === "light" ? "dark" : "light";
	}
</script>

<section class="settings">
	<h2>Settings</h2>
	<label>
		<input type="checkbox" checked={theme === "dark"} on:change={toggleTheme} />
		Dark Mode
	</label>
</section>

<style>
	.settings {
		padding: 2rem;
	}
</style>
