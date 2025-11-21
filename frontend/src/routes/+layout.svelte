<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth';
	import AppLayout from '$lib/components/AppLayout.svelte';
	import favicon from '$lib/assets/favicon.svg';
	import '$lib/styles/design-system.css';

	let { children } = $props();

	let isLoginPage = $derived($page.url.pathname === '/login');
	let isAuthenticated = $derived($authStore.isAuthenticated);

	onMount(() => {
		const unsubscribe = authStore.subscribe((state) => {
			if (!state.isAuthenticated && !isLoginPage) {
				goto('/login');
			}
		});

		return unsubscribe;
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if isLoginPage}
	{@render children()}
{:else if isAuthenticated}
	<AppLayout>
		{@render children()}
	</AppLayout>
{/if}
