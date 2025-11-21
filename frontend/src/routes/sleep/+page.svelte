<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getSleepStats,
		getNightlySummaries,
		type NightlySummary
	} from '$lib/api/client';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import Skeleton from '$lib/components/Skeleton.svelte';

	let stats: Awaited<ReturnType<typeof getSleepStats>> | null = null;
	let summaries: NightlySummary[] = [];
	let loading = true;
	let error: string | null = null;

	async function loadData() {
		loading = true;
		error = null;

		try {
			[stats, summaries] = await Promise.all([getSleepStats(), getNightlySummaries()]);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load data';
		} finally {
			loading = false;
		}
	}

	onMount(loadData);

	// Generate last 30 days tracking visualization
	function getLast30DaysTracking(): boolean[] {
		if (!summaries || summaries.length === 0) return [];

		const today = new Date();
		today.setHours(0, 0, 0, 0);

		const last30Days: boolean[] = [];
		const summaryDates = new Set(summaries.map(s => s.date));

		for (let i = 29; i >= 0; i--) {
			const date = new Date(today);
			date.setDate(date.getDate() - i);
			const dateStr = date.toISOString().split('T')[0];
			last30Days.push(summaryDates.has(dateStr));
		}

		return last30Days;
	}

	// Get sleep hours for last 30 days
	function getLast30DaysSleep(): (number | null)[] {
		if (!summaries || summaries.length === 0) return [];

		const today = new Date();
		today.setHours(0, 0, 0, 0);

		const summaryMap = new Map(summaries.map(s => [s.date, s.total_sleep_hours]));
		const last30Days: (number | null)[] = [];

		for (let i = 29; i >= 0; i--) {
			const date = new Date(today);
			date.setDate(date.getDate() - i);
			const dateStr = date.toISOString().split('T')[0];
			last30Days.push(summaryMap.get(dateStr) ?? null);
		}

		return last30Days;
	}

	// Get efficiency for last 30 days
	function getLast30DaysEfficiency(): (number | null)[] {
		if (!summaries || summaries.length === 0) return [];

		const today = new Date();
		today.setHours(0, 0, 0, 0);

		const summaryMap = new Map(summaries.map(s => [s.date, s.sleep_efficiency_pct]));
		const last30Days: (number | null)[] = [];

		for (let i = 29; i >= 0; i--) {
			const date = new Date(today);
			date.setDate(date.getDate() - i);
			const dateStr = date.toISOString().split('T')[0];
			last30Days.push(summaryMap.get(dateStr) ?? null);
		}

		return last30Days;
	}

	function formatHours(hours: number): string {
		const h = Math.floor(hours);
		const m = Math.round((hours - h) * 60);
		return `${h}:${m.toString().padStart(2, '0')}`;
	}

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
	}

	function formatTime(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toLocaleTimeString('en-US', {
			hour: 'numeric',
			minute: '2-digit',
			hour12: true
		});
	}

	function getEfficiencyClass(efficiency: number): string {
		if (efficiency >= 90) return 'excellent';
		if (efficiency >= 85) return 'good';
		return 'fair';
	}
</script>

<svelte:head>
	<title>Sleep - Baseline</title>
</svelte:head>

<main>
	<!-- Minimal header -->
	<header>
		<h1>Sleep</h1>
	</header>

	{#if loading}
		<!-- Skeleton Loading State -->
		<section class="overview-metrics">
			<div class="metric-card">
				<Skeleton height="2rem" width="60%" />
				<Skeleton height="0.75rem" width="40%" />
				<div style="margin-top: 1rem;">
					<Skeleton height="12px" borderRadius="6px" />
					<div style="margin-top: 0.5rem; display: flex; justify-content: space-between;">
						<Skeleton height="0.75rem" width="15%" />
						<Skeleton height="0.75rem" width="15%" />
						<Skeleton height="0.75rem" width="15%" />
					</div>
				</div>
			</div>
			<div class="metric-card">
				<Skeleton height="2rem" width="60%" />
				<Skeleton height="0.75rem" width="40%" />
				<div style="margin-top: 1rem;">
					<Skeleton height="12px" borderRadius="6px" />
					<div style="margin-top: 0.5rem; display: flex; justify-content: space-between;">
						<Skeleton height="0.75rem" width="15%" />
						<Skeleton height="0.75rem" width="15%" />
					</div>
				</div>
			</div>
			<div class="metric-card">
				<Skeleton height="2rem" width="60%" />
				<Skeleton height="0.75rem" width="40%" />
				<div style="margin-top: 1rem;">
					<Skeleton height="12px" borderRadius="6px" />
					<div style="margin-top: 0.5rem; display: flex; justify-content: space-between;">
						<Skeleton height="0.75rem" width="15%" />
						<Skeleton height="0.75rem" width="15%" />
						<Skeleton height="0.75rem" width="15%" />
					</div>
				</div>
			</div>
		</section>

		<section class="nightly-records">
			<h2>History</h2>
			<div class="nights-list">
				{#each Array(5) as _}
					<div class="night-row-skeleton">
						<Skeleton width="80px" height="1rem" />
						<div>
							<Skeleton width="200px" height="0.875rem" />
							<Skeleton width="100px" height="1rem" />
						</div>
						<Skeleton height="12px" borderRadius="2px" />
						<Skeleton width="60px" height="0.875rem" />
					</div>
				{/each}
			</div>
		</section>
	{:else if error || !stats || stats.total_nights === 0}
		<EmptyState
			title="No sleep data yet"
			description="Import your Apple Health data to start tracking your sleep patterns and gain insights into your sleep quality."
			actionLabel="Import Data"
			actionHref="/data"
		/>
	{:else if stats && stats.total_nights > 0}
		<!-- Overview metrics -->
		<section class="overview-metrics">
			<div class="metric-card">
				<div class="metric-content">
					<span class="metric-value">{formatHours(stats.average_sleep_hours)}</span>
					<span class="metric-label">avg sleep</span>
				</div>
				<div class="range-gauge">
					<div class="range-track">
						<div class="range-target poor" style="left: 0%; width: 70%"></div>
						<div class="range-target optimal" style="left: 70%; width: 20%"></div>
						<div class="range-target warning" style="left: 90%; width: 10%"></div>
						<div class="range-marker" style="left: {Math.min(Math.max((stats.average_sleep_hours / 10) * 100, 0), 100)}%"></div>
					</div>
					<div class="range-labels">
						<span>0h</span>
						<span>7h</span>
						<span>9h</span>
						<span>10h</span>
					</div>
				</div>
			</div>

			<div class="metric-card">
				<div class="metric-content">
					<span class="metric-value">{stats.average_efficiency.toFixed(0)}%</span>
					<span class="metric-label">efficiency</span>
				</div>
				<div class="range-gauge">
					<div class="range-track">
						<div class="range-target poor" style="left: 0%; width: 90%"></div>
						<div class="range-target optimal" style="left: 90%; width: 10%"></div>
						<div class="range-marker" style="left: {stats.average_efficiency}%"></div>
					</div>
					<div class="range-labels">
						<span>0%</span>
						<span>90%</span>
						<span>100%</span>
					</div>
				</div>
			</div>

			<div class="metric-card">
				<div class="metric-content">
					<span class="metric-value">{getLast30DaysTracking().filter(t => t).length}/30</span>
					<span class="metric-label">last 30 days</span>
				</div>
				<div class="range-gauge">
					<div class="range-track">
						<div class="range-target optimal" style="left: 0%; width: 100%"></div>
						<div class="range-marker" style="left: {(getLast30DaysTracking().filter(t => t).length / 30) * 100}%"></div>
					</div>
					<div class="range-labels">
						<span>0</span>
						<span>15</span>
						<span>30</span>
					</div>
				</div>
			</div>
		</section>

		<!-- Nightly records: Timeline view with visual sleep architecture -->
		<section class="nightly-records">
			<h2>History</h2>
			<div class="nights-list">
				{#each summaries as summary}
					<a href="/sleep/{summary.date}" class="night-row">
						<div class="night-date">{formatDate(summary.date)}</div>

						<div class="night-core">
							<div class="night-times">
								{formatTime(summary.sleep_start)} – {formatTime(summary.sleep_end)}
							</div>
							<div class="night-duration">{formatHours(summary.total_sleep_hours)}</div>
						</div>

						<!-- Visual sleep stage breakdown -->
						{#if summary.asleep_rem_pct}
							<div class="stage-bar-wrapper">
								<div class="stage-bar">
									<div class="stage deep" style="width: {summary.asleep_deep_pct}%"></div>
									<div class="stage core" style="width: {summary.asleep_core_pct}%"></div>
									<div class="stage rem" style="width: {summary.asleep_rem_pct}%"></div>
									<div class="stage awake" style="width: {summary.awake_pct || 0}%"></div>
								</div>
								<div class="stage-tooltip">
									Deep: {Math.round(summary.asleep_deep_minutes || 0)}m ({summary.asleep_deep_pct?.toFixed(1)}%) |
									Core: {Math.round(summary.asleep_core_minutes || 0)}m ({summary.asleep_core_pct?.toFixed(1)}%) |
									REM: {Math.round(summary.asleep_rem_minutes || 0)}m ({summary.asleep_rem_pct?.toFixed(1)}%) |
									Awake: {Math.round(summary.awake_minutes || 0)}m ({(summary.awake_pct || 0).toFixed(1)}%)
								</div>
							</div>
						{/if}

						<div class="night-efficiency" class:excellent={summary.sleep_efficiency_pct >= 90}
							 class:good={summary.sleep_efficiency_pct >= 85 && summary.sleep_efficiency_pct < 90}>
							{summary.sleep_efficiency_pct.toFixed(0)}%
						</div>
					</a>
				{/each}
			</div>
		</section>
	{/if}
</main>

<style>
	/* Tufte-style typography with Carta layout */
	main {
		font-family: 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif;
		color: #333;
	}

	/* Minimal header */
	header {
		margin-bottom: 2rem;
	}

	h1 {
		font-size: 2rem;
		font-weight: 400;
		margin: 0 0 1rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	h2 {
		font-size: 1.25rem;
		font-weight: 400;
		margin: 2rem 0 1rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	section {
		margin-bottom: 2rem;
	}

	.status {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
		color: #666;
		font-style: italic;
	}

	.status.error {
		color: #d32f2f;
		border-color: #ffcdd2;
		background: #ffebee;
	}

	/* Overview metrics - unified with page design */
	.overview-metrics {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.5rem;
		margin-bottom: 1.5rem;
	}

	.metric-card {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		border-left: 6px solid #6c7086;
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.metric-card:nth-child(1) {
		border-left-color: #313244; /* Deep sleep - dark */
	}

	.metric-card:nth-child(2) {
		border-left-color: #cba6f7; /* REM - purple */
	}

	.metric-card:nth-child(3) {
		border-left-color: #a6adc8; /* Core - gray-blue */
	}

	.metric-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.metric-value {
		font-size: 2rem;
		font-weight: 300;
		color: #000;
		letter-spacing: -0.02em;
		line-height: 1;
	}

	.metric-label {
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #666;
		font-variant: small-caps;
	}

	/* Range gauge */
	.range-gauge {
		padding-top: 0.5rem;
		border-top: 1px solid #eff1f5;
	}

	.range-track {
		position: relative;
		height: 12px;
		background: #eff1f5;
		border-radius: 6px;
		margin-bottom: 0.5rem;
		overflow: hidden;
	}

	.range-target {
		position: absolute;
		height: 100%;
	}

	.range-target.poor {
		background: #f5e0dc;
	}

	.range-target.warning {
		background: #f9e2af;
	}

	.range-target.optimal {
		background: #a6e3a1;
	}

	.range-marker {
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
		width: 6px;
		height: 20px;
		background: #89b4fa;
		border-radius: 3px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
	}

	.range-labels {
		display: flex;
		justify-content: space-between;
		font-size: 0.75rem;
		color: #6c7086;
	}

	/* Efficiency classes */
	.excellent {
		color: #2e7d32;
	}

	.good {
		color: #1976d2;
	}

	.fair {
		color: #d32f2f;
	}

	/* Nightly records - Timeline list with visual stage bars */
	.nightly-records {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
	}

	.nights-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-top: 1rem;
	}

	.night-row {
		display: grid;
		grid-template-columns: 80px 200px 1fr 60px;
		gap: 1rem;
		align-items: center;
		padding: 0.75rem 1rem;
		background: #fafafa;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		text-decoration: none;
		color: inherit;
		transition: all 0.15s;
	}

	.night-row:hover {
		background: #ffffff;
		border-color: #999;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
	}

	.night-date {
		font-size: 0.875rem;
		font-weight: 600;
		color: #333;
	}

	.night-core {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.night-times {
		font-size: 0.8125rem;
		color: #6c7086;
	}

	.night-duration {
		font-size: 1rem;
		font-weight: 500;
	}

	/* Visual stage bar - Tufte-style data visualization */
	.stage-bar-wrapper {
		position: relative;
		width: 100%;
	}

	.stage-bar {
		display: flex;
		height: 12px;
		border-radius: 2px;
		overflow: hidden;
		background: #eff1f5;
		cursor: pointer;
	}

	.stage {
		transition: all 0.2s;
	}

	.stage.deep {
		background: #313244;
	}

	.stage.core {
		background: #a6adc8;
	}

	.stage.rem {
		background: #cba6f7;
	}

	.stage.awake {
		background: #f5e0dc;
	}

	/* Custom tooltip */
	.stage-tooltip {
		position: absolute;
		bottom: 100%;
		left: 50%;
		transform: translateX(-50%);
		margin-bottom: 8px;
		padding: 8px 12px;
		background: #1e1e2e;
		color: #cdd6f4;
		font-size: 0.75rem;
		border-radius: 4px;
		white-space: nowrap;
		opacity: 0;
		pointer-events: none;
		transition: opacity 0.2s;
		z-index: 10;
		border: 1px solid #6c7086;
	}

	.stage-tooltip::after {
		content: '';
		position: absolute;
		top: 100%;
		left: 50%;
		transform: translateX(-50%);
		border: 4px solid transparent;
		border-top-color: #1e1e2e;
	}

	.stage-bar-wrapper:hover .stage-tooltip {
		opacity: 1;
	}

	.night-efficiency {
		font-size: 0.875rem;
		font-weight: 500;
		text-align: right;
	}

	/* Skeleton Loading */
	.night-row-skeleton {
		display: grid;
		grid-template-columns: 80px 200px 1fr 60px;
		gap: 1rem;
		align-items: center;
		padding: 0.75rem 1rem;
		background: #fafafa;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		margin-bottom: 0.5rem;
	}
</style>
