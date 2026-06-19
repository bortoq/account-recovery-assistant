# Demo Script

## Goal

Show that Account Recovery Assistant turns a stressful account lockout into a safe plan that uses official channels only.

## 5-Minute Flow

1. Open with the boundary:
   - local controlled alpha;
   - not affiliated with providers;
   - no guaranteed recovery;
   - no bypass, passwords, backup codes, or SMS codes.
2. Start the web wizard:
   ```bash
   PYTHONPATH=src python3 -m account_recovery_assistant --serve-web
   ```
3. Pick `Lost MFA device for a Google account`.
4. Answer as the rightful owner with backup codes available.
5. Show the plan:
   - next best action;
   - prepare-now evidence;
   - what can make this worse;
   - official links;
   - support message;
   - knowledge freshness.
6. Click:
   - Copy Support Message;
   - Download Markdown;
   - Print Plan.
7. Explain feedback is opt-in and memory-only in local alpha.

## CLI Fallback

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --format markdown examples/lost_mfa.json
```

## Questions To Ask Viewers

- Which recovery scenario should be covered next?
- Was the next best action specific enough?
- Which evidence item was confusing?
- Would this be useful as self-serve, concierge-assisted, or an MSP tool?
