# Nexus — Graph Physics Model Spec v1

## 1. Objetivo

Definir um modelo de física visual para o grafo do Nexus que transforme o `MAP` em um **instrumento de raciocínio operacional**, e não apenas em uma visualização relacional.

A física do grafo deve servir a quatro fins:

1. manter legibilidade estrutural;
    
2. preservar continuidade cognitiva ao focar, filtrar e mudar profundidade;
    
3. tornar tipos de relação perceptíveis;
    
4. permitir ao usuário ajustar densidade e espalhamento sem quebrar o campo.
    

Este modelo não busca simulação realista.  
Busca **estabilidade interpretativa**.

---

## 2. Princípios

### 2.1 Física como semântica

No Nexus, física não é só layout.  
Ela comunica importância, proximidade, dependência e pressão.

### 2.2 Continuidade antes de exatidão

Quando o usuário muda foco, profundidade ou filtros, o campo deve mudar com continuidade visual.  
É melhor preservar memória espacial do que recalcular o layout “ótimo” do zero.

### 2.3 Centro soberano

Quando há foco ativo, o nó focal deve atrair a organização do campo.  
O grafo deve parecer reordenado ao redor do foco, não simplesmente selecionado.

### 2.4 Ruído estrutural mínimo

A física deve evitar:

- aglomeração excessiva;
    
- nós muito afastados sem necessidade;
    
- cruzamento arbitrário de relações;
    
- oscilação constante.
    

### 2.5 Campo governável

O usuário deve poder modular o comportamento do campo sem entender teoria de grafos.

---

## 3. Entidades físicas do sistema

O motor deve operar sobre:

### Nós

- `cycle`
    
- `activity`
    
- `document`
    
- `evidence`
    
- `risk`
    
- `governance`
    
- `decision`
    
- `trace`
    
- `entity` genérica, se já existir na ontologia atual
    

### Relações

- `blocks`
    
- `supports`
    
- `requires`
    
- `impacts`
    
- `references`
    
- `owns`
    
- `governs`
    
- `validates`
    
- `contradicts`
    
- `escalates`
    

Nem toda relação precisa existir hoje no dado real; o modelo deve ser compatível com a expansão sem reescrita.

---

## 4. Forças básicas

O grafo deve usar quatro famílias de força.

### 4.1 Center Force

Força que puxa nós relevantes para o centro ativo do campo.

Uso:

- sempre existe em baixo nível no `GLOBAL FIELD`;
    
- aumenta fortemente no `FOCUSED FIELD`.
    

Função:

- garantir soberania do foco;
    
- evitar que o usuário se perca;
    
- reforçar a hierarquia de leitura.
    

### 4.2 Repulsion Force

Força que impede sobreposição e aglomeração visual.

Uso:

- aplicada entre todos os nós visíveis;
    
- intensidade modulada por densidade global.
    

Função:

- preservar legibilidade;
    
- abrir respiro no campo.
    

### 4.3 Link Force

Força que mantém proximidade entre nós ligados.

Uso:

- varia conforme tipo de relação;
    
- deve ser semanticamente ponderada.
    

Função:

- tornar vizinhanças coesas;
    
- permitir leitura de clusters.
    

### 4.4 Anchor / Stability Force

Força que impede reorganização caótica após pequenas mudanças.

Uso:

- aplicada como memória do layout anterior;
    
- mais forte quando usuário só altera filtros leves ou profundidade.
    

Função:

- preservar continuidade cognitiva;
    
- evitar “teletransporte” de nós.
    

---

## 5. Pesos semânticos por tipo de nó

Cada tipo ontológico deve ter massa e comportamento diferentes.

## 5.1 Cycle

**Massa:** muito alta  
**Repulsão:** média  
**Center affinity:** muito alta

Comportamento:

- age como âncora organizadora;
    
- resiste a deslocamentos bruscos;
    
- tende a permanecer central no campo local.
    

## 5.2 Activity

**Massa:** média-alta  
**Repulsão:** média  
**Link affinity:** alta

Comportamento:

- nós operacionais dinâmicos;
    
- agrupam-se em torno do cycle ou do objeto focal.
    

## 5.3 Document

**Massa:** média  
**Repulsão:** média-baixa  
**Link affinity:** média-alta

Comportamento:

- devem ficar próximos do que suportam, mas não dominar o campo;
    
- podem formar halo evidencial ao redor de activity/cycle.
    

## 5.4 Evidence

**Massa:** baixa-média  
**Repulsão:** baixa  
**Link affinity:** alta com documentos e decisões

Comportamento:

- deve ser puxada para os vínculos que ancora;
    
- não deve “explodir” o grafo.
    

## 5.5 Risk

**Massa:** alta  
**Repulsão:** média  
**Center affinity:** alta em modos `SIGNAL` e `PRESSURE`

Comportamento:

- altera o campo;
    
- deve tensionar visualmente o cluster que afeta.
    

## 5.6 Governance

**Massa:** média  
**Repulsão:** baixa-média  
**Link affinity:** média

Comportamento:

- normalmente periférico;
    
- aproxima-se do centro quando a leitura é normativa ou quando há escalada.
    

## 5.7 Decision

**Massa:** alta  
**Repulsão:** média  
**Link affinity:** alta com evidence, risk, governance, trace

Comportamento:

- ponto de inflexão;
    
- deve ficar perceptivelmente estruturado, não perdido no campo.
    

## 5.8 Trace

**Massa:** baixa  
**Repulsão:** baixa  
**Link affinity:** média

Comportamento:

- normalmente discreto;
    
- ganha relevância em `TRACE` mode.
    

---

## 6. Pesos semânticos por tipo de relação

Cada relação deve afetar distância e coesão do campo.

### 6.1 `blocks`

- **link force:** alta
    
- **link distance:** curta-média
    
- **efeito:** aproxima fortemente os nós, pois o bloqueio é vínculo operacional intenso
    

### 6.2 `supports`

- **link force:** média-alta
    
- **link distance:** média
    
- **efeito:** mantém proximidade, mas com respiro
    

### 6.3 `requires`

- **link force:** alta
    
- **link distance:** curta
    
- **efeito:** dependência forte; nós precisam ler como acoplados
    

### 6.4 `impacts`

- **link force:** média
    
- **link distance:** média-alta
    
- **efeito:** influência, não acoplamento absoluto
    

### 6.5 `references`

- **link force:** baixa-média
    
- **link distance:** longa
    
- **efeito:** conexão contextual; não deve comprimir o campo
    

### 6.6 `owns`

- **link force:** média
    
- **link distance:** média
    
- **efeito:** estrutura hierárquica estável
    

### 6.7 `governs`

- **link force:** média-alta
    
- **link distance:** média
    
- **efeito:** vínculo normativo que deve se tornar mais forte em `STRUCTURE` e `TRACE`
    

### 6.8 `validates`

- **link force:** média-alta
    
- **link distance:** curta-média
    
- **efeito:** aproxima evidência e decisão/documento
    

### 6.9 `contradicts`

- **link force:** média
    
- **link distance:** média
    
- **efeito:** vínculo tenso; pode usar leve repulsão visual secundária se houver suporte técnico
    

### 6.10 `escalates`

- **link force:** alta
    
- **link distance:** curta
    
- **efeito:** aproxima eventos/objetos em trajetória de pressão
    

---

## 7. Regimes físicos do grafo

## 7.1 Global Field

Modo macro.

Parâmetros:

- `center force`: baixa-média
    
- `repulsion`: média
    
- `link force`: média
    
- `stability`: alta
    

Objetivo:

- visão do todo;
    
- topologia estável;
    
- clusters legíveis;
    
- pouca oscilação.
    

## 7.2 Focused Field

Modo de investigação local.

Parâmetros:

- `center force`: alta
    
- `repulsion`: média-alta
    
- `link force`: alta no entorno focal
    
- `stability`: média-alta
    

Objetivo:

- recentrar o mundo no nó selecionado;
    
- abrir 1 hop legível;
    
- manter 2 hop contextual;
    
- ocultar ou enfraquecer o resto.
    

## 7.3 Signal Mode

Modo semântico.

Parâmetros:

- `risk` e `drift` ganham center affinity
    
- relações `impacts`, `blocks`, `contradicts`, `escalates` ganham força visual
    
- relações estruturais secundárias perdem visibilidade
    

Objetivo:

- tornar tensões perceptíveis.
    

## 7.4 Structure Mode

Parâmetros:

- `owns`, `requires`, `governs` ganham clareza
    
- center force moderada
    
- estabilidade alta
    

Objetivo:

- revelar arquitetura do mundo.
    

## 7.5 Pressure Mode

Parâmetros:

- `blocks`, `escalates`, `impacts` puxam clusters
    
- nodes de `risk` e `activity` ganham peso
    

Objetivo:

- mostrar onde o campo está comprimido.
    

## 7.6 Trace Mode

Parâmetros:

- `decision`, `trace`, `governance`, `references`, `validates` ganham peso
    
- layout enfatiza linhagem e causalidade
    

Objetivo:

- mostrar memória e consequência.
    

---

## 8. Profundidade e recorte

O motor deve suportar recorte por profundidade.

### `ALL`

Mostra toda topologia visível do escopo.

### `1 HOP`

Mostra só relações diretas do nó focal.

### `2 HOPS`

Mostra relações diretas e indiretas imediatas.

### `3 HOPS`

Mostra campo local ampliado.

### Regra

Mudança de profundidade não deve apenas aplicar fade.  
Deve recalcular a topologia visível e reorganizar o campo.

---

## 9. Controles de usuário

## 9.1 Controles básicos

Sempre acessíveis:

- `Depth`: All / 1 / 2 / 3
    
- `Density`: Compact / Balanced / Spread
    
- `Labels`: Sparse / Balanced / Full
    
- `Isolate`
    
- `Reset view`
    

## 9.2 Controles avançados

Colapsados por padrão:

- `Center force`
    
- `Repel force`
    
- `Link force`
    
- `Link distance`
    

### Regra de UX

Usuário comum opera presets.  
Usuário avançado pode mexer nos parâmetros.

---

## 10. Mapeamento dos presets de densidade

### Compact

- repulsion: baixa
    
- link force: alta
    
- link distance: curta
    
- center force: média-alta
    

Resultado:

- clusters mais fechados;
    
- leitura de concentração.
    

### Balanced

- repulsion: média
    
- link force: média
    
- link distance: média
    
- center force: média
    

Resultado:

- modo padrão recomendado.
    

### Spread

- repulsion: alta
    
- link force: média-baixa
    
- link distance: longa
    
- center force: média
    

Resultado:

- mais respiro;
    
- melhor para exploração.
    

---

## 11. Continuidade visual

Mudanças de:

- foco
    
- profundidade
    
- filtro
    
- densidade
    
- modo cognitivo
    

devem preservar:

- posição relativa do que permanecer;
    
- sensação de continuidade;
    
- memória espacial do usuário.
    

### Proibição

Não fazer hard redraw sempre que o estado muda.

---

## 12. Regras de estabilidade

O motor precisa ter comportamento estável.

### Deve evitar

- vibração permanente;
    
- oscilação infinita;
    
- “salto” de cluster sem motivo;
    
- recentragem agressiva demais.
    

### Deve permitir

- acomodação suave;
    
- reorganização gradual;
    
- foco claro.
    

### Estratégia

Depois de qualquer interação:

- animação curta de reequilíbrio;
    
- congelamento relativo após estabilização.
    

---

## 13. Regras de legibilidade

### O grafo está ruim se:

- o usuário vê “massa de conexões”;
    
- edges dominam mais que estruturas;
    
- o centro não é óbvio;
    
- um clique faz o mundo colapsar sem continuidade.
    

### O grafo está bom se:

- o usuário entende rapidamente onde está o centro;
    
- consegue entrar num problema local sem se perder;
    
- consegue voltar ao todo;
    
- sente que controla o campo.
    

---

## 14. Métricas qualitativas de aceitação

O modelo físico está aprovado se:

1. ao clicar num objeto, o usuário sente que entrou no seu mundo local;
    
2. ao mudar profundidade, percebe camadas relacionais, não caos;
    
3. ao filtrar relações, o campo muda estruturalmente, não só em destaque;
    
4. ao alternar entre `Signal`, `Structure`, `Pressure`, `Trace`, o campo muda de leitura sem perder identidade;
    
5. o usuário consegue usar o grafo para pensar, não só para olhar.
    

---

## 15. Implementação pragmática

Para esta fase, a implementação deve seguir esta ordem:

1. formalizar estados do campo:
    

- `global`
    
- `focused`
    
- `isolated`
    

2. implementar recenter + depth
    
3. implementar filtros reais por entidade e relação
    
4. implementar presets de densidade
    
5. expor controles avançados recolhidos
    
6. ajustar pesos semânticos por tipo de nó/relação
    

### Não fazer agora

- engine própria complexa
    
- persistência em banco dos controles
    
- layout 3D
    
- múltiplos grafos simultâneos
    

---

## 16. Resultado esperado

Depois desta spec, o `MAP` do Nexus deve deixar de ser:

- grafo premium central
    
- visualização sofisticada
    

e passar a ser:

> **campo operacional governável de raciocínio relacional**