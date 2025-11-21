<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getSleepStats,
		getNightlySummaries,
		type NightlySummary
	} from '$lib/api/client';

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
		<div class="status">Loading data...</div>
	{:else if error}
		<div class="status error">
			{error}
			<p style="margin-top: 1rem;">
				<a href="/data" style="color: #0066cc; text-decoration: none;">
					Import data to get started →
				</a>
			</p>
		</div>
	{:else if stats && stats.total_nights > 0}
		<!-- Summary statistics - dense, tabular -->
		<section class="summary-stats">
			<table>
				<thead>
					<tr>
						<th>Period</th>
						<th>Nights</th>
						<th>Avg Sleep</th>
						<th>Avg Efficiency</th>
						<th>REM</th>
						<th>Deep</th>
						<th>Core</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>{stats.date_range.start} to {stats.date_range.end}</td>
						<td>{stats.total_nights}</td>
						<td>{formatHours(stats.average_sleep_hours)}</td>
						<td class={getEfficiencyClass(stats.average_efficiency)}>
							{stats.average_efficiency.toFixed(1)}%
						</td>
						<td>{stats.average_rem_pct?.toFixed(1) || '—'}%</td>
						<td>{stats.average_deep_pct?.toFixed(1) || '—'}%</td>
						<td>{stats.average_core_pct?.toFixed(1) || '—'}%</td>
					</tr>
				</tbody>
			</table>
			<p class="benchmark-note">
				Target ranges: Sleep 7-9h [1], Efficiency ≥90% [2], REM 20-25% [3], Deep 13-23% [4], Core 45-55% [4]
			</p>
		</section>

		<!-- Small multiples grid: nights at a glance -->
		<section class="small-multiples">
			<h2>Nightly Records</h2>
			<div class="nights-grid">
				{#each summaries as summary}
					<a href="/sleep/{summary.date}" class="night-card">
						<div class="night-date">{formatDate(summary.date)}</div>
						<div class="night-times">
							{formatTime(summary.sleep_start)}–{formatTime(summary.sleep_end)}
						</div>
						<div class="night-duration">{formatHours(summary.total_sleep_hours)}</div>

						<!-- Minimal sleep stage strip -->
						{#if summary.asleep_rem_pct}
							<div class="stage-strip">
								<div class="stage rem" style="width: {summary.asleep_rem_pct}%"
									 title="REM {summary.asleep_rem_pct.toFixed(1)}%"></div>
								<div class="stage deep" style="width: {summary.asleep_deep_pct}%"
									 title="Deep {summary.asleep_deep_pct.toFixed(1)}%"></div>
								<div class="stage core" style="width: {summary.asleep_core_pct}%"
									 title="Core {summary.asleep_core_pct.toFixed(1)}%"></div>
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

		<!-- Comparative table: see all nights at once -->
		<section class="data-table">
			<h2>Detailed Records</h2>
			<table>
				<thead>
					<tr>
						<th>Date</th>
						<th>Bedtime</th>
						<th>Wake</th>
						<th>Total</th>
						<th>Efficiency</th>
						<th>REM</th>
						<th>Deep</th>
						<th>Core</th>
						<th>Awake</th>
					</tr>
				</thead>
				<tbody>
					{#each summaries as summary}
						<tr>
							<td><a href="/sleep/{summary.date}">{formatDate(summary.date)}</a></td>
							<td>{formatTime(summary.sleep_start)}</td>
							<td>{formatTime(summary.sleep_end)}</td>
							<td>{formatHours(summary.total_sleep_hours)}</td>
							<td class={getEfficiencyClass(summary.sleep_efficiency_pct)}>
								{summary.sleep_efficiency_pct.toFixed(1)}%
							</td>
							<td>{summary.asleep_rem_minutes || 0}m</td>
							<td>{summary.asleep_deep_minutes || 0}m</td>
							<td>{summary.asleep_core_minutes || 0}m</td>
							<td>{summary.awake_minutes || 0}m</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</section>
	{:else}
		<div class="status">
			No sleep data available.
			<p style="margin-top: 1rem;">
				<a href="/data" style="color: #0066cc; text-decoration: none;">
					Import data to get started →
				</a>
			</p>
		</div>
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

	/* Summary statistics table - high data density */
	.summary-stats {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
	}

	.summary-stats table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9375rem;
	}

	.summary-stats th {
		text-align: left;
		font-weight: 500;
		border-bottom: 2px solid #e5e5e5;
		padding: 0.75rem 0.75rem;
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: #666;
	}

	.summary-stats td {
		padding: 0.75rem 0.75rem;
		border-bottom: 1px solid #f5f5f5;
	}

	.benchmark-note {
		margin: 1rem 0 0 0;
		font-size: 0.875rem;
		color: #666;
		font-style: italic;
		line-height: 1.5;
	}

	/* Efficiency classes - vibrant color */
	.excellent {
		color: #2e7d32; /* Vibrant Green */
	}

	.good {
		color: #1976d2; /* Blue */
	}

	.fair {
		color: #d32f2f; /* Vibrant Red */
	}

	/* Small multiples grid - Tufte's favorite */
	.small-multiples {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
	}

	.nights-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
		gap: 1rem;
		margin-top: 1rem;
	}

	.night-card {
		display: block;
		border: 1px solid #e5e5e5;
		border-radius: 4px;
		padding: 0.875rem;
		text-decoration: none;
		color: inherit;
		transition: all 0.15s;
		background: #fafafa;
	}

	.night-card:hover {
		border-color: #999;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
	}

	.night-date {
		font-size: 0.9rem;
		font-weight: 600;
		margin-bottom: 0.25rem;
	}

	.night-times {
		font-size: 0.75rem;
		color: #6c7086; /* Overlay0 */
		margin-bottom: 0.25rem;
	}

	.night-duration {
		font-size: 1.1rem;
		margin-bottom: 0.5rem;
	}

	/* Minimal stage strip - pure data-ink */
	.stage-strip {
		display: flex;
		height: 6px;
		margin-bottom: 0.5rem;
	}

	.stage {
		height: 100%;
	}

	.stage.rem {
		background: #cba6f7; /* Mauve */
	}

	.stage.deep {
		background: #313244; /* Surface0 - darkest */
	}

	.stage.core {
		background: #a6adc8; /* Overlay2 */
	}

	.night-efficiency {
		font-size: 0.85rem;
		text-align: right;
	}

	/* Detailed data table - maximize information */
	.data-table {
		background: #ffffff;
		border: 1px solid #e5e5e5;
		border-radius: 6px;
		padding: 1.5rem;
		overflow-x: auto;
	}

	.data-table table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9375rem;
	}

	.data-table th {
		text-align: left;
		font-weight: 500;
		border-bottom: 2px solid #e5e5e5;
		padding: 0.75rem 0.75rem;
		font-variant: small-caps;
		letter-spacing: 0.05em;
		white-space: nowrap;
		color: #666;
	}

	.data-table td {
		padding: 0.75rem 0.75rem;
		border-bottom: 1px solid #f5f5f5;
		white-space: nowrap;
	}

	.data-table tr:hover {
		background: #fafafa;
	}

	.data-table a {
		color: #0066cc;
		text-decoration: none;
	}

	.data-table a:hover {
		text-decoration: underline;
	}
</style>
