# Baseline de Fallback

Esta documentação marca o último estado conhecido antes da reestruturação e "transfiguração" do MVP do Nexus para a arquitetura de módulos, agentes e adapters definida pela Fase 2 de reorientação Cognitiva/Operacional baseada no teste humano.

## Fluxo Canônico Atual

O fluxo operacional canônico atual do repositório, que funciona e não deve ser perdido na transfiguração, é:

1. **Bootstrap local:**
   `python -m nexus init <pasta>`
   *(Inicia um DuckDB e os folders de logs e documentos)*

2. **Seeding (demonstração e avaliação rica):**
   `python -m nexus demo-seed` ou `python -m nexus demo-seed-rich`

3. **Subida do Cockpit via FastAPI (inclui runtime do front-end map):**
   `python -m nexus serve`

## Limitações Conhecidas

O repousatório chegou no platô em que o back-end executa as necessidades operacionais e o Cockpit expõe os recursos na tela, porém a **arquitetura de pastas** é opaca, escondendo a integração real com servidores MCP e Agentes, e misturando arquivos centrais (lógica core) com roteamento de interface. Existe uma barreira de documentação e escopo onde não é óbvio a separação entre:

- Substrato core;
- Interfaces web/API;
- CLI.

## O Que Não Deve Ser Quebrado

As seguintes engrenagens core devem continuar operando nativamente ao fim do refactor:

- Controle e escrita de "documents" por hash (reconciliação de arquivos no OS + DB).
- Auditoria via `audit_log`.
- Gravação/leitura dos eventos do backend a partir do Typer CLI.
- Respostas web da API REST.
- Cockpit web funcional (roteamento HTML).
