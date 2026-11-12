-- ============================================================================
-- MediAssist – Supabase PostgreSQL Schema
-- Run this in the Supabase SQL Editor to create all required tables
-- ============================================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id          BIGSERIAL PRIMARY KEY,
    email       TEXT UNIQUE NOT NULL,
    pw          TEXT NOT NULL,
    verified    INTEGER DEFAULT 0,
    onboarded   INTEGER DEFAULT 0,
    created     TEXT NOT NULL
);

-- Verification / password reset tokens
CREATE TABLE IF NOT EXISTS tokens (
    token       TEXT PRIMARY KEY,
    user_id     BIGINT REFERENCES users(id) ON DELETE CASCADE,
    kind        TEXT NOT NULL,
    expires     TEXT NOT NULL
);

-- Prescriptions (raw OCR text)
CREATE TABLE IF NOT EXISTS prescriptions (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT REFERENCES users(id) ON DELETE CASCADE,
    raw         TEXT,
    created     TEXT NOT NULL
);

-- Extracted medicines
CREATE TABLE IF NOT EXISTS medicines (
    id          BIGSERIAL PRIMARY KEY,
    rx_id       BIGINT REFERENCES prescriptions(id) ON DELETE CASCADE,
    user_id     BIGINT REFERENCES users(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    strength    TEXT DEFAULT '',
    freq        TEXT DEFAULT '',
    times       TEXT DEFAULT '[]',
    days        INTEGER DEFAULT 5,
    confidence  REAL DEFAULT 1.0
);

-- Individual dose reminders
CREATE TABLE IF NOT EXISTS doses (
    id          BIGSERIAL PRIMARY KEY,
    med_id      BIGINT REFERENCES medicines(id) ON DELETE CASCADE,
    user_id     BIGINT REFERENCES users(id) ON DELETE CASCADE,
    due         TEXT NOT NULL,
    status      TEXT DEFAULT 'pending'
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_tokens_user ON tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_user ON prescriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_medicines_user ON medicines(user_id);
CREATE INDEX IF NOT EXISTS idx_medicines_rx ON medicines(rx_id);
CREATE INDEX IF NOT EXISTS idx_doses_user_status ON doses(user_id, status);
CREATE INDEX IF NOT EXISTS idx_doses_med ON doses(med_id);

-- Row Level Security (RLS) — enable per-user data isolation
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE prescriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE medicines ENABLE ROW LEVEL SECURITY;
ALTER TABLE doses ENABLE ROW LEVEL SECURITY;

-- Policies: service-role key bypasses RLS, so the Flask backend
-- using the service-role key can access all rows. If you switch to
-- anon key + Supabase Auth JWT, add policies like:
--
--   CREATE POLICY "users own data" ON prescriptions
--     FOR ALL USING (user_id = auth.uid()::bigint);

