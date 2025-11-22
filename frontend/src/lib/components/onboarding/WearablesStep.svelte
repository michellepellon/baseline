<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let selectedWearable: string = 'apple_health';

	const dispatch = createEventDispatcher();

	const wearables = [
		{
			id: 'apple_health',
			name: 'Apple HealthKit',
			supported: true,
			icon: '🍎',
			description: 'Export sleep data from your iPhone Health app'
		},
		{
			id: 'fitbit',
			name: 'Fitbit',
			supported: false,
			icon: '⌚',
			description: 'Coming soon'
		},
		{
			id: 'garmin',
			name: 'Garmin',
			supported: false,
			icon: '⌚',
			description: 'Coming soon'
		},
		{
			id: 'oura',
			name: 'Oura Ring',
			supported: false,
			icon: '💍',
			description: 'Coming soon'
		}
	];

	function handleNext() {
		if (!selectedWearable) {
			alert('Please select a wearable device');
			return;
		}
		dispatch('next', { wearableType: selectedWearable });
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div class="wearables-step">
	<div class="header">
		<h1>Choose Your Wearable</h1>
		<p class="subtitle">Select the device you use to track your sleep</p>
	</div>

	<div class="content">
		<div class="wearables-grid">
			{#each wearables as wearable}
				<button
					class="wearable-card"
					class:selected={selectedWearable === wearable.id}
					class:disabled={!wearable.supported}
					on:click={() => wearable.supported && (selectedWearable = wearable.id)}
					disabled={!wearable.supported}
				>
					<div class="wearable-icon">{wearable.icon}</div>
					<div class="wearable-name">{wearable.name}</div>
					<div class="wearable-description">{wearable.description}</div>
					{#if wearable.supported}
						<div class="supported-badge">✅ Supported</div>
					{:else}
						<div class="coming-soon-badge">🔜 Coming Soon</div>
					{/if}
				</button>
			{/each}
		</div>

		{#if selectedWearable === 'apple_health'}
			<div class="instructions">
				<h2>How to Export Your Apple Health Data</h2>
				<div class="steps-list">
					<div class="instruction-step">
						<div class="step-number">1</div>
						<div class="step-content">
							<strong>Open the Health app</strong> on your iPhone
						</div>
					</div>
					<div class="instruction-step">
						<div class="step-number">2</div>
						<div class="step-content">
							<strong>Tap your profile picture</strong> in the top right corner
						</div>
					</div>
					<div class="instruction-step">
						<div class="step-number">3</div>
						<div class="step-content">
							<strong>Scroll down and tap "Export All Health Data"</strong>
						</div>
					</div>
					<div class="instruction-step">
						<div class="step-number">4</div>
						<div class="step-content">
							<strong>Wait for the export to complete</strong> (this may take a few minutes)
						</div>
					</div>
					<div class="instruction-step">
						<div class="step-number">5</div>
						<div class="step-content">
							<strong>Save or share the export.zip file</strong> to this device
						</div>
					</div>
				</div>
				<div class="note">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<circle cx="12" cy="12" r="10" />
						<line x1="12" y1="16" x2="12" y2="12" />
						<line x1="12" y1="8" x2="12.01" y2="8" />
					</svg>
					<p>The export file will be named <code>export.zip</code> and may be several hundred MB depending on your data history.</p>
				</div>
			</div>
		{/if}
	</div>

	<div class="actions">
		<button class="back-button" on:click={handleBack}>
			Back
		</button>
		<button class="next-button" on:click={handleNext} disabled={!selectedWearable}>
			Continue
		</button>
	</div>
</div>

<style>
	.wearables-step {
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

	.wearables-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
	}

	.wearable-card {
		background: white;
		border: 2px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 1.5rem;
		text-align: center;
		cursor: pointer;
		transition: all 0.2s;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.wearable-card:not(.disabled):hover {
		border-color: #3b82f6;
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
	}

	.wearable-card.selected {
		border-color: #3b82f6;
		background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
	}

	.wearable-card.disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.wearable-icon {
		font-size: 3rem;
		margin-bottom: 0.5rem;
	}

	.wearable-name {
		font-size: 1.125rem;
		font-weight: 600;
		color: #111827;
	}

	.wearable-description {
		font-size: 0.875rem;
		color: #6b7280;
	}

	.supported-badge {
		font-size: 0.75rem;
		color: #10b981;
		font-weight: 600;
	}

	.coming-soon-badge {
		font-size: 0.75rem;
		color: #9ca3af;
		font-weight: 600;
	}

	.instructions {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 2rem;
	}

	.instructions h2 {
		font-size: 1.25rem;
		font-weight: 600;
		margin-bottom: 1.5rem;
		color: #111827;
	}

	.steps-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.instruction-step {
		display: flex;
		gap: 1rem;
		align-items: flex-start;
	}

	.step-number {
		width: 2rem;
		height: 2rem;
		border-radius: 50%;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 600;
		font-size: 0.875rem;
		flex-shrink: 0;
	}

	.step-content {
		flex: 1;
		padding-top: 0.25rem;
		line-height: 1.6;
		color: #4b5563;
	}

	.note {
		display: flex;
		gap: 0.75rem;
		padding: 1rem;
		background-color: #eff6ff;
		border-radius: 0.5rem;
		border: 1px solid #bfdbfe;
	}

	.note svg {
		width: 1.25rem;
		height: 1.25rem;
		color: #3b82f6;
		flex-shrink: 0;
		margin-top: 0.125rem;
	}

	.note p {
		font-size: 0.875rem;
		line-height: 1.5;
		color: #1e40af;
		margin: 0;
	}

	code {
		background-color: #dbeafe;
		padding: 0.125rem 0.375rem;
		border-radius: 0.25rem;
		font-family: monospace;
		font-size: 0.875rem;
	}

	.actions {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	.back-button,
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
