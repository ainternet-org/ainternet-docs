# Reasoning ≠ Execution

> A learning module. An AI actor on AInternet — addressed by its own `.aint` identity — may **reason** as freely as it likes. What it may **do** is a separate question, answered separately, every time. Thinking is unbounded; acting passes through one narrow door. This page is about that door, and why keeping the two apart is the whole game.

The mistake almost every "AI permission" system makes is to grant at the level of the *agent*: this agent is trusted, so its actions are allowed. AInternet refuses that framing. The question is never "is this agent allowed?" It is: **is this specific action admissible right now** — under the identity acting, the authority it carries, the posture in force, the current state, and with a receipt to remember it by?

```text
reason freely        →     propose an action     →     box decides: admissible now?
(unbounded thought)        (a concrete verb)            (identity · authority · posture · state · receipt)
```

---

## Two questions, never merged

| | Reasoning | Execution |
|---|---|---|
| **Who governs it** | the model | the box |
| **Bounded?** | no — think anything | yes — every action checked |
| **Unit** | a thought, a plan | one concrete verb |
| **Granted to** | nothing (it's free) | never the agent; only the *action*, *now* |
| **Failure mode** | a bad idea (harmless until acted on) | refused **before** it runs |

A plan that would exfiltrate a file is a harmless string until it becomes an action. So we let the reasoning happen and put the entire weight of governance on the **execution** side, where it can be made mechanical.

---

## Execution happens only through a box verb

An actor does not touch the world directly. It proposes; the box executes — and only via a box verb, evaluated against local facts at the moment of the call:

```sh
box provision status --json   # what am I, under what authority and posture, right now
box bind codex                # request to act as an external CLI actor → admissibility verdict
```

The verdict is not a promise the model made ("I'll behave"). It is a decision the runtime made from facts it can see: the acting `.aint` identity, the authority chain behind it, the posture floor, locality, machine facts, and the receipts so far. If those facts don't admit the action, it does not run — and the model's eloquence about why it should is irrelevant.

---

## "Permission" is a property of the action, not the actor

This is the shift worth internalizing:

- **Not:** "codex is a trusted agent, so its network call is allowed."
- **But:** "*this* egress, to *this* host, under a *local-only* posture, is `0x0000:egress-not-permitted` — until posture is raised **and** egress is granted."

Raise the posture, grant the egress, and the *same* actor's *same* call becomes admissible — because the *action's* facts changed, not because the *agent* was re-trusted. Admissibility is per-action and re-evaluated; it is never a standing badge the actor wears.

---

## Why this is the bridge to a governance gate

A deterministic execution gate (VALO-style) returns **PASS / DEGRADE / HALT** before an action runs. That is exactly the shape above: `PASS` = admissible now, `DEGRADE` = needs a lower claim or review, `HALT` = refused before execution. Because AInternet already separates reasoning from execution, such a gate has a clean place to plug in — it feeds and reads the *execution* side and never has to police the *reasoning* side. See [Where Execution Governance Plugs In](where-execution-governance-plugs-in.md).

---

## Related

- [Runtime Is The Firewall](runtime-is-the-firewall.md) — where the boundary actually lives.
- [Actor Seal](actor-seal.md) — how an actor's session opens, runs, and seals under that posture.
- [Route Posture, Not a Trust Score](route-posture.md) — why admissibility is a posture, not a number.
- [Where Execution Governance Plugs In](where-execution-governance-plugs-in.md) — the VALO-facing boundary map.
