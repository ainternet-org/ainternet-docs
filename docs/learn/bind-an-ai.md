# Bind an AI, Runtime-Bound

> A learning module. Your network stands: identity, routing, consent, evidence. Now you want an AI to actually *do* things in it. This module is about the moment that matters most — how you let an agent act **without turning it into a black box with hands**.

This is the hinge between "my network exists" and "something acts online inside it." Get it right and an AI is a *resident with a key*. Get it wrong and it is an anonymous process with your permissions.

---

## 1. The trap: the bolted-on AI

The common pattern is to hand an AI an API key and hope:

```text
agent  ──(API key)──▶  do anything the key allows
```

A key is a **bearer** — whoever holds it is assumed to be the owner. But:

> A bearer is never an authority.

A leaked key, a copied token, a prompt-injected agent — all of them *hold* the key, so all of them *are* the owner, as far as the system can tell. The AI acted, but you cannot say **who** acted, **under which policy**, or **whether you can prove it afterwards**. That is a black box with hands.

---

## 2. Runtime-bound, not bolted-on

Binding an AI runtime-bound flips this around. Identity is not handed out once at setup and trusted forever — it is **proven at the moment of action**.

```text
bolted-on:     prove once at install  →  trusted forever (a bearer)
runtime-bound: prove per action       →  trusted for this act only (an actor)
```

The agent carries its own identity *into* every action, and the network checks it *as it acts*. Steal the key at rest and it is useless without the fresh proof. An action without identity is just traffic — and traffic does not get to act.

---

## 3. The four wires of "bind"

To bind an AI as a real actor, you wire four things. None of them is optional; together they turn "it ran" into "this actor did this, allowed, and here is the proof."

| Wire | Primitive | What it does |
|---|---|---|
| **Identity** | JIS | the agent gets its *own* `.aint` / key — it acts **as itself**, not as the operator |
| **Intent before action** | TIBET | a receipt is emitted *before* the act (what it intends), linked to completion *after* |
| **Consent at the gate** | SNAFT / Cortex | decides *before* the action runs — allowed? under which policy? |
| **Isolation** | Airlock | the runtime cell is contained — misbehavior is boxed, not loose on your network |

Notice the order. Identity comes first (who), then intent (what it means to do), then consent (may it), then isolation (and if it goes wrong, it is contained). Each wire answers a question the previous one opened.

---

## 4. The shape, walked through

Here is one full action by a bound agent, start to finish:

```text
1. address your first node      → the agent reaches the network as agent.local / your-agent.aint
2. it proves who it is          → fresh JIS proof for THIS action (not a stored token)
3. it proposes an action        → "send this", "read that", "call this number"
4. TIBET records the intent     → receipt e1: who + what + policy + route, signed
5. the gate decides             → SNAFT/Cortex: allowed under policy? yes → continue / no → stop
6. it acts inside an Airlock    → the runtime cell runs the action, contained
7. TIBET records completion     → receipt e2 embeds e1: what actually happened
8. evidence lands               → the chain e1→e2 is now provable, forever
```

Steps 4 and 7 are the same causal chain you met in [Causality: Lamport → TIBET](causality-lamport.md): `e2` embeds `e1`, so "intended" and "happened" are cryptographically linked. The agent did not just act — it left a signed trail of *why* and *what*.

---

## 5. Why runtime-bound is the safe way

- **A stolen key is not enough.** Possession at rest cannot produce the fresh per-action proof. The thief holds a key to a door that asks "but who are *you*, right now?"
- **An action without identity is dropped.** The MUX gate routes proven, related actors — everything else meets `0x0000`, silence. Even an autonomous AI kill-chain cannot act without a valid causal receipt: no receipt, no route.
- **The agent is contained by default.** Airlock means a misbehaving or compromised agent damages its cell, not your network.
- **You can always prove it afterwards.** Every act the agent took is a signed link in a chain you can walk backwards.

The result: the AI is a **first-class resident** — it has a name, a key, a policy, and a paper trail — instead of an anonymous process wearing your credentials.

---

## 6. Start on a network of one

You do not need the public hub for any of this. Your **home-agent**, bound to a local `.aint`, proving per action, receipted and airlocked, is the whole pattern at the smallest scale:

```text
operator.local  ──grants──▶  home-agent.local  ──acts (bound)──▶  audit.local
```

One operator, one bound agent, one evidence node. That is a complete, safe agentic loop — local, private, provable — before a single outside actor enters.

!!! note "The agentic era, made accountable"
    The hard question of the agentic era was never "can an AI do this task?" It was "who authorized this, under which policy, and can I prove the chain?" Binding an AI runtime-bound is how you answer it — at the moment of action, not as an afterthought.

---

## Where this sits

- Comes after [Causality: Lamport → TIBET](causality-lamport.md) — the receipts in step 4/7 are that causal chain.
- Leads into **Everything Falls Back to TIBET** — why the proof under all of this is always there.
- Hands-on: the [`tibet-home-agent`](https://pypi.org/project/tibet-home-agent/) package and [Build Your Network](../network/build.md).

## Machine-Readable

- `https://ainternet.org/api.json` — actor binding, route and audit verbs
- `https://ainternet.org/resources.json` — identity and runtime-binding references
