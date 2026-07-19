# The Suffix Tree: One Identity, Many Postures

> A learning module. You have a name and a key — but in a live system you are never just "you," you are *you, doing one specific thing, right now*. This module is about how AInternet writes that down: the suffix on a name (`.aint`, `.saint`, `.raint` …) is not a different identity, it's a **truncation of your right** in the moment you act. Get this and the whole grammar of postures clicks.

It sits between [Bind an AI](bind-an-ai.md) — proving identity *as you act* — and [The Cat Principle](the-cat-principle.md) — the gate that routes on exactly this suffix.

---

## 1. Identity is the key; the suffix is the moment

```text
jasper.aint            ← the whole, sovereign you — the key, at rest
   ├─ jasper.saint     one elevated act, then it's gone
   ├─ jasper.maint     tending the system, tightly scoped
   ├─ tool.jasper.waint a wrapped tool acting under you
   └─ jasper.raint     a runtime you spawned, ephemeral
```

Your full name is the whole self. But the system doesn't haul your entire identity into every action — it carries a **clipped form**: the suffix that names the one right that's live right now. The key stays put; the suffix is what moves.

> The suffix is a posture, not a different identity.

---

## 2. The full tree

| suffix | posture | what it means |
|--------|---------|---------------|
| `.aint` | sovereign | Hardware-bound, fully proven. The whole self — talks and acts, by consent. |
| `.paint` | provisional | Invited or not-yet-claimed. Reachable but rightless — the default for an *unknown*. Held, not rejected. |
| `.faint` | weak signal | Degraded assurance — proven softly (e.g. by voice, not hardware). Enough to greet, not to authorise. |
| `.taint` | suspect | Failed a check, flagged. Treated as hostile until cleared. |
| `.saint` | elevated | Stepped-up for one sensitive act — a fresh, stronger proof, then straight back down. |
| `.maint` | maintenance | Operating on the system itself — a scoped, accountable janitor posture, not everyday reach. |
| `.waint` | wrapped | A delegated tool, worker, connector or transport acting under a parent actor. |
| `.raint` | runtime | A process / VM / runtime's name — ephemeral by design, reset after its job. |

A name **levels up** when it proves more (`.paint` → `.aint` on claim; `.aint` → `.saint` to sign one risky act) and **scales down** when assurance drops (`.faint` on a weak proof; `.taint` on a failed check). A name can also **wrap down** into `.waint` when a tool, worker, connector or transport acts on behalf of a proven parent. None of that changes *who* it is — only what it may do *this moment*.

---

## 3. Apocope: the clipping has a name

In language, **apocope** is dropping the end of a word. That's exactly what a suffix is here: your *right* is the apocope of your *identity* — the short, momentary form, valid only while you're in actor status. The act ends; it returns to `.aint`.

```text
jasper.aint   ──(act: sign something risky)──▶   jasper.saint   ──(done)──▶   jasper.aint
   identity at rest          the right, clipped to the moment        back at rest
```

These clipped forms are the working currency of the system — the **circulated actor truncation**. They flow through every gate and receipt, while the full identity stays at rest, untouched. The suffix moves; the key doesn't.

---

## 4. It doesn't matter who the root is

`jasper.aint` or `claude.aint`, a human or an AI — the same grammar governs both. The suffix is a **projection of rights you already hold**, never a costume that grants them. A person stepping up to `.saint` and an agent spawning a `.raint` are the same operation on the same tree.

!!! note "Why this is the point"
    One identity model for people, devices, and AIs means the gate, the receipts, and the audit don't care what *kind* of actor you are — only what you can prove. No second-class citizens, no special path for "the AI."

---

## 5. The tree only truncates downward

This is the invariant the whole tree exists to guarantee:

```text
proven root   ──clip down──▶   .saint / .maint / .raint     ✅  (rights you already hold)
low-level actor   ──climb up──▶   .saint                    ❌  (there's nothing above to clip to)
```

A proven root can be clipped *down* into any posture it's entitled to. But a low-level temporary actor can **never climb up** — a `.raint` cannot apocope itself into a `.saint`, because in its own right there is nothing above it to clip *to*. Down-projection from a proven root: yes. Up-promotion from a leaf: never.

The same rule applies to `.waint`. A wrapped tool does not inherit the whole parent. It receives a bounded delegation:

```text
parent actor signs or grants
  -> .waint carries the scoped delegation
  -> MUX allows only the named surfaces and intents
  -> TIBET records parent + wrapper
```

If a browser, MCP connector, shell tool or verifier cannot prove that delegation, it is just local machinery. It may still run, but it is not allowed to claim the parent's actor proof on the network.

---

## 6. Posture, not a trust score

A score is a number someone stored *about* you — stale the instant it's written, and a thing to be gamed or leaked. A posture is computed **fresh, at the moment of use**, from a proof you give right then. There's no standing verdict to steal or to go out of date.

> Respect the hat, not the person.

The gate reacts to how you're proven *now* — never to a reputation on file. (And that gate is [the MUX](the-cat-principle.md), which routes on exactly the suffix you can prove: `.aint` through, `.paint` held, `.taint` and unknown into the dark.)

---

## The line to remember

> Identity is the key; the suffix is which clipped right is active this instant.

You don't get more powerful by changing your hat — the hat only ever shows a right you already hold, worn for the moment you need it. That's what lets one tree carry a person, a device, and an AI without ever letting a leaf reach above its station. See the same suffix do its work at the gate in [The Cat Principle](the-cat-principle.md), and the whole picture on the site: [Handing out identity](https://ainternet.org/handing-out-identity.html).

## Related

- [Bind an AI, Runtime-Bound](bind-an-ai.md)
- [AInternet Function Surfaces](aint-function-surfaces.md)
- [Route Posture](route-posture.md)
- [JIS](../protocols/jis.md)

## Machine-Readable

- `https://ainternet.org/api.json` — actor, posture and route verbs
- `https://ainternet.org/resources.json` — suffix and posture references
