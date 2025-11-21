/**
 * API client for Apple Health Analysis Engine backend.
 */

import { authStore } from '$lib/stores/auth';

const API_BASE_URL = 'http://localhost:5000';

export interface SleepRecord {
	id: number;
	record_type: string;
	source_name: string;
	source_version?: string;
	device?: string;
	creation_date: string;
	start_date: string;
	end_date: string;
	value: string;
	sleep_stage: string;
	duration_minutes: number;
	date: string;
}

export interface NightlySummary {
	id: number;
	date: string;
	sleep_start: string;
	sleep_end: string;
	total_sleep_minutes: number;
	total_sleep_hours: number;
	time_in_bed_minutes: number;
	sleep_efficiency_pct: number;
	source_name: string;
	asleep_core_minutes?: number;
	asleep_deep_minutes?: number;
	asleep_rem_minutes?: number;
	awake_minutes?: number;
	asleep_core_pct?: number;
	asleep_deep_pct?: number;
	asleep_rem_pct?: number;
	awake_pct?: number;
	created_at: string;
	updated_at: string;
}

export interface HealthCheckResponse {
	status: string;
	service: string;
	version: string;
}

/**
 * Fetch wrapper with error handling and authentication.
 */
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
	const url = `${API_BASE_URL}${endpoint}`;
	const token = authStore.getToken();

	const headers: Record<string, string> = {
		...options?.headers
	} as Record<string, string>;

	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	if (options?.body && typeof options.body === 'string') {
		headers['Content-Type'] = 'application/json';
	}

	try {
		const response = await fetch(url, {
			...options,
			headers
		});

		if (response.status === 401) {
			authStore.logout();
			if (typeof window !== 'undefined') {
				window.location.href = '/login';
			}
			throw new Error('Unauthorized');
		}

		if (!response.ok) {
			throw new Error(`API error: ${response.status} ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error(`API request failed: ${url}`, error);
		throw error;
	}
}

/**
 * Login endpoint.
 * Note: email is sent as 'username' to match OAuth2 standard.
 */
export async function login(email: string, password: string): Promise<{ access_token: string; token_type: string }> {
	const formData = new FormData();
	formData.append('username', email);
	formData.append('password', password);

	const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
		method: 'POST',
		body: formData
	});

	if (!response.ok) {
		throw new Error('Invalid credentials');
	}

	return await response.json();
}

/**
 * Health check endpoint.
 */
export async function healthCheck(): Promise<HealthCheckResponse> {
	return apiFetch<HealthCheckResponse>('/');
}

/**
 * Get nightly sleep summaries.
 */
export async function getNightlySummaries(
	startDate?: string,
	endDate?: string
): Promise<NightlySummary[]> {
	const params = new URLSearchParams();
	if (startDate) params.append('start_date', startDate);
	if (endDate) params.append('end_date', endDate);

	const query = params.toString() ? `?${params.toString()}` : '';
	return apiFetch<NightlySummary[]>(`/api/sleep/summary${query}`);
}

/**
 * Get detailed sleep records.
 */
export async function getSleepRecords(
	startDate?: string,
	endDate?: string
): Promise<SleepRecord[]> {
	const params = new URLSearchParams();
	if (startDate) params.append('start_date', startDate);
	if (endDate) params.append('end_date', endDate);

	const query = params.toString() ? `?${params.toString()}` : '';
	return apiFetch<SleepRecord[]>(`/api/sleep/records${query}`);
}

/**
 * Get sleep statistics.
 */
export async function getSleepStats(): Promise<{
	total_nights: number;
	average_sleep_hours: number;
	average_efficiency: number;
	date_range: {
		start: string;
		end: string;
	};
	average_rem_pct?: number;
	average_deep_pct?: number;
	average_core_pct?: number;
}> {
	return apiFetch('/api/sleep/stats');
}

/**
 * Upload and ingest HealthKit XML file.
 */
export async function ingestHealthKitData(
	file: File
): Promise<{
	message: string;
	records: number;
	summaries: number;
	nights: number;
	date_range: {
		start: string;
		end: string;
	};
}> {
	const formData = new FormData();
	formData.append('file', file);

	const token = authStore.getToken();
	const headers: Record<string, string> = {};

	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	const response = await fetch(`${API_BASE_URL}/api/ingest`, {
		method: 'POST',
		headers,
		body: formData
	});

	if (response.status === 401) {
		authStore.logout();
		if (typeof window !== 'undefined') {
			window.location.href = '/login';
		}
		throw new Error('Unauthorized');
	}

	if (!response.ok) {
		throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
	}

	return await response.json();
}

/**
 * Generate health insights using LLM.
 */
export async function generateInsights(
	days: number = 7,
	forceRegenerate: boolean = false
): Promise<{
	insights: {
		overview: string;
		recommendations: string[];
		patterns: string;
	};
	stats: {
		average_sleep_hours: number;
		average_efficiency: number;
		nights_analyzed: number;
		date_range: {
			start: string;
			end: string;
		};
		average_rem_pct?: number;
		average_deep_pct?: number;
	};
	generated_at: string;
	from_cache: boolean;
}> {
	const params = new URLSearchParams();
	params.append('days', days.toString());
	if (forceRegenerate) {
		params.append('force_regenerate', 'true');
	}

	return apiFetch(`/api/insights/generate?${params.toString()}`);
}
