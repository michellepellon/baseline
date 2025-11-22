<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let sleepGoals: string[] = [];
	export let idealBedtime: string = '22:00';
	export let targetSleepDuration: number = 8;
	export let timeFormat: '12h' | '24h' = '12h';

	const dispatch = createEventDispatcher();

	const goalOptions = [
		{ id: 'improve_quality', label: 'Improve sleep quality', icon: '✨' },
		{ id: 'track_patterns', label: 'Track sleep patterns', icon: '📊' },
		{ id: 'optimize_duration', label: 'Optimize sleep duration', icon: '⏰' },
		{ id: 'reduce_awakenings', label: 'Reduce awakenings', icon: '😴' },
		{ id: 'better_consistency', label: 'Better sleep consistency', icon: '📅' }
	];

	function toggleGoal(goalId: string) {
		if (sleepGoals.includes(goalId)) {
			sleepGoals = sleepGoals.filter(g => g !== goalId);
		} else {
			sleepGoals = [...sleepGoals, goalId];
		}
	}

	function handleNext() {
		const preferences = {
			timeFormat,
			idealBedtime,
			targetSleepDuration
		};

		dispatch('next', {
			sleepGoals: JSON.stringify(sleepGoals),
			preferences: JSON.stringify(preferences)
		});
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div class="settings-step">
	<div class="header">
		<h1>Customize Your Experience</h1>
		<p class="subtitle">Help us personalize Baseline for your sleep goals</p>
	</div>

	<div class="content">
		<div class="section">
			<h2>What are your sleep goals?</h2>
			<p class="section-description">Select all that apply</p>

			<div class="goals-grid">
				{#each goalOptions as goal}
					<button
						class="goal-card"
						class:selected={sleepGoals.includes(goal.id)}
						on:click={() => toggleGoal(goal.id)}
					>
						<div class="goal-icon">{goal.icon}</div>
						<div class="goal-label">{goal.label}</div>
						{#if sleepGoals.includes(goal.id)}
							<div class="checkmark">
								<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
								</svg>
							</div>
						{/if}
					</button>
				{/each}
			</div>
		</div>

		<div class="section">
			<h2>Sleep Preferences</h2>

			<div class="preferences-grid">
				<div class="form-group">
					<label for="idealBedtime">Ideal Bedtime</label>
					<input
						id="idealBedtime"
						type="time"
						bind:value={idealBedtime}
						class="input"
					/>
					<p class="help-text">When you ideally want to go to bed</p>
				</div>

				<div class="form-group">
					<label for="targetDuration">Target Sleep Duration (hours)</label>
					<input
						id="targetDuration"
						type="number"
						min="4"
						max="12"
						step="0.5"
						bind:value={targetSleepDuration}
						class="input"
					/>
					<p class="help-text">Your target hours of sleep per night</p>
				</div>

				<div class="form-group">
					<label for="timeFormat">Time Format</label>
					<select id="timeFormat" bind:value={timeFormat} class="input">
						<option value="12h">12-hour (AM/PM)</option>
						<option value="24h">24-hour</option>
					</select>
					<p class="help-text">How to display times in the app</p>
				</div>
			</div>
		</div>
	</div>

	<div class="actions">
		<button class="back-button" on:click={handleBack}>
			Back
		</button>
		<button class="next-button" on:click={handleNext}>
			Continue
		</button>
	</div>
</div>

<style>
	.settings-step {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		max-width: 800px;
		margin: 0 auto;
	}

	.header {
		text-align: center;
	}

	h1 {
		font-size: 2rem;
		font-weight: 700;
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		font-size: 1.125rem;
		color: #6b7280;
	}

	.content {
		display: flex;
		flex-direction: column;
		gap: 2.5rem;
	}

	.section {
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 2rem;
	}

	.section h2 {
		font-size: 1.25rem;
		font-weight: 600;
		color: #111827;
		margin-bottom: 0.5rem;
	}

	.section-description {
		font-size: 0.875rem;
		color: #6b7280;
		margin-bottom: 1.5rem;
	}

	.goals-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
	}

	.goal-card {
		position: relative;
		background: white;
		border: 2px solid #e5e7eb;
		border-radius: 0.75rem;
		padding: 1.5rem;
		text-align: center;
		cursor: pointer;
		transition: all 0.2s;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.goal-card:hover {
		border-color: #3b82f6;
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
	}

	.goal-card.selected {
		border-color: #3b82f6;
		background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
	}

	.goal-icon {
		font-size: 2rem;
	}

	.goal-label {
		font-size: 0.875rem;
		font-weight: 500;
		color: #111827;
	}

	.checkmark {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		width: 1.5rem;
		height: 1.5rem;
		border-radius: 50%;
		background-color: #3b82f6;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.checkmark svg {
		width: 1rem;
		height: 1rem;
	}

	.preferences-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1.5rem;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: #374151;
	}

	.input {
		padding: 0.625rem 0.875rem;
		border: 1px solid #d1d5db;
		border-radius: 0.5rem;
		font-size: 1rem;
		transition: all 0.2s;
	}

	.input:focus {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}

	.help-text {
		font-size: 0.75rem;
		color: #9ca3af;
		margin: 0;
	}

	.actions {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	.back-button,
	.next-button {
		padding: 0.75rem 2rem;
		border-radius: 0.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.back-button {
		background: white;
		color: #6b7280;
		border: 1px solid #d1d5db;
	}

	.back-button:hover {
		background-color: #f9fafb;
	}

	.next-button {
		background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
		color: white;
		border: none;
	}

	.next-button:hover {
		transform: translateY(-1px);
	}
</style>
