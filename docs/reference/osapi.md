# OSAPI Pair

Most AInternet users do not call OSAPI directly. They use `ainternet`, `tibet`, a local node, a hub, or an SDK.

Builders and runtime authors should know what sits underneath:

```text
JIS OSAPI    -> identity plane: who is acting?
TIBET OSAPI  -> evidence plane: what causal proof exists?
```

Production systems bind to both. If either half is missing, the safe behavior is fail closed.

## Why Two Planes?

Identity and evidence are different authorities.

| Plane | Answers | Examples |
|---|---|---|
| JIS | who controls this key now? | claim, bind, challenge, session proof |
| TIBET | what happened and why? | emit, query, fork, verify receipts |

Keeping them separate prevents one layer from silently authorizing both the actor and the history.

## Who Needs To Care?

| Reader | OSAPI expectation |
|---|---|
| client user | none; use `ainternet[client]` |
| local node operator | know both planes must be healthy |
| hub operator | monitor both planes and fail closed |
| package builder | bind to both or use the official bindings |
| runtime builder | treat half-bootstrap as unsafe |

## Bootstrap Shape

```text
start package or runtime
  -> bootstrap JIS identity plane
  -> bootstrap TIBET evidence plane
  -> verify both are usable
  -> accept work
```

If JIS is unavailable, the runtime cannot prove who acts. If TIBET is unavailable, the runtime cannot prove what happened. Either case should block actions that require proof.

## Public AInternet vs Local OSAPI

OSAPI is local substrate. A public hub is optional coordination.

```text
local OSAPI pair:
  identity + evidence

hub API:
  AINS + I-Poll + MUX + federation surfaces
```

A public `.aint` route can use the same primitives, but the public hub is not the identity or evidence authority for your local network.

## Implementation Guidance

Packages should avoid creating private identity or receipt stores that bypass the substrate.

Preferred:

```text
use jis-core for actor binding
use tibet-core for receipts
emit route/action evidence before external effect where possible
fail closed if required proof cannot be written
```

Avoid:

```text
local ad-hoc trust databases
unsigned action logs as proof
public hub credentials as identity
policy that allows action when receipt emission fails
```

## Related

- [JIS](../protocols/jis.md)
- [TIBET](../protocols/tibet.md)
- [The Running Substrate](../learn/the-running-substrate.md)
- [Local Node Quickstart](../quickstart/local-node.md)
