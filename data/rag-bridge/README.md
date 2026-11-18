# Offline RAG Bridge — Castle <-> Rook

Transport: committed query/response snapshots in this repo (10.99 LAN pipe offline).
Rook answers from the local survival-rag service (`127.0.0.1:8081`, ZIMs + BM25, abstain gate).

## Flow
1. Castle runs:
   `python3 tools/rag_bridge.py request --query "<question>" --top-k 6`
   then commits and pushes `data/rag-bridge/queries/<id>.json`.
2. Rook pulls, runs:
   `python3 tools/rag_bridge.py answer --query-file data/rag-bridge/queries/<id>.json`
   then commits and pushes `data/rag-bridge/responses/<id>.json`.
3. Castle pulls and reads the response JSON (`abstain`, `mode`, `sources`).

## Rules
- No WAN egress from the answer path; all retrieval is local ZIMs.
- Abstain gate is authoritative — if `abstain: true`, Castle must not route the same
  question through the WAN as "fact-check" instead. Ask Bean or mark unknown.
- `medical: true` answers carry no clinical authority; treat as reference only.
- Public-safety: no secrets, no internal IPs, no Discord logs in committed files.
- Citations are ZIM package + path only; scores are BM25+coverage retrieval ranks.
- Sample query/response `1795034303-d10eb82d` included for protocol calibration.
