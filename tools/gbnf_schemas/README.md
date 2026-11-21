# GBNF Schemas for Tool Calls

Grammar-constrained decoding (GCD) schemas for our core tools. Guarantees syntactic conformance of tool call JSON.

## Schemas

| Schema | Tool | Purpose |
|--------|------|---------|
| `git.gbnf` | `git` | All git subcommands used in relay protocol |
| `exec.gbnf` | `exec` | Shell command execution with full parameter set |
| `peer_search.gbnf` | `peer_search` | Survival backend queries |
| `peer_survival.gbnf` | `peer_survival` | Survival backend status/telemetry |
| `tool_call.gbnf` | `dispatch_action` | Generic tool call wrapper |

## Validation

Test against llama.cpp constrained decoding:

```bash
# Validate grammar syntax
/opt/llama.cpp/build/bin/llama-cli --grammar tools/gbnf_schemas/git.gbnf -p "git " -n 1 --grammar-trigger "tool" 2>&1 | head -20

# Test git commit generation
/opt/llama.cpp/build/bin/llama-cli --grammar tools/gbnf_schemas/git.gbnf -p "git commit -m \"test commit\"" -n 1 2>&1 | head -20

# Test exec generation
/opt/llama.cpp/build/bin/llama-cli --grammar tools/gbnf_schemas/exec.gbnf -p 'exec {"title": "test", "command": "echo hello"}' -n 1 2>&1 | head -20
```

## Integration

When using llama.cpp for tool call generation:

```python
# In Python tool caller
GRAMMAR_DIR = Path("tools/gbnf_schemas")

def generate_tool_call(tool_name: str, prompt: str) -> str:
    grammar_file = GRAMMAR_DIR / f"{tool_name}.gbnf"
    if grammar_file.exists():
        return llama_cli_with_grammar(grammar_file, prompt)
    return llama_cli_without_grammar(prompt)
```

## Notes

- GBNF guarantees **syntactic conformance only** (per FrancisCuée)
- Does NOT guarantee correct tool choice, arguments, or semantic validity
- Schemas based on actual tool signatures in OpenClaw runtime
- Extend as new tools are added

## Research Basis

- arXiv 2305.13971: Grammar-constrained decoding for structured NLP tasks
- arXiv 2501.10868: JSONSchemaBench benchmark
- arXiv 2502.05111: 17.7x faster preprocessing algorithm