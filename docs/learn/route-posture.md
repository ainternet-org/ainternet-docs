# Route Posture, Not a Trust Score

> **Do not score the actor. Number the proven route.**
>
> AInternet does not rate actors. It reconstructs routes.

This is the canonical reference for how AInternet decides what an actor may do.
If older pages still mention a scalar "trust score", **this page is the source of
truth** — the score model is retired.

## Why a trust score is the wrong shape

A trust score (`trust = 0.87`) says an actor has stable moral credit. But an
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

The old "trust score" survives only as a **human index into evidence**: *"show me
what #24358 meant, and why it changed to #24247."*

## Posture is also a gate

The number doesn't only describe the lane — it bounds what the lane may do. Audit
`A2` (a mirror/observed dump) is measured but not hot-path; `A5` (sign-ahead) and
above may open the hot path. A locked cadence needs a scheduler-free timing lane
*and* a MUX that knows the schedule. The permission engine reads the posture; it
never assumes.

## Machine posture: which routes may *your* machine carry?

A second question no spec answered before: *can this machine carry this route
safely, reproducibly, fast enough?* Not "is my PC trusted?" but **"which routes
may my PC carry?"**. A machine posture is a proven set across cpu / memory /
storage / gpu / kernel / identity / audit — e.g. *"encrypts at line rate with
AES-NI; can carry #24358 hot_transfer; cannot sustain A5 sign-ahead under load
(no AVX-512); not for sealed multi-actor runtime (no TPM)."* Honest, testable,
and it fails closed on a mismatch.

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

This is implemented and public: `pip install tibet-mux` →
`tibet_mux.route_posture` (`encode_posture`, `posture_transition`,
`lane_permissions`, `make_receipt`, `posture_map`, `reconstruct_event`),
`tibet_mux.carrier_policy`, `tibet_mux.machine_posture`. The route is the output
of attestation — and the attestation is something you can re-check yourself.
