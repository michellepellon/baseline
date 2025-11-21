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

	function formatMinutes(minutes: number): string {
		return `${minutes}m`;
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
		<div class="status">Loading...</div>
	{:else if error}
		<div class="status error">{error}</div>
	{:else if summary}
		<!-- Primary metrics table - dense, comparative -->
		<section class="metrics">
			<table>
				<thead>
					<tr>
						<th>Metric</th>
						<th>Value</th>
						<th>Target</th>
						<th>Comparison</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Total Sleep</td>
						<td>{formatDuration(summary.total_sleep_hours)}</td>
						<td>7-9h [1]</td>
						<td class={compareToTarget(summary.total_sleep_hours, 7, 9)}>
							{#if summary.total_sleep_hours < 7}
								{(7 - summary.total_sleep_hours).toFixed(1)}h below minimum
							{:else if summary.total_sleep_hours > 9}
								{(summary.total_sleep_hours - 9).toFixed(1)}h above maximum
							{:else}
								Within target range
							{/if}
						</td>
					</tr>
					<tr>
						<td>Sleep Efficiency</td>
						<td>{summary.sleep_efficiency_pct.toFixed(1)}%</td>
						<td>≥90% [2]</td>
						<td class={compareToTarget(summary.sleep_efficiency_pct, 90, 100)}>
							{#if summary.sleep_efficiency_pct >= 90}
								Optimal ({(summary.sleep_efficiency_pct - 90).toFixed(1)}% above threshold)
							{:else if summary.sleep_efficiency_pct >= 85}
								Good ({(90 - summary.sleep_efficiency_pct).toFixed(1)}% below optimal)
							{:else}
								{(90 - summary.sleep_efficiency_pct).toFixed(1)}% below optimal
							{/if}
						</td>
					</tr>
					<tr>
						<td>Bedtime</td>
						<td>{formatTime(summary.sleep_start)}</td>
						<td>10-11:30 PM [5]</td>
						<td>—</td>
					</tr>
					<tr>
						<td>Wake Time</td>
						<td>{formatTime(summary.sleep_end)}</td>
						<td>6-7:30 AM [5]</td>
						<td>—</td>
					</tr>
				</tbody>
			</table>
		</section>

		<!-- Sleep stages breakdown -->
		{#if summary.asleep_rem_pct}
			<section class="stages">
				<h2>Architecture</h2>
				<table>
					<thead>
						<tr>
							<th>Stage</th>
							<th>Duration</th>
							<th>Percentage</th>
							<th>Target</th>
							<th>Assessment</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>REM</td>
							<td>{formatMinutes(summary.asleep_rem_minutes || 0)}</td>
							<td>{summary.asleep_rem_pct.toFixed(1)}%</td>
							<td>20-25% [3]</td>
							<td class={compareToTarget(summary.asleep_rem_pct || 0, 20, 25)}>
								{#if (summary.asleep_rem_pct || 0) < 20}
									{(20 - (summary.asleep_rem_pct || 0)).toFixed(1)}% below range
								{:else if (summary.asleep_rem_pct || 0) > 25}
									{((summary.asleep_rem_pct || 0) - 25).toFixed(1)}% above range
								{:else}
									Within range
								{/if}
							</td>
						</tr>
						<tr>
							<td>Deep</td>
							<td>{formatMinutes(summary.asleep_deep_minutes || 0)}</td>
							<td>{summary.asleep_deep_pct.toFixed(1)}%</td>
							<td>13-23% [4]</td>
							<td class={compareToTarget(summary.asleep_deep_pct || 0, 13, 23)}>
								{#if (summary.asleep_deep_pct || 0) < 13}
									{(13 - (summary.asleep_deep_pct || 0)).toFixed(1)}% below range
								{:else if (summary.asleep_deep_pct || 0) > 23}
									{((summary.asleep_deep_pct || 0) - 23).toFixed(1)}% above range
								{:else}
									Within range
								{/if}
							</td>
						</tr>
						<tr>
							<td>Core/Light</td>
							<td>{formatMinutes(summary.asleep_core_minutes || 0)}</td>
							<td>{summary.asleep_core_pct.toFixed(1)}%</td>
							<td>45-55% [4]</td>
							<td class={compareToTarget(summary.asleep_core_pct || 0, 45, 55)}>
								{#if (summary.asleep_core_pct || 0) < 45}
									{(45 - (summary.asleep_core_pct || 0)).toFixed(1)}% below range
								{:else if (summary.asleep_core_pct || 0) > 55}
									{((summary.asleep_core_pct || 0) - 55).toFixed(1)}% above range
								{:else}
									Within range
								{/if}
							</td>
						</tr>
						<tr>
							<td>Awake</td>
							<td>{formatMinutes(summary.awake_minutes || 0)}</td>
							<td>{(summary.awake_pct || 0).toFixed(1)}%</td>
							<td>Minimize</td>
							<td>—</td>
						</tr>
					</tbody>
				</table>
			</section>
		{/if}

		<!-- Hypnogram: minimal, data-focused -->
		{#if records.length > 0}
			<section class="visualization">
				<h2>Hypnogram</h2>
				<Hypnogram {records} />
			</section>
		{/if}
	{/if}
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

	.back {
		display: inline-block;
		margin-bottom: 0.5rem;
		font-size: 0.9rem;
		color: #0066cc;
		text-decoration: none;
	}

	.back:hover {
		text-decoration: underline;
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

	/* Tables: maximum data density */
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9375rem;
	}

	th {
		text-align: left;
		font-weight: 500;
		border-bottom: 2px solid #e5e5e5;
		padding: 0.75rem 0.75rem;
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: #666;
	}

	td {
		padding: 0.75rem 0.75rem;
		border-bottom: 1px solid #f5f5f5;
	}

	tr:hover {
		background: #fafafa;
	}

	/* Comparison classes - vibrant, meaningful color */
	.within-target {
		color: #2e7d32; /* Vibrant Green */
	}

	.below-target,
	.above-target {
		color: #d32f2f; /* Vibrant Red */
	}
</style>
