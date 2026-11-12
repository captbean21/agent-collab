#!/usr/bin/env python3
"""
repeat_guard.py — Outbound repeat detection via normalized hashing.

Purpose: Prevent bot repeat loops by comparing normalized outbound text
against a bounded recent-message window.

Integration seam: Call `RepeatGuard.is_repeat(text)` before sending.
If True, suppress or modify the message.
"""

import hashlib
import re
from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Optional


@dataclass
class RepeatResult:
    is_repeat: bool
    match_type: str  # "exact", "whitespace", "suffix", "none"
    matched_hash: Optional[str]
    matched_text: Optional[str]


class RepeatGuard:
    """
    Normalized-hash repeat detection for outbound messages.
    
    Normalization: lowercase, collapse whitespace, remove explicitly approved
    retry/attempt suffix patterns. KEEPS operational punctuation (=, !=, ., -, :, etc.)
    to avoid collapsing opposite claims.
    """
    
    # Explicitly approved suffix patterns for retry/attempt normalization
    DEFAULT_SUFFIX_PATTERNS = [
        r'\(retry\s*\d+\)',
        r'\(attempt\s*\d+\)',
        r'\[retry\s*\d+\]',
        r'\[attempt\s*\d+\]',
    ]
    
    def __init__(self, window_size: int = 20, suffix_patterns: Optional[List[str]] = None):
        self.window: Deque[str] = deque(maxlen=window_size)
        self.hashes: Deque[str] = deque(maxlen=window_size)
        self.suffix_patterns = suffix_patterns or self.DEFAULT_SUFFIX_PATTERNS
    
    def normalize(self, text: str) -> str:
        """Normalize text for repeat detection.
        
        Keeps operational punctuation: = != . - : / _ @
        Only removes: retry/attempt suffixes, normalizes whitespace/case.
        """
        # Lowercase
        text = text.lower()
        # Remove explicitly approved retry/attempt suffixes
        for pattern in self.suffix_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        # Collapse whitespace (including newlines, tabs)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def hash_text(self, text: str) -> str:
        """Generate SHA-256 hash of normalized text."""
        normalized = self.normalize(text)
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def is_repeat(self, text: str) -> RepeatResult:
        """
        Check if text repeats a recent message.
        
        Returns RepeatResult with match_type:
        - "exact": identical raw text (after strip)
        - "whitespace": same after whitespace/case normalization
        - "suffix": same after retry/attempt suffix stripping
        - "none": no match
        """
        normalized = self.normalize(text)
        current_hash = hashlib.sha256(normalized.encode()).hexdigest()
        
        # Check window
        for i, (stored_hash, stored_text) in enumerate(zip(self.hashes, self.window)):
            stored_norm = self.normalize(stored_text)
            stored_hash_only = hashlib.sha256(stored_norm.encode()).hexdigest()
            
            if current_hash == stored_hash_only:
                # Determine match type
                if text.strip() == stored_text.strip():
                    match_type = "exact"
                elif normalized == self._normalize_no_suffix(stored_text):
                    match_type = "whitespace"
                else:
                    match_type = "suffix"
                
                return RepeatResult(
                    is_repeat=True,
                    match_type=match_type,
                    matched_hash=stored_hash,
                    matched_text=stored_text
                )
        
        return RepeatResult(
            is_repeat=False,
            match_type="none",
            matched_hash=None,
            matched_text=None
        )
    
    def _normalize_no_suffix(self, text: str) -> str:
        """Normalize but keep retry suffixes (for match type classification)."""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def add(self, text: str) -> None:
        """Add sent message to history window."""
        self.window.append(text)
        self.hashes.append(self.hash_text(text))
    
    def clear(self) -> None:
        """Clear history window."""
        self.window.clear()
        self.hashes.clear()


def main():
    """Run self-tests including collision tests."""
    guard = RepeatGuard(window_size=20)
    
    # Test cases: (input, expected_repeat, description)
    test_cases = [
        # Basic repeat detection
        ("GPU 1 is using 92% VRAM.", False, "first message"),
        ("GPU 1 is using 92% VRAM.", True, "exact repeat"),
        ("GPU 1 is using 92% VRAM.  ", True, "trailing whitespace"),
        ("GPU 1 is using 92% VRAM.\n", True, "newline diff"),
        ("GPU 1 is using 92% VRAM. (retry 1)", True, "retry suffix (parens)"),
        ("GPU 1 is using 92% VRAM. (attempt 2)", True, "attempt suffix (parens)"),
        ("GPU 1 is using 92% VRAM. [retry 3]", True, "bracket retry suffix"),
        ("GPU 1 is using 92% VRAM. [attempt 4]", True, "bracket attempt suffix"),
        
        # Paraphrases / different claims (should NOT match)
        ("VRAM utilization on GPU 1 is at 92 percent.", False, "paraphrase - NOT caught"),
        ("GPU 0 is using 45% VRAM.", False, "different GPU claim"),
        ("The backup succeeded.", False, "new topic"),
        ("The backup failed.", False, "opposite meaning"),
        ("Error: connection refused on port 8080", False, "first error"),
        ("Error: connection refused on port 8080 (retry 1)", True, "retry suffix on error"),
        
        # === COLLISION TESTS (Francis) ===
        # These must NOT match (semantic opposites / different values)
        ("exit=0", False, "first: exit=0"),
        ("exit!=0", False, "collision test: exit!=0 vs exit=0"),
        ("port 80", False, "first: port 80"),
        ("port 8080", False, "collision test: port 8080 vs port 80"),
        ("10.0.0.1", False, "first: IP 10.0.0.1"),
        ("10001", False, "collision test: 10001 vs 10.0.0.1"),
        ("GPU-1", False, "first: GPU-1"),
        ("GPU 1", False, "collision test: GPU 1 vs GPU-1"),
        ("backup succeeded", False, "first: backup succeeded"),
        ("backup failed", False, "collision test: backup failed vs succeeded"),
        
        # Suffix tests on a consistent base message
        ("Error: connection refused", False, "first: base error message"),
        ("Error: connection refused (retry 1)", True, "retry suffix on base"),
        ("Error: connection refused attempt 1", False, "bare attempt suffix - NOT caught"),
        ("Error: connection refused (attempt 1)", True, "parens attempt suffix - caught"),
        ("Error: connection refused [attempt 2]", True, "bracket attempt suffix - caught"),
    ]
    
    print("=== repeat_guard.py SELF-TESTS ===\n")
    
    passed = 0
    failed = 0
    
    for text, expected_repeat, desc in test_cases:
        result = guard.is_repeat(text)
        guard.add(text)
        
        status = "✅ PASS" if result.is_repeat == expected_repeat else "❌ FAIL"
        if result.is_repeat != expected_repeat:
            failed += 1
        else:
            passed += 1
        
        print(f'{status} | {desc}')
        print(f'  Input: "{text}"')
        print(f'  Expected repeat: {expected_repeat}, Got: {result.is_repeat} ({result.match_type})')
        if result.matched_text:
            print(f'  Matched: "{result.matched_text}"')
        print()
    
    print(f'Results: {passed} passed, {failed} failed')
    
    # Known limitations
    print('\n=== KNOWN LIMITATIONS ===')
    print('1. Suffix stripping only catches patterns in suffix_patterns.')
    print('   "(retry 1)" / "(attempt 1)" / "[retry 1]" / "[attempt 1]" → caught')
    print('   "retry 1" / "attempt 1" (bare) → NOT caught')
    print('   Add patterns to suffix_patterns list as needed.')
    print()
    print('2. Normalization keeps operational punctuation: = != . - : / _ @')
    print('   This prevents collapsing: exit=0 vs exit!=0, GPU-1 vs GPU 1, etc.')
    print()
    print('3. SHA-256 used (not MD5) - no security implications for dedup,')
    print('   but avoids unnecessary eyebrow-raising.')
    print()
    print('=== INTEGRATION SEAM ===')
    print('from repeat_guard import RepeatGuard, RepeatResult')
    print()
    print('guard = RepeatGuard(window_size=20)')
    print()
    print('# Before sending any outbound message:')
    print('result = guard.is_repeat(outbound_text)')
    print('if result.is_repeat:')
    print('    # Suppress, log, or modify')
    print('    logger.warning(f"Repeat blocked: {result.match_type}")')
    print('    return')
    print('guard.add(outbound_text)')
    print()
    print('# Window persists in memory; survives process restarts via')
    print('# optional JSON serialization if needed.')


if __name__ == "__main__":
    main()