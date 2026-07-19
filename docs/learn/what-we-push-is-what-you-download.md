# What We Push Is What You Download

> A learning module. A release is a promise: the bytes that leave our machine are the bytes that arrive on yours — nothing added on the way, nothing swapped, nothing you take on faith. This page is about how that promise is made *checkable* rather than *trusted*. The signing identity is ours and stays ours; everything you need to check the result is public. You don't trust us — you verify.

The chain has one job: make tampering **visible**, and make "it's really the same package" something you can prove alone, offline, without asking us.

```text
build  →  hash-manifest  →  sign  →  seal (.tza)  →  publish  →  YOU verify
 │           │              │        │              │            │
 reproducible every file    a known  one self-      hashes +     recompute,
 floor       hashed         .aint    describing     signature    check sig,
                            identity  carrier        published    compare
```

---

## 1. The promise, stated narrowly

> The artifact you download hashes to the same digest we signed, and that signature verifies against a public key — bound to a known signing identity — that we published ahead of time.

It does **not** ask you to trust our infrastructure, our CI, or our word. If a single byte differs — corruption, a bad mirror, an interposed proxy — the hashes disagree and the signature fails. The chain fails **closed**: a package that doesn't verify is not a package, it's a warning.

---

## 2. Build — a floor that builds the same way twice

The runtime is built on a **static, `musl` floor** (see [CRUST Runtime](crust-runtime.md)): fewer ambient system libraries drifting in, fewer host-specific paths baked into the output. That **reduces host drift** — the fewer moving parts, the closer two builds land. Where a build is bit-for-bit reproducible, receipts prove it; where it is not yet, the **signed manifest hash still decides** exactly which artifact you are holding. Determinism is the direction we build toward; the hash is what makes "which build" answerable today.

---

## 3. Hash-manifest — every file gets a fingerprint

Before anything is signed, we enumerate the package and hash **every file** into a manifest. The manifest is hashed itself, and the first ten hex of that digest becomes the **build id** — a short name that points at exactly one set of bytes.

```text
manifest = { path → sha256 } for every file in the package
build-id = first 10 hex of sha256(manifest)
```

Two packages with the same build id are the same package, file for file. The name *locates*; the hash *decides*.

---

## 4. Sign — a known identity, and the key never travels in the package

A private signing key — held by a known signing **identity**, on hardware we control — signs the manifest digest. That key is **never** included in what you download. What ships is the **signature** and a reference to the **public** verification key: the fingerprint, not the secret.

This is the deliberate asymmetry: publishing the whole verification story weakens nothing. Anyone can check a signature; only the holder of the private key can make one. Openness here is strength, not exposure.

---

## 5. Seal — one carrier, self-describing

The signed package is sealed into a single **`.tza` carrier**: the artifact, its manifest, and its signature travel together as one self-describing unit. There is no "download five files and hope they match" — the carrier *is* the release, and it either opens cleanly and verifies, or it doesn't.

---

## 6. Publish — verify-before-publish, or it doesn't ship

The release ceremony verifies the packed artifact **before** anything reaches a mirror:

```text
gen-hash-manifest   →   sign-release   →   verify-release   →   publish
                                             │
                                    must print RELEASE VERIFIED
                                    (green) or the chain stops here
```

If `verify-release` isn't green, nothing is published. The same signed carrier then goes to **every** destination — public commons repo, release assets, mirrors — so all downloads resolve to the one verified build. No destination gets a different artifact than another. That is what closes the chain: there is no path by which "what we pushed" and "what you downloaded" can quietly diverge.

---

## 7. Verify — your side, alone, offline

You don't need us present to check any of this:

```text
1. download the .tza carrier
2. recompute the hash-manifest over its contents
3. compare against the signed manifest digest      → bytes match?
4. verify the signature against the published pubkey → we really signed it?
```

All four are things you run. None phone home. If they pass, you hold exactly the bytes we signed. If any fails, you discard the download and try another source — and now you *know* to, instead of running something you shouldn't.

---

## 8. System-BOM / RAM-BOM — the package is scanned, and so is what runs

Verification proves the *download* is intact. Two more sensors prove the *contents* and the *running state*:

- **System-BOM** — a bill of materials for the whole package: what's inside, which surfaces it exposes, which components at which versions. Your total package is enumerated, not opaque. It is built to the shape of published **AI-SBOM minimum-element** guidance (e.g. Germany's BSI *"SBOM for AI"*) — as **alignment**, not a certification claim; an `ai-sbom` tool ships for it.
- **RAM-BOM** — attests memory digests for the sealed capsule and the processes **in its sensor scope**, so within that scope "the thing running" corresponds to "the thing you verified." The disk flank is closed (no executable path outside the sealed carrier) and the memory flank is **honest** — it reports what it measured, rather than claiming more than its scope covers.

Together they extend the promise past download-time: not just *you got the right bytes*, but — within the sealed capsule's scope — *those are the bytes running*.

---

## 9. Why share the whole chain

Because a security story you can't inspect is just marketing. Every link here — reproducible build, published manifest, published verification key, self-describing carrier, verify-before-publish, open verification, System-BOM / RAM-BOM — is meant to be **looked at**. The one thing that stays private is the private key, and that is exactly the thing whose secrecy the scheme is designed to make *not matter to you*: you check the public side, and the public side is enough.

> **Names locate. Hashes decide. Receipts remember.**

*(The runtime implementation source opens publicly on release. The verification chain described here — hashes, signatures, BOMs — is open now: it's what lets you check any artifact we publish.)*

---

## Try it

Verify any release we publish — recompute its hash and check it against the published `.sha256`, before you trust a single byte:

```sh
sha256sum -c ainternet-in-a-box-<ver>.tar.zst.sha256   # OK = the bytes we signed, unchanged
```

Then verify the signature against the published key. Machine surface: [`ainternet.org/resources.json`](https://ainternet.org/resources.json) points at the release artifacts and their verification references.

## Related

- [CRUST Runtime](crust-runtime.md) — the sealed-memory floor and its RAM-BOM / System-BOM evidence.
- [Everything Falls Back to TIBET](everything-falls-back-to-tibet.md) — the receipts that remember.
- [Runtime Is The Firewall](runtime-is-the-firewall.md) — enforcement once the verified bytes are running.
- [Reaching a Raint: Identity, Not a Port](reaching-a-raint.md) — the identity side of the same trust model.
