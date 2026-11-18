# Contributing

Thanks for wanting to improve Orquestra. Contributions of domain skills, specialized reviewers, fixes, and documentation are welcome.

## Before you start

- Read [docs/theory.md](docs/theory.md) (the why behind the rules) and [docs/extending.md](docs/extending.md) (templates and lessons).
- For big changes (new skill, change to the workflow), open an issue first to align.

## Running locally

```bash
git clone https://github.com/andradevander/orquestra.git
cd orquestra
claude plugin validate .

# test in a throwaway project
mkdir -p /tmp/orq-test && cd /tmp/orq-test && git init
echo '{"name":"test","scripts":{"test":"echo ok"}}' > package.json
claude --plugin-dir /path/to/orquestra
```

## Conventions

- **Language:** English for all plugin content.
- **Generic:** no file names, components, or rules from a specific project. That is project memory, not plugin content.
- **Lean SKILL.md:** up to ~120 lines; details go in `references/`.
- **Templates embedded** in the SKILL.md of the command that uses them (`## Templates` section).
- **Agents with a short, fixed output contract** and minimal tools.
- **Every loop has a limit** and a defined exit ("stop and ask").
- File and folder names in kebab-case.

## PR checklist

- [ ] `claude plugin validate .` passes
- [ ] I tested the changed command or skill in a throwaway project and checked the **generated files**
- [ ] Nothing specific to a project
- [ ] Cross-references updated (README, docs, other skills that cite the changed one)
- [ ] `CHANGELOG.md` updated
- [ ] Version in `.claude-plugin/plugin.json` bumped if the change affects users (SemVer: MAJOR breaks workflow or format; MINOR adds; PATCH fixes)

## Reporting problems

See [docs/troubleshooting.md](docs/troubleshooting.md#reporting-an-issue).
