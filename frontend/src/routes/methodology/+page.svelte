<script lang="ts">
</script>

<svelte:head>
	<title>Methodology - Baseline</title>
</svelte:head>

<main>
	<header>
		<h1>Methodology</h1>
		<p class="subtitle">Scientific foundations for sleep metrics and target ranges</p>
	</header>

	<section class="target-ranges">
		<h2>Target Ranges</h2>
		<table>
			<thead>
				<tr>
					<th>Metric</th>
					<th>Target Range</th>
					<th>Source</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>Total Sleep Duration</td>
					<td>7-9 hours</td>
					<td>[1] National Sleep Foundation</td>
				</tr>
				<tr>
					<td>Sleep Efficiency</td>
					<td>≥90%</td>
					<td>[2] National Sleep Foundation</td>
				</tr>
				<tr>
					<td>REM Sleep</td>
					<td>20-25% of total sleep</td>
					<td>[3] American Academy of Sleep Medicine</td>
				</tr>
				<tr>
					<td>Deep Sleep</td>
					<td>13-23% of total sleep</td>
					<td>[4] Meta-analysis of sleep parameters</td>
				</tr>
				<tr>
					<td>Core/Light Sleep</td>
					<td>45-55% of total sleep</td>
					<td>[4] Meta-analysis of sleep parameters</td>
				</tr>
				<tr>
					<td>Bedtime</td>
					<td>10:00 PM - 11:30 PM</td>
					<td>[5] Circadian rhythm optimization</td>
				</tr>
				<tr>
					<td>Wake Time</td>
					<td>6:00 AM - 7:30 AM</td>
					<td>[5] Circadian rhythm optimization</td>
				</tr>
			</tbody>
		</table>
	</section>

	<section class="references">
		<h2>Scientific References</h2>
		<ol>
			<li>
				<strong>Hirshkowitz M, Whiton K, Albert SM, et al.</strong> National Sleep
				Foundation's sleep time duration recommendations: methodology and results summary.
				<i>Sleep Health</i>. 2015;1(1):40-43.
				<p class="note">
					Comprehensive review establishing evidence-based sleep duration recommendations
					for different age groups. The 7-9 hour recommendation for adults (26-64 years) is
					based on extensive literature review and expert panel consensus.
				</p>
			</li>
			<li>
				<strong>Ohayon M, Wickwire EM, Hirshkowitz M, et al.</strong> National Sleep
				Foundation's sleep quality recommendations: first report. <i>Sleep Medicine</i>.
				2017;38:6-15.
				<p class="note">
					Established the ≥90% sleep efficiency threshold as a marker of good sleep quality.
					Sleep efficiency is calculated as (total sleep time / time in bed) × 100.
				</p>
			</li>
			<li>
				<strong>Berry RB, Quan SF, Abreu AR, et al.</strong> The AASM Manual for the Scoring
				of Sleep and Associated Events: Rules, Terminology and Technical Specifications.
				Version 2.6. <i>American Academy of Sleep Medicine</i>. 2020.
				<p class="note">
					Authoritative guidelines for sleep stage classification and scoring. Establishes
					normative ranges for REM sleep across the lifespan.
				</p>
			</li>
			<li>
				<strong>Ohayon MM, Carskadon MA, Guilleminault C, Vitiello MV.</strong> Meta-analysis
				of quantitative sleep parameters from childhood to old age in healthy individuals:
				developing normative sleep values across the human lifespan. <i>Sleep</i>.
				2004;27(7):1255-1273.
				<p class="note">
					Landmark meta-analysis synthesizing sleep architecture data from 65 studies
					(3,577 subjects). Provides normative values for deep sleep, light sleep, and REM
					percentages across age groups.
				</p>
			</li>
			<li>
				<strong>Huberman Lab.</strong> Sleep Toolkit: Tools for Optimizing Sleep &
				Sleep-Wake Timing. <i>Huberman Lab Podcast</i>. 2025.
				<p class="note">
					Evidence-based protocols for circadian rhythm optimization, including ideal
					bedtime and wake time windows based on cortisol and melatonin cycles.
				</p>
			</li>
		</ol>
	</section>

	<section class="methodology-notes">
		<h2>Data Processing</h2>
		<p>
			Baseline processes sleep data from Apple HealthKit exports. Sleep stages are classified
			according to the source device (Apple Watch, Oura Ring, etc.), which use accelerometry
			and heart rate variability to estimate sleep architecture.
		</p>
		<p>
			Sleep efficiency is calculated as: <code
				>(Total Sleep Time / Time in Bed) × 100</code
			>
		</p>
		<p>
			All percentages for sleep stages (REM, Deep, Core) are calculated as a percentage of
			total sleep time, not time in bed.
		</p>
	</section>
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

	h1 {
		font-size: 2rem;
		font-weight: 400;
		margin: 0 0 0.5rem 0;
		letter-spacing: -0.01em;
		color: #000;
	}

	.subtitle {
		font-size: 1rem;
		color: #666;
		margin: 0;
		font-style: italic;
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

	/* Target ranges table */
	.target-ranges table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9375rem;
	}

	.target-ranges th {
		text-align: left;
		font-weight: 500;
		border-bottom: 2px solid #e5e5e5;
		padding: 0.75rem 0.75rem;
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: #666;
	}

	.target-ranges td {
		padding: 0.75rem 0.75rem;
		border-bottom: 1px solid #f5f5f5;
	}

	.target-ranges tr:hover {
		background: #fafafa;
	}

	/* References section */
	.references ol {
		margin: 0;
		padding-left: 1.75rem;
		font-size: 0.9375rem;
		line-height: 1.6;
	}

	.references li {
		margin-bottom: 1.5rem;
	}

	.references strong {
		font-weight: 600;
		color: #000;
	}

	.references i {
		font-style: italic;
	}

	.note {
		margin: 0.5rem 0 0 0;
		padding-left: 0;
		font-size: 0.875rem;
		color: #666;
		line-height: 1.5;
	}

	/* Methodology notes */
	.methodology-notes p {
		margin: 0 0 1rem 0;
		line-height: 1.6;
		font-size: 0.9375rem;
	}

	.methodology-notes code {
		background: #f5f5f5;
		padding: 0.125rem 0.375rem;
		border-radius: 3px;
		font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
		font-size: 0.875rem;
		color: #000;
	}
</style>
