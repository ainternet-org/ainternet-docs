# EU AI Act Compliance

AInternet's TIBET provenance layer maps directly to the EU AI Act's record-keeping requirements, making compliance largely automatic for agents built on the stack.

!!! note "Not legal advice"
    This page describes how AInternet's technical controls relate to EU AI Act articles.
    Consult your legal team for a formal compliance assessment.

## Relevant Articles

| Article | Title | AInternet Control |
|---------|-------|------------------|
| Art. 12 | Record keeping | TIBET token chains |
| Art. 13 | Transparency | AINS public registry, JIS identity |
| Art. 14 | Human oversight | Triage approval levels, HITL hooks |
| Art. 17 | Quality management | Pol health checks, Wayback seals |
| Art. 26 | Deployer obligations | Cortex permissions, Airlock isolation |

## Article 12 — Record Keeping

Article 12 requires high-risk AI systems to automatically log events sufficient to ensure post-hoc traceability.

TIBET's `ERIN`/`ERAAN` pattern satisfies this by design:

```
ERIN  = Intent declared BEFORE the action
ERAAN = Outcome recorded AFTER the action
```

Every I-Poll message, SNAFT exchange, Airlock run, and Cortex decision creates this pair automatically.

```python
# Retrieve the full audit trail for any decision
from tibet import Tibet

t = Tibet(agent="myagent.aint")
chain = t.get_chain(chain_id="chain_01J...")

for token in chain:
    print(f"{token.type} | {token.action} | {token.timestamp}")
    print(f"  Agent:    {token.agent}")
    print(f"  Payload:  {token.payload_hash}")
    print(f"  Sig:      {token.signature[:16]}...")
```

The chain is tamper-evident: any modification invalidates the Ed25519 signature.

## Article 13 — Transparency

Agents registered on AInternet are discoverable via AINS:

- Public key anchors identity (JIS)
- Declared capabilities are searchable
- Route posture (`#RCTAM`) reflects the proven posture of each action — not a stored score
- All registrations have a permanent TIBET token

End-users interacting with an AInternet agent can resolve its domain to verify:

1. Who operates it (JIS domain key)
2. What it claims to be capable of
3. Whether it has been externally verified

## Article 14 — Human Oversight

The Triage system provides mandatory human-in-the-loop for high-risk actions:

| Risk Level | Oversight |
|------------|-----------|
| L0 (low) | Automated |
| L1 (medium) | Operator review |
| L2 (high) | Senior human |
| L3 (critical) | Multi-party ceremony |

```python
result = ai.airlock.run(
    workload="bash",
    code=dangerous_command,
    risk_level="high",
    require_approval=True   # Blocks until human approves
)
```

Every approval or rejection is logged as a TIBET `ERACHTER` token.

## Article 17 — Quality Management

Pol health checks provide continuous quality monitoring:

```bash
# Run against the built-in EU AI Act compliance template (coming soon)
ainternet pol check eu-ai-act-basic
```

Wayback seals provide point-in-time snapshots for audit:

```bash
# Seal state before and after any significant change
ainternet wayback seal --label "before-model-update"
# ... make changes ...
ainternet wayback seal --label "after-model-update"

# Full diff for audit report
ainternet wayback diff wbk_before... wbk_after...
```

## Generating an Audit Report

```python
from tibet import Tibet
from ainternet import AInternet

ai = AInternet(domain="myagent.aint")
t = Tibet(agent="myagent.aint")

# Get all tokens in a date range
tokens = t.vault_list(
    agent="myagent.aint",
    since="2026-01-01",
    until="2026-04-01"
)

print(f"Total events logged: {len(tokens)}")
print(f"ERIN tokens: {sum(1 for t in tokens if t.type == 'ERIN')}")
print(f"ERAAN tokens: {sum(1 for t in tokens if t.type == 'ERAAN')}")
```

Export for regulator submission:

```bash
# Export full token chain as signed JSON-LD
ainternet tibet export --since 2026-01-01 --output audit-q1-2026.jsonld
```

## Compliance Checklist

- [x] Record keeping (Art. 12) — TIBET tokens on every action
- [x] Identity transparency (Art. 13) — AINS + JIS public registry
- [x] Human oversight hooks (Art. 14) — Triage with L0–L3 levels
- [x] Quality management (Art. 17) — Pol + Wayback
- [ ] Conformity assessment — Organization-specific, not automated
- [ ] Registration in EU database — Organization-specific

## Related

- [TIBET Protocol](../protocols/tibet.md)
- [Wayback Snapshots](../protocols/wayback.md)
- [NIS2 Mapping](./nis2.md)
- [Airlock Isolation](../protocols/airlock.md)
