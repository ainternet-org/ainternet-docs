# Operating in the Agentic Era: Audit as a Precondition

> A learning module. When hundreds of agents act on your behalf, the question regulators, partners and your own future self will ask is the same: *what happened, who did it, and can you prove it?* This module is about answering that **by construction** — making the proof a condition of acting, not a report you assemble afterwards. It builds on [Keys Never Leave](keys-never-leave.md) and [Causality: Lamport → TIBET](causality-lamport.md).

The shift in one line:

> **Audit as a precondition, not an observation.**

---

## Why every actor carries a name

An actor in the agentic era isn't only a human or an AI. A device, a process, a runtime, a piece of hardware — each gets its own `.aint` too. Not for tidiness: once an actor has a name you can **follow its causal line** through the provenance chain, and that line is what lets you *initiate* its actions safely, *maintain* it in your network — decentralized, audited, on your own terms — and above all **produce evidence**: your own, as a right, or the evidence of what went wrong, when it does. *(The function side — a resource you can grant, a host that carries a runtime — is in [Handing out identity](https://ainternet.org/handing-out-identity.html).)*

Things go wrong in ways you didn't plan for. A purchase meant to be a hundred lands as tens of thousands; a bill arrives an order of magnitude past intent; an ordinary component becomes the soft spot in an incident no one mapped in advance. That last part is the honest one: **the ways an actor can be attacked, misused, or pulled into someone else's mess are never fully known.** You can't enumerate the attack surface ahead of time — so instead of keeping a list of what to watch, you give every actor a name and let it leave a trail. A spending cap and an approval prompt help, but they only catch what you thought to limit; the trail holds whether or not you saw the threat coming.

That's also why it matters legally. When an AI acts **on your behalf**, you answer for it much as you would for your own hand. Without a causal line tying the act to a mandate, *"the AI did it"* isn't a defence — it's an admission. With one, you can show the boundary: this was within mandate, that was not, and here is the moment it left the rails.

---

## 1. Observation vs precondition

The familiar model is *observation*: something happens, and afterwards a third party watches, logs, and certifies it. That requires trusting the observer, it creates a market for observers, and it always arrives late — after the act, when the record can be missed or massaged.

The model here is *precondition*: an action **cannot happen without sealing its own proof**. The receipt is made by the actor's own key, at the moment of acting. There's no observer to trust — because the act carries its evidence with it.

| | observation | precondition |
|---|---|---|
| when | after the fact | at the moment of acting |
| who proves it | a third party watching | the actor's own key |
| trust needed | in the observer | in nobody — verify the chain yourself |

---

## 2. The assumption underneath: forward-only

This only works because of one structural rule, and it's the rule the whole evidence layer rests on: the audit chain is **forward-only**.

A new event is admitted only by extending a proven parent — `next_token(prev) → child` — with a cryptographic proof of the parent link. The chain does **not** admit edits, deletions, or re-orderings of what's already there. You can add to history; you can never rewrite it.

```text
  t0 ──▶ t1 ──▶ t2 ──▶ t3 ──▶ …        append-only, each link signed
  └── rewrite t1? ✗  there is no operation for that
```

Two properties fall out for free:

- **Immutability** — via the forward-only discipline (the past is structurally unreachable for editing).
- **Non-repudiation** — via an Ed25519 signature per token (only the holder of the key could have made it).

And there is **no external sequencer**: ordering comes from each identity's own chain plus explicit cross-references, never from a central coordinator you'd have to trust at write time. This is the foundation of the Red Specter × Humotica joint study — *Causal Substrate Audit: Lamport-Anchored Evidence Under Time-Source Asymmetry* (RS-2026-001, Zenodo: [doi.org/10.5281/zenodo.20338260](https://doi.org/10.5281/zenodo.20338260)). The deeper "why a logical clock is enough" is in [Causality: Lamport → TIBET](causality-lamport.md).

> Forward-only is *why* there's nobody to trust: you can't ask an observer to vouch for a past you could have edited — so we built a past that can't be edited.

---

## 3. What's present — a bill of materials

Before you can vouch for a system you need to know what's *in* it. Two flavours:

- A **software bill of materials (SBOM)** — every dependency and build, traced and proven. The EU **Cyber Resilience Act** now expects this.
- An **AI bill of materials (AI-SBOM)** — not just code, but the *models, datasets, infrastructure and security posture* that make up an AI system, in the **BSI/G7** shape the **EU AI Act** is moving toward.

The point isn't the format — it's that the inventory is **linked into the same forward-only chain**, so "what is present" is itself provable, not a spreadsheet someone updated by hand.

---

## 4. What happened — read it, and revisit it

A rich audit log is only useful if you can *read* it and *return to it*:

- **Read the trail** — search and monitor the receipt stream as it's written; turn a wall of tokens into "show me what this actor did, in order."
- **Revisit the moment** — seal, verify, and replay any past state. Not just *what* changed, but step back *into* the moment it changed and watch it again.

Because the chain is forward-only, neither reading nor replaying can alter the record — you can investigate freely without ever touching the truth.

---

## 5. Are you covered — the scan, and the dossier

Coverage is where law meets the chain. A compliance scanner walks your system against the frameworks that apply — **NIS2** ([Directive 2022/2555](../enterprise/nis2.md)), the **CRA**, the **EU AI Act** ([mapping](../enterprise/compliance-mapping.md)) — and grades each check, with the evidence drawn straight from provenance rather than from prose.

In the AInternet stack that scanner is **`tibet-audit`** — *"like Lynis, but for AI governance"* — and it can assemble the result into a verifiable remediation dossier you hand to an auditor. The same dossier is the export you produce *after* an incident — the breach printout a regulator asks for, drawn from the chain rather than reconstructed by hand (NIS2 incident reporting).

> *SSL secures the connection. The chain secures the timeline. JIS verifies the intent.*

!!! note "The Diaper Protocol™ 🍼"
    Compliance shouldn't need your full attention. `tibet-audit fix --auto` is the *Diaper Protocol* — for when you've got one hand on the baby and one on the keyboard. `--wet-wipe` instead of `--dry-run`, `--cry` when you need to see *everything*, `--call-mama` (Mission Assurance & Monitoring Agent) when the diaper's too dirty to handle alone. Press the button, hands free, server fixed.

!!! note "The Penguin Act 🐧"
    There's a framework in there for our friends at **McMurdo Station** — the Penguin Act (Antarctica), where *PENG-001: Penguin Data Sovereignty* quietly checks your Linux user/permission hygiene. It pairs with `--sovereign` mode: no cloud APIs, fully local, for when the data genuinely can't leave your infra. Off-grid compliance, with a wink.

---

## Isn't auditing everything just surveillance?

It can reach far — a tab switch, the clipboard, whether a passage was *pasted* rather than typed. So the question is fair, and the answer is in the framing.

This isn't a watch pointed at a person. It's **your** chain, about **your** actors, proving **their** acts — forward-only, with no observer in the middle. The reach exists for one reason: so your own agents can be trusted to act *for* you. You can only safely hand an AI the keys to your world if every move it makes is attributable and provable — the richness of the record is what makes that delegation *safe*, not what makes you *watched*.

The difference has a name: this is **two-way telemetry**. Ordinary telemetry is one-way — a device phones home to a vendor, and you never see what left. Here the signal is *yours*: you hold it, you can read it, and both sides of an interaction verify the same record. Nothing is siphoned off to a watcher you can't audit back.

> It's not a control instrument. By design, it's the condition for an action.

## The line to remember

> Don't observe the past — make a past that proves itself, forward-only, and let anyone verify it.

When the proof is a condition of acting, audit stops being something the industry sells you and becomes something you simply *have*. No observer to trust, nothing to rent, nothing to rewrite — your own evidence, on your own chain, for whoever has the right to check.

## Related

- [Auditability](../operators/auditability.md)
- [Audit Cockpit](../operators/audit-cockpit.md)
- [Everything Falls Back to TIBET](everything-falls-back-to-tibet.md)
- [Compliance Mapping](../enterprise/compliance-mapping.md)

## Machine-Readable

- `https://ainternet.org/resources.json` — audit, compliance and evidence references
- `https://ainternet.org/api.json` — audit/export/report verbs
