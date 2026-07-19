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

## 7. The layered bind, in the box

The four wires above are the *why*. In AInternet-in-a-Box the *how* is a short, staged sequence — and it is staged on purpose: **boot is a phase boundary**, so there is no one-line `&&` chain that carries an actor from nothing to bound. You cross each layer deliberately, and each leaves a receipt.

```text
1. enroll        the box has a human/root identity, and the actor gets its own .aint
2. provision     posture floor is set; sandbox is the DEFAULT (not a flag you remember)
3. supply        for a model actor: its runtime is prefetched / staged / switched in
4. grant         only if the actor needs to reach out: open egress for the declared .aint
5. bind          the actor is admitted to act — a verdict, not a promise
6. seal          the session closes to a durable receipt (see Actor Seal)
```

A representative walk for an external CLI actor that needs to reach a provider — each step its own command, checked before the next:

```sh
box provision status --json         # where am I: posture, what's staged, what carries
box provision set-snaft NORMAL      # raise the posture floor, deliberately
box grant egress codex.aint         # open egress for the DECLARED actor (.aint — not .waint)
box bind codex                      # admit it → 0x4000, or 0x0000:<reason> if a fact is missing
```

Sandbox is the floor, always on. The dev escape is **explicit and loud**: `--no-sandbox` is receipted, never a habit and never remembered as a normal flag. If `box bind` returns `0x0000:egress-not-permitted`, the box is telling you a *fact* is missing (posture or grant), not asking you to try harder.

## 8. Four actor shapes, four bindings

"Bind an AI" is not one thing — the binding matches what the actor actually is. Locality matters: **loopback** (`127.0.0.1`) is not the same as a **private LAN host** (`192.168.x.x`), which is not the same as an **external provider** (`api.openai.com`).

| Actor shape | Reaches | Runtime binding |
|---|---|---|
| **Local model** | loopback Ollama / local API (`127.0.0.1`) | request-envelope only — no shell, no filesystem, no egress by default; `LOCAL_ONLY` carries it |
| **LAN model** | a named host on your private network (`192.168.x.x`) | needs explicit posture + grant + relation; loopback rules do **not** silently extend to the LAN |
| **Online API** | one keyed provider endpoint (`api.openai.com`) | a `keyref` + granted egress; the key is referenced, never pasted into the box |
| **External CLI** | a bound PTY + provider egress | runtime supply chain staged, egress granted, then bound; fails closed until both are true |

The local/LAN actor is a *request-envelope* to a model — it asks, it does not get a shell. The external CLI actor is the heaviest: it brings a runtime supply chain and reaches out, so it carries the most and is gated the hardest. Same verb, `box bind`; different facts required to reach `0x4000`.

A real local-model actor session, opened and sealed — note how the runtime **announces exactly what it is** before it does anything:

```text
$ ./box actor cli qwen.aint
  opening tcli as qwen.aint — /quit to seal · /models to list · audit -> …/actors/qwen.aint.tcli-state
qwen.aint · bound actor runtime
  on behalf of jasper.aint
  provider/model local/gemma4:26b (locked)
  runtime request envelope · no shell/fs/egress unless granted
  /models · /whoami · /trail · /clear · /verify · /seal · /help · /quit
qwen.aint› /quit
  ✓ session sealed (qwen.aint) · audit-head no-audit
```

Everything the actor is allowed to be is stated up front: it acts **on behalf of** a human `.aint`, its model is **locked**, and it is a **request envelope** — no shell, no filesystem, no egress unless granted. `/quit` seals the session to a durable receipt ([Actor Seal](actor-seal.md)); here the session did nothing, so its audit head is honestly `no-audit`.

And this `qwen.aint` local model runs **side by side** with a heavier `codex` external-CLI actor on the *same box* — a locked local model and an egressing CLI, two completely different systems, admitted by the same `box bind` verb and held to the same floor. An online-API actor binds the same way. One box, heterogeneous actors, one enforcement model.

## Try it

Watch a bind fail closed, then open it deliberately — the whole safety model in four lines:

```sh
box bind codex                   # 0x0000:egress-not-permitted  (a fact is missing)
box provision set-snaft NORMAL   # raise the posture floor
box grant egress codex.aint      # open egress for the declared actor
box bind codex                   # 0x4000 — same actor, changed facts
```

Machine surface: [`ainternet.org/api.json`](https://ainternet.org/api.json) — actor binding, grant and route verbs an AI can call directly.

## Where this sits

- Comes after [Causality: Lamport → TIBET](causality-lamport.md) — the receipts in step 4/7 are that causal chain.
- Leads into **Everything Falls Back to TIBET** — why the proof under all of this is always there.
- Hands-on: the [`tibet-home-agent`](https://pypi.org/project/tibet-home-agent/) package and [Build Your Network](../network/build.md).

## Machine-Readable

- `https://ainternet.org/api.json` — actor binding, route and audit verbs
- `https://ainternet.org/resources.json` — identity and runtime-binding references
