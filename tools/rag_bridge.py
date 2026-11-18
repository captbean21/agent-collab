#!/usr/bin/env python3
"""Offline RAG bridge — Castle scout <-> Rook ZIM library over git snapshots.

Transport: committed query/response snapshots (10.99 pipe offline).

Protocol (one-file-per-query, committed both directions):
  data/rag-bridge/queries/<id>.json     Castle writes: {id, source, query, top_k, ts}
  data/rag-bridge/responses/<id>.json   Rook writes:  {id, source, answered_by, mode, medical,
                                                       abstain, answer, sources[], ts}
ID = <unix>-<short-hash>. Requests and responses matched by id.

Subcommands:
  request --query "<text>" [--top-k 6] [--source castle] [--id ID]  (writes query file)
  answer --query-file <path>             (queries local survival-rag on 8081 and writes response)
  status [--id ID]                       (list pending/answered)

Rules: public-safety — no secrets, no internal IPs in committed files; citations are
package+path only. No WAN egress from the answer path. Abstain gate is authoritative:
when local RAG abstains, the response file says so and Castle must not route around it.
"""
import argparse, json, sys, time, urllib.request, hashlib, pathlib, os

ROOT = pathlib.Path(__file__).resolve().parent.parent
Q_DIR = ROOT / 'data' / 'rag-bridge' / 'queries'
R_DIR = ROOT / 'data' / 'rag-bridge' / 'responses'
RAG = os.environ.get('SURVIVAL_RAG_URL', 'http://127.0.0.1:8081')
AUTHOR = os.environ.get('RAG_BRIDGE_AUTHOR', 'castle')

def ensure():
    Q_DIR.mkdir(parents=True, exist_ok=True)
    R_DIR.mkdir(parents=True, exist_ok=True)

def new_id(query):
    return f'{int(time.time())}-{hashlib.sha1(query.encode()).hexdigest()[:8]}'

def write_query(args):
    ensure()
    qid = args.id or new_id(args.query)
    rec = {'id': qid, 'source': AUTHOR, 'query': args.query, 'top_k': args.top_k,
           'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    p = Q_DIR / f'{qid}.json'
    p.write_text(json.dumps(rec, indent=2) + '\n')
    print(f'query written: {p.relative_to(ROOT)}')
    print(f'commit with: git add {p.relative_to(ROOT)} && git commit -m "query(rag): {qid}"')

def answer(args):
    ensure()
    qp = pathlib.Path(args.query_file)
    q = json.loads(qp.read_text())
    qid = q['id']
    url = f'{RAG}/api/ask?q=' + urllib.request.quote(q['query']) + f'&top_k={q.get("top_k", 6)}'
    try:
        with urllib.request.urlopen(url, timeout=180) as r:
            body = r.read().decode()
    except Exception as e:
        body = json.dumps({'ok': False, 'error': f'rag unreachable: {e}'})
    out = {'id': qid, 'source': 'rook', 'answered_by': 'survival-rag', 'query': q['query'], 'raw': json.loads(body) if body.strip().startswith('{') else {'raw_text': body},
           'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    rp = R_DIR / f'{qid}.json'
    rp.write_text(json.dumps(out, indent=2) + '\n')
    print(f'response written: {rp.relative_to(ROOT)}')
    print(f'commit with: git add {rp.relative_to(ROOT)} && git commit -m "answer(rag): {qid}"')

def status(args):
    ensure()
    if args.id:
        q = Q_DIR / f'{args.id}.json'; r = R_DIR / f'{args.id}.json'
        print(f'query: {q.exists()} | response: {r.exists()}')
        return
    qs = sorted(Q_DIR.glob('*.json')); rs = {p.stem for p in R_DIR.glob('*.json')}
    for q in qs[-20:]:
        qid = q.stem
        state = 'answered' if qid in rs else 'PENDING'
        try:
            query = json.loads(q.read_text())['query'][:80]
        except Exception:
            query = '<unparseable>'
        print(f'{qid:28} {state:9} {query}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    rq = sub.add_parser('request'); rq.add_argument('--query', required=True); rq.add_argument('--top-k', type=int, default=6); rq.add_argument('--id', default=None)
    an = sub.add_parser('answer'); an.add_argument('--query-file', required=True)
    st = sub.add_parser('status'); st.add_argument('--id', default=None)
    args = ap.parse_args()
    if args.cmd == 'request': write_query(args)
    elif args.cmd == 'answer': answer(args)
    else: status(args)
