<script lang="ts">
    import { Toast } from "flowbite-svelte";
    import { CheckCircleSolid, ExclamationCircleSolid, InfoCircleSolid } from "flowbite-svelte-icons";
    import { toast } from "$lib/stores/toast";

    let visible = false;
    let message = "";
    let color: "green" | "red" | "blue" = "green";

    const unsubscribe = toast.subscribe((data) => {
        if (data) {
            message = data.message;
            color =
                data.type === "success"
                    ? "green"
                    : data.type === "error"
                    ? "red"
                    : "blue";
            visible = true;
            setTimeout(() => (visible = false), 3000);
        }
    });
</script>

{#if visible}
    <div class="fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
        <Toast
            color={color}
            divClass="bg-white dark:bg-gray-900 text-gray-800 dark:text-white shadow-lg rounded-lg"
            class="flex items-center space-x-4 p-4"
        >
            <svelte:fragment slot="icon">
                {#if color === "green"}
                    <CheckCircleSolid class="w-6 h-6" />
                {:else if color === "red"}
                    <ExclamationCircleSolid class="w-6 h-6" />
                {:else}
                    <InfoCircleSolid class="w-6 h-6" />
                {/if}
                <span class="sr-only">Toast icon</span>
            </svelte:fragment>
            {message}
        </Toast>
    </div>
{/if}
