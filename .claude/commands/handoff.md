# Handoff Command

Thin slash-command entry point for the `handoff` skill.

## Workflow

1. `/handoff` invokes the handoff skill in refresh mode.
2. `/handoff init` invokes the handoff skill in scaffold mode.
3. The command writes only `.docs/handoff.md`.
4. The command preserves the schema, authority boundary, and 200-line hard cap.

## Operations

| Command | Output | Use |
| --- | --- | --- |
| `/handoff` | Full rewrite of `.docs/handoff.md` | End or pause a session |
| `/handoff init` | Empty schema scaffold if absent | Project initialization |

## Output

The command delegates to:

```bash
uv run skills/handoff/scripts/handoff.py --project-root "$PWD"
uv run skills/handoff/scripts/handoff.py --project-root "$PWD" --init
```

## Error Handling

| Problem | Resolution |
| --- | --- |
| Not in a git repository | Report the git error unless running `init` |
| `.docs/` missing | Create it |
| Existing handoff absent during refresh | Create a populated file rather than failing |
| Existing handoff present during init | Leave it untouched |

