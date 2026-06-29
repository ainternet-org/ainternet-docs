# Route Posture API

Route posture is a compact evidence coordinate for a route. It does not rate an actor. It describes what route was proven for this action.

```text
Do not score the actor.
Number the proven route.
```

## Coordinate

The current public shape is:

```text
#RCTAM
```

| Digit | Meaning |
|---|---|
| R | route family / actor class |
| C | consent or relation class |
| T | timing / hardware lane |
| A | audit / evidence origin |
| M | MUX-known or exception posture |

## Current Digit Tables

These values mirror the current `tibet-mux` route-posture implementation. A route posture is a coordinate into evidence, so implementations must agree on these tables before they can compare `#RCTAM` values across nodes.

### R: Route Family

| Digit | Meaning |
|---|---|
| 0 | unknown |
| 1 | `.aint` direct identity |
| 2 | `.saint` controller or system service |
| 3 | `.raint` runtime enclave |
| 4 | `.waint` wrapper, tool or resource |
| 5 | `.caint` composite route |

### C: Consent Or Relation Class

| Digit | Meaning |
|---|---|
| 0 | none |
| 1 | token-only |
| 2 | fresh JIS challenge |
| 3 | bilateral consent |
| 4 | active parent relation |
| 5 | 2-of-2 DAG relation |

### T: Timing Or Hardware Lane

| Digit | Meaning |
|---|---|
| 0 | reactive, scheduler in loop |
| 1 | async-batched |
| 2 | CBR sleep metronome |
| 3 | CBR spin, scheduler-free cadence |
| 4 | DMA graph, CPU out of the loop |
| 5 | DMA descriptor ring, isolated device |

### A: Audit Or Evidence Origin

| Digit | Meaning |
|---|---|
| 0 | none |
| 1 | log-only |
| 2 | mirrored / observed off-path |
| 3 | receipted |
| 4 | native seam, signs in-path |
| 5 | sign-ahead |
| 6 | cadenced, aligned to a known partituur |
| 7 | durable |

### M: MUX Posture

| Digit | Meaning |
|---|---|
| 0 | dark, no valid posture |
| 1 | unknown actor |
| 2 | stale posture |
| 3 | unexpected posture |
| 4 | posture changed mid-route |
| 5 | actor-class mismatch |
| 6 | consent expired |
| 7 | hardware lane fell back without receipt |
| 8 | MUX knows the partituur |
| 9 | MUX knows the partituur and verified it |

Example:

```text
#54359
│││││
││││└─ MUX: verified partituur
│││└── Audit: sign-ahead
││└─── Lane: scheduler-free cadence
│└──── Consent: active parent relation
└───── Family: composite actor (.caint)
```

## Normative `verify_at` Predicates

A digit table tells you what a value *means*. It does not yet tell a second
implementer *when they are allowed to assert it*. Two nodes only compute the same
`#RCTAM` if they agree on the **predicate that earns each value** — checked at
verification time, not claimed by the actor. This is that contract.

Rule: assert digit `d` on an axis only if its `verify_at(d)` predicate holds **now**.
If it does not hold, the axis collapses to the highest value whose predicate *does*
hold (often `0`). If any axis is `0`-dark in a way that invalidates the route, the
whole posture collapses to `#00000`. A digit is a proof obligation, never a label.

### R — route family · `verify_at`

| Digit | Asserted only when |
|---|---|
| 0 | no JIS identity resolves for the actor |
| 1 | actor resolves to a direct `.aint` JIS identity |
| 2 | resolves to a `.saint` controller / system-service identity |
| 3 | resolves to a `.raint` runtime-enclave identity (broker-minted, parent-bound) |
| 4 | resolves to a `.waint` tool / resource surface |
| 5 | resolves to a `.caint` composite, i.e. a folded multi-hop route |

### C — consent / relation · `verify_at`

| Digit | Asserted only when |
|---|---|
| 0 | no consent artifact present |
| 1 | a bearer token only — no fresh proof |
| 2 | a fresh JIS challenge: the actor signed a **verifier-issued** nonce inside the challenge window |
| 3 | a bilateral consent record: both sides accepted the same scope |
| 4 | an active, unexpired parent-relation binding exists |
| 5 | a relation contract whose **2-of-2** signatures both verify (DAG edge) |

### T — timing / hardware lane · `verify_at`

| Digit | Asserted only when |
|---|---|
| 0 | the scheduler is in the loop (reactive) |
| 1 | dispatch is async-batched |
| 2 | a CBR sleep metronome holds the cadence |
| 3 | CBR spin, scheduler-free cadence measured (e.g. RDTSC) |
| 4 | a DMA graph runs with the CPU out of the loop |
| 5 | a DMA descriptor ring on an isolated device |

> T references a **capability receipt** (e.g. `compute_lane: fma-avx2` from host
> attestation); it is not the CPU feature encoded directly. Same receipt → same T.

### A — audit / evidence origin · `verify_at`

| Digit | Asserted only when |
|---|---|
| 0 | no evidence origin |
| 1 | a log line only, no receipt |
| 2 | observed off-path (mirror / camera) |
| 3 | a TIBET receipt is written for the action |
| 4 | the native seam signs in-path (the handle signs as it moves) |
| 5 | sign-ahead: the receipt is pre-signed **before** route-open |
| 6 | cadenced: receipts aligned to a known partituur / CBR |
| 7 | durable: receipt persisted to a durable evidence store |

### M — MUX posture · `verify_at`

| Digit | Asserted only when |
|---|---|
| 0 | dark — no valid posture (collapse here) |
| 1 | the actor is not known to MUX |
| 2 | the posture is stale |
| 3 | the posture is unexpected versus declared |
| 4 | the posture changed mid-route |
| 5 | the actor class does not match |
| 6 | consent has expired |
| 7 | a hardware lane fell back without a receipt |
| 8 | MUX holds the partituur (knows the expected route) |
| 9 | MUX holds the partituur **and** verified it against the observed fold |

Conformance: a second implementer is route-posture-compatible when, given the same
evidence inputs, it asserts the same digit on every axis by these predicates — and
collapses identically when a predicate fails. Mismatched predicate → mismatched
`#RCTAM`, which is itself a detectable seam.

## API Use

Route posture should appear where a route is explained, admitted, denied or audited.

Example response shape:

```json
{
  "from": "agent.local",
  "to": "audit.local",
  "intent": "ipoll.push",
  "route_posture": "#24358",
  "expanded_posture": {
    "family": "aint",
    "consent": "active_relation",
    "timing": "cadence_locked",
    "audit": "sign_ahead",
    "mux": "known"
  },
  "causal_seq": 42,
  "transition_reason": "audit_surface_binding"
}
```

## Dark Route

Unknown, unproven, unconsented or malformed routes should collapse to:

```text
#00000
```

The route is not partially trusted. It is dark.

## Common Endpoints

These endpoint names are the intended contract shape for hubs and local nodes:

```text
GET  /api/mux/route/explain?from=A&to=B&intent=...
POST /api/mux/route/challenge
POST /api/mux/route/open
POST /api/mux/route/close
GET  /api/mux/route/audit/{route_id}
```

Local CLIs should expose the same ideas:

```bash
ainternet route explain agent.local audit.local
ainternet route challenge agent.local audit.local
ainternet route close <route-id>
```

## Policy

Policy should consume posture as evidence:

```text
required_posture: "#24358"
observed_posture: "#24008"
decision: hold
reason: audit surface not bound yet
```

Do not convert posture back into a scalar score. The digits matter because they describe different facts.

## Compose / Smoke

When a route crosses multiple hops, compose the observed postures with meet
semantics: per-digit minimum.

```json
{
  "kind": "org.ainternet.route_posture.compose.v1",
  "hops": ["#23856", "#12093", "#88347"],
  "observed_posture": "#12043",
  "law": "meet/per-digit-min"
}
```

A smoke pipeline compares the declared route with the observed fold:

```json
{
  "kind": "org.ainternet.route_posture.smoke.v1",
  "declared_posture": "#24358",
  "observed_posture": "#24258",
  "decision": "hold",
  "reason": "timing lane fell back"
}
```

If one hop is dark, the whole route is dark:

```json
{
  "hops": ["#54359", "#00000", "#54359"],
  "observed_posture": "#00000"
}
```

## Airlock Evidence

Compute-sensitive lanes may require a bifurcated airlock receipt. The route
posture does not encode CPU features directly. It references evidence that the
machine can carry the lane.

```json
{
  "kind": "org.ainternet.airlock.bifurcation.v1",
  "route_posture_before": "#24358",
  "capability_receipt_hash": "sha256:...",
  "compute_semantics": "single-rounding-fma",
  "cell_a_output_hash": "sha256:...",
  "cell_b_output_hash": "sha256:...",
  "verdict": "byte-identical",
  "route_posture_after": "#24358"
}
```

If the compute planes differ, or the bytes differ, the route should hold or
darken rather than claim the lane.

## Related

- [Route Posture](../learn/route-posture.md)
- [MUX](../protocols/mux.md)
- [Machine Posture](../operators/machine-posture.md)
- [Airlock](../protocols/airlock.md)
- [OSAPI Pair](osapi.md)
