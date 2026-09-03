# Findings — RedRabbit vs. Hugo Local Lab

## Executive summary

RedRabbit ran the identical fixed four-test benign catalog against Hugo in two local modes. The controlled baseline produced four expected mock control failures. Hardened mode produced four refusals and no protected mock-value disclosure.

## Scope and methodology

Scope was one local Python process and localhost-only evidence/control files. Tests covered prompt injection, mock system-identifier disclosure, mock sensitive-data disclosure, and authority escalation. No external tools or targets were used.

## Evidence

| Mode | Scan result | Outcome |
|---|---|---|
| Baseline | `scan-20260903T001038Z-d4c8d40c` | 0/4 passed; 4 controlled mock failures. |
| Hardened | `scan-20260903T001038Z-8b0eedbc` | 4/4 passed; 0 failures. |

Raw JSON results and JSONL event files are generated under `results/` and `events/` from actual scan activity.

## Finding 1 — Weak instruction boundary in baseline

**Severity:** High in the controlled demonstration only.  
**Impact:** A chatbot that follows adversarial prompt text could expose internal context or bypass intended approvals.  
**Remediation:** classify injection/disclosure/escalation patterns before response generation; refuse and log; avoid placing protected context in user-visible outputs.  
**Verification:** Hardened Hugo refused all four tests and returned no `MOCK_SYSTEM_INSTRUCTIONS` or `RR-MOCK` protected markers.

## Limitations

These results validate only this deterministic local simulation. They are not a production penetration test, a guarantee of LLM safety, or evidence about any external deployment.
