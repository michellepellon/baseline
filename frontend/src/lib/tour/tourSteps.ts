import type { Step } from 'shepherd.js';

export const tourSteps: Step.StepOptions[] = [
	{
		id: 'welcome',
		text: `
			<h3>Welcome to Baseline!</h3>
			<p>Let's take a quick tour of the key features to help you get the most out of your sleep tracking experience.</p>
		`,
		buttons: [
			{
				text: 'Skip Tour',
				action() {
					this.cancel();
				},
				secondary: true
			},
			{
				text: 'Start',
				action() {
					this.next();
				}
			}
		]
	},
	{
		id: 'dashboard',
		text: `
			<h3>Sleep Dashboard</h3>
			<p>This is your main dashboard showing your recent sleep patterns, including total sleep time, sleep efficiency, and nightly trends.</p>
		`,
		attachTo: {
			element: '.dashboard-card',
			on: 'bottom'
		},
		buttons: [
			{
				text: 'Back',
				action() {
					this.back();
				},
				secondary: true
			},
			{
				text: 'Next',
				action() {
					this.next();
				}
			}
		]
	},
	{
		id: 'insights',
		text: `
			<h3>AI-Powered Insights</h3>
			<p>Get personalized, science-backed insights about your sleep patterns and recommendations for improvement.</p>
		`,
		attachTo: {
			element: '.insights-section',
			on: 'bottom'
		},
		buttons: [
			{
				text: 'Back',
				action() {
					this.back();
				},
				secondary: true
			},
			{
				text: 'Next',
				action() {
					this.next();
				}
			}
		]
	},
	{
		id: 'charts',
		text: `
			<h3>Sleep Trends & Analytics</h3>
			<p>Visualize your sleep patterns over time with interactive charts and detailed breakdowns of sleep stages.</p>
		`,
		attachTo: {
			element: '.visualization-section',
			on: 'top'
		},
		buttons: [
			{
				text: 'Back',
				action() {
					this.back();
				},
				secondary: true
			},
			{
				text: 'Next',
				action() {
					this.next();
				}
			}
		]
	},
	{
		id: 'upload',
		text: `
			<h3>Upload More Data</h3>
			<p>Keep your sleep data up-to-date by uploading new exports from your Apple Health app.</p>
		`,
		attachTo: {
			element: '[href="/data"]',
			on: 'right'
		},
		buttons: [
			{
				text: 'Back',
				action() {
					this.back();
				},
				secondary: true
			},
			{
				text: 'Next',
				action() {
					this.next();
				}
			}
		]
	},
	{
		id: 'profile',
		text: `
			<h3>Profile & Settings</h3>
			<p>Customize your experience, update your profile, and manage your preferences here.</p>
		`,
		attachTo: {
			element: '[href="/profile"]',
			on: 'right'
		},
		buttons: [
			{
				text: 'Back',
				action() {
					this.back();
				},
				secondary: true
			},
			{
				text: 'Finish',
				action() {
					this.complete();
				}
			}
		]
	}
];
