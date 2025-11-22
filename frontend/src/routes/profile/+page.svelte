<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth';
	import { getSleepStats } from '$lib/api/client';
	import { startTour } from '$lib/tour/tour';
	import '$lib/tour/tour.css';

	let username = $derived($authStore.username || '');
	let firstName = $state('');
	let lastName = $state('');
	let loading = $state(false);
	let message = $state('');
	let stats = $state<Awaited<ReturnType<typeof getSleepStats>> | null>(null);
	let createdAt = $state<string | null>(null);
	let profilePictureUrl = $state<string | null>(null);
	let uploadingPicture = $state(false);

	let initials = $derived(() => {
		if (firstName && lastName) {
			return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
		}
		if (firstName) {
			return firstName.charAt(0).toUpperCase();
		}
		if (username) {
			return username.charAt(0).toUpperCase();
		}
		return '?';
	});

	let displayName = $derived(() => {
		if (firstName && lastName) {
			return `${firstName} ${lastName}`;
		}
		if (firstName) {
			return firstName;
		}
		return username;
	});


	async function loadProfile() {
		try {
			const [profileResponse, statsResponse] = await Promise.all([
				fetch('/api/auth/me', {
					headers: {
						Authorization: `Bearer ${$authStore.token}`
					}
				}),
				getSleepStats()
			]);

			if (profileResponse.ok) {
				const data = await profileResponse.json();
				firstName = data.first_name || '';
				lastName = data.last_name || '';
				createdAt = data.created_at || null;
				profilePictureUrl = data.profile_picture_url || null;
			}

			stats = statsResponse;
		} catch (error) {
			console.error('Failed to load profile:', error);
		}
	}

	async function handlePictureUpload(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];

		if (!file) return;

		// Validate file type
		const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
		if (!allowedTypes.includes(file.type)) {
			message = 'Invalid file type. Please upload a JPEG, PNG, GIF, or WebP image.';
			return;
		}

		uploadingPicture = true;
		message = '';

		try {
			// Process image: crop to square and resize
			const processedBlob = await processImage(file);

			const formData = new FormData();
			formData.append('file', processedBlob, 'profile.jpg');

			const response = await fetch('/api/auth/profile-picture', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${$authStore.token}`
				},
				body: formData
			});

			if (response.ok) {
				// Reload profile to get new picture URL
				await loadProfile();
				message = 'Profile picture uploaded successfully';
				setTimeout(() => {
					message = '';
				}, 3000);
			} else {
				const error = await response.json();
				message = error.detail || 'Failed to upload profile picture';
			}
		} catch (error) {
			message = 'Error uploading profile picture';
			console.error('Failed to upload picture:', error);
		} finally {
			uploadingPicture = false;
			// Reset input
			input.value = '';
		}
	}

	async function processImage(file: File): Promise<Blob> {
		return new Promise((resolve, reject) => {
			const img = new Image();
			const reader = new FileReader();

			reader.onload = (e) => {
				img.src = e.target?.result as string;
			};

			img.onload = () => {
				// Create canvas for processing
				const canvas = document.createElement('canvas');
				const ctx = canvas.getContext('2d');

				if (!ctx) {
					reject(new Error('Could not get canvas context'));
					return;
				}

				// Target size for profile pictures
				const targetSize = 400;

				// Calculate dimensions for square crop (centered)
				const minDimension = Math.min(img.width, img.height);
				const sx = (img.width - minDimension) / 2;
				const sy = (img.height - minDimension) / 2;

				// Set canvas to target size
				canvas.width = targetSize;
				canvas.height = targetSize;

				// Draw cropped and resized image
				ctx.drawImage(
					img,
					sx,
					sy,
					minDimension,
					minDimension,
					0,
					0,
					targetSize,
					targetSize
				);

				// Convert to blob (JPEG with good quality)
				canvas.toBlob(
					(blob) => {
						if (blob) {
							resolve(blob);
						} else {
							reject(new Error('Failed to create image blob'));
						}
					},
					'image/jpeg',
					0.9
				);
			};

			img.onerror = () => {
				reject(new Error('Failed to load image'));
			};

			reader.onerror = () => {
				reject(new Error('Failed to read file'));
			};

			reader.readAsDataURL(file);
		});
	}

	async function handlePictureDelete() {
		if (!confirm('Are you sure you want to delete your profile picture?')) {
			return;
		}

		uploadingPicture = true;
		message = '';

		try {
			const response = await fetch('/api/auth/profile-picture', {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${$authStore.token}`
				}
			});

			if (response.ok) {
				profilePictureUrl = null;
				message = 'Profile picture deleted successfully';
				setTimeout(() => {
					message = '';
				}, 3000);
			} else {
				message = 'Failed to delete profile picture';
			}
		} catch (error) {
			message = 'Error deleting profile picture';
			console.error('Failed to delete picture:', error);
		} finally {
			uploadingPicture = false;
		}
	}

	async function saveProfile() {
		loading = true;
		message = '';

		try {
			const response = await fetch('/api/auth/me', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$authStore.token}`
				},
				body: JSON.stringify({
					first_name: firstName || null,
					last_name: lastName || null
				})
			});

			if (response.ok) {
				message = 'Profile updated successfully';
				// Reload to update derived values
				setTimeout(() => {
					message = '';
				}, 3000);
			} else {
				message = 'Failed to update profile';
			}
		} catch (error) {
			message = 'Error updating profile';
			console.error('Failed to save profile:', error);
		} finally {
			loading = false;
		}
	}

	function formatDate(dateStr: string | null): string {
		if (!dateStr) return 'Unknown';
		const date = new Date(dateStr);
		return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
	}

	async function handleRestartTour() {
		try {
			// Reset tour completion status in backend
			const response = await fetch('/api/onboarding/tour/restart', {
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${$authStore.token}`
				}
			});

			if (response.ok) {
				// Start the tour
				startTour();
			} else {
				message = 'Failed to restart tour';
			}
		} catch (error) {
			message = 'Error restarting tour';
			console.error('Failed to restart tour:', error);
		}
	}

	onMount(loadProfile);
</script>

<svelte:head>
	<title>Profile - Baseline</title>
</svelte:head>

<main>
	<header>
		<h1>Profile</h1>
	</header>

	<!-- Profile Header Card -->
	<section class="profile-header">
		<div class="avatar-wrapper">
			<div class="avatar-display">
				{#if profilePictureUrl}
					<img
						src="{profilePictureUrl}?t={Date.now()}"
						alt="Profile"
						class="avatar-image"
					/>
				{:else}
					<div class="avatar">{initials()}</div>
				{/if}
				<label class="avatar-overlay" class:uploading={uploadingPicture}>
					<input
						type="file"
						accept="image/jpeg,image/png,image/gif,image/webp"
						onchange={handlePictureUpload}
						disabled={uploadingPicture}
						style="display: none;"
					/>
					<span class="overlay-text">
						{uploadingPicture ? 'Uploading...' : 'Change'}
					</span>
				</label>
			</div>
			{#if profilePictureUrl && !uploadingPicture}
				<button
					type="button"
					onclick={handlePictureDelete}
					class="avatar-remove-link"
				>
					Remove photo
				</button>
			{/if}
		</div>
		<div class="profile-summary">
			<h2 class="profile-name">{displayName()}</h2>
			<p class="profile-email">{username}</p>
		</div>
	</section>

	<!-- Personal Information Form -->
	<section class="profile-info">
		<h2>Personal Information</h2>
		<form
			onsubmit={(e) => {
				e.preventDefault();
				saveProfile();
			}}
		>
			<div class="form-grid">
				<div class="form-field">
					<label for="firstName">First Name</label>
					<input
						type="text"
						id="firstName"
						bind:value={firstName}
						placeholder="Enter your first name"
					/>
				</div>

				<div class="form-field">
					<label for="lastName">Last Name</label>
					<input
						type="text"
						id="lastName"
						bind:value={lastName}
						placeholder="Enter your last name"
					/>
				</div>

				<div class="form-field">
					<label for="email">Email</label>
					<input type="text" id="email" value={username} disabled />
				</div>
			</div>

			{#if message}
				<div class="message" class:success={message.includes('success')}>
					{message}
				</div>
			{/if}

			<button type="submit" disabled={loading}>
				{loading ? 'Saving...' : 'Save Changes'}
			</button>
		</form>
	</section>

	<!-- Application Tour -->
	<section class="tour-section">
		<h2>Application Tour</h2>
		<p class="tour-description">
			Take a guided tour of Baseline's features to learn how to make the most of your sleep tracking experience.
		</p>
		<button type="button" onclick={handleRestartTour} class="tour-button">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tour-icon">
				<circle cx="12" cy="12" r="10" />
				<polygon points="10 8 16 12 10 16 10 8" />
			</svg>
			Restart Tour
		</button>
	</section>
</main>

<style>
	/* Tufte-style typography with Carta layout */
	main {
		font-family: var(--font-family-base);
		color: var(--color-text-primary);
	}

	header {
		margin-bottom: var(--space-8);
	}

	h1 {
		font-size: var(--text-2xl);
		font-weight: var(--font-weight-normal);
		margin: 0;
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

	section {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-6);
		margin-bottom: var(--space-6);
	}

	/* Profile Header */
	.profile-header {
		display: flex;
		align-items: center;
		gap: var(--space-6);
		padding: var(--space-8);
	}

	.avatar-wrapper {
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-3);
	}

	.avatar-display {
		position: relative;
		width: 120px;
		height: 120px;
	}

	.avatar {
		width: 120px;
		height: 120px;
		border-radius: 50%;
		background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 3rem;
		font-weight: var(--font-weight-medium);
		color: var(--color-bg-primary);
		letter-spacing: -0.02em;
	}

	.avatar-image {
		width: 120px;
		height: 120px;
		border-radius: 50%;
		object-fit: cover;
		border: 3px solid var(--color-border);
	}

	.avatar-overlay {
		position: absolute;
		bottom: 0;
		right: 0;
		width: 120px;
		height: 120px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: transparent;
		cursor: pointer;
		transition: all var(--transition-base);
		opacity: 0;
	}

	.avatar-display:hover .avatar-overlay {
		opacity: 1;
		background: rgba(0, 0, 0, 0.6);
	}

	.avatar-overlay.uploading {
		opacity: 1;
		background: rgba(0, 0, 0, 0.6);
		cursor: not-allowed;
	}

	.overlay-text {
		color: white;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		font-variant: small-caps;
		pointer-events: none;
	}

	.avatar-remove-link {
		background: none;
		border: none;
		color: var(--color-text-secondary);
		font-size: var(--text-xs);
		cursor: pointer;
		text-decoration: underline;
		padding: 0;
		font-family: var(--font-family-base);
		transition: color var(--transition-fast);
	}

	.avatar-remove-link:hover {
		color: var(--color-danger);
	}

	.profile-summary {
		flex: 1;
	}

	.profile-name {
		font-size: var(--text-xl);
		margin: 0 0 var(--space-1) 0;
	}

	.profile-email {
		color: var(--color-text-secondary);
		font-size: var(--text-sm);
		margin: 0 0 var(--space-4) 0;
	}

	/* Form Styles */
	.form-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-4);
		margin-bottom: var(--space-6);
	}

	.form-field {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.form-field:last-child {
		grid-column: 1 / -1;
	}

	label {
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: var(--color-text-secondary);
		font-size: var(--text-sm);
	}

	input {
		font-family: var(--font-family-base);
		font-size: var(--text-base);
		padding: var(--space-3);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-base);
		background: var(--color-bg-primary);
		color: var(--color-text-primary);
		transition: border-color var(--transition-fast);
	}

	input:disabled {
		background: var(--color-bg-tertiary);
		color: var(--color-text-tertiary);
		cursor: not-allowed;
	}

	input:focus {
		outline: none;
		border-color: var(--color-focus);
	}

	button {
		font-family: var(--font-family-base);
		font-size: var(--text-base);
		padding: var(--space-3) var(--space-6);
		background: var(--color-primary);
		color: var(--color-bg-primary);
		border: none;
		border-radius: var(--radius-base);
		cursor: pointer;
		font-weight: var(--font-weight-medium);
		transition: background var(--transition-fast);
	}

	button:hover:not(:disabled) {
		background: var(--color-primary-hover);
	}

	button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.message {
		padding: var(--space-3) var(--space-4);
		border-radius: var(--radius-base);
		margin-bottom: var(--space-4);
		background: var(--color-danger-bg);
		color: var(--color-danger);
		border: 1px solid var(--color-danger-border);
		font-size: var(--text-sm);
	}

	.message.success {
		background: var(--color-success-bg);
		color: var(--color-success);
		border: 1px solid var(--color-success-border);
	}

	/* Tour Section */
	.tour-section {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.tour-description {
		color: var(--color-text-secondary);
		font-size: var(--text-sm);
		line-height: 1.6;
		margin: 0;
	}

	.tour-button {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		width: fit-content;
		background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
		padding: var(--space-3) var(--space-6);
	}

	.tour-button:hover:not(:disabled) {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
	}

	.tour-icon {
		width: 1.25rem;
		height: 1.25rem;
	}

	/* Responsive */
	@media (max-width: 768px) {
		.profile-header {
			flex-direction: column;
			text-align: center;
		}

		.form-grid {
			grid-template-columns: 1fr;
		}

		.tour-button {
			width: 100%;
			justify-content: center;
		}
	}
</style>
