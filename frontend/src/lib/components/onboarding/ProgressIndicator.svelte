<script lang="ts">
	export let currentStep: number = 1;
	export let totalSteps: number = 5;

	const steps = [
		{ number: 1, label: 'Welcome' },
		{ number: 2, label: 'Wearables' },
		{ number: 3, label: 'Upload Data' },
		{ number: 4, label: 'Settings' },
		{ number: 5, label: 'Tour' }
	];
</script>

<div class="progress-container">
	<div class="progress-bar">
		<div class="progress-fill" style="width: {(currentStep / totalSteps) * 100}%"></div>
	</div>

	<div class="steps">
		{#each steps as step}
			<div class="step" class:active={step.number === currentStep} class:completed={step.number < currentStep}>
				<div class="step-number">
					{#if step.number < currentStep}
						<svg class="checkmark" viewBox="0 0 24 24" fill="none" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					{:else}
						{step.number}
					{/if}
				</div>
				<div class="step-label">{step.label}</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.progress-container {
		width: 100%;
		margin-bottom: var(--space-8);
	}

	.progress-bar {
		width: 100%;
		height: 2px;
		background-color: var(--color-border);
		overflow: hidden;
		margin-bottom: var(--space-6);
	}

	.progress-fill {
		height: 100%;
		background-color: var(--color-primary);
		transition: width var(--transition-base);
	}

	.steps {
		display: flex;
		justify-content: space-between;
		gap: var(--space-2);
	}

	.step {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-2);
		flex: 1;
		opacity: 0.4;
		transition: opacity var(--transition-fast);
	}

	.step.active,
	.step.completed {
		opacity: 1;
	}

	.step-number {
		width: 2rem;
		height: 2rem;
		border-radius: 50%;
		border: 1px solid var(--color-border);
		background-color: var(--color-bg-primary);
		color: var(--color-text-secondary);
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: var(--font-weight-medium);
		font-size: var(--text-sm);
		transition: all var(--transition-fast);
	}

	.step.active .step-number {
		border-color: var(--color-primary);
		background-color: var(--color-primary);
		color: var(--color-bg-primary);
	}

	.step.completed .step-number {
		border-color: var(--color-success);
		background-color: var(--color-success);
		color: var(--color-bg-primary);
	}

	.checkmark {
		width: 1rem;
		height: 1rem;
	}

	.step-label {
		font-size: var(--text-xs);
		color: var(--color-text-secondary);
		text-align: center;
		font-weight: var(--font-weight-medium);
		font-variant: small-caps;
		letter-spacing: 0.05em;
	}

	.step.active .step-label {
		color: var(--color-text-primary);
	}

	@media (max-width: 640px) {
		.steps {
			gap: 0;
		}

		.step-number {
			width: 1.75rem;
			height: 1.75rem;
			font-size: var(--text-xs);
		}

		.step-label {
			font-size: 0.625rem;
		}
	}
</style>
