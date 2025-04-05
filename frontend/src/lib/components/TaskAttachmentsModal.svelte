<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Modal, Button, Fileupload, Label } from 'flowbite-svelte';
	import { showToast } from '$lib/stores/toast';
	import { uploadAttachment, getAttachmentUrl } from '$lib/api/attachments';
	import type { Attachment, RawAttachment } from '$lib/types/task/attachment';

	// Props & dispatcher
	export let open = false;
	export let taskId: string;
	const dispatch = createEventDispatcher();

	// Allowed file types
	const allowedTypes = [
		"image/jpeg", "image/png", "image/gif", "image/webp",
		"application/pdf",
		"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		"application/vnd.ms-excel",
		"application/zip",
		"text/plain",
		"text/csv"
	];

	let files: File[] = [];
	let selectedFiles: FileList | undefined;
	let previews: string[] = [];
	let isUploading = false;

	// Helpers
	function isValidFileType(file: File) {
		return allowedTypes.includes(file.type);
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

	function updatePreviews() {
		previews = files
			.filter(file => file.type.startsWith('image/') || file.type === 'application/pdf')
			.map(file => URL.createObjectURL(file));
	}

	function cleanupPreviews() {
		previews.forEach(url => URL.revokeObjectURL(url));
		previews = [];
	}

	function closeModal() {
		open = false;
		files = [];
		selectedFiles = undefined;
		cleanupPreviews();
	}

	// Event Handlers
	function handleFileChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target?.files) {
			const selected = Array.from(target.files);
			const invalid = selected.filter(file => !isValidFileType(file));

			if (invalid.length > 0) {
				showToast(`Invalid file type: ${invalid.map(f => f.name).join(', ')}`, 'error');
				return;
			}

			files = selected;
			updatePreviews();
		}
	}

	async function handleUpload() {
		if (files.length === 0) return;

		const invalidFiles = files.filter(file => !isValidFileType(file));
		if (invalidFiles.length > 0) {
			showToast(`File type not allowed: ${invalidFiles.map(f => f.name).join(', ')}`, 'error');
			return;
		}

		isUploading = true;
		showToast('Uploading files...', 'info');

		try {
			const uploaded: Attachment[] = [];

			for (const file of files) {
				const result = await uploadAttachment(Number(taskId), file);
				uploaded.push(mapRawToAttachment(result));
			}

			showToast('Files uploaded successfully', 'success');
			dispatch('uploaded', uploaded);
			closeModal();
		} catch (err) {
			showToast('Failed to upload files', 'error');
		} finally {
			isUploading = false;
			files = [];
			selectedFiles = undefined;
			cleanupPreviews();
		}
	}
</script>

<Modal bind:open title="📎 Upload Attachments" size="lg" autoclose outsideclose>
	<div class="space-y-4">
		<Label class="block text-sm font-medium text-gray-700 dark:text-white">
			Select files
			<Fileupload
				multiple
				bind:files={selectedFiles}
				on:change={handleFileChange}
				class="mt-2"
			/>
		</Label>

		{#if previews.length > 0}
			<div class="grid grid-cols-1 gap-4 mt-4">
				{#each previews as preview, i}
					<div class="border rounded-lg p-2 bg-gray-100 dark:bg-gray-800 shadow-sm">
						{#if files[i].type === 'application/pdf'}
							<iframe src={preview} class="w-full h-48 rounded" title="PDF Preview"></iframe>
						{:else}
							<img src={preview} alt="Preview" class="w-full h-48 object-contain rounded" />
						{/if}
						<p class="text-sm mt-2 text-center text-gray-600 dark:text-gray-300">
							{files[i].name}
						</p>
					</div>
				{/each}
			</div>
		{/if}
	</div>

	<svelte:fragment slot="footer">
		<div class="w-full flex justify-end gap-3 mt-2">
			<Button color="red" on:click={closeModal}>Cancel</Button>
			<Button color="blue" on:click={handleUpload} disabled={isUploading || files.length === 0}>
				{isUploading ? '⏳ Uploading...' : '⬆️ Upload'}
			</Button>
		</div>
	</svelte:fragment>
</Modal>
