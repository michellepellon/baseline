# Baseline

Your health, continuously understood.

## Privacy & Security

Baseline is designed with privacy as the **highest priority**. Your health data 
never leaves your control.

### Privacy Features

#### 🔒 **Zero External Dependencies**
- **No CDNs**: All assets (JavaScript, CSS, fonts) are self-hosted
- **No analytics**: Zero telemetry or tracking
- **No third-party APIs**: No external service calls
- **System fonts only**: No web font loading from external servers

#### 🏠 **Local-First Architecture**
- **On-device LLM**: Uses local Ollama instance for AI insights
- **Encrypted database**: DuckDB with AES encryption at rest
- **Local processing**: All data analysis happens on your machine
- **No cloud sync**: Data stays on your device

#### 🛡️ **Security Headers**
All responses include comprehensive security headers:
- **Content Security Policy (CSP)**: Prevents loading of any external resources
- **X-Frame-Options**: Prevents clickjacking attacks
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **Referrer-Policy**: No URL leakage to external sites
- **Permissions-Policy**: Disables unnecessary browser features

#### 🔐 **Data Protection**
- **Database encryption**: AES encryption with user-controlled keys
- **Password hashing**: bcrypt with proper salting
- **JWT authentication**: Secure session management
- **HTTPS ready**: Production deployment supports TLS

### What Data is Collected?

Baseline only processes data **you explicitly provide** by uploading your Apple Health export:
- Sleep data (duration, stages, efficiency)
- No data is sent to external servers
- No behavioral tracking
- No usage analytics

### Open Source & Auditable

The entire codebase is open source, allowing you to:
- Inspect exactly what the application does
- Verify no data leakage
- Build from source
- Self-host completely

## Features

### 📊 **Sleep Tracking**
- Detailed sleep stage analysis (REM, Deep, Core)
- Sleep efficiency calculations
- Historical trends and patterns
- Scientific benchmarks comparison

### 🤖 **AI-Powered Insights**
- Local LLM analysis using Ollama
- Personalized sleep recommendations
- Pattern detection and health insights
- Interactive task tracking

### 📈 **Data Visualization**
- Hypnograms for sleep architecture
- Trend charts and statistics
- Nightly summaries
- Historical comparisons

## Architecture

### Backend
- **Python 3.13** with FastAPI
- **DuckDB** for encrypted data storage
- **Ollama** for local LLM inference
- **Polars** for fast data processing

### Frontend
- **SvelteKit** with static generation
- **TypeScript** for type safety
- **Chart.js** for visualizations
- **System fonts** - no external dependencies

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Ollama running locally (for AI insights)

### Running with Docker

```bash
# Start the application
docker-compose up -d

# Access the app
open http://localhost:5000
```

### First-Time Setup

1. Create an account (data stored locally in encrypted database)
2. Export your Apple Health data from your iPhone:
   - Open Health app → Profile → Export All Health Data
3. Upload the `export.xml` file to Baseline
4. Explore your sleep data and insights

## Development

### Backend Development
```bash
# Install dependencies
uv sync

# Run locally
uv run uvicorn backend.api.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Security Considerations

### For Production Deployment

If deploying to a server, enable additional security:

1. **Enable HSTS** in `backend/api/main.py`:
   ```python
   response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
   ```

2. **Use HTTPS** with proper TLS certificates

3. **Change default encryption keys** in environment variables

4. **Restrict CORS origins** to your domain only

### Self-Hosting

For maximum privacy, self-host on your own hardware:
- Run on a home server or NAS
- No internet connection required after setup
- Complete control over your data

## License

MIT

## Contributing

Contributions welcome! Please ensure any changes maintain the privacy-first architecture.

## Disclaimer

Baseline is a personal health tracking tool and is **not medical software**. It does not provide medical advice, diagnosis, or treatment. Always consult healthcare professionals for medical concerns.
