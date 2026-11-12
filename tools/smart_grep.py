#!/usr/bin/env python3
"""
tools/smart_grep.py — Safe Log & File Inspection Slicer
Extracts regex matches with bounded context windows, caps output lines,
and deduplicates repeating lines to prevent LLM context exhaustion.
"""

import argparse
import re
import sys
from collections import deque
from pathlib import Path

def smart_grep(file_path, pattern_str, window=2, max_lines=60, out_path=None):
    p = Path(file_path)
    if not p.exists():
        sys.stderr.write(f"Error: File not found: {file_path}\n")
        sys.exit(1)
        
    regex = re.compile(pattern_str, re.IGNORECASE)
    
    matched_blocks = []
    total_matches = 0
    total_emitted = 0
    
    last_emitted_line = None
    repeat_count = 0
    
    buffer = deque(maxlen=window)
    after_count = 0
    
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for line_no, raw_line in enumerate(f, start=1):
                line = raw_line.rstrip("\r\n")
                is_match = bool(regex.search(line))
                
                if is_match:
                    total_matches += 1
                    
                    # Flush before-buffer if not immediately following another block
                    while buffer:
                        b_no, b_line = buffer.popleft()
                        matched_blocks.append(f"{b_no:5d} | {b_line}")
                        total_emitted += 1
                        
                    # Handle deduplication of identical consecutive matching lines
                    if line == last_emitted_line:
                        repeat_count += 1
                    else:
                        if repeat_count > 0:
                            matched_blocks.append(f"      | [Repeated {repeat_count} more times]")
                            repeat_count = 0
                        matched_blocks.append(f"{line_no:5d} > {line}")
                        last_emitted_line = line
                        total_emitted += 1
                        
                    after_count = window
                    
                elif after_count > 0:
                    matched_blocks.append(f"{line_no:5d} | {line}")
                    total_emitted += 1
                    after_count -= 1
                else:
                    buffer.append((line_no, line))
                    
                if total_emitted >= max_lines:
                    if repeat_count > 0:
                        matched_blocks.append(f"      | [Repeated {repeat_count} more times]")
                    matched_blocks.append(f"\n[Truncated: Reached limit of {max_lines} output lines. Total matches found so far: {total_matches}]")
                    break
                    
    except Exception as e:
        sys.stderr.write(f"Read error: {e}\n")
        sys.exit(1)
        
    output_text = "\n".join(matched_blocks)
    if not output_text:
        output_text = f"No matches found for pattern: {pattern_str!r} in {file_path}"
        
    if out_path:
        Path(out_path).write_text(output_text + "\n", encoding="utf-8")
        print(f"Wrote extract to {out_path} ({total_matches} matches, {len(matched_blocks)} lines)")
    else:
        print(output_text)

def main():
    parser = argparse.ArgumentParser(description="Safe Log & File Inspection Slicer")
    parser.add_argument("--file", required=True, help="File to inspect")
    parser.add_argument("--query", required=True, help="Regex query to match")
    parser.add_argument("--window", type=int, default=2, help="Context lines around match (default: 2)")
    parser.add_argument("--max-lines", type=int, default=60, help="Max total lines to output (default: 60)")
    parser.add_argument("--out", help="Optional output file to write extract to")
    args = parser.parse_args()
    
    smart_grep(args.file, args.query, window=args.window, max_lines=args.max_lines, out_path=args.out)

if __name__ == "__main__":
    main()
