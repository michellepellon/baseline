<script lang="ts">
	import { ingestHealthKitData } from '$lib/api/client';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let uploading = false;
	let error: string | null = null;
	let fileInput: HTMLInputElement;

	async function handleFile(file: File) {
		if (!file.name.endsWith('.xml')) {
			error = 'File must be XML format';
			return;
		}

		uploading = true;
		error = null;

		try {
			const result = await ingestHealthKitData(file);
			dispatch('upload-success', result);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Upload failed';
		} finally {
			uploading = false;
		}
	}

	function handleFileInput(event: Event) {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];
		if (file) {
			handleFile(file);
		}
	}
</script>

<div class="upload">
	<input
		bind:this={fileInput}
		type="file"
		accept=".xml"
		on:change={handleFileInput}
		id="file-upload"
	/>
	<label for="file-upload">
		{#if uploading}
			Processing...
		{:else}
			Upload export.xml
		{/if}
	</label>

	{#if error}
		<span class="error">{error}</span>
	{/if}
</div>

<style>
	.upload {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
	}

	input[type='file'] {
		width: 0.1px;
		height: 0.1px;
		opacity: 0;
		overflow: hidden;
		position: absolute;
		z-index: -1;
	}

	label {
		font-size: 0.9rem;
		padding: 0.4rem 0.8rem;
		border: 1px solid #333;
		cursor: pointer;
		transition: background 0.15s;
		font-family: inherit;
	}

	label:hover {
		background: #f0f0f0;
	}

	.error {
		color: #c00;
		font-size: 0.85rem;
		font-style: italic;
	}
</style>
