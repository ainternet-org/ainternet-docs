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
