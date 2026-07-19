# Where Execution Governance Plugs In

> A learning module. AInternet is not an execution-governance product, and it does not pretend to be one. It is the **substrate** underneath one: it establishes *who* is acting (a `.aint` identity), what they may reach, and it enforces every action against local facts before it runs. This page draws the line — where AInternet stops, and where an external governance or clearance layer (VALO-style) plugs in on top — so the two compose instead of colliding.

The short version: **an external layer may propose policy; the box decides at execution time.** Governance feeds the gate with intent and rules; the box owns the enforcement floor and the receipts. Neither has to rebuild the other.

```text
   external governance layer      →  proposes policy, clearance, workflow, compliance overlays
   ───────────────────────────────────────────────────────────────────────────────────────────
   AInternet substrate (L0–L2)    →  identity · reachability · admissibility · native enforcement · receipts
```

---

## The layer map

Each AInternet layer answers one question and hands the next its facts. An execution-governance layer sits *above* the whole stack and reads from it:

| Layer | Owns | What it gives the layer above |
|---|---|---|
| **AINS** | naming / discovery | *who* exists and how to reach them — resolvable `.aint`, dark-by-default |
| **JIS** | identity / signature | *who is acting*, cryptographically — not an IP, an identity |
| **SNAFT / Cortex** | permission / posture | *is this consented under the current posture* — fail-closed |
| **MUX** | route / surface | *what may this identity reach* — proven posture, not a score |
| **TIBET** | receipt / provenance | *what happened*, in a causal chain you can audit |
| **IAB runtime** | enforcement floor | *does this action carry, natively, before it runs* — `0x4000` / `0x0000:<reason>` |
| **External governance** | policy / clearance | *may propose* rules and workflow — **the box still decides at execution time** |

The boundary is the last two rows. Everything up to and including the IAB runtime is sovereign local substrate. The governance layer is a tenant on top: welcome to shape *what should be allowed*, never the root of authority for *what actually runs*.

---

## PASS / DEGRADE / HALT — the same shape on both sides

A deterministic governance gate returns **PASS / DEGRADE / HALT** before an action executes. AInternet already produces exactly that verdict from local facts, and enforces it natively:

| Gate language | AInternet verdict | Meaning |
|---|---|---|
| PASS | `0x4000`, `can_carry=true` | action may proceed |
| DEGRADE | triage hold · partial posture · degraded sensor | needs review or a lower claim |
| HALT | `0x0000:<reason>` | refused **before** execution starts |

Because the shapes match, a VALO-style layer doesn't translate through guesswork — it reads the substrate's verdict and adds its own policy above it. The gate should be fed by **local facts, not prompt promises**; AInternet is the thing that produces those facts and enforces the result.

```sh
box provision status --json   # authority · posture · admissibility (carry_decision / blocked_by)
```

---

## What the substrate will not hand over

- It will not let "execution allowed" come to mean *approved by an external service* instead of *admissible by current local facts*. External approval can be a **precondition**; it is never the enforcement.
- It will not surrender the receipts. Provenance ([TIBET](../protocols/tibet.md)) stays local and causal, so an audit doesn't depend on the governance vendor's logs.
- It will not require the governance layer to rebuild Layer 0. Identity, posture, isolation and enforcement are already there — the layer above should stand on them, not reimplement them.

That division is the whole offer: a governance layer lands on a **proven L0/L1 floor** instead of next to something vague.

---

## Related

- [Reasoning ≠ Execution](reasoning-not-execution.md) — the split a gate plugs into.
- [Runtime Is The Firewall](runtime-is-the-firewall.md) — why the floor holds without the model's cooperation.
- [What We Push Is What You Download](what-we-push-is-what-you-download.md) — the release chain under all of it.
- The public [Boundary Dossier](https://github.com/ainternet-org/ainternet-iab-boundary-dossier) — architecture, redacted proofs, refusal cases.
