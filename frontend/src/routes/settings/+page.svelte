<script lang="ts">
    import { onMount } from "svelte";
    import { Select, Label, DarkMode } from "flowbite-svelte";
    import { writable } from "svelte/store";

    const language = writable<string>("en");
    const themeColor = writable<string>("blue");

    onMount(() => {
        language.set(localStorage.getItem("language") || "en");
        themeColor.set(localStorage.getItem("themeColor") || "blue");
    });

    language.subscribe(value => localStorage.setItem("language", value));
    themeColor.subscribe(value => localStorage.setItem("themeColor", value));
</script>

<section class="p-4">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1>
	<p class="text-gray-700 dark:text-gray-300 mb-4">Customize your preferences.</p>

    <div class="mb-4">
        <Label class="flex items-center justify-between">Dark Mode
			<DarkMode class="cursor-pointer" size="lg" />
		</Label>
    </div>

    <div class="mb-4">
		<Label class="block text-gray-700 dark:text-gray-300">Language
			<Select bind:value={$language} class="mt-2 w-full dark:bg-gray-700 dark:text-white">
				<option value="en">English</option>
				<option value="id">Bahasa Indonesia</option>
				<option value="es">Español</option>
				<option value="fr">Français</option>
			</Select>
		</Label>
    </div>

    <div class="mb-4">
        <Label class="block text-gray-700 dark:text-gray-300">Theme Color
			<Select bind:value={$themeColor} class="mt-2 w-full dark:bg-gray-700 dark:text-white">
				<option value="blue">Blue</option>
				<option value="red">Red</option>
				<option value="green">Green</option>
				<option value="purple">Purple</option>
			</Select>
		</Label>
    </div>
</section>
