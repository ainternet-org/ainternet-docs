# The CAINT GPU Mailbox Lab

> A learning module. What happens when you route GPU compute the same way you route everything else on AInternet — as a signed, addressed, consent-gated message — and measure it on real hardware. Spoiler: zero-trust turned out to be the *fast* path, not the toll booth.

Companion to [The Running Substrate](the-running-substrate.md), [Reaching a Raint](reaching-a-raint.md) and [The Cat Principle](the-cat-principle.md).

---

## The idea in one line

A model's GPU work is not a raw memory poke — it's a **`tibet-cmail` capsule** dropped in a mailbox, admitted by a **`.caint` gate**, carried over a **pinned-host-DMA ring**, and it leaves a **receipt**. The GPUs become a briefgeheim-guarded post box.

```text
sealed-cmail-gpu-job capsule
  → continuityd inbox-watch        (gpu0.p520.waint/inbox)
  → p520-gpu-controller.saint
  → p520-gpu-pair.caint            (the gate: verify_relation + capability intersection)
  → gpu0 / gpu1 .p520.waint lanes  (pinned-host-DMA ring)
  → reply sealed-cmail + UPIP compute receipt
```

## The `.caint` gate — derived, never expansive

A composite actor (`.caint`) is the **set-intersection** of its member `.waint`s. The route materializes only when *every* member signed the manifest (N-of-N), the binding relation verifies, and the declared capability is a subset of the intersection. No key inheritance, no authority expansion — anything else routes to `0x0000`. The crypto is the shipped verifier family (`tibet_mux.verify` — `verify_relation`, `verify_caint`), so there is no second implementation to drift.

On the hot path you don't re-verify every block: a **parent-handle** (a content-hash over the manifest + relation + consent window) is verified once per epoch, then referenced. The handle says *"you're expected"*; a fresh signature says *"and it's really you"* — never skip the second.

## Content-addressed dedup — *only on proof*

If the receiving GPU already holds a 2 MB block, you send a **32-byte hash pointer** instead of the block — zero-copy becomes zero-transfer. But "I already have it" is **never trusted**: the holder must present a *cryptographically verified, fresh possession receipt* before the transfer is skipped. No pubkey, no skip; bad signature, no skip; fails closed. (Otherwise a compromised node could claim possession to serve stale or poisoned weights.)

---

## Measured, not claimed (27 June 2026, dual-verified)

!!! note "The bypass is real — on two consumer RTX 3060s"
    With **no GPU-to-GPU P2P** available (`nvidia-smi topo` = `NODE`), the pinned-host-DMA ring moves data at **~8 GB/s while the CPU cores sit at ~1.2%** — the DMA engine does the work, the cores sleep on the interrupt (`cudaDeviceScheduleBlockingSync`). Cross-validated by *two independent implementations* — a Rust benchmark and a Python `ctypes` probe — landing on the same number. The attestation gate adds **~30 µs per block on the hot path**, flat across block size: far below anything that would stutter token generation.

!!! note "What we saw live during a 32B run"
    The bottleneck wasn't bandwidth. Inter-GPU traffic was *tens of MB/s* — **activations only; the weights stay resident** — and the two cards **take turns** (pipeline bubbles), each waiting on the other. So the substrate's win here is **prefetch and overlap** (hide the handoff with JIS-driven pre-staging + forward-consent), not raw throughput — the transport keeps ~100× headroom to spare. Honest about *where* it helps; measured about *why*.

## Sign-ahead — the proof is ready before the moment it needs it

A white-box engine knows the *next* handoff before it happens (intent-before-transfer). So it doesn't sign *after* the transfer is ready — it pre-signs the next handoff capsule **during the current layer's compute**, in the compute shadow. The signature carries an *earlier* timestamp than the event it attests:

```text
INLINE (sign as a consequence):
   [GPU compute layer N done]
        │   ◄─ gap of 1.1 ms … up to ~10 ms (CPU busy signing here, on the critical path)
   [layer.handoff.intent.aint signed]
        │
        ▼
   [PCIe transfer starts]

SIGN-AHEAD (sign as a precondition, prepared in the shadow):
   [layer.handoff.intent.aint signed]   @ 14:51:28.100   ◄─ signature already prepared DURING compute
   [GPU compute layer N done]           @ 14:51:28.102
        │   ◄─ only ~0.03 ms gap
        ▼
   [PCIe transfer starts]
```

!!! note "Measured, not claimed — attestation in the compute shadow (dual-verified)"
    A streaming bench (per-token p50/p99/max) compared no-sign baseline · inline-sign · sign-ahead. **Inline signing added ~1.1 ms per handoff with a p99 tail spike; sign-ahead added ~0.02–0.03 ms and a p99 essentially identical to the no-sign baseline — ~98% of the cryptographic latency hidden.** Cross-validated by two independent runs. The predecessor's compute time *is* the signing budget; a black box can only sign-after (or sign-inline and stutter). *Causal note:* the receipt is ready before the event it attests — Lamport/forward-consent, made physical.

## Reproduce it yourself

- The gate: `pip install tibet-mux` → `tibet_mux.verify` (`verify_caint`, `caint_manifest_handle`, `verify_forward_consent`).
- The mailbox: `tibet-cap-bus` → `tibet_cap_bus.gpu_mailbox` (`GPURingBufferInjector`, `ContentAddressedVRAM`, `TTLEnforcer`).
- The hardware path: a `cudaHostAlloc` pinned ring + `userfaultfd` fill, and a `cudaMemcpy` throughput loop with a CPU sampler.

Don't take the numbers from us — run them on your own cards and compare. That's the point: *the route is the output of attestation, and the attestation is something you can re-check.*
