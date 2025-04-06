<script lang="ts">
	import { onMount } from 'svelte';
	import { Button, Modal } from 'flowbite-svelte';
	import { showToast } from '$lib/stores/toast';
	import {
		deleteAttachment,
		fetchAttachments,
		getAttachmentUrl
	} from '$lib/api/attachments';
	import type { Attachment, RawAttachment } from '$lib/types/task/attachment';
	import { ClockSolid, DownloadSolid, EyeSolid, FileSolid, TrashBinSolid } from 'flowbite-svelte-icons';

	export let taskId: string;

	let attachments: Attachment[] = [];
	let previewFile: Attachment | null = null;
	let isPreviewModalOpen = false;
	
	export function reload() {
		loadAttachments();
	}
	
	async function loadAttachments() {
		try {
			const data: RawAttachment[] = await fetchAttachments(Number(taskId));
			attachments = data.map(mapRawToAttachment);
			console.log('Loaded attachments:', attachments);
		} catch (err) {
			showToast('Failed to load attachments', 'error');
		}
	}

	function formatDate(dateStr: string) {
		return new Date(dateStr).toLocaleString();
	}

	function isPreviewable(file: Attachment) {
		const ext = file.filename.split('.').pop()?.toLowerCase();
		return ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'webp'].includes(ext || '');
	}

	function mapRawToAttachment(raw: RawAttachment): Attachment {
		return {
			id: raw.id,
			task_id: raw.task_id,
            original_name: raw.original_name,
			filename: raw.file_name,
			url: getAttachmentUrl(raw.file_name),
			created_at: raw.uploaded_at
		};
	}

	function openPreview(file: Attachment) {
		previewFile = file;
		isPreviewModalOpen = true;
	}

	function closePreview() {
		isPreviewModalOpen = false;
		previewFile = null;
	}

	async function handleDelete(id: number) {
		try {
			await deleteAttachment(id);
			attachments = attachments.filter((f) => f.id !== id);
			showToast('Attachment deleted', 'success');
		} catch (err) {
			showToast('Failed to delete attachment', 'error');
		}
	}
    
    async function downloadFile(url: string, filename: string) {
        try {
            const response = await fetch(url);
            const blob = await response.blob();
            const blobUrl = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
        } catch (error) {
            showToast('Failed to download file', 'error');
        }
    }

	onMount(loadAttachments);
</script>

{#if attachments.length > 0}
    <div class="space-y-4 my-6">
        <h2 class="text-md font-bold text-gray-900 dark:text-white">Uploaded Files</h2>
        <ul class="space-y-2 mt-4 text-sm text-gray-700 dark:text-gray-300">
            {#each attachments as file (file.id)}
                <li class="flex flex-col md:flex-row md:items-start md:justify-between bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 p-4 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="flex-1 space-y-1">
                        <a href={file.url} target="_blank" class="font-medium text-blue-600 dark:text-blue-400 hover:underline break-words items-center">
                            <FileSolid class="inline" /> {file.original_name}
                        </a>
                        <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                            <ClockSolid class="inline" /> Uploaded at: {formatDate(file.created_at)}
                        </div>

                        {#if isPreviewable(file)}
                        <Button color="green" size="xs" on:click={() => openPreview(file)} class="mt-3 md:mt-0 w-max text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer">
                            <EyeSolid class="w-4 h-4 mr-1" /> Preview
                        </Button>
                        {/if}
                        <Button color="red" size="xs" on:click={() => handleDelete(file.id)} class="mt-3 md:mt-0 ml-4 w-max text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer" >
                            <TrashBinSolid class="w-4 h-4 mr-1" /> Delete
                        </Button>
                    </div>
                </li>
            {/each}
        </ul>
    </div>
{/if}

<Modal title={`📄 ${previewFile?.original_name ?? 'Preview'}`} bind:open={isPreviewModalOpen} autoclose outsideclose size="lg">
    <div class="bg-gray-50 dark:bg-gray-800 rounded-lg shadow">
        <div class="text-sm text-gray-700 dark:text-gray-300">
            <div><strong>Filename:</strong> {previewFile?.original_name}</div>
            <div><strong>Stored as:</strong> {previewFile?.filename}</div>
            <div><strong>Uploaded at:</strong> {previewFile ? formatDate(previewFile.created_at) : ''}</div>
        </div>
    </div>

    {#if previewFile}
        {#if previewFile.filename.endsWith('.pdf')}
            <iframe
                src={previewFile.url}
                title="PDF Preview"
                class="w-full h-[70vh] rounded-xl border border-gray-200 dark:border-gray-700"
            ></iframe>
        {:else}
            <img
                src={previewFile.url}
                alt="Preview"
                class="max-w-full max-h-[60vh] rounded-xl mx-auto border border-gray-200 dark:border-gray-700"
            />
        {/if}
    {/if}

    <svelte:fragment slot="footer">
        <div class="w-full flex justify-end gap-3 mt-4">
            <Button color="blue" class="text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer" on:click={() => previewFile && downloadFile(previewFile.url, previewFile.original_name)}>
                <DownloadSolid class="w-5 h-5 me-2" /> Download
            </Button>
            <Button color="red" class="text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 transition duration-200 ease-in-out rounded-lg shadow-md cursor-pointer" on:click={closePreview}>Close</Button>
        </div>
    </svelte:fragment>
</Modal>