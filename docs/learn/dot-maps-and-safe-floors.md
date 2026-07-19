# Dot Maps and Safe Floors

> A learning module. A sandbox should not only be safe; it should *feel*
> readable. Dot maps are the small visible clues that tell an operator what an
> actor can see, what it cannot see, and why absence is protection.

Everything here starts with **who is acting**. An actor is a bound `.aint`
identity (via JIS), acting on behalf of a human `.aint` — not an anonymous
process. That identity is what the floor is built *for*.

When such an actor opens inside AInternet-in-a-box, it is not dropped onto the
host. It receives a small floor: a set of mounted paths, dot folders, key
references and runtime surfaces that were deliberately granted **to that
identity**, and nothing else.

That floor is a language:

```text
.codex exists          → this actor has its own runtime state
.humotica-keys absent  → provider keys are not visible here
/srv absent            → the host workspace is not on this floor
```

This is not cosmetic. It is the operator-facing proof of containment. You do
not have to trust a prompt that says "I will not read `/srv`" if `/srv` simply
does not exist in the actor's filesystem view.

---

## Visible Means Granted

A dot map is the actor's local map of itself. It may include runtime state such
as `.codex`, `.claude`, `.gemini`, `.tcli` or an actor-specific audit directory.
It may include a materialized key reference for the current session.

It should not include broad host secrets.

```text
visible      granted for this runtime
absent       not granted, not reachable, not a hidden challenge
keyref       a reference to a key, not the key copied into the sandbox
```

The important distinction is between *reference* and *secret*. An online actor
may need a provider keyref so the box can open one allowed route. That does not
mean the actor gets a folder full of human secrets. It receives only the
runtime shape the box admitted.

---

## Absence Is Information

From inside a contained actor, missing paths are evidence:

```text
ls /srv
# no such file or directory
```

That result is not a bug. It says the host workspace was not mounted into this
actor's floor.

```text
ls ~/.humotica-keys
# no such file or directory
```

That says provider keys were not exposed as ordinary files.

```text
ls ~/.codex
# present, if this is a Codex runtime with granted state
```

That says the runtime-specific state exists on this floor. It does not imply
access to the operator's whole home directory.

The safest UI can show the same thing in plain language:

```text
Runtime floor
  .codex          visible
  .humotica-keys  absent
  /srv            absent
  provider key    keyref only
```

Small words, hard boundary.

---

## Why Dot Maps Matter

They turn containment from an abstract security claim into something an
operator can inspect:

| Question | Dot-map answer |
|---|---|
| Can this actor see my host workspace? | `/srv` absent |
| Can it read all provider keys? | `.humotica-keys` absent |
| Does it have its own runtime state? | `.codex` / `.tcli` visible |
| Is this key copied into the sandbox? | keyref visible, secret absent |
| Is a missing path a failure? | only if the declared runtime required it |

This is the same doctrine as [Runtime Is The Firewall](runtime-is-the-firewall.md),
but in filesystem form: the runtime floor decides what exists before the model
can ask for it.

---

## The Mini Language

Use this language in CLI, TUI and cockpit surfaces:

```text
visible     this path/surface was deliberately placed on the floor
absent      this path/surface is not part of the actor's world
keyref      the box can use a key without copying the secret into the actor
sealed      the runtime state has a clean closure receipt
stale       the runtime opened but did not leave a clean seal
```

Avoid words that imply a hidden reachable thing:

```text
blocked from /srv       weaker: suggests /srv is there behind a door
/srv absent             stronger: the floor does not contain it
```

An actor cannot exfiltrate a path that is not mounted. A prompt cannot browse a
directory that is not there. The dot map is how the box says that out loud.

---

## Related

- [Runtime Is The Firewall](runtime-is-the-firewall.md) — the broader boundary.
- [Keys Never Leave Your Machine](keys-never-leave.md) — why key material stays home.
- [Actor Seal](actor-seal.md) — how a runtime closes with proof.
- [The Cat Principle](the-cat-principle.md) — absence as protection.
