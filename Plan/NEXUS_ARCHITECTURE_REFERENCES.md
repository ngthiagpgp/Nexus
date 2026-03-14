# NEXUS_ARCHITECTURE_REFERENCES
**Status:** Draft  
**Owner:** Thiago  
**Purpose:** Consolidar referências arquiteturais externas e explicitar a síntese adotada pelo Nexus para reduzir ambiguidade de implementação, orientar decisões de design e aumentar a eficiência do bootstrap.

---

## 1. Por que este documento existe

Os arquivos atuais do repositório já definem bem o **que** o Nexus quer ser no nível de produto e quais são alguns de seus contratos iniciais de operação:

- `NEXUS_MVP_SPEC.md`
- `NEXUS_MVP_API_SPEC.md`
- `NEXUS_MVP_CLI_SPEC.md`
- `NEXUS_MVP_SCHEMA.sql`

Entretanto, ainda há uma lacuna crítica entre:

1. a visão do produto;
2. os contratos locais de API/CLI/schema;
3. a topologia arquitetural de referência para orientar a implementação.

Sem essa ponte, o executor tende a improvisar arquitetura, especialmente em temas como:

- separação entre control plane e runtime;
- papel do banco local versus filesystem;
- papel do UI shell versus engine de execução;
- governança de tools/skills;
- sessões, memória, tracing e auditoria;
- ordem correta de build.

Este documento existe para preencher essa lacuna.

---

## 2. Função deste documento no bootstrap

Este arquivo tem cinco funções operacionais:

1. **Reduzir deriva de implementação**  
   Evitar que o Codex ou qualquer executor assuma uma arquitetura implícita não deliberada.

2. **Explicitar referências de alto valor**  
   Usar arquiteturas já testadas como referência, sem copiar cegamente seus produtos.

3. **Definir a síntese própria do Nexus**  
   O Nexus não é fork conceitual de OpenClaw nem simples app em framework de agentes.  
   É uma superestrutura local-first orientada a governança, memória operacional e execução assistida.

4. **Orientar sequencing de build**  
   Definir o que deve existir antes do quê.

5. **Servir como critério de revisão**  
   Todo módulo novo deve ser comparado contra esta arquitetura de referência.

---

## 3. Referências externas adotadas

### 3.1. OpenClaw como referência de sistema-produto

OpenClaw entra como referência principalmente para:

- **control plane local-first**;
- **modelo de sessões e canais**;
- **skills como camada operacional**;
- **multi-agent routing**;
- **always-on ops**;
- **painel de controle e supervisão**.

A contribuição do OpenClaw para o Nexus não é o runtime interno de raciocínio, mas a forma como um sistema de agente pode ser tratado como produto operacional vivo, com sessões, eventos, skills, superfícies de interação e governança de execução.

#### O que o Nexus herda conceitualmente do OpenClaw
- Separação entre assistente/executor e plano de controle.
- Sessões como unidade operacional de contexto.
- Tools/skills como superfície governada de capacidade.
- Painel de controle como componente central, e não acessório.
- Operação contínua, observabilidade e estado de sistema.

#### O que o Nexus não herda
- Não assume replicar a topologia de canais do OpenClaw.
- Não assume mensageria social/chat-first como núcleo do produto.
- Não assume que automação always-on é requisito do primeiro shipping.
- Não assume dependência estrutural de superfícies externas de mensagem.

#### Leitura arquitetural útil
A principal lição do OpenClaw é:
> o agente não é o sistema inteiro; ele é apenas um componente dentro de um plano de controle maior.

Referência:
- https://github.com/openclaw/openclaw

---

### 3.2. Mastra como referência de runtime composável

Mastra entra como referência principalmente para:

- **workflows estruturados**;
- **tools tipadas**;
- **memory design**;
- **tracing e observabilidade**;
- **evals**;
- **ambiente de inspeção/desenvolvimento**.

A contribuição do Mastra para o Nexus não é a UI final do produto, mas a disciplina de execução: agentes, tools, workflows, memória e rastreabilidade como componentes explícitos, e não implícitos.

#### O que o Nexus herda conceitualmente da Mastra
- Workflows como classe de primeira ordem.
- Tools com contratos definidos.
- Separação entre tipos de memória.
- Tracing e inspeção como parte do sistema, não como debug improvisado.
- Possibilidade de dev mode / studio mode.

#### O que o Nexus não herda
- Não assume adoção obrigatória de stack TypeScript end-to-end.
- Não assume que framework de agentes seja o centro da arquitetura total.
- Não assume que todo comportamento será modelado como workflow formal desde o início.
- Não assume Studio como produto final, apenas como referência de inspeção.

#### Leitura arquitetural útil
A principal lição da Mastra é:
> execução boa não é só inferência; é composição governada de passos, tools, memória e traces.

Referência:
- https://github.com/mastra-ai/mastra
- https://mastra.ai/docs

---

## 4. Síntese arquitetural adotada pelo Nexus

### 4.1. Princípio central

O Nexus será tratado como uma arquitetura em camadas, na qual o executor de IA é apenas uma parte do sistema.

A forma correta de pensar o Nexus é:

**Nexus = Control Plane + Runtime de Execução + Knowledge/State Fabric + Adapters + Cockpit UI**

Não é apenas:
- um chat com memória;
- uma IDE com prompts;
- um wrapper do Codex;
- um banco de notas com agente;
- um framework de agentes puro.

É uma superestrutura local-first para operar trabalho cognitivo, memória, projetos e execução assistida com governança explícita.

---

## 5. Camadas arquiteturais do Nexus

### 5.1. Camada A — Control Plane

Responsável por coordenar e supervisionar o sistema.

Inclui:
- registro de sessões;
- registro de projetos;
- estado do workspace;
- fila/estado de execuções;
- registro de skills/tools instaladas;
- políticas operacionais;
- eventos de sistema;
- auditoria operacional.

Pergunta que esta camada responde:
> o que está acontecendo no sistema agora, em qual contexto, com quais recursos, sob quais regras?

Inspirada principalmente em:
- OpenClaw

Não deve:
- executar lógica de domínio complexa diretamente;
- concentrar persistência documental;
- virar camada monolítica de tudo.

---

### 5.2. Camada B — Runtime de Execução

Responsável por executar tarefas cognitivas, workflows, tool calls e processos guiados.

Inclui:
- agentes;
- workflows;
- políticas de chamada de tools;
- tracing de execução;
- estratégias de memória de trabalho;
- protocolos de avaliação;
- adapters de execução.

Pergunta que esta camada responde:
> como uma tarefa é decomposta, executada, registrada e avaliada?

Inspirada principalmente em:
- Mastra

Não deve:
- ser o único repositório de verdade do sistema;
- carregar responsabilidade de UI;
- decidir sozinho regras de governança global.

---

### 5.3. Camada C — Knowledge and State Fabric

Responsável pelo substrato persistente do sistema.

Inclui:
- Markdown como camada documental viva;
- banco local como estado operacional estruturado;
- logs;
- auditoria;
- índices;
- hashes;
- relações;
- metadados;
- reconciliação entre documentos e estado.

Pergunta que esta camada responde:
> o que o sistema sabe, onde isso está, qual é o estado atual e como isso evoluiu?

Esta é a camada mais própria do Nexus.

Ela não é herdada diretamente nem de OpenClaw nem de Mastra.  
Ela é a síntese mais autoral do projeto.

---

### 5.4. Camada D — Adapters e Integrations

Responsável por conectar o Nexus a executores e sistemas externos.

Inclui:
- Codex CLI;
- VS Code;
- MCP servers;
- scripts locais;
- futuros conectores;
- possíveis subagentes especializados.

Pergunta que esta camada responde:
> por quais superfícies o Nexus age no mundo externo?

Não deve:
- definir a arquitetura central;
- ser a fonte de verdade do sistema;
- concentrar memória estrutural.

---

### 5.5. Camada E — Cockpit UI

Responsável pela supervisão, navegação e intervenção humana.

Inclui:
- painel de sessões;
- hub de memória;
- controle de projetos;
- status do sistema;
- tracing;
- auditoria;
- navegação documental;
- inspeção de tarefas e outputs.

Pergunta que esta camada responde:
> como o humano vê, supervisiona, corrige e orienta o sistema?

Inspirada parcialmente em:
- OpenClaw (control UI)
- Mastra Studio (inspeção/traces)

---

## 6. Princípios obrigatórios de design

### 6.1. Executor não é arquitetura
Codex, Claude Code, Gemini CLI ou qualquer outro executor são componentes substituíveis.  
O Nexus não pode ser desenhado como sinônimo do executor.

### 6.2. Banco e documento têm papéis diferentes
- Markdown = conteúdo vivo, legível, versionável e editável.
- Banco local = estado operacional, relações, índices, logs e queries estruturadas.

### 6.3. Sessão é unidade de operação
Toda ação relevante do sistema deve poder ser associada a uma sessão, contexto ou execução identificável.

### 6.4. Observabilidade não é opcional
Logs, traces, auditoria e estados de execução devem existir desde cedo.

### 6.5. Governança antes de automação
O Nexus deve primeiro saber registrar, explicar, isolar e revisar.  
Só depois deve automatizar agressivamente.

### 6.6. UI é instrumento de controle
A interface não deve ser só bonita ou conversacional.  
Ela deve servir para orientação, inspeção e intervenção.

### 6.7. Bootstrap deve reduzir escopo, não expandir sonho
Toda referência externa deve ser absorvida como princípio, não como convite à sobreconstrução imediata.

---

## 7. Tradução prática para o bootstrap atual

Os arquivos já existentes no repositório cobrem razoavelmente:

- produto mínimo;
- API inicial;
- CLI inicial;
- schema inicial.

Mas ainda precisam ser completados pelas decisões abaixo.

### 7.1. O que este documento adiciona
- referência arquitetural comparada;
- separação explícita entre control plane e runtime;
- noção de camadas;
- função da UI como cockpit;
- papel dos adapters;
- princípios de sequencing.

### 7.2. O que ainda precisa virar documento próprio
Este arquivo não substitui os seguintes artefatos, que ainda devem ser criados:

1. `NEXUS_SYSTEM_ARCHITECTURE.md`  
   arquitetura técnica do sistema, componentes, boundaries e fluxos.

2. `NEXUS_SYNC_RULES.md`  
   protocolo de reconciliação entre Markdown, banco local, logs e Git.

3. `NEXUS_IMPLEMENTATION_SEQUENCE.md`  
   ordem exata de build do MVP.

4. `NEXUS_RUNTIME_CONTRACT.md`  
   contratos do runtime: workflows, tools, tracing, políticas de execução.

5. `NEXUS_CONTROL_PLANE_SPEC.md`  
   contratos específicos do plano de controle.

---

## 8. Decisões explícitas para evitar deriva

### 8.1. Decisão: o Nexus não começa como app total
O primeiro shipping não precisa entregar a visão completa de produto-sistema.  
Precisa entregar um núcleo sólido.

### 8.2. Decisão: o primeiro núcleo é DB + docs + CLI + audit
O primeiro valor estrutural do Nexus está em:
- registrar estado;
- organizar conhecimento;
- manter documentação viva;
- permitir operações confiáveis;
- auditar alterações.

### 8.3. Decisão: control plane entra antes de automação avançada
Mesmo no MVP, o sistema deve já ter noção mínima de:
- sessão;
- execução;
- evento;
- status.

### 8.4. Decisão: runtime sofisticado entra em camadas
Workflows, memória diferenciada, tracing avançado e avaliações devem ser introduzidos progressivamente.

### 8.5. Decisão: UI rica não é pré-condição do núcleo
O cockpit é central como direção de produto, mas não deve atrasar a consolidação do núcleo operacional.

---

## 9. Ordem arquitetural recomendada de construção

### Fase 0 — Fundamento documental
Objetivo:
- consolidar specs;
- fechar arquitetura mínima;
- impedir improvisação.

Entregas:
- specs revisadas;
- arquitetura;
- sequência de implementação;
- regras de sync.

### Fase 1 — Núcleo local
Objetivo:
- criar o substrate confiável do sistema.

Entregas:
- init do workspace;
- banco local;
- schema;
- CRUD mínimo;
- auditoria;
- sessão mínima;
- persistência documental.

### Fase 2 — Control plane mínimo
Objetivo:
- tornar o sistema supervisionável.

Entregas:
- session registry;
- execution registry;
- status;
- event log;
- health checks.

### Fase 3 — Runtime inicial
Objetivo:
- tornar a execução modular e rastreável.

Entregas:
- runner de tasks;
- adapters para executor;
- tool contracts;
- traces básicos.

### Fase 4 — Cockpit básico
Objetivo:
- dar visibilidade e intervenção humana.

Entregas:
- status view;
- sessions view;
- documents view;
- audit view.

### Fase 5 — Expansão controlada
Objetivo:
- incorporar memória avançada, workflows, inbox e integrações.

---

## 10. Heurísticas de revisão para qualquer PR ou geração do Codex

Toda implementação proposta deve responder satisfatoriamente às perguntas abaixo:

1. Em que camada essa mudança vive?
2. Isso pertence ao control plane, runtime, state fabric, adapter ou UI?
3. Qual é a fonte de verdade dessa informação?
4. Como isso será auditado?
5. Como isso se relaciona a uma sessão ou execução?
6. Isso reduz ou aumenta a ambiguidade do sistema?
7. Isso antecipa complexidade cedo demais?
8. Isso foi inspirado por OpenClaw, por Mastra ou por uma necessidade própria do Nexus?
9. Existe risco de misturar cockpit com engine?
10. Existe risco de acoplamento excessivo ao executor atual?

Se essas perguntas não puderem ser respondidas com clareza, a implementação não está madura.

---

## 11. Síntese final

OpenClaw ensina ao Nexus como um sistema de agente pode viver como produto operacional.  
Mastra ensina ao Nexus como a execução pode ser tratada como composição governada.  
O Nexus, porém, não é cópia de nenhum dos dois.

Sua forma própria é:

- local-first;
- orientada a governança;
- baseada em documentos vivos + estado estruturado;
- supervisionável;
- executável por múltiplos adaptadores;
- centrada em cockpit e memória operacional.

A principal consequência arquitetural disso é simples:

> o bootstrap do Nexus deve começar pela clareza das camadas e dos contratos, não pela pressa de gerar interface ou automação.

---

## 12. Referências

- OpenClaw repository: https://github.com/openclaw/openclaw
- Mastra repository: https://github.com/mastra-ai/mastra
- Mastra documentation: https://mastra.ai/docs