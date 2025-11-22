<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let firstName: string = '';
	export let lastName: string = '';
	export let profilePicture: File | null = null;

	const dispatch = createEventDispatcher();

	let fileInput: HTMLInputElement;
	let previewUrl: string = '';

	function handleFileChange(event: Event) {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];

		if (file) {
			if (!file.type.startsWith('image/')) {
				alert('Please select an image file');
				return;
			}

			if (file.size > 5 * 1024 * 1024) {
				alert('Image must be less than 5MB');
				return;
			}

			profilePicture = file;
			previewUrl = URL.createObjectURL(file);
		}
	}

	function handleNext() {
		dispatch('next', {
			firstName,
			lastName,
			profilePicture
		});
	}
</script>

<div class="welcome-step">
	<div class="header">
		<h1>Welcome to Baseline</h1>
		<p class="subtitle">Your personal sleep tracking and analysis companion</p>
	</div>

	<div class="content">
		<p class="description">
			Baseline helps you understand your sleep patterns, track your progress, and improve your sleep quality
			with AI-powered insights based on scientific research.
		</p>

		<div class="form">
			<h2>Let's get started</h2>

			<div class="profile-picture-section">
				<div class="preview">
					{#if previewUrl}
						<img src={previewUrl} alt="Profile preview" class="preview-image" />
					{:else}
						<div class="preview-placeholder">
							<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
								<circle cx="12" cy="7" r="4" />
							</svg>
						</div>
					{/if}
				</div>
				<button
					type="button"
					class="upload-button"
					on:click={() => fileInput.click()}
				>
					{previewUrl ? 'Change Photo' : 'Add Photo (Optional)'}
				</button>
				<input
					type="file"
					bind:this={fileInput}
					on:change={handleFileChange}
					accept="image/*"
					hidden
				/>
			</div>

			<div class="form-group">
				<label for="firstName">First Name</label>
				<input
					id="firstName"
					type="text"
					bind:value={firstName}
					placeholder="Enter your first name"
					class="input"
				/>
			</div>

			<div class="form-group">
				<label for="lastName">Last Name</label>
				<input
					id="lastName"
					type="text"
					bind:value={lastName}
					placeholder="Enter your last name"
					class="input"
				/>
			</div>
		</div>
	</div>

	<div class="actions">
		<button class="next-button" on:click={handleNext}>
			Get Started
		</button>
	</div>
</div>

<style>
	.welcome-step {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		max-width: 600px;
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

	.description {
		font-size: 1rem;
		line-height: 1.6;
		color: #4b5563;
		text-align: center;
	}

	.form {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 2rem;
	}

	.form h2 {
		font-size: 1.25rem;
		font-weight: 600;
		margin-bottom: 1.5rem;
		color: #111827;
	}

	.profile-picture-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.preview {
		width: 100px;
		height: 100px;
		border-radius: 50%;
		overflow: hidden;
		border: 2px solid #e5e7eb;
	}

	.preview-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.preview-placeholder {
		width: 100%;
		height: 100%;
		background-color: #f3f4f6;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #9ca3af;
	}

	.preview-placeholder svg {
		width: 3rem;
		height: 3rem;
	}

	.upload-button {
		padding: 0.5rem 1rem;
		background-color: #f3f4f6;
		border: 1px solid #d1d5db;
		border-radius: 0.5rem;
		font-size: 0.875rem;
		font-weight: 500;
		color: #374151;
		cursor: pointer;
		transition: all 0.2s;
	}

	.upload-button:hover {
		background-color: #e5e7eb;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: #374151;
	}

	.input {
		padding: 0.625rem 0.875rem;
		border: 1px solid #d1d5db;
		border-radius: 0.5rem;
		font-size: 1rem;
		transition: all 0.2s;
	}

	.input:focus {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}

	.actions {
		display: flex;
		justify-content: flex-end;
	}

	.next-button {
		padding: 0.75rem 2rem;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		border: none;
		border-radius: 0.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.2s;
	}

	.next-button:hover {
		transform: translateY(-1px);
	}

	.next-button:active {
		transform: translateY(0);
	}
</style>
