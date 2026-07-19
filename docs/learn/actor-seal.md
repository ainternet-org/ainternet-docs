# Actor Seal

An actor seal is the receipt that says a runtime session closed cleanly.

It is the line between "an AI process was opened" and "the box can carry that
session forward as evidence." Without a seal, the next boot must treat the
session as stale, crashed or unresolved.

```text
open actor runtime
  -> write session grant
  -> run under current posture
  -> close cleanly
  -> write durable seal
  -> carry evidence across boot
```

## Why It Matters

An AI can reason without touching the machine. Execution is different.

When a runtime is opened, the box needs to know:

- who the actor is;
- on whose behalf it is acting;
- which runtime surface was granted;
- whether the session closed cleanly;
- which audit head or receipt survived;
- whether the next boot may trust the closure.

The actor seal is not a chat log. It is not a prompt-level promise. It is a
runtime receipt.

## The Contract

Every bound actor runtime follows the same shape:

| Phase | Evidence |
|---|---|
| Open | session grant, actor, parent/root, runtime surface, current posture |
| Run | TIBET/audit events, allowed surfaces, denials and route posture |
| Clean close | durable seal with `0x4000` closure |
| Crash/kill | no closed stance, reseed or re-attest before carry |

This lets the box answer a hard question:

```text
May this actor carry into the next state?
```

If the answer is not proven, the safe result is a hold or reseed, not a green
status.

## One Box Verb

The important implementation rule is:

```text
the box writes the seal; the UI only runs the box verb
```

The CLI, TUI and web cockpit must not create three meanings of a "sealed"
session. They may present different controls, but they must all drive the same
underlying box contract.

```text
CLI command
TUI workbench
web cockpit PTY
```

all converge on:

```text
box actor cli <actor.aint>
```

or an equivalent runtime-bound box verb.

If a browser says "session sealed" but the durable seal store does not contain a
closed receipt, the browser is wrong. The cockpit is transport; the box is
authority.

## Clean Close Versus Crash

Clean close:

```text
actor exits normally
seal written
seal_state = 0x4000
next boot may carry it
```

Crash, kill, disconnect or power loss:

```text
no closed stance
session remains open/stale
next boot must reseed or re-attest
```

This is why "close" is a ceremony. A runtime that can affect state must leave a
receipt when it leaves.

## Relation To Execution Clearance

The seal does not grant authority by itself. It records the closure of a runtime
that was already admitted under the current posture.

Execution clearance still depends on:

- identity;
- relation;
- SNAFT/Cortex posture;
- MUX surface routing;
- runtime containment;
- current state;
- TIBET evidence.

The seal answers continuity. The gate answers admissibility.

## Operator Rule

If you are operating a box, remember:

```text
open is not carry
exit is not proof
seal is the proof
```

The green state should always point at the receipt that made it green.


## Related

- [Reasoning ≠ Execution](reasoning-not-execution.md) — the reason a session is gated at all.
- [Runtime Is The Firewall](runtime-is-the-firewall.md) — the floor a bound session runs on.
- [CRUST Runtime](crust-runtime.md) — the sealed-memory substrate under the seal.
- [Everything Falls Back to TIBET](everything-falls-back-to-tibet.md) — the receipt a clean close leaves behind.
