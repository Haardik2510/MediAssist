-- ============================================================================
-- MediAssist – Supabase PostgreSQL Schema (for Supabase Auth & Storage)
-- Run this in the Supabase SQL Editor
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing legacy tables if re-running
DROP TABLE IF EXISTS doses CASCADE;
DROP TABLE IF EXISTS medicines CASCADE;
DROP TABLE IF EXISTS prescriptions CASCADE;
DROP TABLE IF EXISTS tokens CASCADE;
DROP TABLE IF EXISTS profiles CASCADE;

-- Profiles table (linked directly to Supabase Auth users)
CREATE TABLE profiles (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email       TEXT NOT NULL,
    onboarded   INTEGER DEFAULT 0,
    created     TIMESTAMPTZ DEFAULT NOW()
);

-- Prescriptions (raw OCR text)
CREATE TABLE prescriptions (
    id          BIGSERIAL PRIMARY KEY,
    user_id     TEXT NOT NULL,
    raw         TEXT,
    created     TEXT NOT NULL
);

-- Extracted medicines
CREATE TABLE medicines (
    id          BIGSERIAL PRIMARY KEY,
    rx_id       BIGINT REFERENCES prescriptions(id) ON DELETE CASCADE,
    user_id     TEXT NOT NULL,
    name        TEXT NOT NULL,
    strength    TEXT DEFAULT '',
    freq        TEXT DEFAULT '',
    times       TEXT DEFAULT '[]',
    days        INTEGER DEFAULT 5,
    confidence  REAL DEFAULT 1.0
);

-- Individual dose reminders
CREATE TABLE doses (
    id          BIGSERIAL PRIMARY KEY,
    med_id      BIGINT REFERENCES medicines(id) ON DELETE CASCADE,
    user_id     TEXT NOT NULL,
    due         TEXT NOT NULL,
    status      TEXT DEFAULT 'pending'
);

-- Indexes for lightning fast queries
CREATE INDEX IF NOT EXISTS idx_prescriptions_user ON prescriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_medicines_user ON medicines(user_id);
CREATE INDEX IF NOT EXISTS idx_medicines_rx ON medicines(rx_id);
CREATE INDEX IF NOT EXISTS idx_doses_user_status ON doses(user_id, status);
CREATE INDEX IF NOT EXISTS idx_doses_med ON doses(med_id);

-- Enable Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE prescriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE medicines ENABLE ROW LEVEL SECURITY;
ALTER TABLE doses ENABLE ROW LEVEL SECURITY;

-- Allow users to access their own profile
CREATE POLICY "Users view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Allow users to manage their own prescriptions
CREATE POLICY "Users manage prescriptions" ON prescriptions
    FOR ALL USING (auth.uid()::text = user_id);

-- Allow users to manage their own medicines
CREATE POLICY "Users manage medicines" ON medicines
    FOR ALL USING (auth.uid()::text = user_id);

-- Allow users to manage their own doses
CREATE POLICY "Users manage doses" ON doses
    FOR ALL USING (auth.uid()::text = user_id);

-- Auto-create profile trigger on Supabase Auth signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, onboarded)
  VALUES (new.id, new.email, 0)
  ON CONFLICT (id) DO NOTHING;
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();
