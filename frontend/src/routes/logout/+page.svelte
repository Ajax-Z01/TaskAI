<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "flowbite-svelte";
    import { goto } from "$app/navigation";
  
    onMount(() => {
    });
  
    function goHome() {
      goto("/");
    }
  </script>
  
  <div class="min-h-screen flex flex-col items-center justify-center text-center px-4 mt-10">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">🚫 Logout Belum Tersedia</h1>
    <p class="text-gray-600 dark:text-gray-300 mb-6">
      Fitur logout belum diimplementasikan saat ini. Kami akan menambahkannya di versi mendatang.
    </p>
    <Button on:click={goHome} class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white px-5 py-2 rounded-lg shadow cursor-pointer">
      Kembali ke Beranda
    </Button>
  </div>
  