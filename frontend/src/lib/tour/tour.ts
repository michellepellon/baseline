import Shepherd from 'shepherd.js';
import { tourSteps } from './tourSteps';

let tourInstance: Shepherd.Tour | null = null;

export function createTour(onComplete?: () => void): Shepherd.Tour {
	if (tourInstance) {
		return tourInstance;
	}

	const tour = new Shepherd.Tour({
		useModalOverlay: true,
		defaultStepOptions: {
			classes: 'baseline-tour-step',
			scrollTo: { behavior: 'smooth', block: 'center' },
			cancelIcon: {
				enabled: true
			}
		}
	});

	// Add all steps
	tourSteps.forEach((step) => {
		tour.addStep(step);
	});

	// Handle tour completion
	tour.on('complete', () => {
		if (onComplete) {
			onComplete();
		}
		tourInstance = null;
	});

	// Handle tour cancellation
	tour.on('cancel', () => {
		tourInstance = null;
	});

	tourInstance = tour;
	return tour;
}

export function startTour(onComplete?: () => void): void {
	const tour = createTour(onComplete);
	tour.start();
}

export function getTour(): Shepherd.Tour | null {
	return tourInstance;
}
