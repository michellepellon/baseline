<script lang="ts">
	import { goto } from '$app/navigation';
	import FileUpload from '$lib/components/FileUpload.svelte';

	let uploadResult: any = null;

	function handleUploadSuccess(event: CustomEvent) {
		uploadResult = event.detail;
		setTimeout(() => {
			goto('/sleep');
		}, 2000);
	}
</script>

<svelte:head>
	<title>Data - Baseline</title>
</svelte:head>

<div class="data-page">
	<h1>Data Management</h1>

	<section class="import-section">
		<h2>Import</h2>
		<p class="description">
			Upload your Apple HealthKit export.xml file to import sleep data into Baseline.
		</p>

		<div class="upload-area">
			<FileUpload on:upload-success={handleUploadSuccess} />
		</div>

		{#if uploadResult}
			<div class="upload-success">
				<h3>Import Successful</h3>
				<div class="result-details">
					<div class="detail-row">
						<span class="label">Records imported:</span>
						<span class="value">{uploadResult.records}</span>
					</div>
					<div class="detail-row">
						<span class="label">Nights processed:</span>
						<span class="value">{uploadResult.nights}</span>
					</div>
					<div class="detail-row">
						<span class="label">Date range:</span>
						<span class="value"
							>{uploadResult.date_range.start} to {uploadResult.date_range.end}</span
						>
					</div>
				</div>
				<p class="redirect-notice">Redirecting to Sleep page...</p>
			</div>
		{/if}
	</section>

	<section class="info-section">
		<h2>About HealthKit Export</h2>
		<div class="info-content">
			<h3>How to export your data from iPhone:</h3>
			<ol>
				<li>Open the Health app on your iPhone</li>
				<li>Tap your profile picture in the top right</li>
				<li>Scroll down and tap "Export All Health Data"</li>
				<li>Share the export.zip file to your computer</li>
				<li>Extract the ZIP file to get export.xml</li>
				<li>Upload export.xml using the form above</li>
			</ol>

		</div>
	</section>
</div>

<style>
	.data-page {
		font-family: var(--font-family-base);
		color: var(--color-text-primary);
	}

	h1 {
		font-size: var(--text-2xl);
		font-weight: var(--font-weight-normal);
		margin: 0 0 var(--space-8) 0;
		letter-spacing: -0.01em;
		color: var(--color-text-primary);
	}

	h2 {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-normal);
		margin: 0 0 var(--space-4) 0;
		letter-spacing: -0.01em;
		color: var(--color-text-primary);
	}

	h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-medium);
		margin: 0 0 var(--space-3) 0;
		color: var(--color-text-primary);
	}

	.description {
		margin: 0 0 var(--space-6) 0;
		line-height: 1.6;
		color: var(--color-text-secondary);
		font-size: var(--text-base);
	}

	/* Import Section */
	.import-section {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-6);
		margin-bottom: var(--space-6);
	}

	.upload-area {
		margin: var(--space-6) 0;
	}

	.upload-success {
		background: var(--color-success-bg);
		border: 1px solid var(--color-success-border);
		border-radius: var(--radius-md);
		padding: var(--space-6);
		margin-top: var(--space-6);
	}

	.upload-success h3 {
		color: var(--color-success);
		margin-bottom: var(--space-4);
	}

	.result-details {
		margin: var(--space-4) 0;
	}

	.detail-row {
		display: flex;
		justify-content: space-between;
		padding: var(--space-3) 0;
		border-bottom: 1px solid var(--color-success-border);
	}

	.detail-row:last-child {
		border-bottom: none;
	}

	.detail-row .label {
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: var(--color-text-secondary);
		font-size: var(--text-sm);
	}

	.detail-row .value {
		font-weight: var(--font-weight-medium);
		color: var(--color-text-primary);
		font-size: var(--text-sm);
	}

	.redirect-notice {
		margin-top: var(--space-4);
		font-style: italic;
		color: var(--color-text-secondary);
		font-size: var(--text-sm);
	}

	/* Info Section */
	.info-section {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-6);
	}

	.info-content {
		line-height: 1.6;
	}

	ol {
		margin: var(--space-4) 0;
		padding-left: var(--space-7);
	}

	ol li {
		margin-bottom: var(--space-2);
		color: var(--color-text-primary);
	}
</style>
