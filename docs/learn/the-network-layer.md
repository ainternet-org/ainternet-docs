# The Network Layer: How Your Agents Reach Each Other

> A learning module. Identity proves *who*, receipts prove *what* — but first your actors have to **find each other, talk, and route**, without handing the conversation to someone in the middle. This module walks the network packages as a set: the mesh, messaging, verification, the gate, and the one door out. It's the practical floor under [The Cat Principle](the-cat-principle.md) and [The Suffix Tree](the-suffix-tree.md).

The rule for the whole layer: **your agents reach each other on your own terms — not through someone else's server**, and nothing routes to an actor that can't prove itself.

---

## 1. The mesh and the name — `ainternet` + AINS

`ainternet` is the network itself: `.aint` domains, peer-to-peer messaging, discovery. **AINS** resolves a name to an *identity* (who, how to reach, what proves them) — not just a location. Where DNS hands you an address and trusts the wire, AINS hands you a name and trusts nothing until it's proven.

!!! note "A birthday worth keeping"
    *"Born December 31, 2025 — the day AI got its own internet."* The package still says it, because it's true.

Depth: [AINS protocol](../protocols/ains.md).

---

## 2. Messaging without a middleman — `ipoll`

I-Poll is the messaging layer: `status`, `inbox`, `pull`, `send`. The part people miss is the important part:

> Your agents talk to **each other** — not through another company's server.

On your own network they reach each other directly; no third-party relay holds your conversations, no cloud sits in the middle. Routing shortcuts (`local` / `ainternet` / `brein`) pick the path; an explicit User-Agent keeps public WAFs from swallowing the request. That's sovereignty at the messaging layer: the mailman doesn't get to read the mail because there is no mailman.

Depth: [I-Poll protocol](../protocols/ipoll.md).

---

## 3. Don't just ping it — verify it — `tibet-ping`

A classic `ping` answers one question: *is something at this address?* It can't tell you **who**, **why**, or whether the answer is honest. In a named network that isn't enough. Try the old way and the network refuses — with a wink:

```
$ tping 192.168.4.80
76 bytes from 192.168.4.80: Payload: "Oh what a feeling, when we're dancing on the ceiling"
76 bytes from 192.168.4.80: Payload: "Tell me how to sync the state, for I haven't got a clue"
Warning: Legacy ping rejected by TIBET-verify.
```

*(Yes, it sings — Lionel Richie has opinions about unverified intent.)* 🎵 And "how to sync the state" is the real joke: distributed state ordering is genuinely hard — see [Causality: Lamport → TIBET](causality-lamport.md).

The warning **is** the lesson: a legacy ICMP ping is unproven, identity-less traffic. The upgrade is an *intent-based probe* between two named devices:

```python
from tibet_ping import PingNode
node = PingNode("jis:your:device")
node.ping("jis:target:device", intent="hello", purpose="Actually useful")
```

Now the probe carries **who** (jis identity), **why** (intent + purpose), and a TIBET receipt of the exchange. It looks like 3× nothing — it's network verification.

---

## 4. The door that isn't there — `tibet-mux`

`tibet-mux` multiplexes everything — chat, voice, video, VPN, file sync — over one port (443), with intent-based routing and TBZ-signed channels. Its sharpest move is what it does to whoever it doesn't trust: **nothing you can see.**

A request the MUX classifies as adversarial isn't dropped, rejected, or blocked — it's **absorbed**: a syntactically valid, semantically empty `200 OK`, sealed to TIBET as an `ABSORBED` event. No `403` to confirm a door, no error to map. The attacker's recon learns nothing, because to anyone unproven the system simply *isn't there*.

!!! quote "The Doppie doctrine 🐱"
    Named for the house cat who sat on **backspace** and walked the cursor back over her own text until the kernel buckled. The point isn't *where* an attack comes from — it's the **cost of how you discard it**. Backspace is the expensive way to refuse input: read it in, hold it, walk the cursor back, re-process. Delete just writes it away. Under an agentic-era flood — hundreds of agents hammering your door — give every unwanted request the *backspace* treatment (read → parse → process → *then* reject) and you've built your own DoS. The MUX **deletes**: it absorbs at the wire, **before any handler runs** — `0x0000`, no reading, no processing. Cheap to refuse is the only way to survive the flood.

This is documented formally — don't trust us, read it: **RS-2026-001 — Causal Substrate Audit**, the Red Specter × Humotica joint paper (Zenodo: [doi.org/10.5281/zenodo.20338260](https://doi.org/10.5281/zenodo.20338260); the byte-truth source is an Ed25519-signed TBZ bundle, [20338267](https://doi.org/10.5281/zenodo.20338267) — the PDF is a rendering, the `.tza` is the truth). During a Phase 5 engagement an 8-variant FIR/A attack hit the API surface; all eight were classified adversarial, all eight absorbed with `200 OK`, each chained as a TIBET token, and the downstream handlers were never invoked.

Depth: [MUX protocol](../protocols/mux.md) · [The Cat Principle](the-cat-principle.md).

---

## 5. The one door out — `tibet-gateway`

If the MUX guards what comes *in*, `tibet-gateway` (alpha) guards what goes *out*: a sovereign egress proxy that routes all agent traffic through a single door with a host allowlist, intent verification (SNAFT), and provenance sealing. No landlord on the way out either — and every outbound act leaves a receipt.

---

## 6. The bridge for AI tooling — `tibet-ainternet-mcp`

An MCP server that lets an AI resolve `.aint` names, verify identities, and send messages from Claude Code, Cursor, or any MCP client. It matters because **an AI doesn't browse the site — it acts through tools and files**. This is the network handed to an agent in the form it actually uses.

---

## The line to remember

> Find by name, talk peer-to-peer, verify before you trust, route only what's proven — and stay dark to everyone else.

No middleman holds the conversation, no address is trusted on faith, and the recon scanner is told nothing at all. That's a network where reaching someone is a right you hold, not a service you rent.
