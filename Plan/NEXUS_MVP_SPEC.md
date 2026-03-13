# NEXUS MVP — Specification Document

**Version**: 1.0  
**Status**: Draft (awaiting validation)  
**Last Updated**: 2026-03-13  
**Author**: Thiago Gardin (with Claude)

---

## 1. Visão e propósito

### 1.1 O problema

Você trabalha em múltiplos contextos (email, chat, pesquisa, código, reuniões) e as informações ficam **fragmentadas em abas, janelas e plataformas diferentes**. Isso cria:

- Atrito cognitivo (onde estava mesmo?)
- Perda de contexto (qual era a premissa?)
- Falta de auditoria (por que decidimos assim?)
- Dependência excessiva de chat como "memória externa"

### 1.2 A solução

**Nexus** é um **unified workspace local** que:
- **Centraliza** entidades (projetos, pessoas, conceitos) e suas relações
- **Indexa** documentos operacionais (dailies, weeklies, monthlies) com estado (draft → approved)
- **Ingere** contexto externo (email, WhatsApp, Teams) de forma estruturada
- **Permite queries** rápidas sobre a estrutura cognitiva já montada
- **Reduz atrito** com inline editing, auto-save e visualização clara

### 1.3 Diferencial

O Nexus **não substitui** suas ferramentas existentes (Obsidian, RStudio, Google Drive, etc.). Ele **integra** como orchestrator local, permitindo:

- Ver relações entre documentos, projetos, pessoas
- Consultar rapidamente "quem depende do quê"
- Auditar decisões (quando foi decidido? por quê? com base em qual contexto?)
- Reduzir copy-paste entre sistemas

---

## 2. Princípios de design

### 2.1 Simplicidade primeiro

- **MVP cubra view + ingest + edit**, não todas as integrações
- **Queries sejam simples**, não Turing-complete
- **Interface reduza atrito**, não adicione

### 2.2 Portabilidade

- **Markdown é fonte canônica** de conteúdo (legível, versionável, Git-friendly)
- **DuckDB é fonte canônica** de estado operacional
- **Git registra diff textual**, sistema registra mudanças lógicas

### 2.3 Rastreabilidade

- **Todo registro** tem `created_by`, `modified_by`, `approved_by`, `timestamp`
- **Conflitos explícitos** entre filesystem, banco e agentes
- **Auditoria completa** de operações sensíveis

### 2.4 Fluidez

- **Inline editing** como padrão (clique e edite, não formulários pesados)
- **Auto-save** em mudanças, feedback visual discreto
- **Versionamento automático** sem você pensar
- **UX estilo Obsidian/Discord**, não Notion/Teams

---

## 3. Arquitetura geral

```
┌─────────────────────────────────────────────────────┐
│           NEXUS CORE (Python + FastAPI)             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌────── CLI (Typer) ──────────────────────────┐   │
│  │ nexus entity add/edit/del                   │   │
│  │ nexus relation add/edit/del                 │   │
│  │ nexus document create/edit/approve          │   │
│  │ nexus query "..."                           │   │
│  │ nexus inbox add/triage                      │   │
│  └─────────────────────────────────────────────┘   │
│           ↓                                          │
│  ┌────── API Local (FastAPI, :3000) ──────────┐   │
│  │ GET/POST /entities, /relations, /documents │   │
│  │ PATCH /entities/:id, etc.                  │   │
│  │ POST /documents/:id/approve                │   │
│  │ GET /query?q=...                           │   │
│  │ GET/POST /inbox                            │   │
│  └─────────────────────────────────────────────┘   │
│           ↓                                          │
│  ┌────── DuckDB (local) ──────────────────────┐   │
│  │ entities | relations | documents           │   │
│  │ inbox_items | cycles | activities | outputs│   │
│  │ system_state | audit_log                   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌────── Filesystem ──────────────────────────┐   │
│  │ documents/                                 │   │
│  │   daily/2026-03-13.md                      │   │
│  │   weekly/2026-W11.md                       │   │
│  │   monthly/2026-03.md                       │   │
│  │ .nexus/                                    │   │
│  │   config.yaml                              │   │
│  │   backups/                                 │   │
│  │ .git (versioning)                          │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
├─────────────────────────────────────────────────────┤
│  ┌──── Web UI (React + TypeScript) ───────────┐   │
│  │ [Tabs: Entities | Relations | Documents]   │   │
│  │ ├─ Inline editing                          │   │
│  │ ├─ Auto-save with visual feedback          │   │
│  │ ├─ Query interface                         │   │
│  │ └─ Inbox triage                            │   │
│  └─────────────────────────────────────────────┘   │
│           ↑                                          │
├─────────────────────────────────────────────────────┤
│  ┌──── Agente Especialista (Codex) ───────────┐   │
│  │ • Ingestão de email/WhatsApp/Teams        │   │
│  │ • Geração de documentos (drafts)           │   │
│  │ • Sugestões de relações                    │   │
│  │ • Reflexão assistida                       │   │
│  │ • Autoengenharia controlada                │   │
│  │ Acesso: CLI + DuckDB direto (auditado)     │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 4. Modelo de dados

### 4.1 Separação: Filesystem vs DuckDB

| Artefato | Fonte canônica | Complementado por |
|----------|---|---|
| **Conteúdo de documento** | Markdown em disco | Frontmatter YAML |
| **Estado operacional** | DuckDB (doc_id, status, version, hash) | Git (diff) |
| **Relações estruturais** | DuckDB (entities, relations) | Obsidian grafo (reader) |
| **Auditoria** | DuckDB (audit_log, changelog) | Git (commit messages) |
| **Inbox externo** | DuckDB (inbox_items) | Metadata JSON |

### 4.2 Campos obrigatórios (todos os registros)

```
id                (UUID)
created_at        (timestamp)
created_by        (user | codex | system)
modified_at       (timestamp)
modified_by       (user | codex | system)
id_workspace      (workspace identifier, default: 'default')
id_cli            (client/instance identifier)
```

### 4.3 Tabelas principais

**entities** — O que você rastreia (projetos, pessoas, conceitos)
```
id, name, type, context, created_at, created_by, ...
```

**relations** — Conexões entre entidades
```
id, entity_a_id, entity_b_id, relation_type, weight, created_at, ...
```

**documents** — Artifacts operacionais (daily, weekly, monthly)
```
id, title, type, cycle_id, status (draft|approved|archived),
path, content_hash, version, approved_at, created_by, ...
```

**inbox_items** — Contexto externo (email, WhatsApp, Teams)
```
id, source, content, metadata (JSON), classification, priority,
triaged, triage_feedback, created_by, ...
```

**cycles** — Temporal structure (daily, weekly, monthly)
```
id, type, start_date, end_date, status, created_by, ...
```

**activities** — O que você faz dentro de cada ciclo
```
id, title, cycle_id, status, priority, type, created_by, ...
```

**outputs** — Artefatos gerados (arquivos, decisões)
```
id, activity_id, type, path, generated_at, status, created_by, ...
```

**system_state** — Configuração e metadados do sistema
```
key, value, last_updated
```

**audit_log** — Rastreabilidade completa
```
id, action, entity_type, entity_id, old_state, new_state,
agent, timestamp, reason
```

---

## 5. Ciclos temporais e renderização

### 5.1 Estrutura

```
DIÁRIO (micro) — 8h (aquecimento) + 18h (resfriamento)
  └─ Mostra: agenda + tarefas críticas + emails urgentes + status de projetos
  └─ Gera: draft de "daily review"

SEMANAL (meso) — domingo/segunda (aquecimento) + sexta/sábado (resfriamento)
  └─ Mostra: retrospectiva semana anterior + padrões + débito + prioridades
  └─ Gera: "weekly review" draft

MENSAL (macro) — ~1º dia
  └─ Mostra: retrospectiva do mês + tendências + pivôs estratégicos
  └─ Gera: "monthly review" draft

SEMESTRAL + ESTRATÉGICO — on-demand
  └─ Refazimento de planejamento se circunstâncias críticas
```

### 5.2 O que o Nexus renderiza

Cada ciclo tem um documento estruturado que:
1. É gerado como **draft** (Codex ou você)
2. É editável **inline** no Nexus Web
3. Viraliza **approved** após você validar
4. Fica versionado no Git + changelog no banco

---

## 6. Fluxo de documentos: draft → approved

### 6.1 Estados

```
draft    → você ou agente cria
↓
edit     → você refina inline (auto-save)
↓
approved → você sinaliza "validado" (timestamp + user)
↓
archived → documento antigo, mantém versão
```

### 6.2 Versionamento

- **Auto-save** a cada keystroke (300ms debounce)
- **Major version** ao mudar estado (draft → approved)
- **Changelog JSON** no banco: `[{version: "1.0", changed: "...", timestamp: "..."}]`
- **Git diff** automático: commit ao aprovar

---

## 7. Ingestão e triagem

### 7.1 Fluxo semanal

```
Semana:
  ├─ Você exporta Email/WhatsApp/Teams manualmente (ou agente estrutura)
  ├─ Joga no Nexus via CLI: nexus inbox add --source=email --content="..."
  ├─ Sistema classifica com placeholder (você valida depois)
  └─ Você triaga manualmente no Inbox tab

Triagem (15-20 min):
  ├─ Vê cada item
  ├─ Marca: action_now | actionable | context | noise
  ├─ Auto-save ao mudar
  └─ Items críticos viram atividades (depois)
```

### 7.2 Classificação (MVP: placeholder)

```
classification: 
  - "action_now"  (< 1% do inbox)
  - "actionable"  (~15%)
  - "context"     (~50%)
  - "noise"       (rest)
```

No MVP, é **manual ou heurística trivial** (você refina depois).

---

## 8. Agente especialista (Codex)

### 8.1 O que pode fazer

- ✅ **Ler** dados do Nexus (entities, relations, documents, inbox)
- ✅ **Criar** novos registros (entities, suggestions de relações, inbox items)
- ✅ **Atualizar** registros em draft/suggestion/untriaged
- ✅ **Gerar** documentos (dailies, weeklies) como drafts
- ✅ **Fazer autoengenharia**: revisar artefatos, otimizar, documentar
- ✅ **Registrar ações** no audit_log (rastreabilidade completa)

### 8.2 O que NÃO pode fazer (sem validação explícita)

- ❌ Deletar entidades, relações, documentos
- ❌ Aprovar documentos sensíveis
- ❌ Alterar `created_by` ou falsificar timestamps
- ❌ Limpar audit_log

### 8.3 Contrato

```
Agente pode operar Nexus como workspace privilegiado, mas:
  • Toda ação é auditada (quem, quando, por quê)
  • Saídas sensíveis ficam em draft até validação
  • Autoengenharia é controlada (pode revisar, melhorar, propor)
  • Não pode canonizar ou apagar trilhas silenciosamente
```

---

## 9. Backups, recovery e reconciliação

### 9.1 Strategy

```
DuckDB      → Backup diário local (/backups/nexus_YYYY-MM-DD.db)
Documentos  → Versionados em Git (markdown + frontmatter)
Audit log   → Rastreamento completo em DuckDB
```

### 9.2 Reconciliação

Se **filesystem ≠ DuckDB**:
- Sistema detecta (hash mismatch)
- Sinaliza conflito explicitamente
- Oferece: merge, revert ou manual reconciliation

---

## 10. Stack técnico

| Layer | Stack |
|-------|-------|
| **Backend API** | Python 3.11+ + FastAPI |
| **CLI** | Python + Typer |
| **Database** | DuckDB (local, SQL-based) |
| **Frontend** | React 18+ + TypeScript |
| **UI Components** | Shadcn/ui or Headless UI |
| **Editor Markdown** | Monaco or CodeMirror |
| **State Management** | TanStack Query + Zustand |
| **Versioning** | Git (local) |

---

## 11. Roadmap MVP

### Phase 1: Fundação (Weeks 1-2)
- [ ] CLI básica (CRUD entities, relations, documents)
- [ ] DuckDB schema + migrations
- [ ] FastAPI API endpoints
- [ ] Markdown I/O (read/write)

### Phase 2: Web UI (Weeks 3-4)
- [ ] React frontend (tabs + inline editing)
- [ ] Entity/Relation list + create forms
- [ ] Document editor (markdown + preview)
- [ ] Auto-save + versioning

### Phase 3: Queries + Inbox (Week 5)
- [ ] Simple query interface
- [ ] Inbox ingestion + triage
- [ ] Audit log visualization

### Phase 4: Polish + Agente (Week 6+)
- [ ] Conflict detection (filesystem vs DB)
- [ ] Backup system
- [ ] Agente integration + examples

---

## 12. Success criteria

- [ ] CLI CRUD works (você consegue criar entidades/relações via comando)
- [ ] Web UI funciona (você edita inline sem atrito)
- [ ] Queries retornam resultados relevantes
- [ ] Documentos draft → approved sem duplicação
- [ ] Agente consegue ingerir email/WhatsApp estruturado
- [ ] Auditoria completa (você consegue rastrear qualquer decisão)

---

## 13. Aberto para refinamento

Esta SPEC é **draft até aprovação**.

**Próximo passo**: Você valida em um chat, eu refino, depois congelamos e Codex começa.

---

**Fim da SPEC v1.0**
