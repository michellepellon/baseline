<script lang="ts">
	import { authStore } from '$lib/stores/auth';

	let username = $derived($authStore.username || '');
</script>

<svelte:head>
	<title>Profile - Baseline</title>
</svelte:head>

<main>
	<header>
		<h1>Profile</h1>
	</header>

	<section class="profile-info">
		<h2>Account Information</h2>
		<div class="info-grid">
			<div class="info-row">
				<span class="label">Email</span>
				<span class="value">{username}</span>
			</div>
			<div class="info-row">
				<span class="label">Account Type</span>
				<span class="value">Personal</span>
			</div>
		</div>
	</section>

	<section class="data-info">
		<h2>Data & Privacy</h2>
		<p class="description">
			Your health data is stored locally and never shared with third parties. All processing
			happens on your device or your personal server instance.
		</p>
	</section>
</main>

<style>
	/* Tufte-style typography with Carta layout */
	main {
		font-family: 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif;
		color: #333;
	}

	header {
		margin-bottom: 2rem;
	}

	h1 {
		font-size: 2rem;
		font-weight: 400;
		margin: 0;
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

	section {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
		margin-bottom: 2rem;
	}

	.info-grid {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.info-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 0;
		border-bottom: 1px solid #f5f5f5;
	}

	.info-row:last-child {
		border-bottom: none;
	}

	.label {
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: #666;
		font-size: 0.9375rem;
	}

	.value {
		font-weight: 500;
		color: #000;
		font-size: 0.9375rem;
	}

	.description {
		margin: 0;
		line-height: 1.6;
		font-size: 0.9375rem;
		color: #666;
	}
</style>
