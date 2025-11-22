-- DuckDB schema for Apple Health sleep data analysis

-- Sequences for auto-incrementing IDs
CREATE SEQUENCE IF NOT EXISTS seq_users START 1;
CREATE SEQUENCE IF NOT EXISTS seq_sleep_records START 1;
CREATE SEQUENCE IF NOT EXISTS seq_nightly_summary START 1;
CREATE SEQUENCE IF NOT EXISTS seq_stage_events START 1;
CREATE SEQUENCE IF NOT EXISTS seq_benchmarks START 1;
CREATE SEQUENCE IF NOT EXISTS seq_metrics START 1;
CREATE SEQUENCE IF NOT EXISTS seq_insights_cache START 1;

-- Users table: stores user authentication and profile data
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_users'),
    username VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    profile_picture BLOB,
    profile_picture_mime_type VARCHAR,

    -- Onboarding fields
    onboarding_completed BOOLEAN DEFAULT FALSE,
    onboarding_completed_at TIMESTAMP WITH TIME ZONE,
    tour_completed BOOLEAN DEFAULT FALSE,
    wearable_type VARCHAR,
    sleep_goals TEXT,
    preferences JSON,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sleep records table: stores individual sleep stage records
CREATE TABLE IF NOT EXISTS sleep_records (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_sleep_records'),
    record_type VARCHAR NOT NULL,
    source_name VARCHAR NOT NULL,
    source_version VARCHAR,
    device VARCHAR,
    creation_date TIMESTAMP WITH TIME ZONE NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    value VARCHAR NOT NULL,
    sleep_stage VARCHAR NOT NULL,
    duration_minutes INTEGER NOT NULL,
    date DATE NOT NULL
);

-- Nightly summary table: aggregated metrics per night
CREATE TABLE IF NOT EXISTS sleep_nightly_summary (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_nightly_summary'),
    date DATE NOT NULL UNIQUE,
    sleep_start TIMESTAMP WITH TIME ZONE NOT NULL,
    sleep_end TIMESTAMP WITH TIME ZONE NOT NULL,
    total_sleep_minutes INTEGER NOT NULL,
    total_sleep_hours DOUBLE NOT NULL,
    time_in_bed_minutes INTEGER NOT NULL,
    sleep_efficiency_pct DOUBLE NOT NULL,
    source_name VARCHAR NOT NULL,

    -- Sleep stage breakdowns
    asleep_core_minutes INTEGER DEFAULT 0,
    asleep_deep_minutes INTEGER DEFAULT 0,
    asleep_rem_minutes INTEGER DEFAULT 0,
    awake_minutes INTEGER DEFAULT 0,

    -- Percentages
    asleep_core_pct DOUBLE,
    asleep_deep_pct DOUBLE,
    asleep_rem_pct DOUBLE,
    awake_pct DOUBLE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sleep stage events table: for tracking transitions and patterns
CREATE TABLE IF NOT EXISTS sleep_stage_events (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_stage_events'),
    date DATE NOT NULL,
    sleep_stage VARCHAR NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER NOT NULL,
    sequence_order INTEGER NOT NULL,

    -- Foreign key to nightly summary
    FOREIGN KEY (date) REFERENCES sleep_nightly_summary(date)
);

-- Scientific benchmarks table: configurable benchmarks from TOML
CREATE TABLE IF NOT EXISTS sleep_benchmarks (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_benchmarks'),
    metric_name VARCHAR NOT NULL UNIQUE,
    optimal_min DOUBLE,
    optimal_max DOUBLE,
    good_threshold DOUBLE,
    unit VARCHAR,
    source VARCHAR NOT NULL,
    citation VARCHAR,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User metrics table: calculated metrics with benchmark comparisons
CREATE TABLE IF NOT EXISTS sleep_metrics (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_metrics'),
    date DATE NOT NULL,
    metric_name VARCHAR NOT NULL,
    value DOUBLE NOT NULL,
    unit VARCHAR,
    deviation_from_optimal DOUBLE,
    meets_benchmark BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (date) REFERENCES sleep_nightly_summary(date)
);

-- Insights cache table: stores generated insights to avoid regeneration
CREATE TABLE IF NOT EXISTS insights_cache (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_insights_cache'),
    days_analyzed INTEGER NOT NULL,
    insights_text TEXT NOT NULL,
    stats JSON NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_sleep_records_date ON sleep_records(date);
CREATE INDEX IF NOT EXISTS idx_sleep_records_stage ON sleep_records(sleep_stage);
CREATE INDEX IF NOT EXISTS idx_sleep_stage_events_date ON sleep_stage_events(date);
CREATE INDEX IF NOT EXISTS idx_sleep_metrics_date ON sleep_metrics(date);
CREATE INDEX IF NOT EXISTS idx_sleep_metrics_name ON sleep_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_insights_cache_days ON insights_cache(days_analyzed);
CREATE INDEX IF NOT EXISTS idx_insights_cache_generated ON insights_cache(generated_at);
