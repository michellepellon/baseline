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
		font-family: 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif;
		color: #333;
	}

	h1 {
		font-size: 2rem;
		font-weight: 400;
		margin: 0 0 2rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	h2 {
		font-size: 1.25rem;
		font-weight: 400;
		margin: 0 0 1rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	h3 {
		font-size: 1.1rem;
		font-weight: 400;
		margin: 0 0 0.75rem 0;
		color: #000;
	}

	.description {
		margin: 0 0 1.5rem 0;
		line-height: 1.6;
		color: #666;
	}

	/* Import Section */
	.import-section {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
		margin-bottom: 2rem;
	}

	.upload-area {
		margin: 2rem 0;
	}

	.upload-success {
		background: #f0f9f4;
		border: 1px solid #4caf50;
		border-radius: 6px;
		padding: 1.5rem;
		margin-top: 2rem;
	}

	.upload-success h3 {
		color: #2e7d32;
		margin-bottom: 1rem;
	}

	.result-details {
		margin: 1rem 0;
	}

	.detail-row {
		display: flex;
		justify-content: space-between;
		padding: 0.5rem 0;
		border-bottom: 1px solid #e0f2e9;
	}

	.detail-row:last-child {
		border-bottom: none;
	}

	.detail-row .label {
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: #666;
	}

	.detail-row .value {
		font-weight: 500;
		color: #000;
	}

	.redirect-notice {
		margin-top: 1rem;
		font-style: italic;
		color: #666;
		font-size: 0.875rem;
	}

	/* Info Section */
	.info-section {
		background: #fafafa;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
	}

	.info-content {
		line-height: 1.6;
	}

	ol {
		margin: 1rem 0;
		padding-left: 1.75rem;
	}

	ol li {
		margin-bottom: 0.5rem;
	}

	.note {
		margin-top: 1.5rem;
		padding: 1rem;
		background: #fff3cd;
		border: 1px solid #ffc107;
		border-radius: 4px;
		font-size: 0.9375rem;
		line-height: 1.5;
	}

	.note strong {
		font-weight: 600;
	}
</style>
