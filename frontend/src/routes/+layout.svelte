<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth';
	import AppLayout from '$lib/components/AppLayout.svelte';
	import favicon from '$lib/assets/favicon.svg';
	import { startTour } from '$lib/tour/tour';
	import '$lib/styles/design-system.css';
	import '$lib/tour/tour.css';

	let { children } = $props();

	let isLoginPage = $derived($page.url.pathname === '/login');
	let isOnboardingPage = $derived($page.url.pathname === '/onboarding');
	let isAuthenticated = $derived($authStore.isAuthenticated);

	async function checkOnboardingStatus() {
		try {
			const token = localStorage.getItem('auth_token');
			if (!token) return;

			const response = await fetch('http://localhost:8000/api/onboarding/status', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			});

			if (response.ok) {
				const status = await response.json();
				// Redirect to onboarding if not completed and not already on onboarding page
				if (!status.is_onboarded && !isOnboardingPage && $page.url.pathname !== '/login') {
					goto('/onboarding');
				}
			}
		} catch (err) {
			console.error('Error checking onboarding status:', err);
		}
	}

	onMount(() => {
		const unsubscribe = authStore.subscribe((state) => {
			if (!state.isAuthenticated && !isLoginPage) {
				goto('/login');
			} else if (state.isAuthenticated && !isOnboardingPage) {
				// Check onboarding status when authenticated
				checkOnboardingStatus();
			}
		});

		// Check if we should start the tour after onboarding
		// This runs once when the layout mounts
		const shouldStartTour = localStorage.getItem('startTourAfterOnboarding');
		if (shouldStartTour === 'true' && $page.url.pathname === '/') {
			localStorage.removeItem('startTourAfterOnboarding');
			// Wait for the page to fully render
			setTimeout(() => {
				startTour();
			}, 1500);
		}

		return unsubscribe;
	});

	// Also watch for page changes to catch tour flag
	$effect(() => {
		// Watch the page URL
		const currentPath = $page.url.pathname;

		// If we just landed on dashboard, check for tour flag
		if (currentPath === '/' && $authStore.isAuthenticated) {
			const shouldStartTour = localStorage.getItem('startTourAfterOnboarding');
			if (shouldStartTour === 'true') {
				localStorage.removeItem('startTourAfterOnboarding');
				// Wait for the page to fully render
				setTimeout(() => {
					startTour();
				}, 1500);
			}
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if isLoginPage || isOnboardingPage}
	{@render children()}
{:else if isAuthenticated}
	<AppLayout>
		{@render children()}
	</AppLayout>
{/if}
