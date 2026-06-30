CREATE TABLE IF NOT EXISTS tasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text    TEXT    NOT NULL,
    tags          TEXT,
    status        TEXT    NOT NULL DEFAULT 'pending',
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    agent_name    TEXT    NOT NULL,
    phase         TEXT    NOT NULL,
    input         TEXT,
    output        TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS proposals (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    agent_name    TEXT    NOT NULL,
    content       TEXT    NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS critiques (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id             INTEGER NOT NULL REFERENCES tasks(id),
    from_agent          TEXT    NOT NULL,
    target_proposal_id  INTEGER NOT NULL REFERENCES proposals(id),
    content             TEXT    NOT NULL,
    severity            TEXT    NOT NULL,
    created_at          TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS votes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    agent_name    TEXT    NOT NULL,
    dimension     TEXT    NOT NULL,
    score         REAL    NOT NULL,
    confidence    REAL    NOT NULL,
    rationale     TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS reputation_scores (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name        TEXT    NOT NULL,
    skill             TEXT    NOT NULL,
    reputation_score  REAL    NOT NULL,
    observations      INTEGER NOT NULL DEFAULT 0,
    variance          REAL    NOT NULL DEFAULT 0.0,
    last_updated      TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(agent_name, skill)
);

CREATE TABLE IF NOT EXISTS case_memory (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER REFERENCES tasks(id),
    summary       TEXT    NOT NULL,
    tags          TEXT,
    outcome       TEXT,
    embedding     TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS procedural_memory (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson            TEXT    NOT NULL,
    tags              TEXT,
    trigger_condition TEXT,
    embedding         TEXT,
    created_at        TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agent_memory (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name    TEXT    NOT NULL,
    note          TEXT    NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS human_feedback (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id           INTEGER NOT NULL REFERENCES tasks(id),
    quality_rating    INTEGER,
    most_useful_agent TEXT,
    missed_by_agent   TEXT,
    created_at        TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS trace_events (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    event_type    TEXT    NOT NULL,
    payload       TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);
