<script lang="ts">
    import { Toast } from "flowbite-svelte";
    import { CheckCircleSolid, ExclamationCircleSolid } from "flowbite-svelte-icons";
    import { onMount } from "svelte";

    let visible = false;
    let message = "";
    let color: "green" | "red" = "green";

    function showToast(msg: string, type: "success" | "error" = "success") {
        message = msg;
        color = type === "success" ? "green" : "red";
        visible = true;
        setTimeout(() => (visible = false), 10000);
    }

    onMount(() => {
        showToast("Task updated successfully.", "success");
    });
</script>

{#if visible}
    <div class="fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
        <Toast color={color} divClass="bg-white dark:bg-gray-900 text-gray-800 dark:text-white shadow-lg rounded-lg" class="flex items-center space-x-4 p-4">
            <svelte:fragment slot="icon">
                {#if color === "green"}
                    <CheckCircleSolid class="w-6 h-6" />
                {:else}
                    <ExclamationCircleSolid class="w-6 h-6" />
                {/if}
                <span class="sr-only">Toast icon</span>
            </svelte:fragment>
            {message}
        </Toast>
    </div>
{/if}
