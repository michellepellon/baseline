<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import ProgressIndicator from './ProgressIndicator.svelte';
	import WelcomeStep from './WelcomeStep.svelte';
	import WearablesStep from './WearablesStep.svelte';
	import DataUploadStep from './DataUploadStep.svelte';
	import SettingsStep from './SettingsStep.svelte';
	import TourStep from './TourStep.svelte';

	let currentStep = 1;
	let totalSteps = 5;

	// Onboarding data
	let firstName = '';
	let lastName = '';
	let profilePicture: File | null = null;
	let wearableType = 'apple_health';
	let sleepGoals: string[] = [];
	let preferences: Record<string, any> = {};
	let tourCompleted = false;

	let isSubmitting = false;
	let error: string | null = null;

	function handleWelcomeNext(event: CustomEvent) {
		const { firstName: fn, lastName: ln, profilePicture: pp } = event.detail;
		firstName = fn;
		lastName = ln;
		profilePicture = pp;

		// Update user profile
		updateProfile();

		currentStep = 2;
	}

	function handleWearablesNext(event: CustomEvent) {
		wearableType = event.detail.wearableType;
		currentStep = 3;
	}

	function handleUploadNext(event: CustomEvent) {
		// Data upload is already handled by FileUpload component
		currentStep = 4;
	}

	function handleSettingsNext(event: CustomEvent) {
		sleepGoals = JSON.parse(event.detail.sleepGoals || '[]');
		preferences = JSON.parse(event.detail.preferences || '{}');
		currentStep = 5;
	}

	async function handleTourComplete(event: CustomEvent) {
		tourCompleted = event.detail.tourCompleted;
		await completeOnboarding();
	}

	function handleBack() {
		if (currentStep > 1) {
			currentStep--;
		}
	}

	async function updateProfile() {
		try {
			const token = localStorage.getItem('auth_token');
			if (!token) return;

			const formData = new FormData();
			if (firstName) formData.append('first_name', firstName);
			if (lastName) formData.append('last_name', lastName);
			if (profilePicture) formData.append('profile_picture', profilePicture);

			const response = await fetch('http://localhost:8000/api/auth/profile', {
				method: 'PUT',
				headers: {
					'Authorization': `Bearer ${token}`
				},
				body: formData
			});

			if (!response.ok) {
				console.error('Failed to update profile');
			}
		} catch (err) {
			console.error('Error updating profile:', err);
		}
	}

	async function completeOnboarding() {
		isSubmitting = true;
		error = null;

		try {
			const token = localStorage.getItem('auth_token');
			if (!token) {
				throw new Error('Not authenticated');
			}

			const response = await fetch('http://localhost:8000/api/onboarding/complete', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					wearable_type: wearableType,
					sleep_goals: JSON.stringify(sleepGoals),
					preferences: JSON.stringify(preferences),
					tour_completed: tourCompleted
				})
			});

			if (!response.ok) {
				const data = await response.json();
				throw new Error(data.detail || 'Failed to complete onboarding');
			}

			// Store onboarding completion in localStorage
			localStorage.setItem('onboardingCompleted', 'true');

			// Redirect to dashboard
			goto('/');
		} catch (err) {
			error = err instanceof Error ? err.message : 'An error occurred';
			isSubmitting = false;
		}
	}

	// Check if user is authenticated on mount
	onMount(() => {
		const token = localStorage.getItem('auth_token');
		if (!token) {
			goto('/login');
		}
	});
</script>

<div class="onboarding-flow">
	<div class="container">
		<ProgressIndicator {currentStep} {totalSteps} />

		<div class="step-container">
			{#if currentStep === 1}
				<WelcomeStep
					bind:firstName
					bind:lastName
					bind:profilePicture
					on:next={handleWelcomeNext}
				/>
			{:else if currentStep === 2}
				<WearablesStep
					bind:selectedWearable={wearableType}
					on:next={handleWearablesNext}
					on:back={handleBack}
				/>
			{:else if currentStep === 3}
				<DataUploadStep
					on:next={handleUploadNext}
					on:back={handleBack}
				/>
			{:else if currentStep === 4}
				<SettingsStep
					bind:sleepGoals
					on:next={handleSettingsNext}
					on:back={handleBack}
				/>
			{:else if currentStep === 5}
				<TourStep
					on:complete={handleTourComplete}
					on:back={handleBack}
				/>
			{/if}
		</div>

		{#if error}
			<div class="error-banner">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<circle cx="12" cy="12" r="10" />
					<line x1="12" y1="8" x2="12" y2="12" />
					<line x1="12" y1="16" x2="12.01" y2="16" />
				</svg>
				<span>{error}</span>
			</div>
		{/if}

		{#if isSubmitting}
			<div class="loading-overlay">
				<div class="spinner"></div>
				<p>Completing onboarding...</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.onboarding-flow {
		min-height: 100vh;
		background: var(--color-bg-secondary);
		padding: var(--space-8) var(--space-4);
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: var(--font-family-base);
	}

	.container {
		width: 100%;
		max-width: 900px;
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-base);
		padding: var(--space-8);
		box-shadow: var(--shadow-sm);
		position: relative;
	}

	.step-container {
		min-height: 400px;
	}

	.error-banner {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-4);
		background-color: var(--color-danger-bg);
		border: 1px solid var(--color-danger-border);
		border-radius: var(--radius-base);
		color: var(--color-danger);
		margin-top: var(--space-4);
		font-size: var(--text-sm);
	}

	.error-banner svg {
		width: 1.25rem;
		height: 1.25rem;
		flex-shrink: 0;
	}

	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.95);
		border-radius: var(--radius-base);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: var(--space-4);
		z-index: 50;
	}

	.spinner {
		width: 3rem;
		height: 3rem;
		border: 4px solid var(--color-border);
		border-top-color: var(--color-primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.loading-overlay p {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		font-weight: var(--font-weight-medium);
	}

	@media (max-width: 640px) {
		.onboarding-flow {
			padding: var(--space-4) var(--space-2);
		}

		.container {
			padding: var(--space-6) var(--space-4);
		}

		.step-container {
			min-height: 300px;
		}
	}
</style>
