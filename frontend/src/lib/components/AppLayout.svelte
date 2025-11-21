<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';

	let { children } = $props();

	let username = $derived($authStore.username || 'User');
	let displayName = $state('');
	let showUserMenu = $state(false);
	let profilePictureUrl = $state<string | null>(null);
	let initials = $state('U');

	async function loadUserProfile() {
		try {
			const response = await fetch('/api/auth/me', {
				headers: {
					Authorization: `Bearer ${$authStore.token}`
				}
			});

			if (response.ok) {
				const data = await response.json();
				if (data.first_name || data.last_name) {
					const parts = [];
					if (data.first_name) parts.push(data.first_name);
					if (data.last_name) parts.push(data.last_name);
					displayName = parts.join(' ');

					// Calculate initials
					if (data.first_name && data.last_name) {
						initials = `${data.first_name.charAt(0)}${data.last_name.charAt(0)}`.toUpperCase();
					} else if (data.first_name) {
						initials = data.first_name.charAt(0).toUpperCase();
					} else {
						initials = username.charAt(0).toUpperCase();
					}
				} else {
					displayName = username;
					initials = username.charAt(0).toUpperCase();
				}

				profilePictureUrl = data.profile_picture_url || null;
			} else {
				displayName = username;
				initials = username.charAt(0).toUpperCase();
			}
		} catch (error) {
			console.error('Failed to load user profile:', error);
			displayName = username;
			initials = username.charAt(0).toUpperCase();
		}
	}

	onMount(() => {
		loadUserProfile();

		// Close dropdown when clicking outside
		const handleClickOutside = (event: MouseEvent) => {
			const target = event.target as HTMLElement;
			if (!target.closest('.user-menu')) {
				showUserMenu = false;
			}
		};

		document.addEventListener('click', handleClickOutside);
		return () => document.removeEventListener('click', handleClickOutside);
	});

	function handleLogout() {
		showUserMenu = false;
		authStore.logout();
		goto('/login');
	}

	function toggleUserMenu(event: MouseEvent) {
		event.stopPropagation();
		showUserMenu = !showUserMenu;
	}

	let navItems = [
		{ name: 'Sleep', path: '/sleep' },
		{ name: 'Data', path: '/data' },
		{ name: 'Science', path: '/methodology' }
	];
</script>

<div class="app-container">
	<!-- Sidebar Navigation -->
	<aside class="sidebar">
		<div class="logo-container">
			<div class="logo">baseline</div>
		</div>

		<nav class="nav">
			<ul class="nav-list">
				<li>
					<a
						href="/sleep"
						class="nav-item"
						class:active={$page.url.pathname === '/sleep'}
					>
						<span class="nav-icon">
							<svg
								width="20"
								height="20"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.5"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<path d="M2 4v16" />
								<path d="M2 8h18a2 2 0 0 1 2 2v10" />
								<path d="M2 17h20" />
								<path d="M6 8v9" />
							</svg>
						</span>
						<span class="nav-label">Sleep</span>
					</a>
				</li>
				<li>
					<a
						href="/data"
						class="nav-item"
						class:active={$page.url.pathname === '/data'}
					>
						<span class="nav-icon">
							<svg
								width="20"
								height="20"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.5"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<ellipse cx="12" cy="5" rx="9" ry="3" />
								<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
								<path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" />
							</svg>
						</span>
						<span class="nav-label">Data</span>
					</a>
				</li>
				<li>
					<a
						href="/methodology"
						class="nav-item"
						class:active={$page.url.pathname === '/methodology'}
					>
						<span class="nav-icon">
							<svg
								width="20"
								height="20"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.5"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<!-- DNA strand icon -->
								<path d="M2 15c3.3 3.3 6.7 0 10 0s6.7 3.3 10 0" />
								<path d="M2 9c3.3-3.3 6.7 0 10 0s6.7-3.3 10 0" />
								<path d="M5 15v-6" />
								<path d="M9 15V9" />
								<path d="M15 15V9" />
								<path d="M19 15v-6" />
							</svg>
						</span>
						<span class="nav-label">Science</span>
					</a>
				</li>
			</ul>
		</nav>
	</aside>

	<!-- Main Content Area -->
	<div class="main-wrapper">
		<!-- Top Header -->
		<header class="top-header">
			<div class="header-left"></div>

			<div class="header-right">
				<div class="user-menu">
					<button class="user-button" onclick={toggleUserMenu}>
						{#if profilePictureUrl}
							<img
								src="{profilePictureUrl}?t={Date.now()}"
								alt="Profile"
								class="user-avatar-image"
							/>
						{:else}
							<div class="user-avatar">{initials}</div>
						{/if}
						<span class="user-name">{displayName || username}</span>
						<span class="dropdown-arrow">▾</span>
					</button>

					{#if showUserMenu}
						<div class="user-dropdown">
							<a href="/profile" class="dropdown-item">Profile</a>
							<hr class="dropdown-divider" />
							<button class="dropdown-item logout" onclick={handleLogout}>
								Sign out
							</button>
						</div>
					{/if}
				</div>
			</div>
		</header>

		<!-- Page Content -->
		<main class="content">
			{@render children()}
		</main>
	</div>
</div>

<style>
	.app-container {
		display: flex;
		min-height: 100vh;
		background: #fafafa;
		font-family:
			-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			sans-serif;
	}

	/* Sidebar Navigation */
	.sidebar {
		width: 220px;
		background: #ffffff;
		border-right: 1px solid #e5e5e5;
		display: flex;
		flex-direction: column;
		position: fixed;
		height: 100vh;
		left: 0;
		top: 0;
	}

	.logo-container {
		padding: 1.25rem 1rem;
		border-bottom: 1px solid #e5e5e5;
		display: flex;
		justify-content: center;
	}

	.logo {
		border: 2px solid #000000;
		padding: 0.5rem 1rem;
		font-size: 1.25rem;
		font-weight: 500;
	}

	.nav {
		flex: 1;
		padding: 1rem;
		overflow-y: auto;
	}

	.nav-list {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.nav-item {
		display: flex;
		align-items: center;
		padding: var(--space-3);
		color: var(--color-text-secondary);
		text-decoration: none;
		border-radius: var(--radius-base);
		border-left: 4px solid transparent;
		font-size: var(--text-sm);
		transition: all var(--transition-fast);
		position: relative;
	}

	.nav-item:hover {
		background: var(--color-hover-bg);
		color: var(--color-text-primary);
	}

	.nav-item.active {
		background: var(--color-bg-tertiary);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-primary);
		border-left-color: var(--color-primary);
	}

	.nav-icon {
		margin-right: var(--space-3);
		display: flex;
		align-items: center;
		transition: color var(--transition-fast);
	}

	.nav-item.active .nav-icon {
		color: var(--color-primary);
	}

	/* Main Content Wrapper */
	.main-wrapper {
		margin-left: 220px;
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	/* Top Header */
	.top-header {
		background: #ffffff;
		border-bottom: 1px solid #e5e5e5;
		padding: 0 2rem;
		height: 60px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.header-right {
		display: flex;
		align-items: center;
		gap: 1.5rem;
		margin-left: auto;
	}

	/* User Menu */
	.user-menu {
		position: relative;
	}

	.user-button {
		background: none;
		border: none;
		color: #333;
		font-size: 0.9375rem;
		cursor: pointer;
		padding: 0.5rem 0.75rem;
		border-radius: 4px;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.user-button:hover {
		background: #f5f5f5;
	}

	.user-avatar {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.75rem;
		font-weight: var(--font-weight-medium);
		color: var(--color-bg-primary);
		letter-spacing: -0.02em;
	}

	.user-avatar-image {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		object-fit: cover;
		border: 1px solid var(--color-border);
	}

	.user-name {
		max-width: 150px;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.dropdown-arrow {
		font-size: 0.75rem;
		color: #999;
	}

	.user-dropdown {
		position: absolute;
		top: 100%;
		right: 0;
		margin-top: 0.5rem;
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		min-width: 180px;
		z-index: 100;
	}

	.dropdown-item {
		display: block;
		padding: 0.75rem 1rem;
		color: #333;
		text-decoration: none;
		font-size: 0.9375rem;
		border: none;
		background: none;
		width: 100%;
		text-align: left;
		cursor: pointer;
	}

	.dropdown-item:hover {
		background: #f5f5f5;
	}

	.dropdown-item.logout {
		color: #d32f2f;
	}

	.dropdown-divider {
		border: none;
		border-top: 1px solid #e5e5e5;
		margin: 0.5rem 0;
	}

	/* Content Area */
	.content {
		flex: 1;
		padding: 2rem;
		max-width: 1400px;
		width: 100%;
	}
</style>
