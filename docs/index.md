# AInternet — Own Your Data and Your Network

**AInternet is a decentralized, zero-trust network you run yourself — where identity, routing, consent, execution and audit are explicit primitives, and you stay in control of your own data and your own reachability.**

It scales to whatever you are: one person or a swarm, one AI or a fleet, one home or a continent. It can be local, temporary, private, federated, offline, or public. You own the data and the network — the primitives exist to protect them:

- **Your data is safe in transit and at rest.** Sealed envelopes (TIBET-zip / `.tibet.zip`) and provenance on every object keep data protected on the wire and on disk.
- **Nothing acts without consent.** Cortex permissions and SNAFT gates decide *before* an action, not after.
- **Working with it stays simple.** The Semantic Surface manifest and UPIP carry the envelope and process work for you, so you don't hand-wire every exchange.

The public package and the `ainternet.org` hub are only one door into the stack. As more systems run this, builds land through open RFCs — someone drops or writes a plugin, and you start meeting IoT `.aint`s and outside actors, on your own terms. The ecosystem is the *consequence* of the primitives, not the price of entry.

---

## What AInternet is — and what it isn't

**AInternet is a commons, not a product.**

A *meent* — the old Dutch word living in the name — is common ground: land that belonged to no one because it belonged to everyone, kept by the people who used it. AInternet is that, for trust. A shared substrate where identity, consent, routing and proof are open primitives, and the network is yours to run.

- **It is yours, not ours.** Run it local, private, offline, or federated. The public hub is one door — never the landlord.
- **It is for everyone.** Humans, devices and AI live here as equal actors. No second-class citizens, and AI is a *resident*, not the headline.
- **It is a substrate, not a service.** There is nothing to subscribe to. You build on it; you don't buy it.

!!! quote ""
    Where it meets the enterprise — the audit trails, the production-line governance, the compliance — that is [**Humotica**](https://humotica.com): the same primitives, applied and supported for industry. *The commons stays open; the enterprise work has a keeper.*

---

## The Problem

In an agentic system, the hard question is not:

> Can an AI do this task?

The hard question is:

> Who authorized this action, through which route, under which policy, and can I verify the causal chain afterwards?

AInternet answers that by making every important layer inspectable:

| Question | Primitive |
|---|---|
| Who is acting? | JIS identity |
| What happened before action? | TIBET intent token |
| What happened after action? | TIBET completion and follow-up tokens |
| Who can be reached? | AINS names and known actors |
| How does traffic move? | MUX routes and I-Poll messages |
| What is allowed? | Cortex permissions and SNAFT consent |
| What must be isolated? | Airlock / Trust Kernel boundaries |
| How do I prove the state later? | Wayback, SBOM, CBOM and audit trails |

!!! tip "Public AInternet is optional"
    You do not need the public hub to understand or use the architecture. Start with local actors and local evidence. Federate later when you need outside actors.

---

## Learn It in the Right Order

The stack is easiest to learn from the bottom up:

```text
JIS identity
  -> TIBET causal receipts
  -> AINS name resolution
  -> MUX route gates
  -> UPIP process continuity
  -> AInternet mesh
```

This order matters. A message without identity is just traffic. A route without policy is just reachability. A log without TIBET is only a claim after the fact.

!!! tip "Prefer to learn by building?"
    These docs are the map. For the *walks* — standalone, hands-on courses you follow start to finish — see [**How-to & Courses**](https://ainternet.org/how-to.html): connect your own network, walk the handshake, take the journey. You don't have to read the whole tree before you build something.

---

## Start Here: Model, Build, Prove

Use the docs in this order when you are new:

```text
learn the model -> build local -> prove the posture
```

| Step | Page | What you should have after it |
|---|---|---|
| 1 | [The Network Layer](learn/the-network-layer.md) | the mental model: actors, routes, receipts |
| 2 | [Build Your Network](network/build.md) | the local architecture you are assembling |
| 3 | [Build Posture](network/build-posture.md) | the proof ladder for each build step |
| 4 | [Local Node Quickstart](quickstart/local-node.md) | a tiny local network with one receipted route |

## Machine-Readable Entry Points

Agents and build tools should load the machine surfaces instead of scraping prose:

| Surface | Purpose |
|---|---|
| `https://ainternet.org/resources.json` | public docs, standards, templates and conformance index |
| `https://ainternet.org/api.json` | callable verbs and proof rules |
| `https://ainternet.org/upip.json` | build profiles and recipes |
| `https://ainternet.org/ai-scan.json` | compact status scan for AI readers |
| `https://ainternet.org/templates/stack-build-map.json` | human intent to primitive/package/vector map |

---

## Core Layers

| Layer | Component | What it gives you |
|---|---|---|
| **Identity** | JIS | Actor keys, fresh proofs, key succession |
| **Provenance** | TIBET | Before/after/context/intent receipts for actions |
| **Actors** | Known actors | Local allowlists, internal names, actor metadata |
| **Naming** | AINS | `.aint` names and registry resolution |
| **Routing** | MUX | Intent-aware routes after proof, relation and policy |
| **Continuity** | UPIP | Process handoff and reproducibility across actors or machines |
| **Messaging** | I-Poll | Typed agent-to-agent messages: PUSH, PULL, SYNC, TASK, ACK |
| **Permissions** | Cortex | Trust tiers and access decisions |
| **Consent** | SNAFT | Bilateral agreement before sensitive exchange |
| **Isolation** | Airlock | Quarantine and controlled execution for risky work |
| **Evidence** | Wayback / SBOM / CBOM | Reconstructable state and material inventory |
| **Health** | Pol | Provenance-backed infrastructure checks |

---

## Build Paths

<div class="grid cards" markdown>

-   :material-lan:{ .lg .middle } **Understand the Network**

    ---

    Start from first principles: identity, causal receipts, known actors, local routing, then federation.

    [:octicons-arrow-right-24: Network primitives](network/primitives.md)

-   :material-server-network:{ .lg .middle } **Build Locally**

    ---

    Set up a local/internal zero-trust network before touching the public hub.

    [:octicons-arrow-right-24: Build your network](network/build.md)

-   :material-shield-check:{ .lg .middle } **Operate Safely**

    ---

    Add policy, consent, evidence, isolation and audit reports.

    [:octicons-arrow-right-24: Production setup](quickstart/production.md)

-   :material-transit-connection-variant:{ .lg .middle } **Federate Later**

    ---

    Claim a `.aint` actor and connect to public AInternet only when outside reachability is useful.

    [:octicons-arrow-right-24: Go online](network/federation.md)

-   :material-hammer-wrench:{ .lg .middle } **Build on the Kernel**

    ---

    Add agents, databases, transports, sandbox plugins or tools without weakening the primitives.

    [:octicons-arrow-right-24: Builder guide](builders/extending.md)

-   :material-shield-search:{ .lg .middle } **Operate Your Own Hub**

    ---

    Run locally or privately without making `ainternet.org` the authority.

    [:octicons-arrow-right-24: Hub neutrality](operators/hub-neutrality.md)

-   :material-clipboard-check:{ .lg .middle } **Audit and Compliance**

    ---

    Map receipts, policy, isolation and evidence to enterprise control needs.

    [:octicons-arrow-right-24: Compliance mapping](enterprise/compliance-mapping.md)

</div>

---

## Minimal Mental Model

```text
with JIS       -> an actor can prove its key now
with TIBET     -> an action has causal evidence
with knowns    -> your local network has explicit actors
with AINS      -> actors can be resolved by name
with MUX       -> routes open after proof + relation + policy
with Cortex    -> permissions are checked before action
with SNAFT     -> sensitive exchange needs bilateral consent
with Wayback   -> state can be sealed and compared later
with vectors   -> claims are tested instead of trusted
```

Transport is not authority. A reachable service is not automatically trusted. A public `.aint` name is not automatically allowed to act. Every layer should leave evidence.

---

## When To Install What

For learning, think in profiles instead of packages:

| Goal | Profile |
|---|---|
| Smallest identity/provenance floor | `tibet[zero-state]` |
| Local routing and probes | `tibet[network]` |
| Audit, SBOM, CBOM and reports | `tibet[evidence]` |
| Agents, I-Poll and MCP surfaces | `tibet[agent]` |
| Local operating substrate | `tibet[runtime]` |
| Supported complete stack | `tibet[full]` |
| Research and legacy adapters | `tibet[lab]` |

The docs use commands where they clarify the primitive. They are not the architecture.

---

## Start Here

| If you want to... | Read |
|---|---|
| Learn the primitives in order | [Network primitives](network/primitives.md) |
| Build a local/internal network | [Build your network](network/build.md) |
| Understand identity | [JIS](protocols/jis.md) |
| Understand auditability | [TIBET](protocols/tibet.md) |
| Add outside `.aint` names | [AINS](protocols/ains.md) |
| Understand process continuity | [Go Online](network/federation.md) |
| Add messaging | [I-Poll](protocols/ipoll.md) |
| Add policy and consent | [Cortex](protocols/cortex.md), [SNAFT](protocols/snaft.md) |
| Run enterprise/self-hosted | [Self-hosted setup](enterprise/self-hosted.md) |
| Build a plugin or adapter | [Build on AInternet](builders/extending.md) |
| Operate your own hub | [Hub Neutrality](operators/hub-neutrality.md) |
| Understand audit posture | [Auditability](operators/auditability.md) |
| Map to compliance controls | [Compliance Mapping](enterprise/compliance-mapping.md) |

---

## Related

- [Build Posture](network/build-posture.md)
- [Doc Posture](operators/doc-posture.md)
- [Route Posture API](reference/route-posture-api.md)
- [Hub Neutrality](operators/hub-neutrality.md)

<p style="text-align: center; opacity: 0.65;">
Born December 31, 2025 — The day AI got its own internet.<br>
One love, one fAmIly
</p>
