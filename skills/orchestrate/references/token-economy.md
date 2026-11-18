# Token economy: where the real cost is

## Where the spending comes from

1. **What comes back into the supervisor's context.** Every subagent result enters the Opus context and is re-read on every following turn. A 3,000-word report costs far more than it seems. **Short, fixed output contracts are the biggest saving.**
2. **Rework from a vague brief.** The subagent guesses, gets it wrong, and you pay twice.
3. **Reading large files in the main context.** Have the `scout` read and return pointers.
4. **LLM review before objective verification.** Build and test first.
5. **Fixed cost of each subagent** (system prompt and tools). Not worth it for tasks of 2–3 calls.

## Quick decision table

| Situation | Do |
|---|---|
| I know the file and the line | Directly |
| I need to find where something is, across several folders | 1–3 `scout` in parallel |
| Change in 1–2 files, already understood | Directly + 1 `goldfish-reviewer` if not trivial |
| Feature with several independent parts | `plan` → `implementer` per `[P]` task in parallel |
| Large or risky change (auth, money, data, migration) | Reviewer on Opus, or two reviewers with different focuses |
| Review an entire folder | Non-overlapping blocks + shared briefing |

## Sizing parallelism

- 2–5 simultaneous agents is the sweet spot for most tasks.
- More than that only pays off if the parts are truly independent and the return is short.
- Sweep with more than 5 directories: one `scout` per group of directories. With fewer, do it directly.

## Signs that you are spending too much

- You are re-reading agent results to understand what happened: the contracts are loose.
- Two agents returned the same information: the scopes overlap.
- A reviewer returned many P3: the brief did not say "material, not stylistic".
- You opened an agent for something a grep would solve.
