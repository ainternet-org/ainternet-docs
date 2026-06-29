# The Running Substrate

> A learning module. Under the concepts you've met — identity, provenance, posture, the gate — there's a substrate that actually runs, in two layers: a **Rust floor** of small kernels, and a **Python operator surface** above it. Same capability, two heights. This is a map of what's there, plainly described — the grander words, if anyone wants them, are for the community to add, not us.

It's the package-level companion to the conceptual modules: [The Suffix Tree](the-suffix-tree.md), [Keys Never Leave](keys-never-leave.md), [The Cat Principle](the-cat-principle.md), [Everything Falls Back to TIBET](everything-falls-back-to-tibet.md).

---

## Two heights, one model

```text
  Python operator surface   ← what you run and wire (tibet[full]: cap-bus, continuityd, audit …)
  ───────────────────────
  Rust floor (kernels)      ← the hardened cores (jis-core, tibet-core, snaft-core, *-kernel)
```

The Rust crates are the floor: small, hardened, embeddable. The Python packages are the operator surface above them. The higher layers can be *substituted* by the trust kernel without changing the model — identity and provenance stay the same all the way down.

---

## The two primitives

- **`jis-core`** — cryptographic identity where *intent comes first*: `jis:` URIs, `.aint` resolution, bilateral consent. The **who**.
- **`tibet-core`** — a forward-only causal substrate for provenance; *snapshot/restore is chain-position + fork, never time-rewind* (the forward-only rule, in the kernel). The **what**.

They're an OSAPI-pair — identity authority and evidence trail, designed to sit side by side, and each exists as a Rust kernel with a Python binding above it.

---

## The sealed format — `tibet-zip` (TBZ / `.tza`)

The on-disk and on-wire envelope: block-level authenticated compression with a TIBET envelope (`tibet-zip-core`), JIS identity binding and authorization (`tibet-zip-jis`), sandboxed decompression with eBPF kernel enforcement (`tibet-zip-airlock`), and a transparency mirror for distributed trust (`tibet-zip-mirror`), with a CLI to pack/unpack/verify/inspect. *(The short `tbz-*` crates are thin aliases of the same thing — read by [magic bytes, not filename](keys-never-leave.md).)*

---

## The kernel & runtime

- **`tibet-trust-kernel`** — the zero-trust foundation: authenticated encryption, integrity, sandboxed execution, cross-machine memory transport.
- **`snaft-core`** — the behavioural firewall kernel: intent verification before an action runs.
- **`tibet-airlock` / `tibet-airlock-kernel`** — a microVM sandbox that boots and attests in ~10ms with a cryptographic proof of every execution; the kernel crate is the hardened core beneath the Python operator surface. (This is the disposable enclave behind the [Arena](https://ainternet.org/build.html).)
- **`oomllama`** — a sovereign inference engine (`.oom` quantization, JIS routing, TIBET provenance) — *"the car where the trust kernel is the engine."*
- **`tibet-dgx`** — run LLMs across machines without NVLink (QUIC multi-stream + encrypted transport); **`tibet-store-mmu`** — transparent RAM virtualization (a `userfaultfd` proof-of-concept).

!!! note "Measured, not claimed — when security becomes the performance optimization"
    A counter-intuitive result, and a reproducible one: **encrypted + compressed blocks can move faster than raw plaintext.** Measured on two servers over a 10 Gbps link — 2234 blocks, zero failures — the kernel held **830 MB/s** verified-fetch throughput at a **53 µs** median per block, every byte AES-256-GCM encrypted, SHA-256 verified, Ed25519 signed.

    The mechanism is **bifurcation**: a shadow kernel pre-computes and verifies before the primary ever touches the data. Compressed blocks cut wire time, pre-verified blocks cut re-reads, and the encryption overhead disappears inside the throughput gain. If integrity fails at any point there's no partial result, no fallback, no retry — you get `0x00`, nothing ([the cat principle](the-cat-principle.md), on the data path). The same Rust binary runs on phones (aarch64), MIPS routers, ARM edge and x86 — one kernel, every architecture.

    Don't take the number from us — `cargo add tibet-trust-kernel` and measure it yourself.

---

## The actor forms — one identity, clipped to what it can prove now

Identity is one thing at rest; in motion it wears a clipped form (apocope) of the right it's actually using:

- **`.aint`** — the sovereign identity at rest (a person, device, AI, package).
- **`.raint`** — a runtime actor: a live process bound to an `.aint`, proving itself fresh per session (the disposable Redstone runtime is a `.raint`).
- **`.waint`** — a wrapper posture: a delegated tool, transport or worker acting *under* a parent actor (an I-Poll transport, an MCP server, a GPU). Not a sovereign actor — but enough authority that the gate must see it.
- **`.caint`** — a composite/derived actor: the *set-intersection* of its member `.waint`s, materialized only when every member signed (N-of-N) and never with more authority than the intersection. No key inheritance, no expansion.
- **`.saint`** — a service/daemon actor (e.g. a controller daemon).

A model file is **none of these** — it isn't an identity. The process is the actor; the loaded model is a mounted `.waint`, attested *by reference* through its `.oom` content-hash carried in the receipt. So "`gravity.aint`, model `claude@<oom-hash>`, intent X" is provable: *which actor, running which brain, under what intent* — recorded fresh at the moment of action, so one process can't later claim a different brain spoke.

---

## When zero-trust became the fast path — the GPU mailbox

The MUX's rule — *route is the output of attestation, not its input* — usually sounds like overhead. On the GPU lane it became the opposite. GPU compute is routed as **signed capsules** through `cap-bus` into a 100 MB pinned-host-DMA ring; a `.caint` gate admits the job, a content-addressed dedup skips a block **only on a cryptographically verified possession receipt** (never on a trusted claim), and every route leaves a causal receipt.

!!! note "Measured, not claimed — the bypass is real (27 June 2026, dual-verified)"
    On two consumer RTX 3060s with **no GPU-to-GPU P2P** (`NODE` topology), the pinned-host-DMA path moves data at **~8 GB/s while the CPU cores sit at ~1.2%** — the DMA engine does the work, the cores sleep on the interrupt. Cross-validated by *two independent implementations* (a Rust bench and a Python `ctypes` probe) landing on the same number. The attestation gate adds **~30 µs per block on the hot path** (parent-handle cached, verify-once-per-epoch), flat across block size — far below anything that would stutter token generation.

    Watched live during a 32B run, the real bottleneck wasn't bandwidth — inter-GPU traffic was *tens of MB/s* (activations only; weights stay resident) — but **pipeline bubbles**: the two cards take turns. So the substrate's win here is *prefetch and overlap*, not raw throughput, and the transport keeps ~100× headroom to spare. Honest about where it helps, measured about why.

---

## Knowledge processing — Cortex

A family for zero-trust handling of AI knowledge: `cortex-core` (TBZ envelopes, TIBET tokens, crypto primitives), `cortex-jis` (multi-dimensional identity claims — role, time, geo, clearance), `cortex-store` (JIS-gated vector storage), `cortex-airlock` (zero-plaintext-lifetime processing with `mlock` + `zeroize` — the secret never lingers in memory), and `cortex-audit` (blackbox-with-window audit trails). *(Published both bare and `tibet-`-prefixed; the `tibet-cortex-*` names are the namespaced form.)*

---

## Capability transfer — `tibet-iddrop`

Identity-bound capability transfer: **offer-first** over proximity, **request-first** over the wire, both carried in sealed TBZ v2 envelopes. The Rust side of ID-Drop — the handshake that hands one actor a scoped capability from another, by consent.

---

## The line to remember

> A Rust floor you can run anywhere, a Python surface to operate it, one identity-and-provenance model through both.

Nothing here needs a slogan. It's a substrate: small kernels that prove who and what, an operator layer to wire them, and sealed envelopes to move anything between them — on your own terms, down to the metal.

## Related

- [Build Posture](../network/build-posture.md)
- [Transfer Carriers](../reference/transfer-carriers.md)
- [Runtime Box Model](../builders/runtime-box-model.md)
- [The CAINT GPU Mailbox Lab](caint-gpu-mailbox-lab.md)
