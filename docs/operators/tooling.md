# Operator Tooling

This page maps common operator questions to tools. Commands are examples; the important part is what each tool proves.

## Local System Health

```bash
tibet system doctor
tibet system walkthrough
```

Use this to check the local trust-system install and see the next operator steps.

What it proves:

- expected packages are present
- local directories/config exist
- the operator can inspect the stack

What it does not prove:

- a remote actor is trusted
- public federation is working
- policy allows an action

## Binding Ladder

When debugging tools, separate these layers:

```text
runtime_seen -> actor_bound -> transport_bound -> tool_bound -> route_allowed
```

| Layer | Meaning |
|---|---|
| runtime_seen | The process or session exists and can be observed. |
| actor_bound | The runtime has actor id, key, custodian or session proof. |
| transport_bound | Messages carry verifiable proof, not only a text claim. |
| tool_bound | The delegated tool, worker, connector or transport is visible as a bounded wrapper. |
| route_allowed | MUX permits the named surface and intent; otherwise it falls dark. |

Do not collapse these layers. A process may be actor-bound while one of its transports still sends unsigned messages. A signed transport may still call a tool that has not been delegated.

The wrapper posture for tool-bound work is `.waint`:

```text
parent actor signs or grants
  -> .waint carries bounded delegation
  -> MUX allows only named surfaces and intents
  -> audit records parent + wrapper
```

Examples:

| Wrapper | Use |
|---|---|
| `ipoll.gravity.waint` | Gravity's signed I-Poll sender |
| `mcp.gravity.waint` | Gravity's MCP transport wrapper |
| `tibet-ping.codex.waint` | Codex running a route posture probe |
| `browser.codex.waint` | Browser/fetch connector under Codex |
| `mux-verifier.root_idd.waint` | Root verifier process |

## Reachability and Route Posture

```bash
tibet-ping actor.local
tibet-ping echo.aint
```

Use `tibet-ping` to test route shape, reachability and MUX behavior.

Read it carefully:

```text
reachable != trusted
alive != allowed
route exists != consent exists
tool can run != tool is delegated
```

For public path tests, use `handshake.aint` as the open fixture. Do not probe real actors as test targets.

## Receipts and Trails

```bash
tibet create task --why "operator approved local route test"
tibet verify <token-id>
tibet export --format json
```

Use this to create, verify and export causal action evidence.

For incident or audit work, operators should be able to retrieve:

- parent token
- actor
- intent
- policy
- route/message/workload
- result
- linked follow-up

## Audit and Reports

```bash
tibet audit .
tibet export --format json
```

Use this to produce an evidence dossier. A report should not be the only source of truth; it should point back to receipts, state seals and material inventories.

## State and Materials

| Tool family | Use |
|---|---|
| Wayback | seal and compare state |
| SBOM | software dependency inventory |
| AI-SBOM | AI/model/tool inventory |
| CBOM | capability and authority inventory |
| Pol | health and drift checks |

## Conformance Runners

Conformance is for independent implementation and interoperability checks.

| Kit | Tests |
|---|---|
| `ztip-conformance` | identity, actor proof, freshness |
| `tibet-comms-conformance` | ping, sendpath, MUX, I-Poll, null-route |
| `tibet-evidence-conformance` | content hash, sealed object, continuity, CBOM, Wayback, reports |
| `tibet-security-conformance` | intent policy, capability gate, SNAFT, Cortex, Airlock, fail-closed |

Rule:

```text
reference runner passing = vectors are internally consistent
second implementation passing = real interop signal
```

## Common Operator Questions

| Question | First tool |
|---|---|
| Is my local stack installed? | `tibet system doctor` |
| Can I reach a route? | `tibet-ping` |
| Is this action grounded? | `tibet verify` |
| What changed? | Wayback diff / TIBET trail |
| What software was involved? | SBOM |
| What AI materials were involved? | AI-SBOM |
| What authority existed? | CBOM |
| Did policy fail closed? | security conformance vector |

## Related

- [Auditability](auditability.md)
- [Security Behavior](security-behavior.md)
- [Build Your Network](../network/build.md)
- [CLI Reference](../reference/cli.md)
