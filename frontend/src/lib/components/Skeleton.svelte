<script lang="ts">
	export let width: string = '100%';
	export let height: string = '1rem';
	export let borderRadius: string = 'var(--radius-base)';
</script>

<div class="skeleton" style="width: {width}; height: {height}; border-radius: {borderRadius}"></div>

<style>
	.skeleton {
		background: linear-gradient(
			90deg,
			var(--color-bg-tertiary) 25%,
			var(--color-bg-secondary) 50%,
			var(--color-bg-tertiary) 75%
		);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
	}

	@keyframes shimmer {
		0% {
			background-position: 200% 0;
		}
		100% {
			background-position: -200% 0;
		}
	}
</style>
