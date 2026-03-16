### Objetivo do teste

Validar se o Nexus, no estado atual, é:

- instalável sem apoio técnico intenso;
    
- compreensível como produto;
    
- utilizável no fluxo principal;
    
- confiável nas ações centrais de supervisão e operação.
    

### Regra do teste

Durante o teste, anote o que aconteceu de fato, não a solução que você imaginou.  
O que importa é:

- onde travou;
    
- onde confundiu;
    
- onde pareceu útil;
    
- o que parecia quebrado;
    
- o que parecia excessivamente técnico.
    

### Cenário do teste

Use o fluxo canônico atual:

1. instalar o projeto;
    
2. inicializar workspace;
    
3. rodar `demo-seed`;
    
4. subir com `serve`;
    
5. abrir cockpit;
    
6. navegar por ciclo, atividade e documento;
    
7. mudar status de uma atividade;
    
8. mudar status de um documento;
    
9. verificar integridade/reconcile de um documento;
    
10. consultar audit trail.
    

### Escala sugerida

Use esta escala quando necessário:

- 1 = muito ruim / impossível
    
- 2 = ruim / travado
    
- 3 = aceitável com esforço
    
- 4 = bom
    
- 5 = muito bom / fluido
    

---

# Formulário de teste humano do Nexus

## 1. Contexto do teste

**Data do teste:**  14/03/2026
[preencher]

**Ambiente:**  Windows 11 
[ex.: Windows 11 / terminal / Python X.Y]

**Você já conhecia o Nexus antes?**  
[ X] Sim  
[ ] Não  
[ ] Parcialmente

**Você seguiu o README / TESTING_GUIDE?**  
[ ] Sim  
[X ] Parcialmente  
[ ] Não

---

## 2. Instalação e setup

### 2.1 Instalação

**Conseguiu instalar o projeto?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**Comando usado:**  
[preencher]

**Houve erro ou confusão?**  
sim, ele criou uma pasta nova e na hora de inicializar tive que criar novo terminal dentro da pasta

**Nota da instalação (1–5):**  
tudo certo, so essa quesstao de instalar no terminal em uma pasta e entrar no terminal na pasta criarda para inicializar

### 2.2 Inicialização do workspace

**Conseguiu rodar `init`?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**Observações:**  

**Nota do init (1–5):**  

### 2.3 Demo seed

**Conseguiu rodar `demo-seed`?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**Observações:**  
tentei abrir o painel antes da demo, vi que ele funciona, mas tava vazio. entao percebi que esqueci de rodar a demo
**O dataset gerado pareceu útil para teste?**  
[ ] Sim  
[ X] Parcialmente  
[ ] Não

**Nota do demo-seed (1–5):**  
consegui ver a atividades mas demorei para perceber como faz para mudar o status delas, demorei para entender o que e Cycle tive uma expectativa de conseguir ter observabilidade sobre o db, e as relacoes,  com grafos, mas acho que eles ainda nao estao la. e o acho que  o view do documento no canto inferio direito e dificil de ler por necessitar de scroll down e ficar no canto inferior da tela
### 2.4 Serve

**Conseguiu rodar `serve`?**  
[X] Sim  
[ ] Parcialmente  
[ ] Não

**Observações:**  
[preencher]

**Nota do serve (1–5):**  
[preencher]

---

## 3. Primeira impressão do produto

### 3.1 Cockpit

**O cockpit carregou corretamente?**  
[X ] Sim  
[ ] Parcialmente  
[ ] Não

**A tela inicial passa sensação de sistema pronto ou frágil?**  
[ ] Pronto  
[ ] Intermediário  
[ X] Frágil

**O loading/readiness ficou claro?**  
[X ] Sim  
[ ] Parcialmente  
[ ] Não

**Observações sobre primeira impressão:**  
consegui ver a atividades mas demorei para perceber como faz para mudar o status delas, demorei para entender o que e Cycle tive uma expectativa de conseguir ter observabilidade sobre o db, e as relacoes,  com grafos, mas acho que eles ainda nao estao la. e o acho que  o view do documento no canto inferio direito e dificil de ler por necessitar de scroll down e ficar no canto inferior da tela

**Nota da primeira impressão (1–5):**  
[preencher]

---

## 4. Navegação e compreensão

### 4.1 Estrutura geral

**Você entendeu rapidamente o que está vendo?**  
[ ] Sim  
[ X] Parcialmente  
[ ] Não

**A organização entre cycles, activities e documents fez sentido?**  
[ ] Sim  
[ ] Parcialmente  
[X ] Não

**O eixo principal do produto pareceu claro?**  
[ ] Sim  
[ ] Parcialmente  
[X ] Não

**O que pareceu mais confuso na navegação?**  
o que e o que, muitos nomes em ingles, tela muito verticalizada.  Recent Audit

**Nota da navegação (1–5):**  
[preencher]

---

## 5. Fluxo principal de uso

### 5.1 Cycle -> Activity -> Document

**Conseguiu navegar do ciclo para atividades e documentos relacionados?**  
[X ] Sim  
[ ] Parcialmente  
[ ] Não

**Esse fluxo pareceu natural?**  
[ ] Sim  
[ X] Parcialmente  
[ ] Não

**Onde travou ou hesitou?**  
demorei para perceber onde ficava o documento, onde selecionava a atividade e onde mudava o status
**Nota do fluxo principal (1–5):**  
[preencher]

---

## 6. Operações

### 6.1 Atualização de status de activity

**Conseguiu alterar o status de uma atividade?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**A ação pareceu segura e compreensível?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**O resultado ficou visível imediatamente?**  
[X] Sim  
[ ] Parcialmente  
[ ] Não

**Observações:**  
[preencher]

**Nota da operação em activity (1–5):**  
[preencher]

### 6.2 Lifecycle de documento

**Conseguiu alterar o status de um documento?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**As regras de transição pareceram compreensíveis?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**Observações:**  
[preencher]

**Nota da operação em document (1–5):**  
[preencher]

### 6.3 Integridade / reconcile

**Conseguiu localizar e entender a função de reconcile?**  
[ ] Sim  
[ ] Parcialmente  
[ X] Não

**A finalidade da reconciliação pareceu clara?**  
[ ] Sim  
[ ] Parcialmente  
[X ] Não

**O resultado da reconciliação ficou claro?**  
[ ] Sim  
[ ] Parcialmente  
[X] Não

**Observações:**  
[preencher]

**Nota de integridade/reconcile (1–5):**  
[preencher]

### 6.4 Audit trail

**Conseguiu ver o audit trail?**  
[ X] Sim  
[ ] Parcialmente  
[ ] Não

**O audit trail pareceu útil para entender o que aconteceu?**  
[ ] Sim  
[ X] Parcialmente  
[ ] Não

**Observações:**  
muita informacao visual para pouca importancia da informacao

**Nota do audit trail (1–5):**  
[preencher]

---

## 7. Problemas encontrados

### 7.1 Quebras reais

Liste aqui comportamentos que pareceram realmente quebrados.

1. a mudar o estado a tela pisca. e altera posicao relativa dos objetos
    
2. [preencher]
    
3. [preencher]
    

### 7.2 Fricções

Liste aqui coisas que funcionaram, mas com atrito.

1. no a navegacao nao parece intuitiva
    
2. [preencher]
    
3. [preencher]
    

### 7.3 Coisas confusas

Liste aqui o que não estava quebrado, mas exigiu esforço excessivo para entender.

1. [preencher]
    
2. [preencher]
    
3. [preencher]
    

---

## 8. Percepção de valor

**Você entendeu para que o Nexus serve?**  
[ ] Sim  
[ X ] Parcialmente  
[ ] Não

**Você usaria isso para trabalho real seu?**  
[ ] Sim  
[ X] Talvez  
[ ] Não

**O que pareceu mais valioso?**  
nao testei com um agente, mas se ele usar isso acho que vou ter mais rastreabilidade

**O que ainda parece inacabado demais para uso real?**  
sim, ele pode ser util para um agente, mas para mim ele prometia: 
- **Centraliza** entidades (projetos, pessoas, conceitos) e suas relações
- **Indexa** documentos operacionais (dailies, weeklies, monthlies) com estado (draft → approved)
- **Ingere** contexto externo (email, WhatsApp, Teams) de forma estruturada
- **Permite queries** rápidas sobre a estrutura cognitiva já montada
- **Reduz atrito** com inline editing, auto-save e visualização clara
  
  eu como usuario so vi lista de atividades que eu podia clicar para alterar, um documento que nao conseguia mexer e eu nao testei essas funcionalidades, e nem saberia como fazer isso sem um agente me acompanhando

**Nota geral de utilidade (1–5):**  
1

---

## 9. Veredito final

**Estado do MVP após este teste:**  
[ ] Pronto para uso inicial controlado  
[ ] Precisa de mais um passe curto de correção  
[ X] Ainda não está pronto para teste real

**Top 3 prioridades de melhoria:**

1. melhorar Ui para hymano. Principio de que o que o agente ve o humano tambem tem que ver
    
2. teste do MCP com um agente 
    
3. ingestao de dados em base real ou simulada
    

**Resumo livre do teste:**  
[preencher]

---

## 10. Resumo executivo para colar aqui

Quando terminar, cole também este bloco preenchido:

**Resumo executivo**

- Instalação/setup: [ médio]
    
- Navegação: [ ruim]
    
- Fluxo cycle -> activity -> document: [ médio ]
    
- Operações de status: [bom ]
    
- Integridade/reconcile: [ ruim]
    
- Audit trail: [bom ]
    
- Principais quebras: [atualizar informacao quebrar continuidade da interface: "pisca"]
    
- Principais fricções: [onde fica o que, hierarquia de informacoes nao intuitiva.]
    
- Veredito final: [mais util para agents que usuario]
