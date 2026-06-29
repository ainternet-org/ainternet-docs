# Route Posture, Not a Trust Score

> **Do not score the actor. Number the proven route.**
>
> AInternet does not rate actors. It reconstructs routes.

This is the canonical reference for how AInternet decides what an actor may do.
If older pages still mention a scalar reputation number, **this page is the source
of truth** — the scalar model is retired.

## Why a scalar rating is the wrong shape

An actor rating (`trust = 0.87`) says an actor has stable moral credit. But an
actor on AInternet is usually a *fleeting runtime*: a process binds a key, passes
a JIS challenge, opens a consent relation, runs through some hardware lane, and
the route expires. Five minutes later the same name is in a different posture, on
a different lane, doing a different thing.

A single integer cannot represent that — and worse, a *score needs a scorer*:
someone who claims the authority to rate you. That is a power move, not a
measurement.

## What replaces it: the route posture number

The useful number is a **route posture**: a compact code for the *currently
proven posture* of a specific action, lane, or runtime window. It is a coordinate
into evidence, not a rating.

```text
#24358
 |||||
 ||||+-- M: MUX-known / exception posture
 |||+--- A: audit / evidence origin   (A2 mirrored .. A5 sign-ahead .. A7 durable)
 ||+---- T: timing / hardware lane     (reactive .. CBR-spin 0.00-bit .. DMA)
 |+----- C: consent / relation class
 +------ R: route family / actor class (aint/saint/raint/waint/caint)
```

`#24358` does **not** mean "78% trustworthy". It means: *this action is on route
family 2, consent class 4, timing lane 3, audit mode 5, and the MUX knows the
partituur.* Change one and the number changes — the actor's character is not
re-scored, the **route** changed:

```text
#24358 -> #24247   hardware lane fell back
#24358 -> #20358   consent/relation weakened
#24358 -> #00000   dark route — no valid posture
```

The old scalar survives only as a **human index into evidence**: *"show me
what #24358 meant, and why it changed to #24247."*

## Posture is also a gate

The number doesn't only describe the lane — it bounds what the lane may do. Audit
`A2` (a mirror/observed dump) is measured but not hot-path; `A5` (sign-ahead) and
above may open the hot path. A locked cadence needs a scheduler-free timing lane
*and* a MUX that knows the schedule. The permission engine reads the posture; it
never assumes.

## Postures compose

A route is a tree, not a label. If a request crosses three hops, the network must
prove the whole path, not average the hops together. AInternet composes postures
with a **meet**: per-digit minimum.

```text
#23856 + #12093 + #88347 = #12043
```

That is not a score calculation. It is the weakest proven coordinate on each
axis. If one hop cannot prove the timing lane, the end-to-end route cannot claim
that lane. If any hop collapses to `#00000`, the whole path is dark.

This makes route checks simple enough to smoke-test. Lay the declared posture
next to the real route, fire a dummy through the path, fold the observed hops,
and compare:

```text
declared: #24358
observed: #24258
result:   hold — timing lane fell back
```

The smoke pipeline is intentionally measurable. Anyone can re-run the fold and
see whether the route carried what it claimed.

## Machine posture: which routes may *your* machine carry?

A second question no spec answered before: *can this machine carry this route
safely, reproducibly, fast enough?* Not "is my PC trusted?" but **"which routes
may my PC carry?"**. A machine posture is a proven set across cpu / memory /
storage / gpu / kernel / identity / audit — e.g. *"encrypts at line rate with
AES-NI; can carry #24358 hot_transfer; cannot sustain A5 sign-ahead under load
(no AVX-512); not for sealed multi-actor runtime (no TPM)."* Honest, testable,
and it fails closed on a mismatch.

## Airlock: byte-identical, or it did not prove the lane

Some lanes claim more than reachability. A cadence lane says the work can be run
reproducibly under a known compute posture. Airlock proves that by bifurcation:
run the same cell twice, under the same attested compute semantics, and accept
only if the outputs are byte-identical.

FMA3 is a good example of why this matters. Fused multiply-add uses one rounding;
separate multiply plus add uses two. Both can be valid compute, but they are not
the same plane. The airlock does not say "close enough". It either proves the
same bytes or refuses the lane.

```text
two forks
same capability receipt
same compute semantics
same bytes
=> lane can be claimed
```

If the forks diverge, the route is held or darkened. The actor is not punished;
the route simply did not prove what it tried to carry.

## Causal, never wall-clock

A posture is ordered by a causal sequence (Lamport), not a timestamp. Wall-clock
is advisory and distrusted — a host can drift hours out of sync. "When" means
*causal position*, not the clock on the wall.

## Reconstruct, don't rate

A log line *"actor X (0.95) ran rm -rf /dir"* tells you nothing. The score
authorises nothing useful. What you do — in software as in real life when you
lose your keys — is **retrace**: where did it stand, what was the lane, what was
said before, who was present. The route posture + the causal trail let you
reconstruct intent. No score is consulted.

## Where it lives

This is implemented and public: `pip install -U tibet-mux` →
`tibet_mux.route_posture`, `tibet_mux.posture_algebra`,
`tibet_mux.machine_posture`, `tibet_mux.cpu_capability` and
`tibet_mux.bifurcated_airlock`. The route is the output of attestation — and the
attestation is something you can re-check yourself.

## Related

- [Route Posture API](../reference/route-posture-api.md)
- [Build Posture](../network/build-posture.md)
- [MUX](../protocols/mux.md)
- [Machine Posture](../operators/machine-posture.md)
