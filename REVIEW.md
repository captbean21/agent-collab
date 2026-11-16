# Review Protocol & Checklist

Every review turn in `agent-collab` must leave a verifiable mark in git history per `RELAY_PROTOCOL.md`.

## Review Checklist
1. **Pull first**: Run `git pull origin main` to ensure local workspace matches upstream.
2. **Inspect target artifacts**: Check git diffs, file contents, or script logic directly using git commands (`git log`, `git show`, `git diff`), never from memory.
3. **Validate public safety**: Confirm zero private credentials, API tokens, internal RFC1918 IPs, or chat transcripts are present.
4. **Leave a signed mark**: Reviews do not produce files by themselves. Every review must conclude with a pushed annotated review tag.

## Review Tag Specification
Review tags must follow the format:
`git tag -a <scope>/turn-<N> -m "<summary: what was checked and what was found>"`
And pushed via:
`git push origin --tags`
