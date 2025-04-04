<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Modal, Label, Input, Textarea, Select, Button } from "flowbite-svelte";
    
    const dispatch = createEventDispatcher();
    
    export let open: boolean;
    export let onConfirm: () => void;
    export let onCancel: () => void;
    
    $: if (!open) {
        dispatch('close');
    }
</script>

<Modal bind:open={open} autoclose outsideclose title="Confirm Delete">
    <p class="text-gray-700 dark:text-gray-300">Are you sure you want to delete this task?</p>
    <svelte:fragment slot="footer">
        <div class="w-full flex justify-end gap-4">
            <Button on:click={onConfirm} class="text-white bg-red-600 hover:bg-red-700 
            dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Yes, Delete</Button>
            <Button on:click={onCancel} class="text-white bg-blue-600 hover:bg-blue-700 
            dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">Cancel</Button>
        </div>
    </svelte:fragment>
</Modal>
