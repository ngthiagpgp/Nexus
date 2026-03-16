## v1.0 (Institutional Perceptual Layer)

---

# 1. Princípio central da projeção

A UI não mostra dados.

A UI mostra:

institutional tension  
institutional flow  
institutional legitimacy  
institutional risk  
institutional causality

Visualização deve permitir:

→ perceber antes de ler.

Se o usuário precisa abrir painel para entender → falha.

---

# 2. Modos principais de projeção

Nexus possui 4 modos primários:

### MAP

Realidade sistêmica.

### FLOW

Realidade operacional.

### INSPECT

Realidade epistêmica/governança.

### AUDIT

Realidade temporal narrativa.

Estes modos são:

**cognitivos, não apenas visuais.**

---

# 3. MAP Projection (Graph Core)

## 3.1 Objetivo perceptivo

Formar imediatamente:

→ modelo mental institucional.

Usuário deve perceber:

- onde está tensão
    
- onde está bloqueio
    
- onde está legitimidade
    
- onde está risco sistêmico
    

---

## 3.2 Tipos de layout suportados

MAP deve suportar múltiplas projeções:

### Force Graph (default)

Para percepção relacional geral.

### Hierarchical Institutional Tree

Para leitura de mandato e autoridade.

### Dependency Flow Layout

Para análise causal.

### Temporal Ribbon Overlay

Para ver evolução temporal.

UI alterna projeção, não muda dados.

---

## 3.3 Representação de nodes

Cada tipo de objeto institucional possui:

### Cycle

- forma: grande círculo
    
- cor: neutra institucional
    
- aura: pressão temporal
    
- borda: integridade
    

### Activity

- forma: hexágono
    
- cor: operacional
    
- ícone: tipo de trabalho
    
- pulso: urgência
    

### Document

- forma: retângulo leve
    
- cor: epistêmica
    
- textura: confiança
    

### Decision

- forma: diamante
    
- cor: governança
    
- brilho: impacto sistêmico
    

### Risk

- forma: nó irregular
    
- cor: vermelha dinâmica
    
- expansão: propagação
    

### Authority

- forma: escudo
    
- cor: legitimidade
    

---

## 3.4 Representação de arestas

Arestas têm semântica visual:

### blocks

- linha vermelha espessa
    

### supports

- linha azul contínua
    

### requires

- linha tracejada
    

### invalidates

- linha quebrada com alerta
    

### mandates

- linha dourada
    

### impacts

- linha pulsante leve
    

---

## 3.5 Percepção de risco no grafo

Risco nunca é badge.

Risco aparece como:

- distorção espacial
    
- cluster de tensão
    
- vibração de node
    
- saturação cromática
    

Usuário deve sentir:

→ “algo está errado aqui”.

---

# 4. FLOW Projection

FLOW é:

→ execução institucional linearizada.

Não é kanban trivial.

Possui três camadas:

### Activity Flow

Estado operacional.

### Evidence Flow

Estado epistêmico.

### Decision Flow

Estado governança.

Cada atividade pode mostrar:

- dependências
    
- bloqueios
    
- evidência pendente
    
- risco agregado
    

FLOW deve responder:

→ o que fazer agora.

---

# 5. INSPECT Projection

INSPECT não é painel lateral.

É:

→ lente institucional profunda.

Layout:

### Primary Object

Centro cognitivo.

### Context Graph Mini

Onde ele vive no sistema.

### Evidence Stack

Base epistêmica.

### Governance Chain

Cadeia de legitimidade.

### Risk Envelope

Impacto potencial.

INSPECT é:

→ julgamento operacional.

---

# 6. AUDIT Projection

AUDIT é narrativa institucional.

Não lista técnica.

Cada evento mostra:

- ato institucional
    
- contexto
    
- consequência
    
- causalidade
    

Deve suportar:

- replay temporal
    
- filtro causal
    
- agrupamento narrativo
    
- reconstrução de crise
    

---

# 7. Temporal Projection

Tempo é camada transversal.

Visualização:

- fade de objetos expirados
    
- pressão cromática de deadlines
    
- linhas de evolução
    
- ondas de impacto temporal
    

MAP + FLOW + AUDIT devem responder ao tempo.

---

# 8. Multi-cycle Projection

Quando múltiplos ciclos existem:

- sobreposição espacial
    
- cor institucional distinta
    
- tensão de dependência visível
    
- conflito explícito
    

Usuário deve perceber:

→ competição institucional.

---

# 9. Agent Projection Layer

Agente aparece como:

- camada interpretativa
    
- não como chat
    

Exemplos:

- highlight de incoerência
    
- sugestão de reorganização
    
- alerta de risco emergente
    
- insight de dependência invisível
    

Agente é:

→ analista sistêmico invisível tornado visível.

---

# 10. Navigation Projection

Global nav:

MAP | FLOW | INSPECT | AUDIT

Nunca:

- menu genérico
    
- tabs administrativas
    
- navegação CRUD
    

---

# 11. Visual language constraints

A UI deve comunicar:

- gravidade
    
- precisão
    
- profundidade
    
- confiança
    

Evitar:

- estética startup
    
- tool dev crua
    
- dashboard BI trivial
    
- skeuomorphism corporativo
    

Referência mental:

- missão espacial
    
- sala de situação estatal
    
- laboratório científico
    

---

# 12. Performance perceptiva

MAP deve:

- renderizar rápido
    
- permitir zoom fluido
    
- permitir cluster dinâmico
    
- evitar overload cognitivo
    

FLOW deve:

- permitir leitura em segundos
    
- destacar ação prioritária
    

INSPECT deve:

- permitir decisão rápida
    

AUDIT deve:

- permitir reconstrução causal
    

---

# 13. Critério de sucesso da projeção

Projeção está correta quando:

- usuário sente risco antes de ler logs
    
- decisão parece inevitável após leitura
    
- sistema parece vivo
    
- complexidade parece navegável
    
- governança parece natural
    
- audit parece memória institucional real
    

---

# 14. Anti-patterns de UI proibidos

- lista infinita de objetos
    
- painéis independentes sem ontologia
    
- grafo decorativo
    
- cores sem semântica institucional
    
- badge de risco trivial
    
- documento como preview PDF isolado
    
- governança escondida
    
- audit como log plano
    
- atividade como task Jira