# Nexus MVP

Workspace inicial do Nexus MVP com artefatos de especificacao e planejamento.

## Estrutura atual

- `Plan/`: especificacoes do MVP, API, CLI, schema e artefatos visuais.

## Objetivo deste bootstrap

- tornar o workspace versionavel com `git`
- preparar publicacao em repositorio GitHub
- registrar um rastro minimo de mudancas estruturais

## Bootstrap local

Para expor o comando `nexus` localmente:

```bash
python -m pip install -e .
```

Para inicializar um workspace Nexus:

```bash
nexus init ./sandbox-workspace
```

Alternativamente, sem instalar o script:

```bash
python -m nexus init ./sandbox-workspace
```

Para inspecionar se o diretorio atual ja e um workspace Nexus:

```bash
python -m nexus status
```

Para criar e listar entidades no workspace atual:

```bash
python -m nexus entity create --name "Projeto X" --type project
python -m nexus entity list --type project
```

Para criar e listar documentos no workspace atual:

```bash
python -m nexus document create --type daily --title "Daily 2026-03-13"
python -m nexus document list --type daily
python -m nexus document show "Daily 2026-03-13"
```

Para criar e listar relacoes no workspace atual:

```bash
python -m nexus relation create --from "Projeto X" --to "Projeto Y" --type depende_de
python -m nexus relation list --from "Projeto X"
```

Para criar e listar atividades no workspace atual:

```bash
python -m nexus activity create --title "Finish report" --cycle-id cycle-daily-2026-03-13
python -m nexus activity list --cycle-id cycle-daily-2026-03-13
```

Para criar e listar ciclos no workspace atual:

```bash
python -m nexus cycle create --type daily --start 2026-03-13
python -m nexus cycle list --type daily
```

Para subir a API local read-only sobre um workspace Nexus:

```bash
cd ./sandbox-workspace
python -m uvicorn nexus.api:app --port 3000
```

Para abrir o cockpit minimo no navegador local:

```text
http://127.0.0.1:3000/
```

O cockpit atual e read-only e usa cycles como foco operacional principal, com inspeccao ligada a activities e documents.
