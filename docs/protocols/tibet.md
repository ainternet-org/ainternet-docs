# TIBET — Traceable Intent-Based Event Tokens

TIBET is the causal evidence layer. It records why an action was started, what it touched, which context surrounded it, and what happened afterwards.

It works locally, privately or federated. A public AInternet actor can use TIBET, but TIBET does not depend on the public network.

## Why TIBET Exists

Normal logs are usually written after something happened. That is useful, but weak.

TIBET is stronger because it can create an evidence chain around the action:

```text
intent -> policy/context -> action -> result -> consequence
```

This lets an operator answer:

- who acted?
- what was the declared intent?
- which object, message or route was involved?
- which policy applied?
- what was attached or referenced?
- what changed afterwards?
- can another party verify the chain?

## Four Provenance Dimensions

TIBET uses four Dutch-inspired dimensions:

| Dimension | Literal sense | Evidence question |
|---|---|---|
| `ERIN` | "in it" | What is inside the action or object? |
| `ERAAN` | "attached to it" | What references, dependencies or links are attached? |
| `EROMHEEN` | "around it" | What context, environment or policy surrounds it? |
| `ERACHTER` | "behind it" | What intent, reason or consequence is behind it? |

These can be represented as token types, fields or linked events depending on the implementation. The important part is the model: action evidence is multi-dimensional, not just a timestamped string.

## Example Token

```json
{
  "token_id": "TBT_01J...",
  "actor": "agent.local",
  "action": "ipoll_send",
  "target": "audit.local",
  "erin": {
    "payload_hash": "sha256:abc..."
  },
  "eraan": {
    "refs": ["task-123", "policy:default-local"]
  },
  "eromheen": {
    "route": "mux:local",
    "policy_decision": "allow",
    "environment": "local-network"
  },
  "erachter": {
    "intent": "send audit summary for operator review"
  },
  "parent_token": null,
  "timestamp": "2026-04-12T10:00:00Z",
  "signature": "ed25519:...",
  "chain_id": "chain_01J..."
}
```

## Action Chain

A strong action chain looks like this:

```text
ERACHTER intent declared
  -> EROMHEEN policy and context captured
  -> ERIN payload/object hash recorded
  -> ERAAN references attached
  -> action executes
  -> result token links back to the intent
```

For a message:

```text
actor proves identity
policy allows route
message hash is recorded
I-Poll delivery happens
ACK links to original message
audit report can reconstruct the chain
```

## Local Network Example

```python
from tibet import Tibet

t = Tibet(actor="agent.local", identity=identity)

intent = t.create_token(
    action="task_prepare",
    erachter={"intent": "summarize sensor report for operator.local"},
    eromheen={"policy": "operator-review-required"}
)

result = t.create_token(
    action="task_complete",
    parent_token=intent.token_id,
    erin={"payload_hash": "sha256:..."},
    eraan={"refs": ["sensor-report-2026-06-24"]}
)

print(result.chain_id)
```

## Verification

Any party with the actor public key and token chain can verify:

```python
ok = t.verify_token(token_id="TBT_01J...")
print(ok.valid)
print(ok.actor)
print(ok.signed_at)
```

CLI form:

```bash
tibet verify TBT_01J...
tibet export --format json
```

## What TIBET Records

| Network event | TIBET evidence |
|---|---|
| actor identity proof | challenge, response, key, timestamp |
| route open | actor, target, policy, route, decision |
| message send | payload hash, type, target, parent task |
| task request | intent, scope, approval state |
| consent exchange | proposal, acceptance/rejection, scope |
| airlock run | input hash, constraints, result |
| snapshot | state seal, SBOM/CBOM refs |
| key succession | old key, new key, reason, proof |

## Integration Points

| Component | Token events |
|---|---|
| JIS | identity proofs, key succession |
| AINS | registration, resolution, public/private claim changes |
| MUX | route request, allow/deny, route close |
| I-Poll | send, receive, ACK, thread continuation |
| Cortex | permission decision |
| SNAFT | consent proposal and agreement |
| Airlock | quarantine, run, denial, release |
| Wayback | seal, diff, restore |
| Pol | health check, drift detection |

## EU AI Act Mapping

TIBET helps with record keeping because it links intent, action, context and result. For high-risk AI systems this supports reconstructability: not just "the system produced output," but "this actor acted under this policy with this evidence chain."

See [EU AI Act Compliance](../enterprise/eu-ai-act.md) for the broader mapping.

## Related

- [Network Primitives](../network/primitives.md)
- [JIS Identity](./jis.md)
- [I-Poll Protocol](./ipoll.md)
- [Cortex Permissions](./cortex.md)
- [Wayback Snapshots](./wayback.md)
