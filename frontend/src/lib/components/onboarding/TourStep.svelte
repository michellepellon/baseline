<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	function handleStartTour() {
		// Set flag to start tour after navigating to dashboard
		localStorage.setItem('startTourAfterOnboarding', 'true');
		dispatch('complete', { tourCompleted: true });
	}

	function handleSkipTour() {
		dispatch('complete', { tourCompleted: false });
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div class="tour-step">
	<div class="header">
		<h1>You're All Set!</h1>
		<p class="subtitle">Let's take a quick tour of Baseline's features</p>
	</div>

	<div class="content">
		<div class="tour-preview">
				<div class="preview-card">
					<div class="preview-icon">🎯</div>
					<h3>Interactive Tour</h3>
					<p>
						We'll guide you through the key features of Baseline, including:
					</p>
					<ul class="features-list">
						<li>
							<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
							</svg>
							Your sleep dashboard and metrics
						</li>
						<li>
							<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
							</svg>
							AI-powered health insights
						</li>
						<li>
							<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
							</svg>
							Sleep trends and analytics
						</li>
						<li>
							<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
							</svg>
							How to upload more data
						</li>
						<li>
							<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
							</svg>
							Settings and customization
						</li>
					</ul>
					<p class="tour-duration">
						<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<circle cx="12" cy="12" r="10" />
							<polyline points="12 6 12 12 16 14" />
						</svg>
						Takes about 2 minutes
					</p>
				</div>

				<div class="options">
					<button class="start-tour-button" on:click={handleStartTour}>
						<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<circle cx="12" cy="12" r="10" />
							<polygon points="10 8 16 12 10 16 10 8" />
						</svg>
						Start Tour
					</button>

					<button class="skip-tour-button" on:click={handleSkipTour}>
						Skip Tour (You can restart it later from Settings)
					</button>
				</div>
			</div>
	</div>

	<div class="actions">
		<button class="back-button" on:click={handleBack}>
			Back
		</button>
	</div>
</div>

<style>
	.tour-step {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		max-width: 700px;
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

	.tour-preview {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.preview-card {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 2rem;
		text-align: center;
	}

	.preview-icon {
		font-size: 4rem;
		margin-bottom: 1rem;
	}

	.preview-card h3 {
		font-size: 1.5rem;
		font-weight: 600;
		color: #111827;
		margin-bottom: 1rem;
	}

	.preview-card > p {
		font-size: 1rem;
		color: #4b5563;
		margin-bottom: 1.5rem;
	}

	.features-list {
		list-style: none;
		padding: 0;
		margin: 0 0 1.5rem 0;
		text-align: left;
		max-width: 500px;
		margin-left: auto;
		margin-right: auto;
	}

	.features-list li {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.625rem 0;
		font-size: 0.9375rem;
		color: #374151;
	}

	.features-list svg {
		width: 1.25rem;
		height: 1.25rem;
		color: #10b981;
		flex-shrink: 0;
	}

	.tour-duration {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		color: #6b7280;
		margin: 0;
	}

	.tour-duration svg {
		width: 1rem;
		height: 1rem;
	}

	.options {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	.start-tour-button {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 1rem 2.5rem;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		border: none;
		border-radius: 0.5rem;
		font-size: 1.125rem;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.2s;
	}

	.start-tour-button svg {
		width: 1.5rem;
		height: 1.5rem;
	}

	.start-tour-button:hover {
		transform: translateY(-2px);
	}

	.skip-tour-button {
		padding: 0.5rem 1rem;
		background: transparent;
		color: #6b7280;
		border: none;
		font-size: 0.875rem;
		cursor: pointer;
		text-decoration: underline;
		transition: color 0.2s;
	}

	.skip-tour-button:hover {
		color: #374151;
	}

	.tour-running {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 3rem 2rem;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	.tour-running-icon {
		width: 5rem;
		height: 5rem;
		border-radius: 50%;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.tour-running-icon svg {
		width: 3rem;
		height: 3rem;
	}

	.spin {
		animation: spin 2s linear infinite;
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	.tour-running h2 {
		font-size: 1.5rem;
		font-weight: 600;
		color: #111827;
		margin: 0;
	}

	.tour-running p {
		font-size: 1rem;
		color: #6b7280;
		margin: 0;
	}

	.complete-button {
		padding: 0.75rem 2rem;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		border: none;
		border-radius: 0.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.2s;
		margin-top: 1rem;
	}

	.complete-button:hover {
		transform: translateY(-1px);
	}

	.actions {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	.back-button {
		padding: 0.75rem 2rem;
		background: white;
		color: #6b7280;
		border: 1px solid #d1d5db;
		border-radius: 0.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.back-button:hover {
		background-color: #f9fafb;
	}
</style>
