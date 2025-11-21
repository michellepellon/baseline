/**
 * Authentication store for managing user session.
 */

import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface AuthState {
	token: string | null;
	username: string | null;
	isAuthenticated: boolean;
}

function createAuthStore() {
	const initialToken = browser ? localStorage.getItem('auth_token') : null;
	const initialUsername = browser ? localStorage.getItem('username') : null;

	const { subscribe, set, update } = writable<AuthState>({
		token: initialToken,
		username: initialUsername,
		isAuthenticated: !!initialToken
	});

	return {
		subscribe,
		login: (token: string, username: string) => {
			if (browser) {
				localStorage.setItem('auth_token', token);
				localStorage.setItem('username', username);
			}
			set({ token, username, isAuthenticated: true });
		},
		logout: () => {
			if (browser) {
				localStorage.removeItem('auth_token');
				localStorage.removeItem('username');
			}
			set({ token: null, username: null, isAuthenticated: false });
		},
		getToken: (): string | null => {
			if (browser) {
				return localStorage.getItem('auth_token');
			}
			return null;
		}
	};
}

export const authStore = createAuthStore();
