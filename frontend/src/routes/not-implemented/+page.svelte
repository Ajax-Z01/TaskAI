<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { goto } from "$app/navigation";
  
    function goHome() {
      goto("/");
    }
  </script>
  
  <div class="min-h-screen flex flex-col items-center justify-center px-4 text-center">
    <h1 class="text-3xl font-bold text-yellow-500 mb-4">⚠️ Fitur Belum Tersedia</h1>
    <p class="text-gray-700 dark:text-gray-300 mb-6">
      Halaman ini belum tersedia. Kami masih dalam proses mengembangkan fitur ini.
    </p>
    <Button on:click={goHome} class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white px-5 py-2 rounded-lg shadow">
      Kembali ke Beranda
    </Button>
  </div>
  