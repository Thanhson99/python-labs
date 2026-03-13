CREATE TABLE IF NOT EXISTS events (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  kind TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_user_created_at ON events(user_id, created_at DESC);

EXPLAIN ANALYZE
SELECT *
FROM events
WHERE user_id = 42
ORDER BY created_at DESC
LIMIT 50;
