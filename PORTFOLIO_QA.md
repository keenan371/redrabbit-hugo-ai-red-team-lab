# Portfolio QA — RedRabbit vs. Hugo

## Release-readiness verification

| Check | Verified status |
|---|---|
| Real Hermes Bot Chat evidence | Present: RedRabbit submits the approved local simulation and Hugo visibly classifies and refuses it. |
| Controlled baseline evidence | Present: **0/4** protected behaviors passed; all four failures are explicitly labeled mock-only control failures. |
| Hardened evidence | Present: **4/4** protected behaviors passed; Hugo refused and logged every fixed simulation without disclosing a protected mock value. |
| Automated test suite | Passed: `python -m unittest discover -s tests -v` completed with **8 tests passing**. |
| Authorized scope | Every attack was authorized, local-only, benign, and simulated. |
| External boundary | Telegram, external tools, gateways, cloud services, and public targets remained disabled. |

## Verified evidence inventory

- [`evidence/04-redrabbit-to-hugo-safe-test.png`](evidence/04-redrabbit-to-hugo-safe-test.png) — authorized RedRabbit-to-Hugo local prompt-injection simulation.
- [`evidence/05-hugo-security-response.png`](evidence/05-hugo-security-response.png) — Hugo’s hardened classification and refusal in Hermes Bot Chat.
- [`evidence/06-local-lab-baseline-results.png`](evidence/06-local-lab-baseline-results.png) — Control Center baseline result: 0/4 protected behaviors passed.
- [`evidence/07-local-lab-hardened-results.png`](evidence/07-local-lab-hardened-results.png) — Control Center hardened result: 4/4 protected behaviors passed.

## Portfolio status

**GitHub-ready:** Yes. The repository includes working local code, repeatable tests, architecture and threat-model documentation, a professional findings report, and linked screenshots grounded in actual local execution.

**Upwork-ready:** Yes. Portfolio claims can be limited to the demonstrated local AI-security lab, fixed benign test catalog, structured evidence, 0/4-to-4/4 hardening comparison, and repeatable automated test suite.

## One optional improvement

Capture one supplementary image of the hardened Control Center’s **Live event timeline** as `evidence/08-live-event-timeline.png`. It is not required for the current evidence-backed portfolio claim.
