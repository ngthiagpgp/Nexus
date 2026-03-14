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
