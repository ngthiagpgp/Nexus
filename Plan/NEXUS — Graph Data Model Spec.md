## v1.0 (Implementable Institutional Graph Model)

---

# 1. Objetivo do modelo

O modelo de dados do grafo deve representar, de forma explícita e auditável:

- objetos institucionais;
    
- relações institucionais;
    
- estado operacional;
    
- peso epistêmico;
    
- vínculo de governança;
    
- propagação de risco;
    
- temporalidade;
    
- memória de eventos.
    

O modelo não serve apenas para armazenar entidades.  
Serve para sustentar:

- projeções visuais;
    
- raciocínio institucional;
    
- queries causais;
    
- reconstrução histórica;
    
- cálculo de risco e legitimidade.
    

---

# 2. Princípio estrutural

O grafo do Nexus deve ser modelado em duas camadas:

## A. Canonical Object Layer

Camada canônica dos objetos institucionais.

## B. Relationship/Event Layer

Camada relacional e temporal que transforma objetos em realidade sistêmica.

Em termos práticos:

Objects + Edges + Events + State Projections = Institutional Graph

---

# 3. Entidades canônicas do modelo

## 3.1 Institutional Object

Todo nó do grafo deriva de um objeto institucional canônico.

Campos mínimos:

object_id  
object_type  
slug  
title  
description  
status  
created_at  
updated_at  
archived_at  
source_system  
workspace_id  
cycle_id (nullable, dependendo do tipo)

### `object_type` permitido inicialmente

- cycle
    
- activity
    
- document
    
- entity
    
- decision
    
- risk
    
- authority
    
- mandate
    

Esses tipos podem crescer depois, mas devem começar fechados.

---

## 3.2 Object Identity Rules

Cada objeto deve ter:

- `object_id`: identificador interno estável
    
- `slug`: identificador legível e persistente
    
- `title`: label humano principal
    
- `description`: texto interpretável
    
- `source_system`: origem operacional (`nexus`, `imported`, `external`)
    
- `workspace_id`: delimitação local-first
    

Regra:

- `slug` é para navegação humana
    
- `object_id` é para integridade interna
    
- ids crus não devem ser label primário da UI
    

---

# 4. Especializações por tipo de objeto

## 4.1 Cycle

Representa a unidade institucional principal.

Campos adicionais:

cycle_kind  
cycle_state  
start_at  
end_at  
priority_level  
owner_entity_id  
authority_id  
integrity_state  
risk_state

### `cycle_state`

- planned
    
- active
    
- blocked
    
- completed
    
- archived
    

### `integrity_state`

- healthy
    
- degraded
    
- contested
    

---

## 4.2 Activity

Representa ato operacional institucionalmente relevante.

Campos adicionais:

activity_state  
activity_kind  
priority_level  
due_at  
started_at  
completed_at  
blocked_reason  
assignee_entity_id  
decision_required (boolean)

### `activity_state`

- queued
    
- in_progress
    
- blocked
    
- completed
    
- cancelled
    

---

## 4.3 Document

Representa objeto epistêmico ativo.

Campos adicionais:

document_kind  
document_state  
version_label  
content_hash  
integrity_state  
drift_state  
trust_state  
effective_from  
effective_to  
supersedes_object_id

### `document_state`

- draft
    
- active
    
- approved
    
- obsolete
    
- archived
    

### `drift_state`

- none
    
- suspected
    
- confirmed
    
- reconciled
    

### `trust_state`

- trusted
    
- provisional
    
- contested
    
- invalid
    

---

## 4.4 Entity

Representa ator institucional, unidade organizacional, stakeholder ou sistema.

Campos adicionais:

entity_kind  
entity_state  
parent_entity_id  
external_ref

### `entity_kind`

- person
    
- team
    
- office
    
- system
    
- stakeholder
    
- external_body
    

---

## 4.5 Decision

Representa ato decisório institucional.

Campos adicionais:

decision_state  
decision_kind  
decided_at  
decided_by_entity_id  
authority_id  
justification  
outcome

### `decision_state`

- proposed
    
- pending
    
- approved
    
- rejected
    
- overridden
    

---

## 4.6 Risk

Representa risco institucional explicitado pelo sistema ou por humano.

Campos adicionais:

risk_kind  
risk_level  
risk_state  
emergence_mode  
detected_at  
resolved_at  
owner_entity_id

### `risk_kind`

- evidential
    
- temporal
    
- governance
    
- systemic
    

### `emergence_mode`

- manual
    
- inferred
    
- propagated
    

---

## 4.7 Authority

Representa fonte de legitimidade/autorização.

Campos adicionais:

authority_kind  
authority_state  
valid_from  
valid_to  
scope_description

---

## 4.8 Mandate

Representa mandato institucional formal associado a um ciclo ou decisão.

Campos adicionais:

mandate_state  
mandate_kind  
issued_at  
expires_at  
issued_by_entity_id

---

# 5. Camada relacional do grafo

## 5.1 Institutional Edge

Toda relação causal/institucional entre dois objetos deve existir explicitamente.

Campos mínimos:

edge_id  
from_object_id  
to_object_id  
edge_type  
edge_state  
strength  
created_at  
updated_at  
valid_from  
valid_to  
evidential_basis_object_id  
governance_source_object_id  
created_by

### `edge_type` inicial

- blocks
    
- supports
    
- requires
    
- derives_from
    
- supersedes
    
- mandates
    
- invalidates
    
- escalates
    
- owns
    
- impacts
    
- authorizes
    
- references
    

### `edge_state`

- active
    
- inactive
    
- contested
    
- expired
    

### `strength`

Pode ser inteiro ou decimal simples, por exemplo:

- 1 = fraco
    
- 2 = moderado
    
- 3 = forte
    

No início, não precisa ser probabilístico sofisticado.

---

## 5.2 Regras de integridade de arestas

Regras mínimas:

- `from_object_id` e `to_object_id` devem existir
    
- `edge_type` deve ser semanticamente válido para o par de tipos
    
- self-edge só permitido quando explicitamente modelado
    
- arestas vencidas não somem; passam para `expired`
    
- arestas contestadas continuam visíveis para audit e reconstrução histórica
    

---

# 6. Temporalidade do modelo

O grafo é temporal por definição.

Toda tabela principal deve suportar pelo menos:

created_at  
updated_at  
archived_at (nullable)  
valid_from (nullable, quando fizer sentido)  
valid_to (nullable, quando fizer sentido)

Isso permite três operações críticas:

- **state now**
    
- **historical replay**
    
- **future projection / pending expiration**
    

---

# 7. Camada epistêmica

O Nexus precisa representar não só documentos, mas seu peso institucional.

## 7.1 Evidence Link

Relação explícita entre objeto e evidência.

Campos:

evidence_link_id  
subject_object_id  
document_object_id  
evidence_role  
confidence_score  
required_for_decision (boolean)  
created_at  
updated_at

### `evidence_role`

- supports
    
- justifies
    
- validates
    
- contextualizes
    
- constrains
    
- invalidates
    

### `confidence_score`

Faixa inicial simples:

- 0.0 a 1.0
    

No MVP pode até ser:

- low
    
- medium
    
- high
    

---

## 7.2 Epistemic State Projection

Tabela ou view derivada para leitura rápida:

object_id  
evidence_count  
trusted_evidence_count  
contested_evidence_count  
drifted_evidence_count  
epistemic_status  
last_evidence_change_at

### `epistemic_status`

- sufficient
    
- fragile
    
- degraded
    
- contested
    
- missing
    

Essa projeção é extremamente importante para UI e grafo.

---

# 8. Camada de governança

## 8.1 Governance Binding

Vínculo explícito entre objeto e legitimidade/autorização.

Campos:

binding_id  
object_id  
authority_object_id  
binding_kind  
binding_state  
issued_at  
expires_at  
notes

### `binding_kind`

- authorized_by
    
- reviewed_by
    
- mandated_by
    
- delegated_by
    
- overridden_by
    

### `binding_state`

- active
    
- expired
    
- contested
    
- revoked
    

---

## 8.2 Governance State Projection

View para uso rápido em UI/engine:

object_id  
governance_status  
authority_count  
active_binding_count  
expired_binding_count  
contested_binding_count  
last_governance_change_at

### `governance_status`

- clear
    
- provisional
    
- contested
    
- expired
    
- missing
    

---

# 9. Camada de risco

## 9.1 Risk Record

Risco pode ser um objeto, mas também precisa de registro operacional.

Campos:

risk_record_id  
risk_object_id  
subject_object_id  
risk_kind  
risk_level  
risk_state  
emergence_mode  
detected_at  
resolved_at  
explanation

### `risk_level`

- low
    
- medium
    
- high
    
- critical
    

### `risk_state`

- open
    
- monitoring
    
- mitigated
    
- resolved
    

---

## 9.2 Risk Projection

View de leitura sistêmica:

object_id  
open_risk_count  
critical_risk_count  
systemic_risk_count  
risk_pressure_score  
last_risk_change_at

`risk_pressure_score` pode começar como heurística simples.  
Não precisa ser IA desde o início.

---

# 10. Camada de eventos/memória institucional

Esta é a parte que impede o Nexus de virar CRUD.

## 10.1 Institutional Event

Todo ato relevante gera evento institucional.

Campos:

event_id  
event_type  
event_title  
event_summary  
actor_type  
actor_id  
subject_object_id  
related_object_id  
cycle_id  
workspace_id  
caused_by_event_id  
occurred_at  
recorded_at  
technical_trace_ref

### `event_type` inicial

- object_created
    
- object_updated
    
- status_changed
    
- document_attached
    
- evidence_drift_detected
    
- document_reconciled
    
- activity_blocked
    
- activity_unblocked
    
- decision_recorded
    
- authority_bound
    
- risk_detected
    
- risk_resolved
    
- cycle_completed
    
- cycle_archived
    

O ponto importante:  
o evento tem **título e resumo humanos**, não só mutação técnica.

---

## 10.2 Event Relation

Eventos podem depender de outros eventos.

Campos:

event_relation_id  
from_event_id  
to_event_id  
relation_type

### `relation_type`

- caused
    
- followed
    
- invalidated
    
- resolved
    
- escalated
    

Isso permite reconstrução narrativa.

---

# 11. Projeções materializadas / views do grafo

O modelo canônico pode ser relacional.  
Mas a UI e o engine precisam de projeções específicas.

## 11.1 Graph Node View

node_id  
node_type  
label  
secondary_label  
status  
epistemic_status  
governance_status  
risk_pressure_score  
cycle_id  
is_primary_focus  
visual_group

---

## 11.2 Graph Edge View

edge_id  
from_node_id  
to_node_id  
edge_type  
strength  
edge_state  
is_risk_edge  
is_governance_edge  
is_epistemic_edge

---

## 11.3 Cycle Situation View

cycle_id  
cycle_label  
cycle_state  
activity_count  
blocked_activity_count  
document_count  
degraded_document_count  
open_risk_count  
governance_status  
epistemic_status  
next_deadline_at

Essa view deve alimentar topo do cockpit, contexto persistente e overview.

---

## 11.4 Inspect View Model

object_id  
object_type  
title  
primary_status  
secondary_status  
cycle_label  
context_summary  
content_summary  
evidence_summary  
governance_summary  
risk_summary  
last_change_at

Esta view serve diretamente à aba/painel de inspeção.

---

# 12. Regras de derivação

O sistema não deve depender só de estados digitados manualmente.

Alguns estados devem ser derivados.

## Exemplo 1 — atividade bloqueada

Uma activity é `blocked` se:

- seu estado explícito for `blocked`; ou
    
- existir edge `requires` para documento com `trust_state != trusted`; ou
    
- existir risk crítico aberto ligado a ela.
    

## Exemplo 2 — ciclo degradado

Um cycle entra em `integrity_state = degraded` se:

- houver activity bloqueada crítica; ou
    
- documento essencial com drift confirmado; ou
    
- governance status contested/expired em objeto central.
    

## Exemplo 3 — risco sistêmico

`systemic risk` emerge se:

- mesmo ciclo reúne bloqueio + drift + deadline iminente; ou
    
- há múltiplos edges `blocks` entre ciclos conectados.
    

Essas regras podem começar simples e crescer depois.

---

# 13. Compatibilidade com implementação atual do Nexus

Este spec não deve exigir que você abandone o modelo atual imediatamente.

Estratégia correta:

## Fase 1

Manter tabelas/estruturas atuais e introduzir projeções compatíveis.

## Fase 2

Adicionar camadas explícitas:

- institutional objects
    
- institutional edges
    
- institutional events
    

## Fase 3

Introduzir engine de derivação e views ricas.

## Fase 4

Suportar projeção gráfica avançada, replay temporal e raciocínio multi-ciclo.

Ou seja:  
este spec é alvo estrutural, não refactor destrutivo imediato.

---

# 14. Regras de implementação prudente

## Deve fazer agora

- unificar ids estáveis
    
- separar melhor objetos e relações
    
- tratar eventos como memória institucional
    
- criar views de projeção para UI
    
- explicitar estados epistêmicos e de governança
    

## Não precisa fazer agora

- banco de grafos dedicado
    
- inferência probabilística sofisticada
    
- simulação temporal completa
    
- motor causal avançado
    
- algoritmo de layout inteligente
    

---

# 15. Anti-patterns proibidos

- usar `cycle` só como tag de agrupamento
    
- tratar documento como blob sem estado epistêmico
    
- tratar risco como badge visual
    
- tratar audit como log plano
    
- esconder governança em metadata irrelevante
    
- desenhar grafo sem semântica operacional
    
- misturar id técnico e label humano
    
- deixar UI depender diretamente de tabelas brutas
    

---

# 16. Teste de validade do modelo

O modelo está correto quando permite responder, sem gambiarra conceitual:

- qual ciclo está mais frágil?
    
- qual atividade está bloqueada por evidência?
    
- que documento invalida esta decisão?
    
- que risco emergiu desta mudança?
    
- quem autorizou este estado?
    
- o que mudou institucionalmente nas últimas 24h?
    
- como este ciclo se conecta aos demais?
    
- quais eventos explicam o estado atual?
    

Se não responde isso, ainda não é o modelo do Nexus.

---

# 17. Forma física recomendada no repositório

Eu recomendo que isso vire, no mínimo, quatro artefatos separados depois:

1. `GRAPH_DATA_MODEL_SPEC.md`
    
2. `GRAPH_EDGE_SEMANTICS.md`
    
3. `INSTITUTIONAL_EVENT_MODEL.md`
    
4. `STATE_DERIVATION_RULES.md`
    

Porque este conteúdo é denso demais para ficar saudável num documento único por muito tempo.