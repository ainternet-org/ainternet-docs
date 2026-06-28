# Audit Cockpit

`tibet-audit` is the local reconstruction cockpit for an AInternet node.

It does not score an actor. It reads evidence that already exists on your machine and shows which route, policy, material and state can be reconstructed.

```text
Do not score the actor.
Number the proven route.
```

## What It Answers

Run the cockpit when you need to know:

```text
what happened?
which actor or runtime was involved?
which route posture was proven?
which policy allowed, denied or darkened the action?
which object, model, tool or package was touched?
which evidence is missing?
```

The output is meant for operators first: a terminal view you can read during an incident, a lab run, a compliance check or a local node setup.

## Run It

```bash
pip install tibet-audit
tibet-audit dashboard .
```

For a repo or node that carries a profile map:

```bash
TIBET_AUDIT_REPO_POSTURE=./repo_posture.json tibet-audit dashboard .
```

The command should not phone a central service by default. If a report endpoint is used, it must be explicitly configured by the operator.

## The Six Panes

| Pane | Meaning |
|---|---|
| Pulse | latest events, tail-style flow and warnings |
| Machine and Hardware Evidence | local compute evidence such as CPU capability and runtime posture |
| Surfaces and Enclaves | SSM cards, sealed carriers, suspicious surfaces and enclave evidence |
| Evidence Chains | correlated story from parent event to policy, route, result and follow-up |
| Stack | packages present for the selected profile, such as `ainternet[node]` |
| Next Actions | missing packages, policy gaps or operator follow-up |

The header folds evidence lanes into a single route posture:

```text
SYSTEM POSTURE #34307 · smoke RED · 8/8 evidence active
```

That is not a grade. It is the weakest proven route across the current evidence tree.

## What It Reads

`tibet-audit` sits above the evidence spine:

| Source | Role |
|---|---|
| `tibet-tail` | live and recent event flow |
| `tibet-pol` | policy verdicts, drift and runtime checks |
| TIBET receipts | causal action chain |
| MUX | route posture, named surfaces and null routes |
| SNAFT / Cortex | consent and policy decisions |
| Airlock | quarantine, run, release and darkening evidence |
| Wayback | state seal, diff and restore point |
| SBOM | software materials |
| AI-SBOM | model, prompt, tool and runtime materials |
| CBOM | capability and authority inventory |
| SSM | surface hints checked against sealed manifest truth |

## Magic Bytes, Not Filenames

The cockpit follows the same rule as transfer carriers:

```text
surface = greeting and index
manifest = truth
```

A file named `.tza` is not trusted because of its extension. A sealed carrier is recognized by structure, magic bytes, signature and manifest. If the name and the manifest disagree, the manifest wins and the surface drift is evidence.

## Good Output

Good output is not always green. A useful cockpit can say:

```text
route darkened
consent expired
external tool call denied
zombie .tza surface rejected
hardware cadence not proven
package missing for this profile
```

That is the point. Audit is not a decorative report. It is how a local actor knows what it can prove.

## Related

- [Auditability](auditability.md)
- [Operator Tooling](tooling.md)
- [Route Posture](../learn/route-posture.md)
- [Semantic Surface Manifest](../reference/semantic-surface-manifest.md)
- [Transfer Carriers](../reference/transfer-carriers.md)
