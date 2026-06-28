# Causality: From Lamport to TIBET

> A learning module. No central clock, no central authority — yet you can still prove *what happened before what*. This is the idea that makes a decentralized, zero-trust network possible at all. Lamport formalized it in 1978; TIBET makes it cryptographic and signed.

This module is self-contained. If you understand it, you understand why AInternet records **causal receipts** instead of timestamps, and why "a log without TIBET is only a claim after the fact."

---

## 1. The problem: there is no global clock

In a decentralized network there is no single authority and no shared wall-clock. Two machines never agree perfectly on the time, and you cannot trust a timestamp that another actor wrote for itself. So this question becomes hard:

> Did event **A** happen before event **B**, or were they concurrent?

If you cannot answer that, you cannot order actions, detect conflicts, or prove a causal chain after an incident. A central time server would "solve" it — by making everyone trust one box. That is exactly what a zero-trust network refuses to do.

So we need ordering that comes from **local facts and message passing**, not from a trusted center.

---

## 2. Lamport's happened-before (`→`)

Leslie Lamport defined a relation called **happened-before**, written `→`, using only three rules:

1. **Same actor, in order.** If `A` and `B` happen in the same process and `A` comes first, then `A → B`.
2. **Send before receive.** If `A` is *sending* a message and `B` is *receiving* that same message, then `A → B`.
3. **Transitivity.** If `A → B` and `B → C`, then `A → C`.

If neither `A → B` nor `B → A`, the events are **concurrent** — there is no causal relationship between them, and no honest observer can put them in a strict order.

That is the whole foundation. Notice what it does **not** need: no synchronized clocks, no central server. Causality is derived from "same actor" + "this message caused that one."

---

## 3. Logical clocks: counting causality

To work with `→` in code, give every actor a counter `C` (a **logical clock**):

```text
on a local event:        C = C + 1
on sending a message:    C = C + 1 ; attach C to the message
on receiving a message:  C = max(C, received_C) + 1
```

Now if `A → B`, then `clock(A) < clock(B)`. The counter respects causality without any real time.

The catch: `clock(A) < clock(B)` does **not** prove `A → B` — they might just be concurrent events that happened to get those numbers. Logical clocks give you a *consistent total order*, but they blur the difference between "caused" and "merely concurrent."

---

## 4. Vector clocks: true causality + concurrency detection

To capture *real* causality (and to *detect* concurrency), each actor keeps a **vector** — one counter per actor it knows about:

```text
on a local event:        V[self] = V[self] + 1
on sending:              V[self] = V[self] + 1 ; attach the whole vector V
on receiving V_in:       for each k: V[k] = max(V[k], V_in[k]) ; then V[self] += 1
```

Compare two vectors:

- `A → B`  iff every component of `V(A)` is ≤ `V(B)` and at least one is strictly less.
- **Concurrent** iff neither vector dominates the other.

Vector clocks tell you not just *an* order, but *who knew what when* — and they can prove two events were independent. This is the layer that catches drift and conflict.

> In AInternet this is the **Causal TimeVector** layer: a vector-clock over actors so multiple agents can act in parallel and the system can still tell causal chains apart from coincidence.

---

## 5. The bridge: TIBET is a signed happened-before chain

Here is the convergence. A TIBET causal receipt is exactly Lamport's `→`, made **cryptographic**.

Each event `Eₙ` embeds the hash of the previous event `Eₙ₋₁` and is signed by the actor's hardware-bound key:

```text
bodyₙ = domain ∥ actor_id ∥ mode ∥ principal ∥ action ∥ target
        ∥ capability ∥ policy ∥ Eₙ₋₁ ∥ nonce ∥ ttl
sigₙ  = Sign_key(bodyₙ)
Eₙ    = Hash(domain ∥ bodyₙ ∥ sigₙ)
```

The `∥ Eₙ₋₁` term **is** rule #1 (same actor, in order) — but now it is a hash link, not a counter, so it cannot be reordered or forged after the fact. When the message crosses to another actor, the receiving chain embeds the sender's `Eₙ`, which **is** rule #2 (send before receive). Transitivity (rule #3) follows the hash chain.

| Lamport (1978) | TIBET |
|---|---|
| happened-before `→` | hash-linked event chain (`Eₙ` embeds `Eₙ₋₁`) |
| logical clock counter | monotonic causal reference, but tamper-evident |
| vector clock | Causal TimeVector (per-actor vectors) |
| "ordering without a global clock" | "provenance without a central authority" |
| ordering you *assume* is honest | ordering you can *cryptographically verify* |

TIBET also records what a bare counter never could — the **context** around the event:

| Dimension | Meaning |
|---|---|
| `ERIN` | what is *in* the action (payload, object) |
| `ERAAN` | what is *attached* (references, dependencies) |
| `EROMHEEN` | what is *around* it (environment, policy) |
| `ERACHTER` | what is *behind* it (intent, reason) |

So a TIBET chain answers Lamport's "what happened before what" **and** "who authorized it, under which policy, with what intent."

---

## 6. A worked micro-example

Two actors on a local network: `agent.local` and `audit.local`. No shared clock.

```text
agent.local                              audit.local
-----------                              -----------
e1: decide to act        (C=1)
e2: send request  ──────────────▶  e3: receive request   (C = max(0,2)+1 = 3)
                                        e4: write evidence       (C=4)
e5: receive ack   ◀──────────────  (ack carries C=4 → e5: C = max(2,4)+1 = 5)
```

Happened-before facts you can now prove:

- `e1 → e2` (same actor, in order)
- `e2 → e3` (send before receive) ⇒ `e1 → e4` by transitivity
- `e4 → e5` (audit's evidence causally precedes agent's ack)

In TIBET terms: `e2` is an *intent* receipt signed by `agent.local`; `e4` is a *completion* receipt signed by `audit.local` that embeds `e2`'s `Eₙ`. After an incident you can walk the chain backwards and prove the **causal** order — not because a clock said so, but because each link is signed and hash-bound.

---

## 7. Why this matters for AInternet

- **Decentralized.** Causality comes from local facts and messages, never a central clock or authority. You can run a network of one household and still have provable order.
- **Zero-trust.** You never trust an actor's self-asserted timestamp. You verify the signed link instead.
- **Auditable.** "What happened before what" is a property you can *check*, not a story you tell afterwards.

!!! note "Intuition first, theory second"
    TIBET's causal receipts were built from first principles — the need to prove *what led to what* in an agentic system. They converge, after the fact, with Lamport's 1978 result and with vector clocks. That convergence is a good sign: the same idea, reached independently, holding from two directions.

---

## Further reading

- Lamport, L. (1978). *Time, Clocks, and the Ordering of Events in a Distributed System.* CACM.
- [TIBET (Provenance)](../protocols/tibet.md) — the protocol page.
- [Network Primitives](../network/primitives.md) — where TIBET sits in the stack.
- [Causal Action Receipts](https://ainternet.org/causal-action-receipts.html) — the `Eₙ` doctrine.
