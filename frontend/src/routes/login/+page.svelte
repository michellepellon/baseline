<script lang="ts">
    import { goto } from "$app/navigation";
    import { login as apiLogin } from "$lib/api/client";
    import { authStore } from "$lib/stores/auth";

    let email = "";
    let password = "";
    let showPassword = false;
    let error = "";
    let loading = false;

    async function handleSubmit() {
        error = "";
        loading = true;

        try {
            const response = await apiLogin(email, password);
            authStore.login(response.access_token, email);
            goto("/");
        } catch (e) {
            error = e instanceof Error ? e.message : "Login failed";
        } finally {
            loading = false;
        }
    }
</script>

<svelte:head>
    <title>Log in - Baseline</title>
</svelte:head>

<main>
    <div class="login-container">
        <div class="branding">
            <div class="logo">baseline</div>
            <p class="tagline">Your health, continuously understood.</p>
        </div>

        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-group">
                <label for="email">Email</label>
                <input
                    id="email"
                    type="email"
                    bind:value={email}
                    required
                    pattern="[^@\s]+@[^@\s]+\.[^@\s]+"
                    disabled={loading}
                    autocomplete="email"
                    placeholder="name@example.com"
                />
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    bind:value={password}
                    required
                    disabled={loading}
                    autocomplete="current-password"
                />
            </div>

            <div class="checkbox-group">
                <input
                    id="show-password"
                    type="checkbox"
                    bind:checked={showPassword}
                />
                <label for="show-password" class="checkbox-label"
                    >Show password</label
                >
            </div>

            {#if error}
                <div class="error">{error}</div>
            {/if}

            <button type="submit" disabled={loading} class="primary-button">
                {loading ? "Logging in..." : "Log in"}
            </button>
        </form>

        <div class="footer-links">
            Copyright (c) 2025 Michelle Pellon. All rights reserved.
        </div>
    </div>
</main>

<style>
    main {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--color-bg-secondary);
        font-family: var(--font-family-base);
    }

    .login-container {
        width: 100%;
        max-width: 480px;
        padding: var(--space-8);
    }

    .branding {
        margin-bottom: var(--space-12);
    }

    .logo {
        display: inline-block;
        border: 2px solid var(--color-text-primary);
        padding: var(--space-3) var(--space-6);
        font-size: var(--text-xl);
        font-weight: var(--font-weight-medium);
        letter-spacing: -0.02em;
    }

    .tagline {
        margin-top: var(--space-2);
        font-size: var(--text-sm);
        color: var(--color-text-secondary);
    }

    form {
        margin-bottom: var(--space-8);
    }

    .form-group {
        margin-bottom: var(--space-5);
    }

    label {
        display: block;
        margin-bottom: var(--space-2);
        font-size: var(--text-sm);
        font-weight: var(--font-weight-medium);
        color: var(--color-text-primary);
        font-variant: small-caps;
        letter-spacing: 0.05em;
    }

    input[type="email"],
    input[type="password"],
    input[type="text"] {
        width: 100%;
        padding: var(--space-3);
        font-size: var(--text-base);
        font-family: var(--font-family-base);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-base);
        background: var(--color-bg-primary);
        color: var(--color-text-primary);
        box-sizing: border-box;
        transition: border-color var(--transition-fast);
    }

    input[type="email"]:focus,
    input[type="password"]:focus,
    input[type="text"]:focus {
        outline: none;
        border-color: var(--color-focus);
    }

    input[type="email"]:invalid:not(:placeholder-shown) {
        border-color: var(--color-danger);
    }

    input[type="email"]:invalid:not(:placeholder-shown):focus {
        border-color: var(--color-danger);
    }

    input:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        background: var(--color-bg-tertiary);
    }

    .checkbox-group {
        display: flex;
        align-items: center;
        margin-bottom: var(--space-6);
    }

    input[type="checkbox"] {
        width: 1rem;
        height: 1rem;
        margin: 0;
        margin-right: var(--space-2);
        cursor: pointer;
    }

    .checkbox-label {
        font-size: var(--text-sm);
        font-weight: var(--font-weight-normal);
        color: var(--color-text-primary);
        cursor: pointer;
        margin: 0;
    }

    .primary-button {
        width: 100%;
        padding: var(--space-3) var(--space-4);
        font-size: var(--text-base);
        font-weight: var(--font-weight-medium);
        font-family: var(--font-family-base);
        background: var(--color-primary);
        color: var(--color-bg-primary);
        border: none;
        border-radius: var(--radius-base);
        cursor: pointer;
        transition: background var(--transition-fast);
    }

    .primary-button:hover:not(:disabled) {
        background: var(--color-primary-hover);
    }

    .primary-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .error {
        margin-bottom: var(--space-4);
        padding: var(--space-3);
        background: var(--color-danger-bg);
        border: 1px solid var(--color-danger-border);
        border-radius: var(--radius-base);
        color: var(--color-danger);
        font-size: var(--text-sm);
    }

    .footer-links {
        position: fixed;
        bottom: var(--space-4);
        right: var(--space-4);
        font-size: var(--text-xs);
        color: var(--color-text-tertiary);
    }
</style>
