<script lang="ts">
	export let title: string;
	export let description: string;
	export let actionLabel: string | null = null;
	export let actionHref: string | null = null;
</script>

<div class="empty-state">
	<div class="empty-icon">
		<svg
			width="64"
			height="64"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="1"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<path d="M2 4v16" />
			<path d="M2 8h18a2 2 0 0 1 2 2v10" />
			<path d="M2 17h20" />
			<path d="M6 8v9" />
		</svg>
	</div>
	<h2 class="empty-title">{title}</h2>
	<p class="empty-description">{description}</p>
	{#if actionLabel && actionHref}
		<a href={actionHref} class="empty-action">{actionLabel}</a>
	{/if}
</div>

<style>
	.empty-state {
		background: var(--color-bg-primary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-12) var(--space-8);
		text-align: center;
		max-width: 480px;
		margin: var(--space-8) auto;
	}

	.empty-icon {
		width: 64px;
		height: 64px;
		margin: 0 auto var(--space-4);
		color: var(--color-text-tertiary);
	}

	.empty-title {
		font-family: var(--font-family-base);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-normal);
		color: var(--color-text-primary);
		margin: 0 0 var(--space-2) 0;
		letter-spacing: -0.01em;
	}

	.empty-description {
		font-family: var(--font-family-base);
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin: 0 0 var(--space-6) 0;
		line-height: 1.6;
	}

	.empty-action {
		display: inline-block;
		padding: var(--space-3) var(--space-6);
		background: var(--color-primary);
		color: var(--color-bg-primary);
		text-decoration: none;
		border-radius: var(--radius-base);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		transition: background var(--transition-fast);
	}

	.empty-action:hover {
		background: var(--color-primary-hover);
	}
</style>
