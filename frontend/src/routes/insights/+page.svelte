<script lang="ts">
	import { onMount } from 'svelte';
	import { generateInsights } from '$lib/api/client';

	let loading = $state(true);
	let regenerating = $state(false);
	let error = $state<string | null>(null);
	let insights = $state<{
		overview: string;
		recommendations: string[];
		patterns: string;
	}>({ overview: '', recommendations: [], patterns: '' });
	let stats = $state<any>(null);
	let generatedAt = $state<string | null>(null);
	let fromCache = $state(false);
	let selectedDays = $state(7);
	let completedTasks = $state<Set<number>>(new Set());

	function loadTaskState() {
		if (typeof window === 'undefined') return;
		const saved = localStorage.getItem('baseline-completed-tasks');
		if (saved) {
			try {
				completedTasks = new Set(JSON.parse(saved));
			} catch (e) {
				completedTasks = new Set();
			}
		}
	}

	function saveTaskState() {
		if (typeof window === 'undefined') return;
		localStorage.setItem('baseline-completed-tasks', JSON.stringify([...completedTasks]));
	}

	function toggleTask(index: number) {
		// Create a new Set to trigger reactivity
		const newSet = new Set(completedTasks);
		if (newSet.has(index)) {
			newSet.delete(index);
		} else {
			newSet.add(index);
		}
		completedTasks = newSet;
		saveTaskState();

		// Force UI update by manually updating the DOM
		updateTaskUI();
	}

	function updateTaskUI() {
		// Update all task items to reflect current state
		document.querySelectorAll('.task-item').forEach((item) => {
			const taskIndex = parseInt(item.getAttribute('data-task-index') || '0', 10);
			const isCompleted = completedTasks.has(taskIndex);

			if (isCompleted) {
				item.classList.add('completed');
			} else {
				item.classList.remove('completed');
			}

			// Update checkbox
			const checkbox = item.querySelector('.task-checkbox');
			if (checkbox) {
				const checkIcon = checkbox.querySelector('.check-icon');
				if (isCompleted && !checkIcon) {
					// Add check icon
					checkbox.innerHTML = '<svg class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>';
				} else if (!isCompleted && checkIcon) {
					// Remove check icon
					checkbox.innerHTML = '';
				}
			}
		});

		// Update notification badge
		updateNotificationBadge();
	}

	function updateNotificationBadge() {
		const badge = document.querySelector('.notification-badge');
		const bell = document.querySelector('.notification-bell');
		const incompleteCount = insights.recommendations.length - completedTasks.size;

		if (badge) {
			badge.textContent = incompleteCount.toString();
			if (incompleteCount === 0) {
				badge.style.display = 'none';
			} else {
				badge.style.display = 'flex';
			}
		}

		// Update progress indicator
		const progressIndicator = document.querySelector('.progress-indicator');
		if (progressIndicator) {
			progressIndicator.textContent = `${completedTasks.size} of ${insights.recommendations.length} completed`;
		}
	}

	async function loadInsights(forceRegenerate: boolean = false) {
		if (forceRegenerate) {
			regenerating = true;
			completedTasks.clear();
			saveTaskState();
		} else {
			loading = true;
		}
		error = null;

		try {
			const data = await generateInsights(selectedDays, forceRegenerate);
			insights = data.insights;
			stats = data.stats;
			generatedAt = data.generated_at;
			fromCache = data.from_cache;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to generate insights';
			console.error('Failed to load insights:', err);
		} finally {
			loading = false;
			regenerating = false;
		}
	}

	function handleRegenerate() {
		loadInsights(true);
	}

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	onMount(() => {
		loadTaskState();
		loadInsights();

		// Pure JavaScript event delegation for task checkboxes
		const handleTaskClick = (e: Event) => {
			const target = e.target as HTMLElement;
			const checkbox = target.closest('.task-checkbox') as HTMLButtonElement;

			if (checkbox) {
				const taskIndex = parseInt(checkbox.getAttribute('data-task-index') || '0', 10);
				toggleTask(taskIndex);
			}
		};

		document.addEventListener('click', handleTaskClick);

		// Inject notification bell into header
		injectNotificationBell();

		return () => {
			document.removeEventListener('click', handleTaskClick);
			removeNotificationBell();
		};
	});

	function injectNotificationBell() {
		if (typeof window === 'undefined') return;

		const headerRight = document.querySelector('.header-right');
		if (!headerRight) return;

		// Create bell element
		const bellDiv = document.createElement('div');
		bellDiv.className = 'notification-bell insights-notification';
		bellDiv.innerHTML = `
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
				<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
				<path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
			</svg>
			<span class="notification-badge" style="display: none;"></span>
		`;

		// Insert before user menu
		const userMenu = headerRight.querySelector('.user-menu');
		if (userMenu) {
			headerRight.insertBefore(bellDiv, userMenu);
		}

		updateNotificationBadge();
	}

	function removeNotificationBell() {
		const bell = document.querySelector('.insights-notification');
		if (bell) {
			bell.remove();
		}
	}
</script>

<svelte:head>
	<title>Insights - Baseline</title>
</svelte:head>

<main>
	<header class="page-header">
		<div class="header-content">
			<h1>Health Insights</h1>
			{#if stats && !loading}
				<p class="subtitle">
					{formatDate(stats.date_range.start)} – {formatDate(stats.date_range.end)}
				</p>
			{/if}
		</div>
		<div class="controls">
			<select bind:value={selectedDays} onchange={() => loadInsights(false)} disabled={loading || regenerating}>
				<option value={7}>Last 7 days</option>
				<option value={14}>Last 14 days</option>
				<option value={30}>Last 30 days</option>
			</select>
			{#if !loading && !error}
				<button
					class="regenerate-btn"
					onclick={handleRegenerate}
					disabled={regenerating}
				>
					{regenerating ? 'Regenerating...' : 'Regenerate'}
				</button>
			{/if}
		</div>
	</header>

	{#if loading}
		<div class="loading-state">
			<div class="spinner"></div>
			<p>Analyzing your sleep patterns...</p>
		</div>
	{:else if error}
		<div class="error-state">
			<svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<circle cx="12" cy="12" r="10"></circle>
				<line x1="12" y1="8" x2="12" y2="12"></line>
				<line x1="12" y1="16" x2="12.01" y2="16"></line>
			</svg>
			<p>{error}</p>
		</div>
	{:else}
		<div class="insights-container" class:regenerating={regenerating}>
			{#if regenerating}
				<div class="regenerating-overlay">
					<div class="spinner"></div>
					<p>Regenerating insights...</p>
				</div>
			{/if}

			<!-- Overview Card -->
			<section class="overview-card">
				<h2>Overview</h2>
				<p class="overview-text">{insights.overview}</p>
			</section>

			<!-- Recommendations Card -->
			{#if insights.recommendations && insights.recommendations.length > 0}
				<section class="recommendations-card">
					<div class="card-header">
						<h2>Action Items</h2>
						<span class="progress-indicator">
							{completedTasks.size} of {insights.recommendations.length} completed
						</span>
					</div>

					<ul class="task-list">
						{#each insights.recommendations as recommendation, index}
							<li class="task-item" class:completed={completedTasks.has(index)} data-task-index={index}>
								<button
									class="task-checkbox"
									data-task-index={index}
									aria-label={completedTasks.has(index) ? 'Mark as incomplete' : 'Mark as complete'}
								>
									{#if completedTasks.has(index)}
										<svg class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
											<polyline points="20 6 9 17 4 12"></polyline>
										</svg>
									{/if}
								</button>
								<span class="task-text">{recommendation}</span>
							</li>
						{/each}
					</ul>
				</section>
			{/if}
		</div>
	{/if}
</main>

<style>
	/* Tufte-inspired design matching app aesthetic */
	main {
		font-family: var(--font-family-base);
		color: #333;
	}

	/* Header */
	.page-header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		margin-bottom: 2rem;
	}

	.header-content {
		flex: 1;
	}

	h1 {
		font-size: 2rem;
		font-weight: 400;
		margin: 0 0 0.5rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	.subtitle {
		font-size: 0.875rem;
		color: #666;
		margin: 0;
		font-style: italic;
	}

	.controls {
		display: flex;
		gap: 0.75rem;
		align-items: center;
		flex-shrink: 0;
	}


	.controls select {
		font-family: var(--font-family-base);
		font-size: 0.875rem;
		padding: 0.5rem 0.75rem;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		background: #ffffff;
		color: #333;
		cursor: pointer;
	}

	.controls select:hover:not(:disabled) {
		border-color: #ccc;
	}

	.controls select:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.regenerate-btn {
		font-family: var(--font-family-base);
		font-size: 0.875rem;
		padding: 0.5rem 1rem;
		background: #ffffff;
		color: #333;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		cursor: pointer;
		transition: all 150ms ease;
	}

	.regenerate-btn:hover:not(:disabled) {
		background: #fafafa;
		border-color: #ccc;
	}

	.regenerate-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	/* Loading & Error States */
	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 4rem 0;
		color: #666;
	}

	.spinner {
		width: 32px;
		height: 32px;
		border: 2px solid #e5e5e5;
		border-top-color: #313244;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.loading-state p {
		font-size: 0.875rem;
		font-style: italic;
	}

	.error-state {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 1rem;
		background: var(--color-danger-bg);
		border: 1px solid var(--color-danger-border);
		border-radius: 6px;
		color: var(--color-danger);
	}

	.error-icon {
		width: 20px;
		height: 20px;
		flex-shrink: 0;
	}

	/* Insights Container */
	.insights-container {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		position: relative;
		transition: opacity 300ms ease;
	}

	.insights-container.regenerating {
		opacity: 0.3;
	}

	.regenerating-overlay {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 100;
		background: #ffffff;
		padding: 2rem;
		border-radius: 6px;
		border: 1px solid #e5e5e5;
	}

	.regenerating-overlay p {
		margin-top: 1rem;
		color: #666;
		font-size: 0.875rem;
		font-style: italic;
	}

	/* Cards - matching sleep page metric cards */
	.overview-card,
	.recommendations-card {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
	}

	h2 {
		font-size: 1.25rem;
		font-weight: 400;
		margin: 0 0 1rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	.overview-text {
		font-size: 1rem;
		line-height: 1.7;
		color: #333;
		margin: 0;
	}

	/* Action Items */
	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		margin-bottom: 1rem;
	}

	.progress-indicator {
		font-size: 0.875rem;
		color: #666;
		font-variant-numeric: tabular-nums;
	}

	.task-list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.task-item {
		display: flex;
		align-items: flex-start;
		gap: 0.75rem;
		padding: 0.75rem 0;
		border-bottom: 1px solid #f5f5f5;
		transition: background-color 150ms ease;
	}

	.task-item:last-child {
		border-bottom: none;
	}

	.task-item.completed .task-text {
		text-decoration: line-through;
		opacity: 0.4;
	}

	.task-checkbox {
		flex-shrink: 0;
		width: 18px;
		height: 18px;
		border: 1.5px solid #ccc;
		border-radius: 3px;
		background: #ffffff;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 150ms ease;
		padding: 0;
		margin-top: 2px;
	}

	.task-checkbox:hover {
		border-color: #313244;
	}

	.task-item.completed .task-checkbox {
		background: #313244;
		border-color: #313244;
	}

	.check-icon {
		width: 12px;
		height: 12px;
		stroke: white;
		stroke-linecap: round;
		stroke-linejoin: round;
	}

	.task-text {
		flex: 1;
		font-size: 1rem;
		line-height: 1.6;
		color: #333;
		transition: opacity 150ms ease;
	}

	/* Responsive */
	@media (max-width: 768px) {
		.page-header {
			flex-direction: column;
			align-items: stretch;
			gap: 1rem;
		}

		.controls {
			justify-content: space-between;
		}

		h1 {
			font-size: 1.75rem;
		}

		.overview-card,
		.recommendations-card {
			padding: 1.25rem;
		}
	}
</style>
