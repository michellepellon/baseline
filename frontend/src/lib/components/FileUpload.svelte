<script lang="ts">
	import { ingestHealthKitData } from '$lib/api/client';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let uploading = $state(false);
	let error = $state<string | null>(null);
	let fileInput: HTMLInputElement;
	let isDragging = $state(false);
	let fileName = $state<string | null>(null);
	let progress = $state(0);

	const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB

	async function handleFile(file: File) {
		// Validate file extension
		if (!file.name.endsWith('.xml')) {
			error = 'File must be in XML format (export.xml)';
			return;
		}

		// Validate file size
		if (file.size > MAX_FILE_SIZE) {
			error = `File too large (max ${MAX_FILE_SIZE / (1024 * 1024)}MB)`;
			return;
		}

		uploading = true;
		error = null;
		fileName = file.name;
		progress = 0;

		// Simulate progress (since fetch doesn't provide upload progress easily)
		const progressInterval = setInterval(() => {
			if (progress < 90) {
				progress += 10;
			}
		}, 200);

		try {
			const result = await ingestHealthKitData(file);
			progress = 100;
			clearInterval(progressInterval);
			dispatch('upload-success', result);
		} catch (e) {
			clearInterval(progressInterval);
			error = e instanceof Error ? e.message : 'Upload failed';
			fileName = null;
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

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
		isDragging = true;
	}

	function handleDragLeave(event: DragEvent) {
		event.preventDefault();
		isDragging = false;
	}

	function handleDrop(event: DragEvent) {
		event.preventDefault();
		isDragging = false;

		const file = event.dataTransfer?.files[0];
		if (file) {
			handleFile(file);
		}
	}

	function triggerFileInput() {
		fileInput.click();
	}
</script>

<div class="upload-container">
	<input
		bind:this={fileInput}
		type="file"
		accept=".xml"
		onchange={handleFileInput}
		style="display: none;"
	/>

	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div
		class="drop-zone"
		class:dragging={isDragging}
		class:uploading={uploading}
		ondragover={handleDragOver}
		ondragleave={handleDragLeave}
		ondrop={handleDrop}
		onclick={!uploading ? triggerFileInput : undefined}
		role="button"
		tabindex="0"
	>
		<div class="drop-zone-content">
			{#if uploading}
				<div class="upload-icon">
					<svg
						width="48"
						height="48"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.5"
					>
						<circle cx="12" cy="12" r="10" />
						<path d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
					</svg>
				</div>
				<p class="upload-text">Processing {fileName}...</p>
				<div class="progress-bar">
					<div class="progress-fill" style="width: {progress}%"></div>
				</div>
				<p class="progress-text">{progress}%</p>
			{:else}
				<div class="upload-icon">
					<svg
						width="48"
						height="48"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.5"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
						<polyline points="17 8 12 3 7 8" />
						<line x1="12" y1="3" x2="12" y2="15" />
					</svg>
				</div>
				<p class="upload-text">Drop your export.xml file here</p>
				<p class="upload-subtext">or click to browse</p>
				<p class="file-requirements">Max file size: 500MB • XML format only</p>
			{/if}
		</div>
	</div>

	{#if error}
		<div class="error">{error}</div>
	{/if}
</div>

<style>
	.upload-container {
		width: 100%;
	}

	.drop-zone {
		border: 2px dashed var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-12);
		text-align: center;
		cursor: pointer;
		transition: all var(--transition-fast);
		background: var(--color-bg-secondary);
	}

	.drop-zone:hover:not(.uploading) {
		border-color: var(--color-primary);
		background: var(--color-bg-primary);
	}

	.drop-zone.dragging {
		border-color: var(--color-accent);
		background: var(--color-bg-primary);
		transform: scale(1.02);
	}

	.drop-zone.uploading {
		cursor: default;
		border-color: var(--color-accent);
	}

	.drop-zone-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-3);
	}

	.upload-icon {
		color: var(--color-text-tertiary);
	}

	.drop-zone:hover:not(.uploading) .upload-icon {
		color: var(--color-primary);
	}

	.upload-text {
		font-size: var(--text-base);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-primary);
		margin: 0;
	}

	.upload-subtext {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin: 0;
	}

	.file-requirements {
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		margin: var(--space-2) 0 0 0;
	}

	.progress-bar {
		width: 100%;
		max-width: 300px;
		height: 8px;
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-full);
		overflow: hidden;
		margin-top: var(--space-2);
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
		transition: width var(--transition-base);
	}

	.progress-text {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-secondary);
		margin: var(--space-1) 0 0 0;
	}

	.error {
		margin-top: var(--space-4);
		padding: var(--space-3) var(--space-4);
		background: var(--color-danger-bg);
		color: var(--color-danger);
		border: 1px solid var(--color-danger-border);
		border-radius: var(--radius-base);
		font-size: var(--text-sm);
	}
</style>
