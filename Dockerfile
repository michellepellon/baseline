# Multi-stage Dockerfile for baseline health tracking application
# Stage 1: Build frontend
FROM node:22-slim AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies and adapter-static
RUN npm ci && npm install -D @sveltejs/adapter-static

# Copy frontend source
COPY frontend/ ./

# Configure adapter-static for SPA mode
RUN echo "import adapter from '@sveltejs/adapter-static';" > svelte.config.js && \
    echo "import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';" >> svelte.config.js && \
    echo "const config = {" >> svelte.config.js && \
    echo "  preprocess: vitePreprocess()," >> svelte.config.js && \
    echo "  kit: {" >> svelte.config.js && \
    echo "    adapter: adapter({ fallback: 'index.html', strict: false })" >> svelte.config.js && \
    echo "  }" >> svelte.config.js && \
    echo "};" >> svelte.config.js && \
    echo "export default config;" >> svelte.config.js

# Build frontend
RUN npm run build

# Stage 2: Python backend with uv
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy Python project files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy backend source
COPY backend/ ./backend/
COPY main.py ./
COPY load_benchmarks.py ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Copy backend configuration
COPY backend/config/ ./backend/config/
COPY backend/database/schema.sql ./backend/database/

# Create data directory for DuckDB
RUN mkdir -p /app/data

# Create staging directory for HealthKit XML uploads
RUN mkdir -p /app/staging

# Expose port for FastAPI
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the FastAPI application using uvicorn
CMD ["uv", "run", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "5000"]
