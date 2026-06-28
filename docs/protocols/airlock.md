# Airlock — Isolation and Reproducibility Gate

Airlock is the boundary where AInternet runs work it should not simply trust:
unknown code, high-risk tasks, model conversion, sealed payload handling, or a
route that claims a cadence lane.

It has two jobs:

1. **Isolate the work** in a disposable runtime or microVM.
2. **Prove the lane** when a route claims reproducible compute.

It is not a central service you must join. A self-hosted AInternet can run its
own airlock locally.

## Isolation Model

When an actor receives a risky `TASK`, or needs to transform a sealed artifact,
the airlock materializes a bounded runtime:

```text
actor / route request
      |
      v
airlock preflight
      |
      v
isolated cell or microVM
      |
      v
workload runs under limits
      |
      v
output hash + receipts
      |
      v
cell destroyed or sealed
```

Default posture:

| Resource | Default |
|---|---|
| Network | none or explicit allow-list |
| Filesystem | ephemeral overlay |
| Identity | runtime-bound `.aint` or local operator identity |
| Duration | bounded TTL |
| Output | hashed, receipted, optionally materialized |
| Audit | TIBET chain, not a standing trust score |

## Bifurcated Airlock

Some route postures claim that a lane is not only isolated, but reproducible.
For those routes, one run is not enough. The bifurcated airlock runs the same
cell twice and accepts only byte-identical output.

```text
cell A: capability receipt + workload -> bytes A
cell B: capability receipt + workload -> bytes B

pass iff:
  compute semantics match
  bytes A == bytes B
```

This is why CPU capability receipts matter. FMA3 is not a security primitive and
not a sixth route digit, but it changes compute semantics: fused multiply-add
uses one rounding; separate multiply/add uses two. If the forks are on different
planes, the airlock refuses to compare them. If they are on the same plane but
produce different bytes, the lane is not proven.

```text
same workload
same capability receipt
same compute semantics
same bytes
=> cadence lane may be claimed
```

That makes the smoke pipeline measurable. A builder can run the same test and
see whether the route carried what it claimed.

## Route Posture

Airlock does not score an actor. It contributes evidence to the route:

```text
Do not score the actor.
Number the proven route.
```

If the airlock proves the cell, the route may carry the lane it claimed. If the
airlock cannot prove it, the route holds, degrades, or collapses to `#00000`.

Examples:

```text
#24358  route claims cadence + sign-ahead evidence
#24258  timing lane fell back
#00000  airlock failed or route not proven
```

## TIBET Integration

Every airlock run should leave a TIBET trail:

```text
ERIN      workload declared
ERAAN     output hash + exit status + duration
ERACHTER  side effects, materialized files, network calls
```

For reproducibility gates, the receipt should also include:

```text
capability_receipt_hash
compute_semantics
cell_a_output_hash
cell_b_output_hash
bifurcation_verdict
route_posture_before
route_posture_after
```

## Example Shape

Python surfaces may expose airlock as an operator API:

```python
from tibet_mux import bifurcated_airlock as airlock
from tibet_mux import cpu_capability

receipt = cpu_capability.cpu_capability_receipt()

cell_a = airlock.Cell("a", receipt)
cell_b = airlock.Cell("b", receipt)

verdict = airlock.run_bifurcated(
    airlock.fused_accumulate,
    ([(1e16, 1.0000000000000002), (-1e16, 1.0)],),
    cell_a,
    cell_b,
)

assert airlock.lane_provable(verdict) is True
```

The exact API may vary per package. The contract is stable: compare bytes, not
"close enough" floats.

## Requirements

Airlock implementations usually need:

- KVM or another local isolation boundary for high-risk work
- JIS-bound runtime identity for the actor or cell
- TIBET receipts for input, output and side effects
- a machine capability receipt for compute-sensitive lanes
- fail-closed behavior when a claim cannot be proven

Self-hosted hubs can run this without internet access. Public hubs can offer it
as a convenience, but they are not the authority.

## Related

- [Route Posture](../learn/route-posture.md)
- [Machine Posture](../operators/machine-posture.md)
- [TIBET Provenance](./tibet.md)
- [MUX Routing](./mux.md)
- [Cortex Permissions](./cortex.md)
