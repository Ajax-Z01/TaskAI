<script lang="ts">
    export let error: Error;
    export let status: number;
  </script>
  
  <div class="min-h-screen flex flex-col items-center justify-center px-4 text-center">
    <h1 class="text-6xl font-bold text-red-600 mb-4">{status}</h1>
    <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
      {status === 404 ? "Page Not Found" : "Something Went Wrong"}
    </h2>
    <p class="text-gray-600 dark:text-gray-300 mb-6">{error?.message || "We couldn't find what you're looking for."}</p>
    <a href="/" class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white px-5 py-2 rounded-lg shadow">
      Go Home
    </a>
  </div>
  