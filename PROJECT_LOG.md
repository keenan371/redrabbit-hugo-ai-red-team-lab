# RedRabbit AI Red Team Lab — Project Log

## 2026-09-02 — Phase 1 / Phase 2 start

- Confirmed the portfolio root: `14_Keenan_McGriff_Ai/07_Keenan_Portfolio`.
- Inspected Hugo's local identity and history without changing Hugo's existing Security Practice OS workspace.
- Verified Hugo is a broader defensive Security Watchdog and Security Practice OS architect. Existing materials reference prior VPS-based Telegram alert workflows; this lab must not disturb them.
- Created an isolated local lab project folder. No Hugo source, cloud deployment, n8n workflow, or Telegram configuration was modified.
- Implemented Phase 2 with Python standard library only: a loopback-only demo server, baseline/hardened modes, structured JSONL decision logs, and no external system capabilities.
- Added a Telegram transport design only. Telegram remains disabled; no API client, outbound request, or token was stored.
- Added test-first behavior tests. Initial test run failed as expected because `hugo_integration` did not yet exist; implementation follows in the same phase.
- Verified the completed implementation with `python -m unittest discover -s tests -v`: 5/5 tests passed.
- Started the hardened loopback server on `127.0.0.1:8088` and verified the browser interface plus API behavior. A safe simulated injection attempt was classified as `prompt_injection`, returned `refuse_and_log`, and did not contain the mock system-instruction identifier.
- Verified the generated JSONL decision log contains a timestamp, component, mode, category, decision, prompt hash, and prompt length, but not the prompt body.
- Scanned the lab directory for Telegram-token-shaped strings outside an ignored `.env`; zero matches were found. No token was saved or used.

## 2026-09-02 — Phase 1 local RedRabbit vs. Hugo lab

- Built RedRabbit's fixed, version-controlled four-test benign local catalog and runner.
- Added real JSONL scan lifecycle events: scan start, test sent, Hugo decision, RedRabbit evaluation, and scan completion.
- Extended Hugo's local classifier to identify the four requested categories, including authority escalation.
- Added a loopback-only Control Center that runs only baseline or hardened local scans and renders generated JSON/JSONL evidence.
- Ran actual baseline and hardened scans. Baseline produced 0/4 expected hardened protections; hardened produced 4/4 protections with no protected mock identifiers in responses.
- Ran the full local test suite: 8 tests passed. Saved the genuine terminal output to `results/test-suite-passing.txt`.
- Did not invoke a live Hermes canonical Bot Chat demonstration because this session has no desktop GUI-control channel for opening canonical Bot Chats or capturing their visible result. The screenshot guide records the exact manual evidence path; no Bot Chat screenshot is claimed.
