# Network Primitives

AInternet is best understood as a chain of primitives. Each primitive answers one security or coordination question. Do not skip the earlier layers: a route is not trust, a message is not consent, and a log is not proof.

## 1. Actor Identity: JIS

An actor is anything that can act: an AI agent, service, device, operator, node or internal automation.

JIS gives every actor cryptographic identity:

- a long-lived domain or actor key
- deployment or instance keys
- session keys for short-lived work
- challenge-response proofs
- key succession when identity changes

The first rule is simple:

> Before you trust what an actor says, verify that it controls the key it claims.

Local networks can use internal actor names before public `.aint` names exist:

```text
home-agent.local
audit-node.local
factory-line-3.local
finance-bot.internal
```

Public `.aint` is a federation layer, not the beginning of identity.

## 2. Causal Evidence: TIBET

TIBET records the causal chain around actions. It is not just logging. The important part is that intent can be recorded before action and linked to completion afterwards.

| Dimension | Meaning |
|---|---|
| `ERIN` | What is in the action: payload, object, material |
| `ERAAN` | What is attached to it: references, dependencies, links |
| `EROMHEEN` | What is around it: environment, policy, context |
| `ERACHTER` | What is behind it: intent, reason, consequence |

In practice a chain should answer:

```text
who acted
what they intended
what object or message was involved
which policy applied
what route was used
what changed
what follow-up happened
```

If the evidence is created only after everything happened, it is weaker. The stronger pattern is:

```text
declare intent -> act -> record result -> link follow-up
```

## 3. Known Actors

Before global discovery, build a known-actor set. This is your local trust map.

```yaml
actors:
  audit-node.local:
    identity: jis:ed25519:...
    role: evidence
    allowed_routes: [audit, report]
  home-agent.local:
    identity: jis:ed25519:...
    role: operator-agent
    allowed_routes: [ipoll, command-request]
  build-runner.local:
    identity: jis:ed25519:...
    role: ci
    allowed_routes: [sbom, wayback]
```

Known actors should be explicit. Discovery helps find actors; it should not silently grant authority.

## 4. Names: AINS

AINS resolves names to actor metadata. A name can be local, private or public.

```text
local name     -> internal registry
private .aint  -> self-hosted registry
public .aint   -> federated AInternet registry
```

Resolution answers:

- which public key belongs to this actor?
- which endpoints are advertised?
- what capabilities are claimed?
- what trust or verification metadata exists?

Resolution does not answer:

- may this actor perform this action?
- has the other side consented?
- is this payload safe?

Those belong to Cortex, SNAFT and Airlock.

## 5. Routes: MUX

MUX is the routing layer. It should open routes after proof, relation and policy.

```text
resolve actor
verify fresh proof
check known relation
check policy
open route
emit TIBET receipt
```

This keeps the network from treating reachability as permission.

## 6. Messages: I-Poll

I-Poll is typed messaging for actors and agents:

| Type | Use |
|---|---|
| `PUSH` | Share information |
| `PULL` | Ask for information |
| `SYNC` | Exchange context |
| `TASK` | Request work |
| `ACK` | Confirm receipt or result |

Message type matters because a `TASK` is not just text. It can trigger work, state change, cost, tool calls or external effects. That means it needs stronger checks than a simple `PUSH`.

## 7. Policy: Cortex

Cortex decides whether an actor is allowed to do something.

Good policy checks include:

- actor identity
- actor tier or role
- requested action
- route
- current route posture (`#RCTAM`, not a trust score)
- local allow/deny rules
- required consent
- required isolation

Policy should fail closed. Unknown actor, unknown route or unknown intent should not become implicit permission.

## 8. Consent: SNAFT

SNAFT adds bilateral consent. This matters when both sides must agree to the exchange.

Examples:

- private data transfer
- long-running task delegation
- tool execution
- sensitive model context
- cross-organization exchange

Unilateral auth says "I have a token." SNAFT says "both sides agreed to this kind of exchange under this scope."

## 9. Isolation: Airlock

Some work should not run directly in your normal environment.

Airlock is the boundary for:

- unknown input
- generated code
- risky tools
- untrusted artifacts
- commands with external effects

The goal is not only to block bad work. It is to create a controlled place where risky work can be inspected, constrained, approved or rejected.

## 10. Evidence: Wayback, SBOM, CBOM

Once actors can act, you need to reconstruct what existed and what changed.

| Evidence type | Answers |
|---|---|
| Wayback seal | What was the system state at this point? |
| SBOM | Which software materials were present? |
| AI-SBOM | Which AI/model/tool materials were involved? |
| CBOM | Which capabilities and authorities existed? |
| TIBET trail | Which actions happened, in what causal order? |

The network becomes audit-ready when identity, action, route, policy and material state can be linked.

## 11. Federation: AInternet

Public AInternet federation is what you use when local or private actors need to discover and communicate with outside actors.

Federation gives you:

- public `.aint` names
- broader discovery
- cross-agent messaging
- public verification paths
- known public actors

It should not remove local control. Your network can remain local, private, self-hosted or partially federated.

## The Short Version

```text
Identity before messages.
Intent before action.
Policy before route.
Consent before sensitive exchange.
Isolation before risky execution.
Evidence before trust claims.
Federation only when useful.
```

## Conformance Families

The protocol docs explain the model. Conformance vectors test whether another implementation computes the same result.

| Family | Question |
|---|---|
| `ztip-conformance` | Can implementations agree on actor proof, offer envelopes, freshness and DID/namespace boundaries? |
| `tibet-comms-conformance` | Can implementations resolve, reach, route, deliver, reject and prove a message? |
| `tibet-evidence-conformance` | Can implementations store, seal, trace, restore and report evidence objects? |
| `tibet-security-conformance` | Can implementations make the same allow/deny/quarantine/null-route decision and fail closed? |

Shared primitives:

| Primitive | Primary conformance home | Consumed by |
|---|---|---|
| TimeVector / causal time | `tibet-evidence-conformance` | identity, comms, security |
| UPIP process reproducibility | `tibet-evidence-conformance` | comms, security, triage/runtime |

Short rule:

```text
docs explain
vectors decide
independent implementations prove
```

## Doctrine vs Documentation

Keep the separation clear:

| Kind | Purpose | Examples |
|---|---|---|
| Doctrine | why and invariants | `doctrine-l0.html`, `connect.html`, `causal-action-receipts.html` |
| Documentation | how and reference | these protocol pages |
| Machine-readable | what an AI agent can load and call | `resources.json`, `api.json`, `upip.json` |
| Conformance | what another implementation must reproduce | JSON vector families |

## Related

- [Build Your Network](build.md)
- [JIS](../protocols/jis.md)
- [TIBET](../protocols/tibet.md)
- [AINS](../protocols/ains.md)
- [MUX](../protocols/mux.md)
- [I-Poll](../protocols/ipoll.md)
