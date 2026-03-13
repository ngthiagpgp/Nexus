-- NEXUS MVP — FastAPI Specification
-- Base URL: http://localhost:3000/api
-- All responses include: status (ok|error), data, message (if error)

-- ============================================================================
-- ENTITIES
-- ============================================================================

GET /entities
  Description: Lista todas as entidades
  Query params:
    - type (optional): filter by type (e.g., 'project', 'person')
    - workspace (optional): default 'default'
  Response 200:
    {
      "status": "ok",
      "data": [
        {
          "id": "uuid-1",
          "name": "Projeto X",
          "type": "project",
          "context": "Pesquisa em economia",
          "created_by": "user",
          "created_at": "2026-03-13T08:00:00Z",
          ...
        }
      ]
    }

POST /entities
  Description: Cria nova entidade
  Body:
    {
      "name": "Projeto Y" (required),
      "type": "project" (required),
      "context": "Descrição opcional"
    }
  Response 201:
    {
      "status": "ok",
      "data": {
        "id": "uuid-new",
        "name": "Projeto Y",
        "type": "project",
        "context": "...",
        "created_by": "user",
        "created_at": "2026-03-13T08:00:00Z",
        ...
      }
    }

GET /entities/{id}
  Description: Obter detalhes de uma entidade
  Response 200:
    {
      "status": "ok",
      "data": { ... entity object ... }
    }
  Response 404:
    {
      "status": "error",
      "message": "Entity not found"
    }

PATCH /entities/{id}
  Description: Atualizar entidade (nome, tipo, context)
  Body:
    {
      "name": "Novo nome" (optional),
      "type": "novo_tipo" (optional),
      "context": "Novo contexto" (optional)
    }
  Response 200:
    {
      "status": "ok",
      "data": { ... updated entity ... }
    }

DELETE /entities/{id}
  Description: Deletar entidade
  Note: Requer validação (não deleta se tem relações)
  Response 204: (no content)
  Response 409:
    {
      "status": "error",
      "message": "Cannot delete entity with existing relations"
    }

-- ============================================================================
-- RELATIONS
-- ============================================================================

GET /relations
  Description: Lista todas as relações
  Query params:
    - entity_a (optional): filter by entity_a_id
    - entity_b (optional): filter by entity_b_id
    - type (optional): filter by relation_type
  Response 200:
    {
      "status": "ok",
      "data": [
        {
          "id": "uuid-rel-1",
          "entity_a_id": "uuid-1",
          "entity_b_id": "uuid-2",
          "relation_type": "depende_de",
          "weight": 0.8,
          "context": "Projeto Y depende de dados do Projeto X",
          "created_by": "user",
          "created_at": "2026-03-13T09:00:00Z",
          ...
        }
      ]
    }

POST /relations
  Description: Criar nova relação
  Body:
    {
      "entity_a_id": "uuid-1" (required),
      "entity_b_id": "uuid-2" (required),
      "relation_type": "depende_de" (required),
      "weight": 0.8 (optional, default 0.5),
      "context": "Contexto breve" (optional)
    }
  Response 201:
    {
      "status": "ok",
      "data": { ... new relation ... }
    }

GET /relations/{id}
  Description: Detalhes de uma relação
  Response 200:
    {
      "status": "ok",
      "data": { ... relation object ... }
    }

PATCH /relations/{id}
  Description: Atualizar relação (type, weight, context)
  Body:
    {
      "relation_type": "novo_tipo" (optional),
      "weight": 0.7 (optional),
      "context": "Novo contexto" (optional)
    }
  Response 200:
    {
      "status": "ok",
      "data": { ... updated relation ... }
    }

DELETE /relations/{id}
  Description: Deletar relação
  Response 204: (no content)

-- ============================================================================
-- DOCUMENTS
-- ============================================================================

GET /documents
  Description: Lista documentos (filtrar por tipo, status, cycle)
  Query params:
    - type (optional): 'daily', 'weekly', 'monthly'
    - status (optional): 'draft', 'approved', 'archived'
    - cycle_id (optional)
  Response 200:
    {
      "status": "ok",
      "data": [
        {
          "id": "uuid-doc-1",
          "title": "Daily 2026-03-13",
          "type": "daily",
          "cycle_id": "cycle-daily-2026-03-13",
          "status": "draft",
          "path": "daily/2026-03-13.md",
          "content_hash": "sha256...",
          "version": "1.0",
          "approved_at": null,
          "created_by": "user",
          "created_at": "2026-03-13T08:00:00Z",
          "changelog": "[{\"version\": \"1.0\", \"changed\": \"Initial draft\", ...}]",
          ...
        }
      ]
    }

POST /documents
  Description: Criar novo documento
  Body:
    {
      "title": "Daily 2026-03-13" (required),
      "type": "daily" (required),
      "cycle_id": "cycle-id-optional" (optional),
      "content": "# Markdown content here" (optional, default empty)
    }
  Response 201:
    {
      "status": "ok",
      "data": { ... new document ... }
    }

GET /documents/{id}
  Description: Obter documento (com conteúdo markdown)
  Response 200:
    {
      "status": "ok",
      "data": {
        "id": "...",
        "title": "...",
        ... (other fields),
        "content": "# Markdown content here\n\n..."
      }
    }

PATCH /documents/{id}
  Description: Atualizar conteúdo do documento
  Body:
    {
      "content": "# Novo conteúdo" (required),
      "auto_version": true (optional, default true)
    }
  Behavior:
    - Recalcula content_hash
    - Se mudança significativa, incrementa version
    - Auto-save, feedback visual: "saving..." → "saved"
  Response 200:
    {
      "status": "ok",
      "data": {
        "id": "...",
        "version": "1.1",
        "modified_at": "2026-03-13T08:30:00Z",
        "content": "# Novo conteúdo"
      }
    }

POST /documents/{id}/approve
  Description: Aprovar documento (draft → approved)
  Body: {} (empty)
  Behavior:
    - Muda status para 'approved'
    - Registra approved_at timestamp
    - Cria commit automático em Git
    - Incrementa version major
  Response 200:
    {
      "status": "ok",
      "data": {
        "id": "...",
        "status": "approved",
        "approved_at": "2026-03-13T08:35:00Z",
        "version": "2.0"
      }
    }

DELETE /documents/{id}
  Description: Deletar (ou arquivar) documento
  Query params:
    - hard_delete (optional, default false): if true, remove from disk
  Response 204: (no content)

-- ============================================================================
-- CYCLES
-- ============================================================================

GET /cycles
  Description: Lista ciclos (daily, weekly, monthly, etc.)
  Query params:
    - type (optional): 'daily', 'weekly', 'monthly'
    - status (optional): 'active', 'completed', 'archived'
  Response 200:
    {
      "status": "ok",
      "data": [
        {
          "id": "cycle-daily-2026-03-13",
          "type": "daily",
          "start_date": "2026-03-13T00:00:00Z",
          "end_date": "2026-03-13T23:59:59Z",
          "status": "active",
          ...
        }
      ]
    }

POST /cycles
  Description: Criar novo ciclo
  Body:
    {
      "type": "daily" (required),
      "start_date": "2026-03-13T00:00:00Z" (required),
      "end_date": "2026-03-13T23:59:59Z" (optional),
      "description": "..." (optional)
    }
  Response 201:
    {
      "status": "ok",
      "data": { ... new cycle ... }
    }

-- ============================================================================
-- ACTIVITIES
-- ============================================================================

GET /activities
  Description: Lista atividades (filtrar por cycle, status, priority)
  Query params:
    - cycle_id (optional)
    - status (optional): 'pending', 'in_progress', 'completed', 'blocked'
    - priority (optional): 1-5
  Response 200:
    {
      "status": "ok",
      "data": [ ... ]
    }

POST /activities
  Description: Criar nova atividade
  Body:
    {
      "title": "Título da atividade" (required),
      "cycle_id": "..." (required),
      "status": "pending" (optional),
      "priority": 3 (optional),
      "type": "task" (optional),
      "description": "..." (optional)
    }
  Response 201:
    {
      "status": "ok",
      "data": { ... new activity ... }
    }

PATCH /activities/{id}
  Description: Atualizar atividade
  Body:
    {
      "status": "in_progress" (optional),
      "priority": 1 (optional),
      ... (other fields)
    }
  Response 200:
    {
      "status": "ok",
      "data": { ... updated activity ... }
    }

-- ============================================================================
-- INBOX
-- ============================================================================

GET /inbox
  Description: Lista itens de inbox
  Query params:
    - triaged (optional, default false): mostrar apenas não-triados
    - source (optional): filtrar por fonte ('email_gmail', 'whatsapp', etc.)
    - classification (optional): filtrar por classificação
  Response 200:
    {
      "status": "ok",
      "data": [
        {
          "id": "inbox-item-1",
          "source": "email_gmail",
          "content": "Resumo do email ou texto bruto",
          "metadata": "{\"from\": \"...\", \"subject\": \"...\", \"date\": \"...\"}",
          "classification": null,
          "priority": 3,
          "triaged": false,
          "created_at": "2026-03-13T07:30:00Z",
          ...
        }
      ]
    }

POST /inbox
  Description: Ingerir novo item no inbox
  Body:
    {
      "source": "email_gmail" (required),
      "content": "Conteúdo ou resumo" (required),
      "metadata": {
        "from": "...",
        "subject": "...",
        "date": "...",
        ... (flexible)
      } (optional),
      "priority": 3 (optional, default 3)
    }
  Response 201:
    {
      "status": "ok",
      "data": { ... new inbox item ... }
    }

PATCH /inbox/{id}
  Description: Triagiar inbox item (marcar classificação, prioridade)
  Body:
    {
      "classification": "actionable" (optional),
      "priority": 1 (optional),
      "triage_feedback": "Isso é contexto importante" (optional)
    }
  Response 200:
    {
      "status": "ok",
      "data": {
        "id": "...",
        "triaged": true,
        "classification": "actionable",
        "priority": 1
      }
    }

DELETE /inbox/{id}
  Description: Deletar item (marcar como ignorado)
  Response 204: (no content)

-- ============================================================================
-- QUERIES
-- ============================================================================

GET /query?q=...
  Description: Executar query simples e declarativa
  Query params:
    - q (required): query string
  Examples:
    - /query?q=entity where type='project'
    - /query?q=relation where entity_a='uuid-1'
    - /query?q=document where type='daily' and status='draft'
    - /query?q=all entities related to 'uuid-1'
  
  Query syntax:
    - entity where <condition>
    - relation where <condition>
    - document where <condition>
    - activity where <condition>
    - inbox where <condition>
    - all entities related to '<entity_name_or_id>'
    - Conditions: type='...', status='...', date>='...', etc.
    - Operators: where, and, or, like
  
  Response 200:
    {
      "status": "ok",
      "data": [ ... results ... ]
    }
  
  Response 400:
    {
      "status": "error",
      "message": "Invalid query syntax"
    }

-- ============================================================================
-- SYSTEM
-- ============================================================================

GET /system/status
  Description: Status do sistema (version, db, backups)
  Response 200:
    {
      "status": "ok",
      "data": {
        "schema_version": "1.0",
        "last_backup": "2026-03-13T00:00:00Z",
        "last_sync": "2026-03-13T08:30:00Z",
        "workspace": "default",
        ... (more metadata)
      }
    }

GET /audit-log?entity_id=...&limit=100
  Description: Ver histórico de auditoria
  Query params:
    - entity_id (optional): filtrar por entidade
    - entity_type (optional): filtrar por tipo
    - agent (optional): filtrar por agente (user|codex|system)
    - limit (optional, default 50): quantidade de registros
  Response 200:
    {
      "status": "ok",
      "data": [
        {
          "id": "...",
          "action": "update",
          "entity_type": "document",
          "entity_id": "...",
          "old_state": "{...}",
          "new_state": "{...}",
          "agent": "user",
          "timestamp": "2026-03-13T08:30:00Z",
          "reason": "Inline edit: updated summary"
        }
      ]
    }

POST /backup
  Description: Disparar backup manual
  Response 201:
    {
      "status": "ok",
      "data": {
        "backup_path": "/backups/nexus_2026-03-13_143000.db",
        "timestamp": "2026-03-13T14:30:00Z"
      }
    }

-- ============================================================================
-- ERROR RESPONSES
-- ============================================================================

All endpoints can return:
  400: Bad Request
    {
      "status": "error",
      "message": "Invalid request body"
    }
  
  401: Unauthorized (future: auth)
    {
      "status": "error",
      "message": "Not authenticated"
    }
  
  404: Not Found
    {
      "status": "error",
      "message": "Resource not found"
    }
  
  409: Conflict
    {
      "status": "error",
      "message": "Conflict detected (e.g., filesystem vs DB mismatch)"
    }
  
  500: Internal Server Error
    {
      "status": "error",
      "message": "Internal server error"
    }

-- ============================================================================
-- END OF API SPEC
-- ============================================================================
