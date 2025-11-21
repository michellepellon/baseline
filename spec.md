# Apple HealthKit Advanced Analysis Engine & Visualization Tool

## Project Overview

An advanced analysis engine and visualization tool for Apple HealthKit data, focusing initially on sleep analysis with a flexible architecture to support multiple health domains. The tool leverages bleeding-edge Python and JavaScript tooling to provide scientifically-grounded insights following Huberman-style circadian optimization principles and Tufte's visualization excellence.

## Core Technology Stack

### Frontend
- **Framework**: SvelteKit (modern, performant, excellent DX)
- **Build Tool**: Vite (built into SvelteKit)
- **Visualization**: Chart.js (https://www.chartjs.org/)
- **Design Philosophy**: Edward Tufte principles
  - Maximize data-ink ratio
  - Show data variation, not design variation
  - Support multiple visualization types based on analytical question:
    - Small multiples for comparisons
    - Sparklines for quick trends
    - Dense layered graphics for deep exploration

### Backend
- **Framework**: FastAPI (Python)
- **Data Processing**: Polars (https://pola.rs/) - blazing fast DataFrame operations
- **Analytical Queries**: DuckDB (https://duckdb.org/) - SQL-based analytics, can query Polars DataFrames directly
- **Package Management**: `uv` for all Python dependencies

### Data Pipeline
1. Manual HealthKit XML export from iPhone
2. Upload to staging directory
3. Manual trigger to process files (command or button)
4. Polars-based data transformation and cleaning
5. DuckDB for complex analytical queries
6. Results served via FastAPI to SvelteKit frontend

## Phase 1: Sleep Analysis Focus

### Scientific Grounding

**Approach**: Curated scientific sources and metrics
- Use established sleep science metrics from peer-reviewed research
- Follow guidelines from National Sleep Foundation (NSF) and American Academy of Sleep Medicine (AASM)
- Include citations and references for each metric and interpretation
- Configuration via TOML files for scientific sources and benchmarks

**Analysis Framework**: Huberman-style circadian optimization
- Focus on actionable protocols and insights
- Analyze what can be changed to improve sleep quality
- Prioritize circadian alignment and consistency

### Data Source Research Required

**Action Item**: Research HealthKit XML export format to determine:
- What sleep metrics are available (sleep stages: REM, deep, light, awake?)
- Granularity of data (per-minute, per-hour?)
- Start/end times, interruptions, heart rate during sleep?
- Any other sleep-related data points

### Huberman-Aligned Metrics (Based on Available Data)

Calculate and visualize the following metrics where HealthKit data permits:

1. **Sleep Timing Consistency**
   - Sleep onset time consistency (circadian alignment)
   - Wake time consistency
   - Sleep midpoint (chronotype assessment)
   - Night-to-night variability in timing

2. **Sleep Architecture**
   - Total sleep duration vs. optimal (7-9 hours for most adults)
   - REM sleep percentage (target: ~20-25% of total sleep)
   - Deep sleep percentage (target: ~15-20% of total sleep)
   - Light sleep percentage

3. **Sleep Quality Metrics**
   - Sleep efficiency (time asleep / time in bed)
   - Sleep latency (time to fall asleep)
   - Wake After Sleep Onset (WASO)
   - Number of awakenings

4. **Circadian Optimization**
   - Regularity of sleep-wake schedule
   - Alignment with natural circadian rhythms
   - Temperature minimum estimation (based on wake time)

### State-of-the-Art Algorithms (2025)

Focus on Huberman-aligned actionable insights:

1. **Circadian Rhythm Analysis**
   - Cosinor analysis for rhythm detection
   - Phase alignment assessment
   - Chronotype classification

2. **Protocol Effectiveness Tracking**
   - Before/after analysis for sleep interventions
   - Trend detection for sleep quality improvements
   - Consistency scoring

3. **Anomaly Detection**
   - Identify unusual sleep patterns
   - Flag potential sleep disorders
   - Detect degradation in sleep quality

4. **Time Series Analysis**
   - Rolling averages for trend visualization
   - Seasonality detection
   - Sleep debt calculation over time

### Visualization Strategy

Following Tufte principles, let the analytical question drive visualization type:

1. **Small Multiples**
   - Compare sleep patterns across weeks/months
   - Before/after protocol comparisons
   - Weekday vs. weekend patterns

2. **Sparklines**
   - Embedded in metric tables for quick trend assessment
   - Sleep duration trends
   - Consistency metrics over time

3. **Dense Layered Graphics**
   - Hypnograms (sleep stage progression through night)
   - Multi-metric correlation views
   - Time series with annotations for interventions

4. **Minimalist Time Series**
   - Clean trend lines
   - Minimal chartjunk
   - High data-ink ratio

### Scientific Source Configuration (TOML)

Example structure for `sleep_science_config.toml`:

```toml
[sources]
    [[sources.primary]]
    name = "National Sleep Foundation"
    abbreviation = "NSF"
    url = "https://www.sleepfoundation.org"
    year = 2025

    [[sources.primary]]
    name = "American Academy of Sleep Medicine"
    abbreviation = "AASM"
    url = "https://aasm.org"
    year = 2025

[metrics.sleep_duration]
    optimal_min_hours = 7.0
    optimal_max_hours = 9.0
    source = "NSF"
    citation = "Hirshkowitz et al., 2015"

[metrics.rem_sleep]
    target_percentage_min = 20.0
    target_percentage_max = 25.0
    source = "AASM"
    citation = "Berry et al., 2020"

[metrics.deep_sleep]
    target_percentage_min = 15.0
    target_percentage_max = 20.0
    source = "AASM"
    citation = "Berry et al., 2020"

[metrics.sleep_efficiency]
    good_threshold = 85.0
    optimal_threshold = 90.0
    source = "NSF"
    citation = "Ohayon et al., 2017"
```

## Architecture Design

### Flexible Multi-Domain Foundation

Design system to easily extend beyond sleep to other health metrics:

1. **Modular Data Parsers**
   - Generic HealthKit XML parser
   - Domain-specific extractors (sleep, heart rate, HRV, workouts, etc.)
   - Plugin architecture for new domains

2. **Domain-Agnostic Database Schema**
   - DuckDB schema supporting multiple metric types
   - Metadata tables for metric definitions
   - Flexible time-series structure

3. **Configurable Analysis Pipeline**
   - Domain-specific configuration files (TOML)
   - Pluggable algorithm modules
   - Reusable visualization components

4. **API Design**
   - RESTful endpoints per health domain
   - Consistent response formats
   - Easy to add new domains

### Data Flow

```
HealthKit XML Export (iPhone)
    ↓
Staging Directory (local filesystem)
    ↓
Manual Trigger (CLI command or UI button)
    ↓
FastAPI Ingestion Endpoint
    ↓
Polars Parser & Transformer
    ↓
DuckDB Storage & Analytics
    ↓
FastAPI Query Endpoints
    ↓
SvelteKit Frontend
    ↓
Chart.js Visualizations
```

### Deployment

**Target**: Local development environment only
- Runs on localhost
- No cloud deployment required
- Self-contained application
- All data stays on local machine

## Project Structure (Proposed)

```
apple_health_tools/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app
│   │   ├── routes/
│   │   │   ├── sleep.py         # Sleep analysis endpoints
│   │   │   └── ingest.py        # Data ingestion endpoints
│   ├── parsers/
│   │   ├── healthkit_xml.py     # XML parser
│   │   └── sleep_extractor.py   # Sleep-specific extraction
│   ├── analysis/
│   │   ├── sleep/
│   │   │   ├── metrics.py       # Sleep metric calculations
│   │   │   ├── algorithms.py    # Circadian analysis, etc.
│   │   │   └── benchmarks.py    # Scientific benchmark comparisons
│   ├── database/
│   │   ├── schema.sql           # DuckDB schema
│   │   └── queries.py           # Common queries
│   └── config/
│       └── sleep_science_config.toml
├── frontend/
│   ├── src/
│   │   ├── routes/              # SvelteKit routes
│   │   ├── lib/
│   │   │   ├── components/      # Reusable components
│   │   │   ├── visualizations/  # Chart.js wrappers
│   │   │   └── api/             # API client
│   └── static/
├── staging/                      # HealthKit XML upload directory
├── data/                         # DuckDB database files
├── pyproject.toml               # Python dependencies (uv)
├── spec.md                      # This document
└── README.md
```

## Development Phases

### Phase 1: Foundation & Sleep Analysis
1. Research HealthKit XML export format
2. Set up project structure
3. Implement HealthKit XML parser (Polars)
4. Design DuckDB schema for sleep data
5. Implement basic FastAPI endpoints
6. Create SvelteKit frontend scaffold
7. Implement core sleep metrics calculation
8. Build initial visualizations (Tufte-style)
9. Integrate scientific benchmarks (TOML config)
10. Implement Huberman-aligned circadian analysis

### Phase 2: Advanced Sleep Analysis
1. Implement state-of-the-art algorithms:
   - Cosinor analysis
   - Anomaly detection
   - Protocol effectiveness tracking
2. Build comprehensive visualization suite:
   - Small multiples
   - Sparklines
   - Dense layered graphics
3. Add scientific citations to UI
4. Implement export functionality (reports, charts)

### Phase 3: Multi-Domain Expansion
1. Add heart rate analysis
2. Add HRV analysis
3. Add workout/activity analysis
4. Cross-domain correlations
5. Unified health dashboard

## Success Criteria

1. **Scientific Rigor**: All metrics grounded in peer-reviewed research with citations
2. **Visual Excellence**: Tufte principles evident in all visualizations
3. **Actionable Insights**: Huberman-style practical recommendations
4. **Performance**: Fast data processing with Polars, responsive queries with DuckDB
5. **Extensibility**: Easy to add new health domains
6. **Local Control**: All data processing happens locally, no cloud dependencies

## Open Questions / Research Items

1. **HealthKit Data Format**: Complete analysis of XML export structure
2. **Specific Algorithms**: Detailed algorithm selection for circadian analysis
3. **Chart.js Capabilities**: Verify Chart.js can support all desired Tufte-style visualizations (may need additional libraries like D3.js for certain advanced visualizations)
4. **Performance Benchmarks**: Test Polars + DuckDB performance with real HealthKit datasets

## References

- Polars: https://pola.rs/
- Chart.js: https://www.chartjs.org/
- DuckDB: https://duckdb.org/
- Edward Tufte's Visual Display of Quantitative Information
- Andrew Huberman's sleep optimization protocols
- National Sleep Foundation guidelines
- AASM sleep scoring manual
