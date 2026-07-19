# Security Behavior

AInternet security is layered. Each layer has a narrow job. Do not use one layer to replace another.

## Layer Jobs

| Layer | Job |
|---|---|
| JIS | prove actor identity now |
| TIBET | record the causal action chain |
| Cortex | decide whether an actor may perform an action |
| SNAFT | enforce bilateral consent and semantic scope |
| MUX | open or deny routes without leaking status |
| Airlock | isolate risky work and return a verdict |
| Triage | handle exceptional or risky actions without weakening guardrails |
| Trust Kernel | runtime enforcement floor |

## SNAFT Is Not a Runtime Toggle

SNAFT is a guardrail. It should not be edited mid-flight to make an operation pass.

Bad pattern:

```text
action blocked
operator weakens SNAFT rule live
action passes
audit trail claims policy was satisfied
```

Correct pattern:

```text
action blocked
triage opens an explicit review path
operator approves, rejects or scopes exception
TIBET records the decision
SNAFT remains the guardrail
```

If a rule can only be installed by disabling the rule system, the system is not secure.

## What Triage Does

Triage is the operator intervention layer. It handles work that is not safe to auto-allow.

Examples:

- unknown actor requests a task
- risky payload needs inspection
- canary or fixture operation needs temporary opening
- policy is incomplete
- generated code wants execution
- consent scope is ambiguous

Triage should create an explicit action trail:

```text
incoming request
  -> risk classification
  -> hold/quarantine
  -> operator or policy review
  -> allow/deny/scope
  -> receipt
```

## Airlock Behavior

Airlock is the isolation boundary for risky work.

Default behavior:

```text
unknown -> quarantine
risky -> isolate
unsafe -> deny
approved -> execute with constraints and receipt
```

An Airlock run should record:

- input hash
- requested capability
- policy decision
- constraints
- runtime posture
- output hash
- verdict
- TIBET receipt

## MUX and L0

MUX must avoid differential answers to unentitled callers.

```text
world -> 0x0000
proven but unrelated -> 0x0000
proven and related -> scoped status or route
```

`handshake.aint` is the test fixture for reachability. Real actors should not be probed as test targets.

## Fail-Closed Matrix

| Condition | Behavior |
|---|---|
| no actor proof | deny or floor |
| stale proof | deny or require freshness |
| unknown actor | `.paint` / quarantine |
| no relation | floor / no route |
| missing consent | hold or deny |
| ambiguous intent | triage |
| risky workload | Airlock |
| failed Airlock verdict | deny |
| missing receipt | do not finalize action |

## Related

- [SNAFT](../protocols/snaft.md)
- [Cortex](../protocols/cortex.md)
- [Airlock](../protocols/airlock.md)
- [MUX](../protocols/mux.md)
- [TIBET](../protocols/tibet.md)

## Machine-Readable

- `https://ainternet.org/api.json` — security gate, policy and route verbs
- `https://ainternet.org/resources.json` — security behavior and conformance references
