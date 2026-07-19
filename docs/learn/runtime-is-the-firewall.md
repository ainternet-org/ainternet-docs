# Runtime Is The Firewall

> A learning module. If you remember one thing about how AInternet contains an AI actor, make it this: **the prompt is not the security boundary — the runtime is.** An actor is bound to a `.aint` identity and a posture, and what it can reach is decided by the substrate around it (SNAFT, MUX, the sandbox), not by instructions you wrote in a system prompt and hope it obeys.

Prompt-level rules ("do not access the filesystem", "never call external APIs") are guidance to a model that is free to reason its way around them. Treating that as your firewall is treating a *suggestion* as a *wall*. AInternet puts the wall where a wall belongs: below the model, in the runtime, where it holds whether the model cooperates or not.

```text
        prompt policy   ──  guidance to a mind that can reason around it   (NOT the boundary)
        ─────────────────────────────────────────────────────────────────
        runtime floor   ──  SNAFT · MUX · sandbox · posture                (THE boundary)
```

---

## The actor sees only its floor

When an actor runs, it does not run "on the box." It runs inside a floor the box builds for it, and that floor is deliberately small:

- **no `/srv`**, no host configuration, no other actors' state;
- **no host devices**, no raw disk, no executable path outside the sealed image;
- only the surfaces its identity was granted, at the posture in force.

What isn't on the floor doesn't exist for the actor — not "forbidden," simply absent. There is nothing to escalate *to*, because the host isn't in view. (This is the same instinct as [The Cat Principle](the-cat-principle.md): the strongest protection is the door not being there.)

You can watch this in the dot-folders. An actor's floor holds its own working area — a bound `codex` actor sees `.codex` — but the key material, `.humotica-keys`, is **not in its view at all**. Same disk, one folder present and one absent, decided by the runtime, not by trust. The box **routes** keys for the actor; it never hands them over. Keys stay human-owned and out of reach ([Keys Never Leave Your Machine](keys-never-leave.md)) — the box is a key-router, not a vault. [Dot Maps and Safe Floors](dot-maps-and-safe-floors.md) walks the whole visible/absent picture, folder by folder.

---

## Three enforcers, one below the model

The boundary isn't a single check; it's a small stack the model never sits above:

| Layer | Enforces |
|---|---|
| **SNAFT** (consent) | whether an action is consented under the current posture — fail-closed by default |
| **MUX** (routing) | what an identity can even reach; dark-by-default, routes on proven posture |
| **Sandbox** (isolation) | the process floor: no host paths, no devices, memory it cannot escape |

Each reads facts, not promises. None of them asks the model whether it intends to behave.

---

## Different actor shapes, different runtime binding

"Runtime is the firewall" is not one-size-fits-all — the binding matches the actor's shape:

```text
local model   →  loopback only; carries with no egress at all
LAN model     →  reaches a named host on the local network, nothing beyond
online API    →  egress to one keyed endpoint, only after posture is raised AND egress granted
external CLI  →  a bound PTY under a grant; egress fails closed until explicitly opened
```

A Codex CLI actor whose traffic would go to `api.openai.com` sits at `0x0000:egress-not-permitted` under a local-only posture — not because a prompt told it no, but because the runtime will not route it. Raise posture, grant egress, and the route opens. Same actor, different runtime facts.

```sh
box provision status --json   # posture, granted surfaces, and what each actor may reach
```

---

## Why this matters for anyone building governance on top

If your security depends on the model choosing to follow instructions, a cleverer prompt defeats it. If it depends on the runtime, a cleverer prompt changes nothing — the reasoning is still free, but the *action* still meets the same floor. That is what makes an external governance layer safe to stack here: it plugs in above a boundary that already holds, instead of re-implementing containment in prose. See [Where Execution Governance Plugs In](where-execution-governance-plugs-in.md).

---

## Try it

See the floor an actor actually gets — its posture, granted surfaces, and what each may reach:

```sh
box provision status --json      # posture floor + granted surfaces, per actor
box bind codex                   # external CLI actor → 0x0000:egress-not-permitted under a local-only posture
```

Raise it deliberately, never by default — sandbox is the default; `--no-sandbox` is a loud, receipted dev escape, not a habit:

```sh
box provision set-snaft NORMAL   # raise the posture floor
box grant egress codex.aint      # then open egress for the declared actor (.aint, not .waint)
box bind codex                   # now the same actor carries
```

Machine surface: [`ainternet.org/api.json`](https://ainternet.org/api.json) lists the actor / route / grant verbs an AI can call directly.

## Related

- [Reasoning ≠ Execution](reasoning-not-execution.md) — why the model reasons freely but acts only through a verb.
- [Actor Seal](actor-seal.md) — how a bound session opens, runs, and seals.
- [CRUST Runtime](crust-runtime.md) — the sealed-memory floor the sandbox stands on.
- [SNAFT](../protocols/snaft.md) · [MUX](../protocols/mux.md) — the enforcers, in protocol detail.
