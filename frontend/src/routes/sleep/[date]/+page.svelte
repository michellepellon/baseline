<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import {
		getSleepRecords,
		getNightlySummaries,
		type SleepRecord,
		type NightlySummary
	} from '$lib/api/client';
	import Hypnogram from '$lib/components/visualizations/Hypnogram.svelte';
	import Skeleton from '$lib/components/Skeleton.svelte';

	let date: string;
	let records: SleepRecord[] = [];
	let summary: NightlySummary | null = null;
	let loading = true;
	let error: string | null = null;

	$: date = $page.params.date;

	async function loadData() {
		loading = true;
		error = null;

		try {
			const [recordsData, summariesData] = await Promise.all([
				getSleepRecords(date, date),
				getNightlySummaries(date, date)
			]);

			records = recordsData;
			summary = summariesData[0] || null;

			if (!summary) {
				error = 'No data for this date';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load data';
		} finally {
			loading = false;
		}
	}

	onMount(loadData);

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toLocaleDateString('en-US', {
			weekday: 'short',
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		});
	}

	function formatTime(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toLocaleTimeString('en-US', {
			hour: 'numeric',
			minute: '2-digit',
			hour12: true
		});
	}

	function formatDuration(hours: number): string {
		const h = Math.floor(hours);
		const m = Math.round((hours - h) * 60);
		return `${h}:${m.toString().padStart(2, '0')}`;
	}

	function compareToTarget(value: number, min: number, max: number): string {
		if (value >= min && value <= max) return 'within-target';
		if (value < min) return 'below-target';
		return 'above-target';
	}
</script>

<svelte:head>
	<title>Sleep: {date}</title>
</svelte:head>

<main>
	<header>
		<a href="/sleep" class="back">← Sleep</a>
		{#if summary}
			<h1>{formatDate(summary.date)}</h1>
		{/if}
	</header>

	{#if loading}
		<!-- Skeleton Loading State -->
		<header>
			<a href="/sleep" class="back">← Sleep</a>
			<Skeleton width="250px" height="2rem" />
		</header>

		<section class="visualization">
			<Skeleton height="300px" borderRadius="6px" />
		</section>

		<section class="metrics-grid">
			{#each Array(4) as _}
				<div class="metric-card">
					<Skeleton height="0.75rem" width="40%" />
					<Skeleton height="2rem" width="60%" />
					<Skeleton height="1px" width="100%" />
					<Skeleton height="0.8125rem" width="70%" />
				</div>
			{/each}
		</section>

		<section class="stage-breakdown">
			<Skeleton height="1.25rem" width="180px" />
			<div class="stage-grid">
				{#each Array(4) as _}
					<div class="stage-card">
						<Skeleton height="0.75rem" width="60%" />
						<Skeleton height="1.5rem" width="50%" />
						<Skeleton height="1px" width="100%" />
						<Skeleton height="0.75rem" width="70%" />
					</div>
				{/each}
			</div>
		</section>
	{:else if error}
		<div class="status error">{error}</div>
	{:else if summary && records.length > 0}
		<!-- Hypnogram: Visual first -->
		<section class="visualization">
			<Hypnogram {records} {summary} />
		</section>

		<!-- Key metrics: Card-based design -->
		<section class="metrics-grid">
			<div class="metric-card sleep-card">
				<div class="metric-content">
					<span class="metric-label">Total Sleep</span>
					<span class="metric-value">{formatDuration(summary.total_sleep_hours)}</span>
				</div>
				<div class="metric-assessment {compareToTarget(summary.total_sleep_hours, 7, 9)}">
					{#if summary.total_sleep_hours < 7}
						{(7 - summary.total_sleep_hours).toFixed(1)}h below optimal
					{:else if summary.total_sleep_hours > 9}
						{(summary.total_sleep_hours - 9).toFixed(1)}h above optimal
					{:else}
						Optimal
					{/if}
				</div>
			</div>

			<div class="metric-card efficiency-card">
				<div class="metric-content">
					<span class="metric-label">Efficiency</span>
					<span class="metric-value">{summary.sleep_efficiency_pct.toFixed(0)}%</span>
				</div>
				<div class="metric-assessment {compareToTarget(summary.sleep_efficiency_pct, 90, 100)}">
					{#if summary.sleep_efficiency_pct >= 90}
						Optimal
					{:else}
						{(90 - summary.sleep_efficiency_pct).toFixed(0)}% below optimal
					{/if}
				</div>
			</div>

			<div class="metric-card time-card">
				<div class="metric-content">
					<span class="metric-label">Bedtime</span>
					<span class="metric-value-time">{formatTime(summary.sleep_start)}</span>
				</div>
				<div class="metric-info">Target: 10-11:30 PM</div>
			</div>

			<div class="metric-card time-card">
				<div class="metric-content">
					<span class="metric-label">Wake Time</span>
					<span class="metric-value-time">{formatTime(summary.sleep_end)}</span>
				</div>
				<div class="metric-info">Target: 6-7:30 AM</div>
			</div>
		</section>

		<!-- Sleep Stage Breakdown -->
		{#if summary.asleep_rem_pct}
			<section class="stage-breakdown">
				<h2>Sleep Architecture</h2>
				<div class="stage-grid">
					<div class="stage-card deep-stage">
						<div class="stage-content">
							<span class="stage-label">Deep Sleep</span>
							<span class="stage-value">{summary.asleep_deep_pct.toFixed(1)}%</span>
						</div>
						<div class="stage-assessment {compareToTarget(summary.asleep_deep_pct || 0, 13, 23)}">
							{#if (summary.asleep_deep_pct || 0) < 13}
								Below optimal
							{:else if (summary.asleep_deep_pct || 0) > 23}
								Above optimal
							{:else}
								Optimal
							{/if}
						</div>
					</div>

					<div class="stage-card core-stage">
						<div class="stage-content">
							<span class="stage-label">Core Sleep</span>
							<span class="stage-value">{summary.asleep_core_pct.toFixed(1)}%</span>
						</div>
						<div class="stage-assessment {compareToTarget(summary.asleep_core_pct || 0, 45, 55)}">
							{#if (summary.asleep_core_pct || 0) < 45}
								Below optimal
							{:else if (summary.asleep_core_pct || 0) > 55}
								Above optimal
							{:else}
								Optimal
							{/if}
						</div>
					</div>

					<div class="stage-card rem-stage">
						<div class="stage-content">
							<span class="stage-label">REM Sleep</span>
							<span class="stage-value">{summary.asleep_rem_pct.toFixed(1)}%</span>
						</div>
						<div class="stage-assessment {compareToTarget(summary.asleep_rem_pct || 0, 20, 25)}">
							{#if (summary.asleep_rem_pct || 0) < 20}
								Below optimal
							{:else if (summary.asleep_rem_pct || 0) > 25}
								Above optimal
							{:else}
								Optimal
							{/if}
						</div>
					</div>

					<div class="stage-card awake-stage">
						<div class="stage-content">
							<span class="stage-label">Awake</span>
							<span class="stage-value">{(summary.awake_pct || 0).toFixed(1)}%</span>
						</div>
					</div>
				</div>
			</section>
		{/if}

	{/if}
</main>

<style>
	/* Tufte-style typography */
	main {
		font-family: 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif;
		color: #333;
	}

	header {
		margin-bottom: 2rem;
	}

	.back {
		display: inline-block;
		margin-bottom: 0.5rem;
		font-size: 0.9375rem;
		color: #6c7086;
		text-decoration: none;
		transition: color 0.15s;
	}

	.back:hover {
		color: #313244;
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

	.visualization {
		margin-bottom: 1.5rem;
	}

	/* Metrics Grid - Card based design */
	.metrics-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
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
		gap: 0.75rem;
	}

	.sleep-card {
		border-left-color: #313244;
	}

	.efficiency-card {
		border-left-color: #cba6f7;
	}

	.time-card {
		border-left-color: #a6adc8;
	}

	.metric-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.metric-label {
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #666;
		font-variant: small-caps;
	}

	.metric-value {
		font-size: 2rem;
		font-weight: 300;
		color: #000;
		letter-spacing: -0.02em;
		line-height: 1;
	}

	.metric-value-time {
		font-size: 1.25rem;
		font-weight: 400;
		color: #000;
		letter-spacing: -0.01em;
		line-height: 1.2;
	}

	.metric-assessment {
		font-size: 0.8125rem;
		padding-top: 0.5rem;
		border-top: 1px solid #eff1f5;
	}

	.metric-info {
		font-size: 0.8125rem;
		color: #6c7086;
		padding-top: 0.5rem;
		border-top: 1px solid #eff1f5;
	}

	/* Sleep Stage Breakdown */
	.stage-breakdown {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
		margin-bottom: 1.5rem;
	}

	.stage-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1.5rem;
		margin-top: 1rem;
	}

	.stage-card {
		background: #fafafa;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		border-left: 6px solid #6c7086;
		padding: 1.25rem;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.deep-stage {
		border-left-color: #313244;
	}

	.core-stage {
		border-left-color: #a6adc8;
	}

	.rem-stage {
		border-left-color: #cba6f7;
	}

	.awake-stage {
		border-left-color: #f5e0dc;
	}

	.stage-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stage-label {
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #666;
		font-variant: small-caps;
	}

	.stage-value {
		font-size: 1.5rem;
		font-weight: 300;
		color: #000;
		letter-spacing: -0.02em;
		line-height: 1;
	}

	.stage-percent {
		font-size: 1rem;
		color: #6c7086;
	}

	.stage-assessment {
		font-size: 0.75rem;
		padding-top: 0.5rem;
		border-top: 1px solid #e5e5e5;
	}

	.stage-info {
		font-size: 0.75rem;
		color: #6c7086;
		padding-top: 0.5rem;
		border-top: 1px solid #e5e5e5;
	}

	.within-target {
		color: #2e7d32;
	}

	.below-target,
	.above-target {
		color: #d32f2f;
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) {
		.stage-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media (max-width: 640px) {
		.metrics-grid {
			grid-template-columns: 1fr;
		}

		.stage-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
