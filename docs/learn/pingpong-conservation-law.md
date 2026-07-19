# Software in a Box: The PingPong Conservation Law

AInternet boxes should be able to revive themselves.

Not by trusting a saved folder. Not by logging into a cloud account. Not by hoping
the old runtime still exists somewhere.

They revive because every valid state transition can be proven from the previous
one.

```text
genesis
  -> bounded move
  -> signed transition
  -> next valid state
```

That is the PingPong conservation law.

## Why PingPong Does Not Explode

The game stays simple because the state is tiny and bounded:

```text
ball position
ball direction
paddle position
score
next tick
```

Every frame follows from the frame before it. The ball does not need a biography.
The system only needs enough state to decide the next valid move.

Software-in-a-box should behave the same way.

An AInternet node does not need a central account to remember who it is. It needs:

```text
actor claim
JIS key
TIBET receipt root
surface grant
route posture
next transition envelope
```

If those pieces verify, the box can continue. If they do not verify, the route goes
dark.

## Revive, Do Not Recreate

Reinstalling software is easy. Continuing an actor is the hard part.

```text
installed software != living actor
```

A living actor has a receipt trail. It has a key. It has a last known state. It may
have a parent relation, a successor, or a tombstone.

So every AInternet-in-a-box needs reseed as a native path:

```text
New      create genesis
Restore  bind a verified local identity bundle
Reseed   continue through a successor key
Retire   write an explicit tombstone
Replace  retire old actor, point to successor
```

This is not account recovery. It is state compilation.

The identity compiler reads local proof and emits the next actor state.

## Name Is Greeting, Key Is Truth

A name is useful for humans and routing. It is not continuity.

```text
name says:       "I am node-451bcc53.aint"
key proves:      "I can sign for this actor"
receipts prove:  "this is the causal chain I came from"
```

Name-only restore must not exist.

If you only have a name, the box may inspect public or local records, but it cannot
claim continuity. It can start a new actor or create a successor, but it cannot
pretend to be the old state.

## The `.tza` Identity Bundle

The portable form is a Tibet-Zip Archive:

```text
<actor>.identity.tza
```

The extension is a human label. The verifier reads magic bytes, manifest,
signatures and receipts.

A useful identity bundle carries:

```text
claims/
public keys/
TIBET receipt chain/
last receipt root/
relation form/
signatures/
audit evidence/
```

Private keys stay local unless the operator explicitly creates a sealed custody
package. The default bundle should be safe to inspect and move without turning into
a secret leak.

## The Conservation Rule

The next state must conserve the proof of the previous state.

```text
previous receipt root
  + signed transition
  + bounded policy envelope
  + current verification
  = next valid state
```

If any required term is missing, the box does not improvise.

```text
missing old key       -> successor, not continuity
missing receipts      -> new actor, not restore
missing tombstone     -> not retired
forked sequence       -> dark
expired envelope      -> re-anchor
unknown surface grant -> 0x0000
```

The actor is not scored. The route is proven or it is not.

## Software-in-a-Box

A proper AInternet box should be able to answer four questions before it runs:

```text
Who am I carrying?
What proof did I receive?
What state can I compile?
What surfaces may I open?
```

That is why AInternet-in-a-box carries more than a root filesystem.

It carries:

```text
node floor
identity floor
evidence floor
local package shelf
operator recipe
scanner / verifier
```

The box can run fully local. It can stay offline forever. It can later federate if
the operator chooses. Online publication is a later route, not a hidden dependency.

## The TUI Rule

The onboarding TUI should expose the conservation law without making the operator
learn the internals first.

Each mode should show:

```text
What changes?
What stays local?
What proof did we write?
What can you do now?
```

Example:

```text
Restore / reseed

This machine can continue an actor only from local proof.

[1] Use old key
[2] Use identity bundle
[3] Create successor
[4] Start new

Nothing contacts an online instance.
```

The equivalent command should always be visible.

```bash
tibet-zip verify ./node-451bcc53.identity.tza
ainternet identity compile ./node-451bcc53.identity.tza --dry-run
ainternet actor reseed node-451bcc53.aint --from ./node-451bcc53.identity.tza
```

## The Short Version

```text
Do not trust the player.
Verify the next tick.
```

An AInternet actor survives because its next state is locally provable.

That is how a machine can be wiped, moved, restored, reseeded, retired or replaced
without turning identity into a cloud account.

That is software-in-a-box.

## Related

- [The Running Substrate](the-running-substrate.md) — what actually runs beneath the concepts.
- [A Computer Inside a Computer](computer-inside-computer.md) — local loops and isolation.
- [Reaching a Raint: Identity, Not a Port](reaching-a-raint.md) — how a revived actor is still addressable.
- [Everything Falls Back to TIBET](everything-falls-back-to-tibet.md) — provable next state.
