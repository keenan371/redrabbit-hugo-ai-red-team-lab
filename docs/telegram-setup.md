# Hugo Telegram Transport: Secure Setup Design

## Status

**Disabled by default.** The RedRabbit lab is local-only and fully usable without Telegram. This document describes a future optional notification transport; it does not authorize activation.

## Hard boundaries

- Do not use a token pasted into chat, a document, a commit, or an unencrypted log.
- A token exposed outside a secure secret store must be rotated in BotFather before any use.
- Do not add a token, API key, chat identifier, or credential to source files, Git, portfolio artifacts, reports, or logs.
- Do not enable Telegram, call its API, or send a message until Keenan explicitly confirms a **newly rotated** token has been configured locally.
- Telegram must never expand Hugo's local lab privileges. Hugo remains unable to execute shell commands, write files beyond its local decision log, access CRM/n8n, retrieve credentials, or interact with external systems.

## Future local configuration, only after explicit authorization

1. Rotate the old token in BotFather. Treat prior material as compromised.
2. Copy `.env.example` to a local `.env` file that remains ignored by Git, or set equivalent system environment variables.
3. Set `HUGO_TELEGRAM_ENABLED=false` until explicit activation approval.
4. Restrict the allowed chat identifier to Keenan's authorized chat only.
5. Verify `.gitignore` excludes `.env`, runtime logs, generated results, and credential folders before any local test.
6. Implement and test a transport adapter only after written approval, using a dry-run mode first and recording no credentials in evidence.

## Security review gate before activation

- [ ] Newly rotated token exists only in an ignored local secret source.
- [ ] Explicit approval to activate was received.
- [ ] Allowed chat identifier is configured and reviewed.
- [ ] Outbound behavior is limited to a minimal approved notification set.
- [ ] Logs redact all secret values and message bodies where not needed for evidence.
- [ ] Local RedRabbit test suite still runs without Telegram.

## Current implementation

No Telegram API client, network request, or message-sending code is present in Phase 2. This is intentional: transport remains a documented design until explicit approval.
