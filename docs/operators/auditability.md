# Auditability

AInternet should be auditable by construction. The goal is not to collect more logs. The goal is to make important actions reconstructable.

An audit-ready action answers:

```text
who acted?
under which identity proof?
what was intended?
which policy applied?
what route or message was used?
what object or payload was touched?
what changed afterwards?
can another implementation verify the evidence?
```

## Evidence Spine

| Layer | Evidence |
|---|---|
| JIS | actor proof, key succession, challenge-response |
| TIBET | causal action receipts |
| Cortex | allow/deny decision |
| SNAFT | consent proposal, acceptance, rejection and scope |
| MUX/I-Poll | route/message event and delivery state |
| Airlock | quarantine/run/release verdict |
| Wayback | state seal, diff and restore point |
| SBOM / AI-SBOM | software, model and tool materials |
| CBOM | capabilities and authorities |
| Pol | health check and drift evidence |

## Minimum Receipt Chain

```text
parent event
  -> intent
  -> policy check
  -> proof
  -> route/message/workload
  -> result
  -> follow-up or ACK
```

If there is no parent, the action is not grounded. If there is no fresh proof, the action is replayable. If there is no policy decision, the route is only reachability.

## Operator Commands

Common operator flow:

```bash
tibet system doctor
tibet create deploy --why "roll out local hub policy"
tibet verify <token-id>
tibet export --format json
tibet audit .
```

Network checks should be read correctly:

```bash
tibet-ping actor.local
```

`tibet-ping` proves reachability or route posture. It does not prove permission by itself. Permission still comes from policy, consent and receipts.

## Material Evidence

For software and AI systems, action receipts are not enough. You also need to know what materials existed.

| Material view | Use |
|---|---|
| SBOM | software packages and dependencies |
| AI-SBOM | model, prompt, tool and AI pipeline materials |
| CBOM | capabilities, authority and object rights |
| Wayback | point-in-time state |
| Report pack | exported audit dossier |

## Conformance

Auditability should be testable:

| Evidence question | Conformance family |
|---|---|
| actor proof is valid | `ztip-conformance` |
| message/route behavior is reproducible | `tibet-comms-conformance` |
| evidence object verifies | `tibet-evidence-conformance` |
| policy fails closed | `tibet-security-conformance` |

The vectors are the contract. A second implementation should be able to verify the same records.

## Compliance Posture

This supports compliance work because it gives you records for:

- access control
- change traceability
- incident reconstruction
- software supply-chain evidence
- AI decision trail evidence
- human approval and consent trail
- system state before and after significant events

This is compliance-enabling. It is not a certification claim.

## Related

- [TIBET](../protocols/tibet.md)
- [Wayback](../protocols/wayback.md)
- [Pol](../protocols/pol.md)
- [EU AI Act Mapping](../enterprise/eu-ai-act.md)
- [NIS2 Mapping](../enterprise/nis2.md)
