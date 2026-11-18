# Extending Orquestra

How to create new skills and agents that work well with the rest of the package.

## Plugin anatomy

```
.claude-plugin/plugin.json      manifest (name, version, author)
.claude-plugin/marketplace.json lets you install straight from GitHub
agents/<name>.md                subagents (frontmatter + system prompt)
skills/<name>/SKILL.md          skills and commands
skills/<name>/references/*.md   material loaded on demand
skills/<name>/scripts/*         executable verifiers
```

## Command skill × automatic skill

| Type | Frontmatter | Who triggers it | Examples |
|---|---|---|---|
| Command | `disable-model-invocation: true` | Only the user, via `/orquestra:<name>` | `specify`, `implement`, `review` |
| Automatic | without that line | Claude, when the `description` matches the subject | `orchestrate`, `responsive-ui`, `note` |

In an automatic skill, the **`description` is the trigger**. Write when to use it, with the phrases the user would say ("breaks on mobile", "note this"), and when **not** to use it. A description that is too broad makes the skill load for nothing and wastes tokens.

Commands receive the typed text in `$ARGUMENTS`. Use `argument-hint` to show the expected format.

## Lessons that already cost dearly (read before creating)

1. **Templates embedded in SKILL.md, not in a separate file.** Reading files from the plugin folder depends on permission. In some modes it is denied, and the model improvises the format. Put the template at the end of SKILL.md itself, in a `## Templates` section with a ` ````markdown ` block.
2. **A skill does not read another skill's folder.** To use another skill's content, tell it to load that skill with the Skill tool ("load the `orchestrate` skill with the Skill tool").
3. **Inside a command, domain skills don't fire on their own.** If the command can touch an area that has its own skill, explicitly say to load it.
4. **Plugin agents have a prefix.** In `subagent_type`, the name is `orquestra:scout`, not `scout`.
5. **Every rule has a limit.** Review loops, questions and attempts need a cap (e.g. "at most 3 rounds") and an exit ("stop and ask").

## Mold: domain skill

Use `skills/responsive-ui` as the model. A good domain skill has:

```
skills/<domain>/
  SKILL.md                 central rule + flow + "done" checklist
  references/patterns.md   solutions by type of problem, with before → after
  references/pitfalls.md   mistakes that cause regressions
  references/orchestration.md  (optional) how to split large scope among agents
  scripts/<verifier>       (optional, but very valuable) objective proof
```

Principles:

- **Testable central rule.** "Only add below the breakpoint" is verifiable. "Make a nice layout" is not.
- **Verifier script when possible.** A rule checked by a script is cheaper and more reliable than a rule that depends on review.
- **Short SKILL.md** (up to ~120 lines). Detail goes to `references/`, which is read only when needed.
- **Touchpoint with memory:** "project-specific pitfall → `/orquestra:note`; generic pitfall → suggestion for this skill".
- **Nothing project-specific.** File names, layout widths and components of a project go in that project's memory, not in the skill.

Domain skill ideas: accessibility, REST API, database migrations, front-end performance, i18n, endpoint security.

## Mold: worker agent

```markdown
---
name: <name-in-kebab-case>
description: <what it does + when to use + what it does NOT do>
tools: <minimum necessary>
model: haiku | sonnet | opus | inherit
color: <color>
---

You are <role>. <1 sentence on context: a supervisor planned and handed you X>.

## Rules
- <scope>, <what to never do>, <when to stop>

## Output (always in this format)
<short, fixed format>
```

What matters most:

- **Short, fixed output contract.** Everything the agent returns enters the supervisor's context and is re-read on every turn. This is the main token saving.
- **Minimal tools.** A reviewer doesn't need `Edit`. A locator doesn't need `Write`.
- **Model by type of reasoning:** Haiku for locating and mechanical transformation, Sonnet for executing and reviewing, Opus only for critical judgment.
- **Stop rule:** "if the same error appears twice, stop and report".

## Mold: clean-context reviewer

Copy `agents/goldfish-reviewer.md` and keep:

- `tools: Read, Grep, Glob` (read-only);
- `omitClaudeMd: true` (doesn't load the project's CLAUDE.md; requires Claude Code 2.1.271+);
- the binary contract: `[LGTM]` only with zero findings, otherwise the findings with severity.

Change only the "What to look for" section to your reviewer's focus (security, performance, accessibility…). In the brief, the supervisor passes the artifact and the criteria, **never its own conclusion**.

## Testing

```bash
# 1. structure and manifests
claude plugin validate .

# 2. load the local plugin in a session, without installing
cd /a/test/project
claude --plugin-dir /path/to/orquestra

# 3. non-interactive test of a command
claude -p --plugin-dir /path/to/orquestra --permission-mode acceptEdits \
  "/orquestra:init automated test, accept the proposed principles" < /dev/null
```

Always test in a throwaway project (`git init` in a temporary folder, with a minimal `package.json`). Check what it **wrote**, not just what it **said**. In earlier tests the model claimed to have followed the template and had not.
