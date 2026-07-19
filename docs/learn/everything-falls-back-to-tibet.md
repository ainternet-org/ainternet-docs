# Everything Falls Back to TIBET

> A learning module — and the floor of the whole stack. Actors come and go, keys get stolen, agents misbehave, incidents happen. When everything above is in doubt, one thing is still standing: the signed causal record. This module is about *why proof is the ground you always land on.*

It closes the Learn arc. [Causality](causality-lamport.md) showed **why order holds** without a center. [Bind an AI](bind-an-ai.md) showed **how an actor acts** accountably. This one shows **why you can always prove it** — afterwards, under pressure, even when an actor lies.

---

## 1. The question this answers

Ask the worst-case question of any system:

> When something goes wrong — a node lies, a key is stolen, an agent goes rogue, an incident hits — what is *left* that I can still trust?

In most systems the honest answer is "the logs, if no one touched them." That is not trust; that is hope. AInternet's answer is different: **the receipts**. They were signed as things happened, hash-linked to each other, and they do not depend on the good behavior of whoever is talking now.

---

## 2. A log is a claim; a receipt is proof

This is the whole difference, and it is worth being blunt about:

| A log line | A TIBET receipt |
|---|---|
| written after the fact | emitted *as* the action happened |
| editable, append-anywhere | hash-chained — change one link, break the chain |
| self-asserted ("trust me") | signed by a hardware-bound key |
| an actor's *story* | an actor's *commitment* |

A log says *we think this happened*. A receipt says *here is the proof, and here is what it links to*. When you cannot trust the storyteller, only the second one survives.

---

## 3. Everything important emits a receipt

TIBET is not a side-channel you remember to call. The important acts across every primitive each leave a token, so the system's history is one continuous, provable fabric:

```text
JIS         identity claimed / key succeeded   → receipt
MUX         route opened / refused              → receipt
SNAFT/Cortex consent granted / denied           → receipt
the agent   intent → completion (Bind an AI)    → receipt
continuityd arrival / heartbeat                  → receipt
Wayback     snapshot taken                       → receipt
```

Because each is signed and each embeds the one before it (the [happened-before chain](causality-lamport.md)), the whole becomes a single fabric you can walk — not a pile of separate logs you have to correlate and hope agree.

---

## 4. The fallback property

Here is the part that makes it a *floor* and not just a feature:

- **When a higher layer fails, the truth does not.** A compromised service, a lying actor, a crashed node — none of them can un-sign what was already signed. You drop down to the receipts and the truth is intact.
- **When an actor lies *now*, the chain from *then* does not.** Identity is proven per action and recorded; a story told after the fact cannot overwrite a signature made before it.
- **After an incident, you reconstruct — you don't guess.** The causal chain *is* the forensic timeline. You walk it backwards: who acted, what they intended, which policy applied, what actually happened.

> A message without identity is just traffic. A route without policy is just reachability. **A log without TIBET is only a claim after the fact.** TIBET is the floor you land on when the claims run out.

---

## 5. Two floors: silence and proof

AInternet has *two* bedrock layers, and they protect different things:

- **The network floor — silence.** To a stranger, every `.aint` answers `0x0000`: nothing. The MUX absorbs floods and probes into that silence — internal or external, it makes no difference[^doppie] (see [Doctrine L0](https://ainternet.org/doctrine-l0.html)). Silence protects **reachability**: you cannot attack a door you cannot find.
- **The evidence floor — proof.** Every act that *did* happen left a signed receipt. Proof protects **truth**: you cannot rewrite what was already committed.

Nothing leaks (silence), and nothing is unprovable (proof). Those two floors under everything are why the higher layers are allowed to be flexible — they can fail soft, because the ground does not move.

---

## 6. A worked incident walk

Suppose an agent `agent.local` did something it should not have. You do not take its word for anything. You pull the fabric:

```text
e1  JIS    agent.local proved key K at 13:02            (signed)
e2  TIBET  intent: "send report to audit.local"          (signed, embeds e1)
e3  SNAFT  consent: ALLOWED under policy P-7             (signed, embeds e2)
e4  MUX    route opened agent.local → audit.local         (signed, embeds e3)
e5  TIBET  completion: report delivered, hash H          (signed, embeds e4)
```

You did not reconstruct this from five systems' logs and hope they line up. It is one chain, each link signed and embedding the last. You export it as a `.tibet.zip` and it verifies on someone else's machine. *That* is falling back to TIBET.

---

## 7. Why it matters

- **Auditable always.** Not "auditable if logging was on" — the fabric was always being written.
- **Compliance is a read, not a rebuild.** NIS2, the EU AI Act, an incident review — they are *queries against the fabric*, not reports you reconstruct after the fact. (This is where [Humotica](https://humotica.com) lives: reading this floor at production scale.)
- **The agentic era can be trusted.** Autonomy is only safe if every autonomous act is provable. The floor is what makes "let it act" survivable.

!!! note "The arc, closed"
    Lamport gave you *order without a center*. Binding gave you *action with accountability*. This gives you *proof as the floor under both*. Order → action → assurance. Everything falls back to TIBET, because TIBET is the one thing nothing above it can rewrite.

---

## Where this sits

- Closes the arc with [Causality: Lamport → TIBET](causality-lamport.md) and [Bind an AI, Runtime-Bound](bind-an-ai.md).
- The protocol page: [TIBET (Provenance)](../protocols/tibet.md).
- Hands-on: [Build Your Network](../network/build.md) — wire an evidence node and watch the fabric fill.

[^doppie]: The flood-absorbing silence has a co-author: **Doppie**, the household cat, who once strolled across the keyboard mid-incident and backspace-panicked the kernel flat. If my own cat can take me down from the inside, the fix has to catch a flood from *anywhere* — and `0x0000` does. Thanks, Doppie. 🐈

## Machine-Readable

- `https://ainternet.org/resources.json` — TIBET, carrier and evidence references
- `https://ainternet.org/api.json` — receipt verification and export verbs
