<script lang="ts">
    export let title = "TaskAI";
</script>

<header class="bg-gray-900 text-white shadow-md">
    <div class="container mx-auto flex items-center justify-between p-4">
        <h1 class="text-xl font-bold">{title}</h1>
        <nav class="space-x-4">
            <a href="/tasks" class="hover:text-gray-300 transition duration-300">Tasks</a>
            <a href="/settings" class="hover:text-gray-300 transition duration-300">Settings</a>
        </nav>
    </div>
</header>
