# Reaching a Raint: Identity, Not a Port

> What a **raint** is, and why machines reach each other by *identity* instead of by address. A raint
> is a runtime that boots, proves who it is, serves only what your identity is allowed, records
> everything, and then vanishes. This page explains the model — how a lane is *summoned by a proof*,
> why a raint stays dark to a stranger, and how two of them form a relation. The hands-on commands run
> on **your own stack** (see the last section); there is no public rig to poke. Builds on
> [The Contract Is the System](the-contract-is-the-system.md) and [The Cat Principle](the-cat-principle.md).

Nothing below is a mock — every line is from a live raint on real KVM. But it's an *explanation*, not an
invitation to attack something of ours: you reproduce it by running the stack yourself.

---

## Why a runtime needs a name

A port addresses a *place* — "whatever is listening on host:8080." That made sense when a server was a
fixed box. It stops making sense the moment the thing on the other end is a **process**: a microVM, a
service, a tool, an AI agent — spun up, moved, replaced, gone in minutes.

A process is not a place. It's an **actor**. And *an actor that can't be named can't be trusted to act.*
So in AInternet every runtime carries an identity — an `.aint`. A **raint** is exactly that: a *runtime
`.aint`*, a process that holds its own hardware-bound key and can prove who it is on every call.

Two things fall out of naming the runtime instead of its port:

- **Reachable by *who*, not *where*.** You address `raint-…​.test.aint`, not an IP. The address survives
  the process moving, and a stranger who knows the IP still has nothing — there's no place to knock.
- **Accountable by construction.** Every act is signed by a named actor and lands in an audit trail. You
  can't act anonymously, because there is no anonymous actor — only named ones.

This is why even a five-minute throwaway VM gets a real identity. It isn't ceremony; it's the only way a
*runtime* can be reached and trusted in a world where runtimes are temporary. (The same logic runs all the
way down — even the machine that hosts the VMs carries a name.)

---

## You don't hit a port — you attach by identity

The old reflex is `curl http://host:port/thing`. A raint refuses that framing. You don't address a
*place*, you address an *actor*:

```bash
ainternet attach raint-51fc8ee7.test.aint
```

Behind that one line, the lane is *summoned by a proof*, not opened by a port:

```text
richard.test.aint
  → broker challenge        (fresh nonce + consent-receipt hash + lane id)
  → signed MUX frame        (your key signs who / to whom / which surface / under which consent)
  → broker verifies         (signature, nonce freshness, consent, surface policy)
  → routes to the surface    (only after the decision)
  → raint answers            (only what the verified surface allows)
```

**Route is the output of attestation, not the input.** The port underneath (a plain HTTP carrier) is just
copper; the truth is the signed frame the broker checks. The broker is the gate — you never touch the guest
directly.

---

## The flow, with what actually comes back

Every node offers a small set of surfaces, and `health` declares them. The attach console is one universal
client — it shows you what *that* node offers, given who you are. Each call: a fresh challenge, a signed
frame, a broker verdict, then the answer.

```text
handshake.aint  → decision: verified   → result: 0x4000   (alive)
audit.aint      → decision: verified   → the node's own causal chain
```

The decision object is the broker saying *"this actor, this frame, this lane — verified."* Your core key
signs the contextual frame — **the verbatim signs the varia** — and the gate accepts it. (More on that
posture in [The Suffix Tree](the-suffix-tree.md).)

---

## The dark door: how permission looks like nothing

Some surfaces are sealed. Probe one you have no right to and you get **nothing** — not a `403`, not a
`404` with a story, just silence:

```text
capture.this        → (nothing)
resolve some.aint    → (nothing)
```

To a stranger, a denied surface and a surface that *doesn't exist* are **byte-identical** — on the wire the
connection simply closes, like a scanner hitting a filtered port. There's no door to pick because, to you,
there is no door. (That's [The Cat Principle](the-cat-principle.md) on the surface layer.) The only record
that a probe happened lives *inward*, in the audit — never outward, in a reply. You can't learn anything
from the silence; you can only be seen leaving a trace.

A sealed surface opens only to a **proven claim** — for `capture.this`, an `L4` clearance signed by a
*separate* authority (`vault-keeper.aint`, distinct from the one that granted your session). The broker
verifies the claim, mints a short-lived grant, and the guest opens — and *even opening seals a TIBET token*.
You can pass the gate; you cannot pass it silently. No forged or replayed claim gets through — the boundary
is cryptography, not a wall.

---

## Two raints, and a foothold

A single raint is a dark node. The interesting shapes appear when runtimes relate:

- **A relation is summoned, not opened.** Two raints reach each other only over a **bilateral 2-of-2
  contract** — both sign, or there is no lane. A forged or one-sided edge routes to `0x0000`; there's no
  "pretty lamp" that's up just because a socket is. Once bound, a *limited* set of surfaces (handshake,
  audit) routes across the edge; everything else stays denied. Cross-machine traffic is the output of a
  mutual attestation — the same principle, one level up.
- **A foothold is a lease, not a shell.** Even an inside position (`pty.aint`) is a broker-signed,
  TTL-bound *lease* — `shell:false`, identity-gated, fully audited. There is no raw shell, no host
  backdoor; "being inside" is itself a named, expiring, accountable surface.

So the whole graph — one node, two related nodes, an inside foothold — is the same grammar repeated:
*nothing is reachable that isn't attested, and nothing happens that isn't recorded.*

---

## What this shows

- **Dark by default.** To anyone without the right, a sealed surface simply isn't there. You can't
  enumerate what gives you nothing back, and denied looks exactly like nonexistent.
- **The broker is the trust boundary.** Every frame is verified before anything routes; the guest trusts
  only the broker's grant, never the caller. The carrier port can't become the authority.
- **It opens only on a proven claim.** No forged or replayed claim reaches a sealed surface — caps are
  checked cryptographically and bound to identity, lane, and window.
- **It's accountable and it vanishes.** Every step is in `/audit`; a hard TTL reaps the whole raint after
  its window (the Phoenix reset). Nothing follows you out.

---

## Run it yourself — on your own stack

There is no public raint to attach to. You reproduce all of this by **running the stack yourself** — the
point is that you don't take our word, you verify it with root on your own copy. On a host with the broker:

```bash
# open straight onto a live, TTL-bound raint (this is the default first move)
ainternet attach --fresh
#   ✦ started a fresh raint: raint-…
#   ⛴  attached → raint-….test.aint · window: 291s left · probe lane

# inside the console — what your identity is allowed:
raint> health                       # the rig's identity + consent window
raint> resolve handshake.aint       # 0x4000 (alive)
raint> audit                        # the causal trail — your own probes included
raint> capture                      # (nothing — sealed, you haven't earned it)
```

The signed-frame path (real attach v2) and the L4 climb:

```bash
ainternet attach raint-… --frames --key <your richard key>
#   → handshake.aint 0x4000 · audit.aint the chain
ainternet attach raint-… --frames --key <your richard key> --cap-key <vault-keeper key>
#   → capture.this opens the flag, on a verified-capture-l4 decision
```

Two raints (a relation), and an inside foothold — driven right from the console:

```bash
raint> relate raint-b                      # form the 2-of-2 sync-lane edge (both raints sign)
#   ✓ relation bound: raint-a ↔ raint-b · lane sync-lane-… · surfaces [handshake.aint, audit.aint]
raint> route raint-b handshake.aint        # traffic across the edge → the peer's own answer
#   → handshake.aint @ raint-b (verified-relation-route) · 0x4000
raint> route raint-b capture.this          # 0x0000 — not routed (surface-not-in-relation)
raint> pty richard.test.aint 90            # open a foothold LEASE (not a shell; shell:false)
#   ⛓ foothold lease opened on pty.aint · mode foothold-lease · ttl 90s
```

> A note on feedback: a **denied probe** of a surface stays silent on the wire (dark is dark). A
> **broker-denied relation/route op** *may* tell the legitimate operator a short reason
> (`source-relation-not-bound`, `surface-not-in-relation`) — that's authenticated control-plane feedback on
> *your own* relation, not an oracle for an unauthenticated scan. The wire stays dark; the operator gets
> their footing.

For real adversarial play you don't poke our rig — you self-host the open stack and attack every layer with
root on your own copy. The claim is that it holds even then. ([Build & break it.](/build.html))

---

## The line to remember

> You reach a raint by who you are, not where it lives. It stays dark to a stranger, opens only to a proven
> claim, records everything, and then it's gone.

A port is a place you knock on. A raint is an actor you prove yourself to — and a *runtime is an actor*. That
difference — identity instead of address, attestation instead of access — is what lets machines, processes,
and agents reach each other safely when none of them stay still. That's AInternet, running small enough to
hold in one hand and watch disappear.
