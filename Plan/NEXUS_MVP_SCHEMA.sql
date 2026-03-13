-- NEXUS MVP — DuckDB Schema
-- Version: 1.0
-- Database: nexus.duckdb (local)

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- CYCLES: Temporal structure (daily, weekly, monthly, etc.)
CREATE TABLE IF NOT EXISTS cycles (
    id VARCHAR PRIMARY KEY,
    type VARCHAR NOT NULL,  -- 'daily', 'weekly', 'monthly', 'semestral', 'strategic'
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    status VARCHAR DEFAULT 'active',  -- 'active', 'completed', 'archived'
    description VARCHAR,
    created_by VARCHAR NOT NULL DEFAULT 'user',  -- 'user', 'codex', 'system'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR DEFAULT 'user',
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local'
);

-- ENTITIES: Projetos, pessoas, conceitos, etc.
CREATE TABLE IF NOT EXISTS entities (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,  -- 'project', 'person', 'concept', 'outcome', 'resource', etc.
    context VARCHAR,  -- Descrição/contexto breve
    created_by VARCHAR NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR DEFAULT 'user',
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local'
);

-- RELATIONS: Conexões entre entidades
CREATE TABLE IF NOT EXISTS relations (
    id VARCHAR PRIMARY KEY,
    entity_a_id VARCHAR NOT NULL,
    entity_b_id VARCHAR NOT NULL,
    relation_type VARCHAR NOT NULL,  -- 'depende_de', 'trabalha_em', 'referencia', 'gera', 'contradiz', etc.
    weight FLOAT DEFAULT 0.5,  -- 0.1 a 1.0 (força da relação)
    context VARCHAR,  -- Nota breve sobre a relação
    created_by VARCHAR NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR DEFAULT 'user',
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local',
    FOREIGN KEY (entity_a_id) REFERENCES entities(id),
    FOREIGN KEY (entity_b_id) REFERENCES entities(id)
);

-- DOCUMENTS: Artifacts operacionais (dailies, weeklies, monthlies)
CREATE TABLE IF NOT EXISTS documents (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    type VARCHAR NOT NULL,  -- 'daily', 'weekly', 'monthly', 'report', 'note', etc.
    cycle_id VARCHAR,  -- Referência ao ciclo (pode ser NULL)
    status VARCHAR DEFAULT 'draft',  -- 'draft', 'approved', 'archived'
    path VARCHAR,  -- Caminho relativo: 'daily/2026-03-13.md', etc.
    content_hash VARCHAR,  -- SHA256 do conteúdo (para conflict detection)
    version VARCHAR DEFAULT '1.0',
    approved_at TIMESTAMP,
    created_by VARCHAR NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR DEFAULT 'user',
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local',
    changelog VARCHAR,  -- JSON: [{version, what_changed, timestamp}]
    FOREIGN KEY (cycle_id) REFERENCES cycles(id)
);

-- ACTIVITIES: O que você faz dentro de cada ciclo
CREATE TABLE IF NOT EXISTS activities (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    cycle_id VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'blocked'
    priority INTEGER DEFAULT 3,  -- 1 (crítica) a 5 (baixa)
    type VARCHAR,  -- 'task', 'meeting', 'research', 'writing', etc.
    description VARCHAR,
    created_by VARCHAR NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR DEFAULT 'user',
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local',
    FOREIGN KEY (cycle_id) REFERENCES cycles(id)
);

-- OUTPUTS: Artefatos gerados (arquivos, decisões)
CREATE TABLE IF NOT EXISTS outputs (
    id VARCHAR PRIMARY KEY,
    activity_id VARCHAR,
    type VARCHAR NOT NULL,  -- 'file', 'decision', 'document', 'analysis', etc.
    path VARCHAR,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR DEFAULT 'draft',  -- 'draft', 'final', 'archived'
    description VARCHAR,
    created_by VARCHAR NOT NULL DEFAULT 'user',
    approved_at TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local',
    FOREIGN KEY (activity_id) REFERENCES activities(id)
);

-- INBOX_ITEMS: Contexto externo (email, WhatsApp, Teams, Drive)
CREATE TABLE IF NOT EXISTS inbox_items (
    id VARCHAR PRIMARY KEY,
    source VARCHAR NOT NULL,  -- 'email_gmail', 'email_outlook', 'whatsapp', 'teams', 'drive', 'slack'
    content VARCHAR,  -- Texto bruto ou resumo
    metadata VARCHAR,  -- JSON: {from, to, subject, date, file_path, etc.}
    classification VARCHAR,  -- 'action_now', 'actionable', 'context', 'noise', NULL (não triado)
    priority INTEGER DEFAULT 3,  -- 1 (urgente) a 5 (baixa)
    triaged BOOLEAN DEFAULT FALSE,
    triage_feedback VARCHAR,  -- Notas sobre a triagem
    created_by VARCHAR NOT NULL DEFAULT 'system',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local'
);

-- ============================================================================
-- SYSTEM & AUDIT TABLES
-- ============================================================================

-- SYSTEM_STATE: Configuração e metadados do sistema
CREATE TABLE IF NOT EXISTS system_state (
    key VARCHAR PRIMARY KEY,
    value VARCHAR NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AUDIT_LOG: Rastreabilidade completa
CREATE TABLE IF NOT EXISTS audit_log (
    id VARCHAR PRIMARY KEY,
    action VARCHAR NOT NULL,  -- 'create', 'update', 'delete', 'approve', 'triage', etc.
    entity_type VARCHAR NOT NULL,  -- 'entity', 'relation', 'document', 'activity', 'inbox_item'
    entity_id VARCHAR,
    old_state VARCHAR,  -- JSON snapshot do estado anterior
    new_state VARCHAR,  -- JSON snapshot do estado novo
    agent VARCHAR NOT NULL,  -- 'user', 'codex', 'system'
    reason VARCHAR,  -- Por que essa ação foi tomada?
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_workspace VARCHAR DEFAULT 'default',
    id_cli VARCHAR NOT NULL DEFAULT 'local'
);

-- ============================================================================
-- INDEXES (para performance)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
CREATE INDEX IF NOT EXISTS idx_entities_workspace ON entities(id_workspace);
CREATE INDEX IF NOT EXISTS idx_relations_entity_a ON relations(entity_a_id);
CREATE INDEX IF NOT EXISTS idx_relations_entity_b ON relations(entity_b_id);
CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(relation_type);
CREATE INDEX IF NOT EXISTS idx_relations_workspace ON relations(id_workspace);
CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(type);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_cycle_id ON documents(cycle_id);
CREATE INDEX IF NOT EXISTS idx_documents_workspace ON documents(id_workspace);
CREATE INDEX IF NOT EXISTS idx_activities_cycle_id ON activities(cycle_id);
CREATE INDEX IF NOT EXISTS idx_activities_status ON activities(status);
CREATE INDEX IF NOT EXISTS idx_activities_workspace ON activities(id_workspace);
CREATE INDEX IF NOT EXISTS idx_inbox_triaged ON inbox_items(triaged);
CREATE INDEX IF NOT EXISTS idx_inbox_source ON inbox_items(source);
CREATE INDEX IF NOT EXISTS idx_inbox_workspace ON inbox_items(id_workspace);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);

-- ============================================================================
-- INITIAL STATE
-- ============================================================================

-- Default workspace marker
INSERT OR IGNORE INTO system_state (key, value) VALUES ('default_workspace', 'default');
INSERT OR IGNORE INTO system_state (key, value) VALUES ('schema_version', '1.0');
INSERT OR IGNORE INTO system_state (key, value) VALUES ('last_backup', NULL);
INSERT OR IGNORE INTO system_state (key, value) VALUES ('last_sync', NULL);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
