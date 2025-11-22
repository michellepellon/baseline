<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import FileUpload from '$lib/components/FileUpload.svelte';

	const dispatch = createEventDispatcher();

	let uploadComplete = false;
	let uploadStats: {
		recordsImported?: number;
		dateRange?: { start: string; end: string };
		nightsOfData?: number;
	} | null = null;

	function handleUploadSuccess(event: CustomEvent) {
		uploadComplete = true;
		const result = event.detail;

		uploadStats = {
			recordsImported: result.sleep_records_inserted || 0,
			nightsOfData: result.nightly_summaries_inserted || 0,
			dateRange: result.date_range
		};
	}

	function handleSkip() {
		dispatch('next', { skipped: true });
	}

	function handleNext() {
		dispatch('next', { uploadStats });
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div class="upload-step">
	<div class="header">
		<h1>Upload Your Sleep Data</h1>
		<p class="subtitle">Import your Apple Health export file to start analyzing your sleep</p>
	</div>

	<div class="content">
		{#if !uploadComplete}
			<div class="upload-container">
				<FileUpload on:success={handleUploadSuccess} />

				<div class="help-section">
					<h3>Need help exporting your data?</h3>
					<p>
						Go back to the previous step for detailed instructions on how to export your Apple Health data.
					</p>
				</div>
			</div>
		{:else}
			<div class="success-container">
				<div class="success-icon">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
					</svg>
				</div>

				<h2>Data Imported Successfully!</h2>

				{#if uploadStats}
					<div class="stats-grid">
						<div class="stat-card">
							<div class="stat-value">{uploadStats.recordsImported?.toLocaleString()}</div>
							<div class="stat-label">Sleep Records</div>
						</div>

						<div class="stat-card">
							<div class="stat-value">{uploadStats.nightsOfData?.toLocaleString()}</div>
							<div class="stat-label">Nights of Data</div>
						</div>

						{#if uploadStats.dateRange}
							<div class="stat-card date-range">
								<div class="stat-value">
									{new Date(uploadStats.dateRange.start).toLocaleDateString()} -
									{new Date(uploadStats.dateRange.end).toLocaleDateString()}
								</div>
								<div class="stat-label">Date Range</div>
							</div>
						{/if}
					</div>
				{/if}

				<p class="success-message">
					Your sleep data has been successfully imported and is ready for analysis.
					Let's continue with a few settings to personalize your experience.
				</p>
			</div>
		{/if}
	</div>

	<div class="actions">
		<button class="back-button" on:click={handleBack}>
			Back
		</button>
		<div class="right-actions">
			{#if !uploadComplete}
				<button class="skip-button" on:click={handleSkip}>
					Skip for Now
				</button>
			{/if}
			<button
				class="next-button"
				on:click={handleNext}
				disabled={!uploadComplete}
			>
				Continue
			</button>
		</div>
	</div>
</div>

<style>
	.upload-step {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		max-width: 800px;
		margin: 0 auto;
	}

	.header {
		text-align: center;
	}

	h1 {
		font-size: 2rem;
		font-weight: 700;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		font-size: 1.125rem;
		color: #6b7280;
	}

	.content {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.upload-container {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.help-section {
		background: #eff6ff;
		border: 1px solid #bfdbfe;
		border-radius: 0.75rem;
		padding: 1.5rem;
	}

	.help-section h3 {
		font-size: 1rem;
		font-weight: 600;
		color: #1e40af;
		margin-bottom: 0.5rem;
	}

	.help-section p {
		font-size: 0.875rem;
		color: #1e3a8a;
		line-height: 1.5;
		margin: 0;
	}

	.success-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		padding: 2rem;
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 0.75rem;
	}

	.success-icon {
		width: 4rem;
		height: 4rem;
		border-radius: 50%;
		background-color: #10b981;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.success-icon svg {
		width: 2.5rem;
		height: 2.5rem;
	}

	.success-container h2 {
		font-size: 1.5rem;
		font-weight: 600;
		color: #111827;
		margin: 0;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
		gap: 1rem;
		width: 100%;
	}

	.stat-card {
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		padding: 1.5rem;
		border-radius: 0.75rem;
		text-align: center;
	}

	.stat-card.date-range {
		grid-column: 1 / -1;
	}

	.stat-value {
		font-size: 1.75rem;
		font-weight: 700;
		margin-bottom: 0.5rem;
	}

	.stat-card.date-range .stat-value {
		font-size: 1.125rem;
	}

	.stat-label {
		font-size: 0.875rem;
		opacity: 0.9;
	}

	.success-message {
		text-align: center;
		color: #4b5563;
		line-height: 1.6;
		max-width: 500px;
	}

	.actions {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	.right-actions {
		display: flex;
		gap: 1rem;
	}

	.back-button,
	.skip-button,
	.next-button {
		padding: 0.75rem 2rem;
		border-radius: 0.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.back-button {
		background: white;
		color: #6b7280;
		border: 1px solid #d1d5db;
	}

	.back-button:hover {
		background-color: #f9fafb;
	}

	.skip-button {
		background: white;
		color: #6b7280;
		border: 1px solid #d1d5db;
	}

	.skip-button:hover {
		background-color: #f9fafb;
	}

	.next-button {
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		border: none;
	}

	.next-button:hover:not(:disabled) {
		transform: translateY(-1px);
	}

	.next-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style>
