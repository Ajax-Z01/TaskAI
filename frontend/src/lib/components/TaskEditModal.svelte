<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Modal, Label, Input, Textarea, Select, Button } from "flowbite-svelte";

    const dispatch = createEventDispatcher();

    export let open: boolean;
    export let editedTask: any;
    export let onSave: () => void;
    export let onCancel: () => void;
    export let isSaving: boolean = false;

    $: if (!open) {
        dispatch('close');
    }
</script>

<Modal bind:open={open} autoclose outsideclose title="Edit Task">
    <div class="space-y-4">
        <Label>Title
            <Input bind:value={editedTask.title} class="mt-2 dark:bg-gray-700 dark:text-white" />
        </Label>
        <Label>Description
            <Textarea bind:value={editedTask.description} class="mt-2 dark:bg-gray-700 dark:text-white" />
        </Label>
        <Label>Priority
            <Select bind:value={editedTask.priority} class="mt-2 dark:bg-gray-700 dark:text-white cursor-pointer">
                <option value="1">High</option>
                <option value="2">Medium</option>
                <option value="3">Low</option>
            </Select>
        </Label>
        <Label>Status
            <Input bind:value={editedTask.status} readonly class="mt-2 dark:bg-gray-700 dark:text-white cursor-not-allowed" />
        </Label>
        <Label>Progress = {editedTask.progress}%
            <input type="range" min="0" max="100" bind:value={editedTask.progress} class="w-full mt-2 accent-blue-600 cursor-pointer" />
        </Label>
    </div>

    <svelte:fragment slot="footer">
        <div class="w-full flex justify-end gap-4">
            <Button
                on:click={onSave}
                disabled={isSaving}
                class="text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isSaving ? 'Saving...' : 'Save'}
            </Button>
            <Button
                on:click={onCancel}
                disabled={isSaving}
                class="text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
                Cancel
            </Button>
        </div>
    </svelte:fragment>
</Modal>
