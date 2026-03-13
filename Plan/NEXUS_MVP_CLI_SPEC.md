-- NEXUS MVP — CLI Specification (Python + Typer)
-- Command format: nexus <resource> <action> [options]

-- ============================================================================
-- ENTITIES
-- ============================================================================

nexus entity add <name> [--type TYPE] [--context CONTEXT]
  Add a new entity
  Examples:
    nexus entity add "Projeto X" --type project --context "Pesquisa em economia"
    nexus entity add "Alice" --type person
  Output:
    ✓ Entity created: uuid-1
    Name: Projeto X
    Type: project
    Context: Pesquisa em economia

nexus entity list [--type TYPE] [--workspace WORKSPACE]
  List all entities (optionally filtered)
  Examples:
    nexus entity list
    nexus entity list --type project
  Output:
    ID                                  | Name          | Type     | Context
    ──────────────────────────────────────────────────────────────────────────
    uuid-1                              | Projeto X     | project  | Pesquisa...
    uuid-2                              | Alice         | person   | -
    ...

nexus entity show <id_or_name>
  Show details of an entity
  Examples:
    nexus entity show uuid-1
    nexus entity show "Projeto X"
  Output:
    Entity: Projeto X
    ID: uuid-1
    Type: project
    Context: Pesquisa em economia
    Created: 2026-03-13 08:00:00
    Modified: 2026-03-13 09:30:00
    Related relations: 3

nexus entity edit <id_or_name> [--name NAME] [--type TYPE] [--context CONTEXT]
  Edit an entity
  Examples:
    nexus entity edit uuid-1 --name "Projeto X (Rev. 2)"
    nexus entity edit "Projeto X" --context "Pesquisa em economia urbana"
  Output:
    ✓ Entity updated: uuid-1

nexus entity delete <id_or_name> [--force]
  Delete an entity
  Note: Fails if entity has relations (use --force to override)
  Examples:
    nexus entity delete uuid-1
  Output:
    ✓ Entity deleted: uuid-1

-- ============================================================================
-- RELATIONS
-- ============================================================================

nexus relation add <entity_a> <entity_b> <type> [--weight WEIGHT] [--context CONTEXT]
  Create a new relation
  Args:
    - entity_a: name or id
    - entity_b: name or id
    - type: relation_type string
  Examples:
    nexus relation add "Projeto X" "Projeto Y" "depende_de" --weight 0.8
    nexus relation add "Alice" "Projeto X" "trabalha_em"
  Output:
    ✓ Relation created: uuid-rel-1
    Projeto X → Projeto Y: depende_de (weight: 0.8)

nexus relation list [--entity_a ID] [--entity_b ID] [--type TYPE]
  List relations (optionally filtered)
  Examples:
    nexus relation list
    nexus relation list --entity_a uuid-1
    nexus relation list --type depende_de
  Output:
    ID                  | From           | To             | Type           | Weight
    ────────────────────────────────────────────────────────────────────────────
    uuid-rel-1          | Projeto X      | Projeto Y      | depende_de     | 0.8
    uuid-rel-2          | Alice          | Projeto X      | trabalha_em    | 0.9
    ...

nexus relation show <id>
  Show details of a relation
  Output:
    Relation: uuid-rel-1
    From: Projeto X
    To: Projeto Y
    Type: depende_de
    Weight: 0.8
    Context: Projeto Y depende de dados do Projeto X
    Created: 2026-03-13 08:30:00

nexus relation edit <id> [--type TYPE] [--weight WEIGHT] [--context CONTEXT]
  Edit a relation
  Examples:
    nexus relation edit uuid-rel-1 --weight 0.5
  Output:
    ✓ Relation updated: uuid-rel-1

nexus relation delete <id> [--force]
  Delete a relation
  Output:
    ✓ Relation deleted: uuid-rel-1

nexus relation graph [--entity ID] [--depth DEPTH]
  Show graph/tree visualization of relations (text-based)
  Examples:
    nexus relation graph
    nexus relation graph --entity "Projeto X" --depth 2
  Output:
    Projeto X
    ├── depende_de → Projeto Y
    │   └── referencia → Dataset A
    └── trabalha_em ← Alice

-- ============================================================================
-- DOCUMENTS
-- ============================================================================

nexus document create --type TYPE [--title TITLE] [--cycle_id CYCLE_ID]
  Create a new document
  Types: daily, weekly, monthly, report, note
  Examples:
    nexus document create --type daily
    nexus document create --type weekly --title "Week 11 Review"
  Output:
    ✓ Document created: uuid-doc-1
    Type: daily
    Status: draft
    Path: daily/2026-03-13.md
    Opens editor: vim daily/2026-03-13.md

nexus document list [--type TYPE] [--status STATUS]
  List documents (optionally filtered)
  Examples:
    nexus document list
    nexus document list --type daily --status draft
  Output:
    ID              | Title              | Type    | Status    | Path
    ────────────────────────────────────────────────────────────────────
    uuid-doc-1      | Daily 2026-03-13   | daily   | draft     | daily/2026-03-13.md
    uuid-doc-2      | Weekly 2026-W11    | weekly  | approved  | weekly/2026-W11.md
    ...

nexus document show <id_or_path>
  Show document content + metadata
  Examples:
    nexus document show uuid-doc-1
    nexus document show daily/2026-03-13.md
  Output:
    Document: Daily 2026-03-13
    ID: uuid-doc-1
    Path: daily/2026-03-13.md
    Status: draft
    Version: 1.0
    Created: 2026-03-13 08:00:00
    ──────────────────────────────────────
    # Daily Review — 2026-03-13
    
    ## Completed
    - Task 1
    - Task 2
    ...

nexus document edit <id_or_path>
  Open document in editor (vim/nano/code)
  Triggers auto-save behavior on close
  Output:
    ✓ Document saved: uuid-doc-1 (version 1.1)
    Hash updated, Git tracked

nexus document approve <id>
  Approve document (draft → approved)
  Requires explicit confirmation
  Output:
    ✓ Document approved: uuid-doc-1
    Status: approved
    Version bumped to 2.0
    Git commit created: "Approve daily 2026-03-13"

nexus document delete <id> [--hard]
  Delete (or archive) document
  Default: archive (move to status='archived')
  --hard: remove from disk entirely
  Output:
    ✓ Document archived: uuid-doc-1

nexus document validate [--id ID]
  Check for conflicts (filesystem vs DB mismatch)
  Examples:
    nexus document validate
    nexus document validate --id uuid-doc-1
  Output:
    Validating documents...
    ✓ All documents in sync
    
    Or:
    ⚠ Conflict detected: uuid-doc-1
    File hash: abc123...
    DB hash: def456...
    Action: [r]evert file | [u]pdate db | [m]erge (interactive)

-- ============================================================================
-- CYCLES
-- ============================================================================

nexus cycle list [--type TYPE] [--status STATUS]
  List cycles (daily, weekly, monthly, etc.)
  Examples:
    nexus cycle list
    nexus cycle list --type daily
  Output:
    ID                          | Type    | Start              | Status
    ──────────────────────────────────────────────────────────────────
    cycle-daily-2026-03-13      | daily   | 2026-03-13 00:00   | active
    cycle-weekly-2026-W11       | weekly  | 2026-03-10 00:00   | active
    ...

nexus cycle create --type TYPE --start START [--end END]
  Create a new cycle
  Examples:
    nexus cycle create --type daily --start 2026-03-13
    nexus cycle create --type weekly --start 2026-03-10 --end 2026-03-16
  Output:
    ✓ Cycle created: cycle-daily-2026-03-13

-- ============================================================================
-- ACTIVITIES
-- ============================================================================

nexus activity add --cycle_id CYCLE_ID <title> [--priority PRIORITY] [--type TYPE]
  Add activity to a cycle
  Examples:
    nexus activity add --cycle_id cycle-daily-2026-03-13 "Finish report"
    nexus activity add --cycle_id cycle-daily-2026-03-13 "Finish report" --priority 1
  Output:
    ✓ Activity created: uuid-activity-1
    Cycle: Daily 2026-03-13
    Title: Finish report
    Status: pending
    Priority: 3

nexus activity list [--cycle_id CYCLE_ID] [--status STATUS]
  List activities
  Examples:
    nexus activity list
    nexus activity list --cycle_id cycle-daily-2026-03-13 --status pending
  Output:
    ID              | Title          | Cycle              | Status      | Priority
    ───────────────────────────────────────────────────────────────────────────
    uuid-act-1      | Finish report  | Daily 2026-03-13   | pending     | 1
    uuid-act-2      | Review email   | Daily 2026-03-13   | in_progress | 3
    ...

nexus activity edit <id> [--status STATUS] [--priority PRIORITY]
  Edit activity
  Examples:
    nexus activity edit uuid-act-1 --status completed
  Output:
    ✓ Activity updated: uuid-act-1

-- ============================================================================
-- INBOX & INGESTION
-- ============================================================================

nexus inbox add --source SOURCE [--priority PRIORITY] <content>
  Add item to inbox (manual ingestion)
  Sources: email_gmail, email_outlook, whatsapp, teams, drive, slack
  Examples:
    nexus inbox add --source email_gmail "Subject: Important meeting confirmed"
    nexus inbox add --source whatsapp --priority 1 "Need this done ASAP"
  Output:
    ✓ Inbox item created: uuid-inbox-1
    Source: email_gmail
    Priority: 3
    Status: untriad

nexus inbox list [--triaged FALSE] [--source SOURCE]
  List inbox items
  Examples:
    nexus inbox list
    nexus inbox list --triaged false  # Show only untriad
    nexus inbox list --source email_gmail
  Output:
    ID              | Source           | Content          | Priority | Triaged
    ────────────────────────────────────────────────────────────────────────
    uuid-inbox-1    | email_gmail      | Subject: ...     | 3        | false
    uuid-inbox-2    | whatsapp         | Need this done...|1        | false
    ...

nexus inbox triage <id> --classification CLASS [--priority PRIORITY]
  Triage an inbox item
  Classes: action_now, actionable, context, noise
  Examples:
    nexus inbox triage uuid-inbox-1 --classification actionable
    nexus inbox triage uuid-inbox-2 --classification action_now --priority 1
  Output:
    ✓ Item triaged: uuid-inbox-1
    Classification: actionable
    Priority: 3
    Status: triaged

nexus inbox delete <id>
  Delete inbox item
  Output:
    ✓ Inbox item deleted: uuid-inbox-1

nexus inbox ingest --source SOURCE --file FILE
  Batch ingest from file (CSV or JSON)
  Examples:
    nexus inbox ingest --source email_gmail --file emails.csv
  Output:
    Ingesting from emails.csv...
    ✓ 15 items imported
    Ready for triage

-- ============================================================================
-- QUERIES (Simple & Declarative)
-- ============================================================================

nexus query <query_string>
  Execute a simple query
  Syntax:
    - entity where <condition>
    - relation where <condition>
    - document where <condition>
    - activity where <condition>
    - inbox where <condition>
    - all entities related to '<name>'
  
  Conditions:
    - type='...'
    - status='...'
    - priority=1
    - date>='2026-03-13'
    - created_by='user' | 'codex' | 'system'
  
  Operators: where, and, or, like
  
  Examples:
    nexus query "entity where type = 'project'"
    nexus query "entity where type = 'project' and created_by = 'user'"
    nexus query "relation where type = 'depende_de'"
    nexus query "document where type = 'daily' and status = 'draft'"
    nexus query "activity where status = 'pending' and priority <= 2"
    nexus query "inbox where triaged = false and source = 'email_gmail'"
    nexus query "all entities related to 'Projeto X'"
  
  Output (table format):
    Entity Query Results:
    ID              | Name           | Type     | Context
    ─────────────────────────────────────────────────────
    uuid-1          | Projeto X      | project  | Pesquisa...
    uuid-3          | Projeto Z      | project  | Análise...
    
    2 results found

nexus query --json <query_string>
  Execute query and output JSON
  Output: JSON array of results
  Useful for: piping to other tools, programmatic use

-- ============================================================================
-- SYSTEM
-- ============================================================================

nexus status
  Show system status
  Output:
    NEXUS Status
    ─────────────────
    Schema version: 1.0
    Workspace: default
    Database: nexus.duckdb
    Size: 2.3 MB
    
    Last backup: 2026-03-13 00:00:00
    Last sync: 2026-03-13 14:30:00
    
    Entities: 42
    Relations: 127
    Documents: 18 (5 draft, 13 approved)
    Inbox items: 156 (12 untriaged)

nexus init [--workspace WORKSPACE]
  Initialize Nexus in current directory
  Creates:
    - nexus.duckdb
    - .nexus/config.yaml
    - documents/ directory structure
    - .gitignore
  Output:
    ✓ Nexus initialized: nexus.duckdb
    Ready to use!

nexus backup [--output PATH]
  Create manual backup
  Output:
    ✓ Backup created: /backups/nexus_2026-03-13_143000.db
    Size: 2.3 MB

nexus restore --file PATH
  Restore from backup
  Output:
    ⚠ This will overwrite current data. Continue? [y/N]
    ✓ Restored from: /backups/nexus_2026-03-13_143000.db

nexus audit [--entity_id ID] [--limit LIMIT]
  View audit log
  Examples:
    nexus audit
    nexus audit --entity_id uuid-1 --limit 20
  Output:
    Audit Log (latest 50 entries)
    ──────────────────────────────────────────────────────
    2026-03-13 14:30:00 | update | document | uuid-doc-1 | user | "Inline edit"
    2026-03-13 14:25:00 | create | activity | uuid-act-2 | user | "Added task"
    ...

nexus config [--show] [--set KEY=VALUE]
  Manage configuration
  Examples:
    nexus config --show
    nexus config --set default_workspace=myspace
  Output:
    workspace: default
    editor: vim
    auto_backup: true
    backup_interval: 86400 (1 day)

nexus help
  Show help (global or per-command)
  Examples:
    nexus help
    nexus help entity
    nexus help document create

-- ============================================================================
-- OUTPUT CONSISTENCY
-- ============================================================================

Success outputs:
  ✓ [Action completed]: [details]

Error outputs:
  ✗ Error: [error message]
  Hint: [helpful hint]

Warnings:
  ⚠ [Warning message]
  Action: [prompt for confirmation]

Verbose mode:
  --verbose or -v flag adds extra details

JSON mode:
  --json flag outputs JSON (useful for scripting)

-- ============================================================================
-- END OF CLI SPEC
-- ============================================================================
