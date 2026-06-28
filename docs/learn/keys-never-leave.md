# Keys Never Leave Your Machine

> A learning module. Your network stands and your agents act. Now the question underneath all of it: where does the *key* live? Get this wrong once and everything above it is theatre. This module is the line that's key to the whole process — **a private key is born on your machine, stays on your machine, and never travels.**

This is the companion to [Bind an AI, Runtime-Bound](bind-an-ai.md). That module was about proving identity *as you act*. This one is about the thing that does the proving — the key — and the single rule that keeps it trustworthy: it does not leave.

---

## 1. The rule

```text
private key   →  born local, kept local, signs in place
the server    →  verifies, never holds
what travels  →  only the public key, and signatures
```

If a private key is ever generated **on** the server, uploaded **to** it, or pasted into a session or CI secret that gets logged — the server can now sign as you. From that moment it can impersonate you, and every guarantee above it collapses. So we never move the key to the work.

> We bring the work to the key — **detached signing** — and ship only the signature.

---

## 2. Why: a bearer is never an authority

A private key at rest is a bearer secret: whoever holds it is treated as the owner. A key that travels is a key that can be copied in transit, logged at the destination, or read off a disk you don't control.

> A key that travels is a key that leaks.

The fix isn't "guard the key better while it moves." It's **don't move it**. The key has exactly one job — to emit signatures — and it can do that job without ever leaving the machine it was born on.

---

## 3. The cat principle, on the key layer

Elsewhere in AInternet the [MUX](../protocols/mux.md) is dark-by-default: to anyone who can't prove themselves, the system simply *isn't there*. You can't attack a door you can't find. We call it the cat principle — you don't out-pattern an attacker, you stop being a target.

Key custody is the same idea, one layer down:

```text
WAF thinking:   keep the secret on the server, guard it harder
cat thinking:   the secret was never on the server — there is nothing to take
```

A server that never holds your private key cannot leak it, cannot be subpoenaed for it, cannot have it stolen in a breach. The strongest protection for a secret is its **absence**. Dark-by-default, applied to keys: the secret simply isn't there.

---

## 4. The local ceremony

Reproducible — these commands actually run (Ed25519, via OpenSSL):

```bash
# 1. generate on YOUR machine — the private key never leaves this file
openssl genpkey -algorithm ed25519 -out builder.key
openssl pkey -in builder.key -pubout -out builder.pub

# 2. publish ONLY the public half, under your .aint (via AINS)

# 3. sign detached — bring the payload to the key
openssl pkeyutl -sign -inkey builder.key -rawin -in release.tza -out release.sig

# 4. anyone verifies with only the public key
openssl pkeyutl -verify -pubin -inkey builder.pub -rawin -in release.tza -sigfile release.sig
# -> Signature Verified Successfully
```

That's the whole trust chain: a public key the world holds, a signature you alone could make. No account, no upload, no shared secret.

!!! tip "The full runbook"
    The step-by-step ceremony, custody do's and don'ts, and recovery live in the runbook on the site:
    [**The signing ceremony →**](https://ainternet.org/signing-ceremony.html)

---

## 5. Two ways to keep it — cold vs sealed

One rule, two custody models, chosen by whether a human must be present and whether a secret may sit at rest at all.

| role | custody | used for | secret at rest? |
|------|---------|----------|-----------------|
| **builder** (cold key) | a human, offline, own machine | golden builds, releases — vouched for by a person | yes, encrypted offline — **never on the server** |
| **governor** (sealed key) | a machine's TPM | automated signing with no human present | **no** — materialises per-window (derived from a TPM-sealed root), then gone |

The cold key trades convenience for the strongest custody. The sealed key trades a human's presence for a guarantee that **no usable secret ever sits on disk** — it's computed at the moment of use and discarded. Either way, the principle holds: nothing the server could sign with is ever lying around.

---

## 6. What the server ever sees

```text
at registration:   your public key
at every use:      a fresh challenge  →  your signature over it
the server:        checks signature against public key, moves on
```

There's no logged-in session to steal, because there's nothing *to* sit around — you prove yourself fresh, each time. That's identity as a [condition, not a claim](everything-falls-back-to-tibet.md): the key proves the act in the moment, and then the moment is over.

---

## The line to remember

> Born local, kept local, signs detached, verified by all. The key never moves; only the proof does.

That's not a convenience choice — it's the floor the whole stack stands on. An agent can be perfectly runtime-bound and every receipt perfectly chained, and it all means nothing if the key that signs them lives somewhere a stranger can reach. Keep the key home, and everything above it can be trusted.
