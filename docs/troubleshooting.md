# Troubleshooting

## Recommended permissions

The commands ship with the templates embedded and don't depend on reading plugin files. The references (`patterns.md`, `pitfalls.md`, `briefing.md`) and `desktop_guard.py`, however, live in the plugin folder, outside your project. To avoid a permission prompt on every use, add this to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(~/.claude/plugins/**)",
      "Bash(python3 ~/.claude/plugins/*)"
    ]
  }
}
```

If you use the plugin from a local clone (`--plugin-dir` or a marketplace pointing to a folder), allow that path too.

## Common problems

### The `/orquestra:` commands don't show up
- Check that the plugin is installed and enabled: `/plugin` inside Claude Code.
- Restart the session after installing.
- Update the marketplace: `claude plugin marketplace update orquestra`.

### "I couldn't read the template" or the generated file doesn't follow the format
Current versions embed the templates in the command itself. Update the plugin. If the problem is with `references/` or `scripts/`, apply the [recommended permissions](#recommended-permissions).

### The reviewer seems to know the project or agrees too much
- Check the version: `claude --version` must be **2.1.271+** for `omitClaudeMd` to work. On old versions, the reviewer loads `CLAUDE.md` and loses the outside view.
- Check that the brief didn't include the supervisor's conclusion ("I think this is right"). The rule is to pass only the artifact and the criteria.

### "Clean-context review is not possible"
`review` requires the subagent tool. Without it, it stops on purpose, because reviewing in the same context doesn't have the same value. Check that the environment allows subagents.

### `desktop_guard` says "zero alerts", but the desktop changed
- If the changes were already committed, pass the base: `desktop_guard.py main -- <files>`. Without a base, it compares against `HEAD` and sees nothing.
- The guard is heuristic: it doesn't see new elements (wrappers, `lg:hidden` blocks) or the CSS cascade. Zero alerts doesn't excuse reading the diff and checking in the browser.

### The `responsive-ui` skill wasn't used on a layout change
Inside commands, domain skills only load when the command says so. The current commands say to load it when the change touches layout. Outside commands, mention it explicitly ("use the responsive-ui skill").

### The command worked on the wrong feature
The active feature is stored in `.orquestra/state.json`. Pass the feature as an argument (`/orquestra:implement 003-coupon`) or edit the file. It is local and each person has their own.

### The review says the diff is empty
The base recorded in `tasks.md` (or `HEAD`) already includes everything. Pass the base explicitly: `/orquestra:review main`.

### High token spend
- Use `/orquestra:quick` for small changes; the full feature flow is for features.
- Check that the agents are returning short outputs (each one's fixed format). If you customized an agent, keep the output contract.
- See `skills/orchestrate/references/token-economy.md`.

## Reporting an issue

Open an issue at <https://github.com/andradevander/orquestra/issues> with:
- Claude Code version (`claude --version`) and plugin version;
- the command used;
- what you expected and what happened (generated files help more than the response text);
- **no** sensitive data from your project.
