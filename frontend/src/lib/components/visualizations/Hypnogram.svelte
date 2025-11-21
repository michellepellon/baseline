<script lang="ts">
	import { onMount } from 'svelte';
	import type { SleepRecord } from '$lib/api/client';
	import {
		Chart,
		LineController,
		LineElement,
		PointElement,
		LinearScale,
		TimeScale,
		CategoryScale
	} from 'chart.js';
	import 'chartjs-adapter-date-fns';

	export let records: SleepRecord[];

	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;

	Chart.register(
		LineController,
		LineElement,
		PointElement,
		LinearScale,
		TimeScale,
		CategoryScale
	);

	const stageOrder = {
		in_bed: 0,
		asleep_deep: 1,
		asleep_core: 2,
		asleep_unspecified: 2,
		asleep_rem: 3,
		awake: 4
	};

	const stageColors: Record<string, string> = {
		awake: '#f5e0dc',        // Rosewater - lightest for awake
		asleep_rem: '#cba6f7',   // Mauve - distinct for REM
		asleep_core: '#a6adc8',  // Overlay2 - medium gray for core
		asleep_deep: '#313244',  // Surface0 - darkest for deep sleep
		in_bed: '#eff1f5',       // Light gray for in bed
		asleep_unspecified: '#9399b2' // Overlay1 - generic sleep
	};

	const stageLabels: Record<string, string> = {
		awake: 'Awake',
		asleep_rem: 'REM',
		asleep_core: 'Core',
		asleep_deep: 'Deep',
		in_bed: 'In Bed',
		asleep_unspecified: 'Sleep'
	};

	function prepareChartData() {
		const sortedRecords = [...records].sort(
			(a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
		);

		const dataPoints: { x: number; y: number; stage: string }[] = [];

		sortedRecords.forEach((record) => {
			const stage = record.sleep_stage;
			const stageValue = stageOrder[stage as keyof typeof stageOrder] ?? 2;
			const startTime = new Date(record.start_date).getTime();
			const endTime = new Date(record.end_date).getTime();

			dataPoints.push({
				x: startTime,
				y: stageValue,
				stage: stage
			});

			dataPoints.push({
				x: endTime,
				y: stageValue,
				stage: stage
			});
		});

		return dataPoints;
	}

	function createChart() {
		if (!canvas || !records || records.length === 0) return;

		const dataPoints = prepareChartData();

		if (chart) {
			chart.destroy();
		}

		const ctx = canvas.getContext('2d');
		if (!ctx) return;

		chart = new Chart(ctx, {
			type: 'line',
			data: {
				datasets: [
					{
						data: dataPoints,
						borderColor: '#6c7086',
						borderWidth: 2,
						stepped: true,
						pointRadius: 0,
						pointHoverRadius: 4,
						fill: false,
						segment: {
							borderColor: (ctx) => {
								if (ctx.p0DataIndex === undefined) return '#6c7086';
								const point = dataPoints[ctx.p0DataIndex];
								return stageColors[point?.stage] ?? '#6c7086';
							}
						}
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						display: false
					},
					tooltip: {
						callbacks: {
							title: (context) => {
								const point = dataPoints[context[0].dataIndex];
								const time = new Date(point.x).toLocaleTimeString('en-US', {
									hour: 'numeric',
									minute: '2-digit'
								});
								return time;
							},
							label: (context) => {
								const point = dataPoints[context.dataIndex];
								const stageName = stageLabels[point.stage] ?? point.stage;
								return stageName;
							}
						},
						backgroundColor: '#1e1e2e',
						borderColor: '#6c7086',
						borderWidth: 1,
						padding: 8,
						displayColors: false,
						titleColor: '#cdd6f4',
						bodyColor: '#cdd6f4'
					}
				},
				scales: {
					x: {
						type: 'linear',
						ticks: {
							callback: (value) => {
								const date = new Date(value as number);
								return date.toLocaleTimeString('en-US', {
									hour: 'numeric',
									minute: '2-digit'
								});
							},
							color: '#6c7086',
							font: {
								size: 11
							}
						},
						grid: {
							color: '#eff1f5',
							drawTicks: false
						},
						border: {
							display: false
						}
					},
					y: {
						type: 'linear',
						min: 0,
						max: 4,
						ticks: {
							stepSize: 1,
							callback: (value) => {
								const labels = ['In Bed', 'Deep', 'Core', 'REM', 'Awake'];
								return labels[value as number] || '';
							},
							color: '#6c7086',
							font: {
								size: 11
							}
						},
						grid: {
							color: '#eff1f5',
							drawTicks: false
						},
						border: {
							display: false
						}
					}
				},
				interaction: {
					mode: 'nearest',
					axis: 'x',
					intersect: false
				}
			}
		});
	}

	onMount(() => {
		createChart();
	});

	$: if (records && canvas) {
		createChart();
	}
</script>

<div class="hypnogram-container">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.hypnogram-container {
		width: 100%;
		height: 300px;
		border-top: 1px solid #cdd6f4;
		border-bottom: 1px solid #cdd6f4;
		padding: 1rem 0;
		background: #eff1f5;
	}

	canvas {
		max-width: 100%;
	}
</style>
