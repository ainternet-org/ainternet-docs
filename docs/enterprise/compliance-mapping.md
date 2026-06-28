# Compliance Mapping

AInternet and TIBET are compliance-enabling infrastructure. They are not a certification by themselves.

The stack helps organizations produce the technical evidence that legal, risk and security teams need for frameworks such as EU AI Act, NIS2, DORA, ISO 27001-style controls, GDPR accountability and software supply-chain governance.

## Positioning

Use this language:

```text
supports
maps to
provides controls for
produces evidence for
helps demonstrate
```

Avoid this language unless a formal audit has happened:

```text
certified
compliant by default
guarantees legal compliance
approved by regulator
```

## Control Families

| Need | Stack control |
|---|---|
| actor accountability | JIS identity and fresh proof |
| action traceability | TIBET causal receipts |
| access control | Cortex policy |
| consent and scope | SNAFT |
| risky execution control | Airlock and triage |
| incident reconstruction | TIBET trail, Wayback, Pol |
| software supply-chain evidence | SBOM |
| AI material evidence | AI-SBOM |
| capability and authority inventory | CBOM |
| interoperability assurance | conformance vectors |

## EU AI Act

Relevant support:

- record keeping for AI actions
- actor and system traceability
- human oversight receipts
- policy and consent evidence
- state before/after significant changes
- AI material inventory through AI-SBOM

See also [EU AI Act Compliance](eu-ai-act.md).

## NIS2

Relevant support:

- risk management evidence
- incident timeline reconstruction
- supply-chain visibility
- access control records
- health and drift checks
- audit export for reporting

See also [NIS2 Mapping](nis2.md).

## DORA

Relevant support:

- ICT risk evidence
- operational resilience checks
- state seals before and after changes
- incident trail exports
- third-party or plugin boundary evidence

## ISO 27001-Style Controls

Relevant support:

| ISO-style area | Evidence |
|---|---|
| identity and access management | JIS, Cortex, SNAFT |
| logging and monitoring | TIBET, Pol |
| change management | TIBET receipts, Wayback diffs |
| asset management | SBOM, AI-SBOM, CBOM |
| supplier/plugin governance | conformance vectors, receipts |
| incident management | trail export, report packs |

## GDPR Accountability

Relevant support:

- actor identity for processing actions
- purpose/intention receipts
- consent scope where relevant
- audit trail for automated or agentic actions
- data-sharing evidence across actors or hubs

This does not replace legal basis analysis. It gives your legal and privacy teams better technical evidence.

## Hub-Neutral Benefit

Because the stack is hub-neutral, an organization can keep evidence and policy local:

```text
own hub
own registry
own policy
own evidence store
optional public federation
```

That matters when regulations require control over processing, audit evidence, data locality or vendor risk.

## Related

- [Hub Neutrality](../operators/hub-neutrality.md)
- [Auditability](../operators/auditability.md)
- [Security Behavior](../operators/security-behavior.md)
- [EU AI Act Compliance](eu-ai-act.md)
- [NIS2 Mapping](nis2.md)
