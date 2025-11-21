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
        <div class="logo">baseline</div>

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
        background: #ffffff;
        font-family:
            -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
            "Helvetica Neue", Arial, sans-serif;
    }

    .login-container {
        width: 100%;
        max-width: 480px;
        padding: 2rem;
    }

    .logo {
        display: inline-block;
        border: 3px solid #000000;
        padding: 0.75rem 1.5rem;
        font-size: 1.75rem;
        font-weight: 500;
        margin-bottom: 3rem;
        letter-spacing: -0.02em;
    }

    form {
        margin-bottom: 2rem;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9375rem;
        font-weight: 500;
        color: #000000;
    }

    input[type="email"],
    input[type="password"],
    input[type="text"] {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        border: 2px solid #bfbfbf;
        border-radius: 4px;
        background: #ffffff;
        color: #000000;
        box-sizing: border-box;
        transition: border-color 0.15s;
    }

    input[type="email"]:focus,
    input[type="password"]:focus,
    input[type="text"]:focus {
        outline: none;
        border-color: #5b9bd5;
    }

    input[type="email"]:invalid:not(:placeholder-shown) {
        border-color: #d32f2f;
    }

    input[type="email"]:invalid:not(:placeholder-shown):focus {
        border-color: #d32f2f;
    }

    input:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        background: #f5f5f5;
    }

    .checkbox-group {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    input[type="checkbox"] {
        width: 1rem;
        height: 1rem;
        margin: 0;
        margin-right: 0.5rem;
        cursor: pointer;
    }

    .checkbox-label {
        font-size: 0.9375rem;
        font-weight: normal;
        color: #000000;
        cursor: pointer;
        margin: 0;
    }

    .primary-button {
        width: 100%;
        padding: 0.875rem;
        font-size: 1rem;
        font-weight: 500;
        background: #2b2b2b;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.15s;
    }

    .primary-button:hover:not(:disabled) {
        background: #1a1a1a;
    }

    .primary-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .error {
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: #fee;
        border: 1px solid #fcc;
        border-radius: 4px;
        color: #c00;
        font-size: 0.875rem;
    }

    .footer-links {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9375rem;
    }
</style>
