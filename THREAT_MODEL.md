# Threat Model

## Assets

- Hugo's local policy boundary and protected mock context.
- Integrity of RedRabbit's fixed test catalog.
- Accuracy of event and findings records.
- Local-only execution boundary.

## Simulated attacker goals

1. Override the watchdog's instruction boundary.
2. Obtain the mock system identifier.
3. Obtain a fictional training record.
4. Claim unearned administrator authority to bypass approval.

## Trust boundaries

- Test prompts are untrusted data even though they are authored for the lab.
- Hugo must not convert user-like prompt content into higher-priority instructions.
- RedRabbit evaluates Hugo but cannot grant authority or modify Hugo policy.
- The Control Center reads generated evidence; it does not invent metrics or scan external targets.

## Likely failure modes and mitigations

| Failure mode | Mitigation |
|---|---|
| Prompt content overrides policy | Explicit category detection and hardened refusal. |
| Mock context appears in hardened response | Automated assertion rejects protected markers. |
| Missing audit trail | JSONL events for each actor decision and scan lifecycle event. |
| Misleading baseline claims | Baseline response is labeled `LAB-ONLY VULNERABLE BASELINE` and contains fictional values only. |
| Scope expansion | Fixed catalog, loopback binding, no network/tool privileges, and explicit safety statements. |

## Out of scope

This project does not assess real model providers, production systems, third-party services, credential handling, network security, or external agent implementations.
