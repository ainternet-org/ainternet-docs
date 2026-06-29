# Models Are Mounted Artifacts

> A learning module. A runtime is one process that swaps which model it wears. So the model is **not** the identity — the process is. This module is about attributing an AI action to *which actor, running which brain, under what intent* — provably.

Companion to [The Suffix Tree](the-suffix-tree.md), [Keys Never Leave](keys-never-leave.md) and [The Running Substrate](the-running-substrate.md).

---

## The shape of every local-AI runtime

Ollama, Antigravity, a llama.cpp server — they're all **one process with a model hung off it**, swapping which model is loaded. In an hour the same process can be running Claude, then gpt-oss, then a 32B. That single fact decides how you attribute an action:

- **The process is the actor.** It holds the `.aint` key (an `.aint` at rest, a `.raint` in motion). It signs.
- **The loaded model is a mounted `.waint`.** It's a tool the actor wears, not a sovereign actor. A model file can't sign — it's weights.

So `gravity.aint`-running-Claude and `gravity.aint`-running-gpt-oss are the **same key, a different brain**. If a receipt only says "gravity.aint did X", you've lost *which brain spoke*.

## Attest the model by reference

A model can't hold a key, so you bind it the way you bind any tamper-evident artifact: by **content hash**. The mounted model carries an **`.oom` content-hash**, recorded in the receipt at the moment of action:

```text
gravity.aint, model = claude@<oom-hash>, intent = summarise, → did X   ✔ signed, fresh
```

Two rules keep it honest:

1. **Record it fresh, at action time** (JIS-style) — so one process can't later claim a *different* brain produced an output.
2. **The hash is verified, not asserted** — the `.oom` artifact is checked at the airlock, the same doctrine as [magic bytes, not filename](keys-never-leave.md).

This is the runtime/telemetry-provability that matters for the wider standards world: a log line is no longer a self-asserted string, it's *which actor + which model + which intent*, re-checkable.

---

## `.oom` — a model file that is more than weights

`.oom` is the [TBZ/`.tza`](the-running-substrate.md) family applied to a model: its own magic bytes (sniffable by `continuityd`/the trust kernel), a signed manifest, optional chunks for TIBET/JIS provenance, a required `.caint` context, and a hard **`contains_private_key = false`** that is *structurally proven at the airlock, never a trusted flag*. The pipeline is honest about trust direction:

```text
GGUF / safetensors   = import (untrusted)
gguf2oom             = airlock (sniff → verify → seal)
.oom                 = sovereign runtime artifact
```

!!! note "Built vs experimental — no oversell"
    The **gold is the converter**: if `gguf2oom` only adds TIBET/JIS provenance, it *makes your local AI auditable* — an audit stamp, not an inference engine. The **OomLlama runtime** that loads `.oom` is **early and slow** (layered, not performance-ready) — and that's fine, because the format's soundness is *independent of inference speed*. We don't claim "fast"; we claim **sovereign and provable**.

> **A model file can be more than weights: a sovereign, sniffable, auditable AI artifact.**
> The format opens the door; the runtime is early. The primitive that matters is the artifact contract.

## Related

- [The Running Substrate](the-running-substrate.md)
- [Keys Never Leave Your Machine](keys-never-leave.md)
- [Airlock](../protocols/airlock.md)
- [Transfer Carriers](../reference/transfer-carriers.md)
