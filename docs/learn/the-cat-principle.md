# The Cat Principle: Dark by Default

> A learning module. Every message into your system passes one gate — the MUX. This module is about the single decision that gate makes, and the doctrine behind it: **don't out-pattern the attacker, stop being a target.** It's the companion to [Keys Never Leave Your Machine](keys-never-leave.md) — the same idea, one layer up: there the strongest protection was a secret's *absence*; here it's the system's.

If [Keys Never Leave](keys-never-leave.md) kept the secret out of reach, this keeps the *door* out of reach. Together they're one principle worn at two layers.

---

## 1. The rule

```text
arrives, can prove itself   →  through, by consent
arrives, cannot prove        →  0x0000  (silence — nothing here)
```

The MUX is dark-by-default. To anyone who can prove themselves, your system is reachable, by consent. To everyone else, it simply **isn't there** — no banner, no error, no "access denied," nothing to confirm a door even exists.

> You can't pick a lock you can't find.

---

## 2. Meet the cat

A web application firewall reads every request and tries to *recognise* attacks: signatures, rules, heuristics — a forever game of catch-up where you are always one pattern behind whoever's knocking. Match the known-bad, hope you wrote enough rules.

The cat doesn't play that game. A cat in the garden doesn't inspect each visitor for bad intent and argue with the clever ones — to anyone it didn't invite, it's simply not interested in being found. You don't out-pattern an attacker; **you stop being a target.**

> cat beats waf.

??? note "Doppie's footnote"
    The doctrine is named for Doppie, who null-routes the garden uninvited and has never once filed a CVE. The cat principle is just her habit, written down.

---

## 3. WAF vs MUX

| | a WAF | the MUX |
|---|-------|---------|
| **asks** | "does this look like an attack?" | "what can you prove, right now?" |
| **reads** | the content, for badness | nothing — only the proof |
| **on no match** | lets it through | absorbs it: `0x0000` |
| **on bad** | returns an error (an *answer*) | silence (no answer at all) |
| **failure mode** | one pattern behind, forever | you must hold a valid key — there is no pattern to be behind |

A WAF is a wall that announces *"I am a wall — attack me cleverly."* The MUX announces nothing. The wall invites a contest; the dark declines to play.

---

## 4. Why silence, not an error

An error is information. `403 Forbidden` confirms there's something here, listening, worth attacking — it tells a scanner it found a door, and now it knows where to push. Every distinct error is a hint, and a thousand probes turn hints into a map.

`0x0000` is not an answer. No door, no service, no signal — the same nothing a scanner gets from empty space. That's the difference between a lock and **no enumeration oracle**: nothing the system says can be used to chart what it has. (See [Doctrine L0](https://ainternet.org/doctrine-l0.html) and the [MUX protocol](../protocols/mux.md).)

!!! tip "Honest where it's earned"
    Dark to the unproven isn't dark to *everyone*. A peer you've already proven a path with can get an honest signal — "I'm here," or even "that endpoint is gone." Silence is the default for the unknown, not a wall against your own.

---

## 5. The MUX classifies — it doesn't judge

The MUX is fast and stupid on purpose. It reads the posture an actor can prove — the [suffix it currently wears](https://ainternet.org/handing-out-identity.html) — and routes on that:

```text
.aint  proven    →  through, by consent
.paint pending   →  held in the airlock, not rejected
.taint suspect   →  0x0000
unknown          →  0x0000
```

That's classify-and-route, not interrogate-and-rule. The harder question — *is this proof actually good?* — belongs to the trust-kernel. Keeping the two apart is what lets the gate stay quick and silent while the judgement stays rigorous. The MUX is the knife at the door; it clips you to what you can prove and lets the dark swallow the rest.

---

## 6. One principle, every layer

The cat principle isn't a MUX feature — it's a habit the whole stack keeps:

| layer | the question | the cat's answer |
|-------|--------------|------------------|
| **keys** | how do we protect the secret? | don't hold it — [it never leaves your machine](keys-never-leave.md) |
| **network** | how do we protect the door? | don't announce it — `0x0000` to the unproven |
| **presence** | how do we protect who's home? | don't leak absence — silence isn't a status to read |

Each time, the strongest protection turns out to be **absence**: the secret that isn't there, the door that isn't there, the status that isn't there. You don't harden the target. You decline to be one.

---

## The line to remember

> A WAF makes you a cleverer wall. The cat makes you no longer a target.

The attacker's whole method is to learn your shape by poking it. Dark-by-default gives the poke nothing back — no error to read, no service to map, no key to lift. Everything above the gate can be open and provable, precisely because the gate gives nothing away.

## Related

- [MUX](../protocols/mux.md)
- [Keys Never Leave Your Machine](keys-never-leave.md)
- [Security Behavior](../operators/security-behavior.md)
- [Route Posture](route-posture.md)
