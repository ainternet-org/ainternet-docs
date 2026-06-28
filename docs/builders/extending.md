# Build on AInternet

AInternet should feel like a kernel boundary for decentralized AI systems.

The core primitives are small and strict:

```text
JIS identity
TIBET receipts
AINS resolution
MUX routing
I-Poll messages
Cortex policy
SNAFT consent
Airlock isolation
Wayback/SBOM/CBOM evidence
```

Your code lives in user space. It can be an AI agent, database adapter, voice bridge, red-team tool, workflow runner, UI, model router, storage backend or new sandbox implementation.

## Kernel vs User Space

| Kernel primitive | User-space extension |
|---|---|
| actor identity | your agent, service, device or process |
| receipt creation and verification | your action log, workflow or app event |
| route open/deny | your transport, bridge or protocol adapter |
| policy decision | your product permission model |
| consent scope | your sharing workflow |
| isolation verdict | your runner, sandbox or executor |
| evidence object | your database, artifact store or report |

The boundary is simple:

```text
extensions may request
kernel primitives decide
receipts prove what happened
vectors define compatibility
```

## Standard Hooks

Every extension should know where to hook in:

| Hook | What the extension provides | What the kernel primitive provides |
|---|---|---|
| `identity.prove` | actor name and challenge | JIS fresh proof |
| `receipt.issue` | action, target, parent, payload hash | TIBET event id and signature |
| `route.request` | from, to, intent | MUX allow/deny/null-route |
| `message.send` | typed message and target | I-Poll envelope and receipt |
| `policy.check` | actor, action, scope | Cortex verdict |
| `consent.propose` | scope and peer | SNAFT accept/reject chain |
| `isolation.run` | workload and risk metadata | Airlock verdict and run receipt |
| `evidence.attach` | object hash and metadata | Wayback/SBOM/CBOM/trail reference |

Agents should use machine-readable surfaces where available:

```text
https://ainternet.org/resources.json
https://ainternet.org/api.json
https://ainternet.org/upip.json
https://ainternet.org/templates/stack-build-map.json
```

## Plugin Shape

A plugin should be boring to load:

```json
{
  "id": "hello-receipt-plugin",
  "kind": "org.ainternet.plugin.v1",
  "actor": "plugin.local",
  "requires": ["jis.prove_request", "tibet.issue_receipt"],
  "provides": ["hello.say"],
  "conformance": ["tibet-evidence-conformance:v1"]
}
```

The plugin can implement anything, but it should expose:

- what verbs it provides
- which primitives it calls
- what receipts it emits
- which conformance vectors cover it
- whether it needs network, filesystem, secrets, model access or isolation

## Hello World Plugin

The smallest useful plugin proves identity, performs one harmless action, and emits one receipt.

```python
from ainternet import AInternet
from tibet import Tibet

ai = AInternet(agent_id="plugin.local")
tibet = Tibet(actor="plugin.local", identity=ai.identity)

parent = tibet.create_token(
    action="plugin.intent",
    erachter={"intent": "say hello to audit.local"},
    eromheen={"plugin": "hello-receipt-plugin"}
)

message = "hello from plugin.local"

receipt = tibet.create_token(
    action="plugin.hello",
    parent_token=parent.token_id,
    erin={"payload_hash": "sha256:<hash-of-message>"},
    eraan={"target": "audit.local"}
)

ai.send("audit.local", message)
print(receipt.token_id)
```

That is not production code. It is the shape:

```text
load identity
declare intent
perform scoped action
emit receipt
send or attach result
```

## Sandbox Plugins

If someone invents a better sandbox, it should live beside the existing Airlock/Trust Kernel path without rewriting the network.

Minimum sandbox plugin contract:

| Field | Meaning |
|---|---|
| input hash | what entered the sandbox |
| policy | why it was allowed or denied |
| constraints | CPU, memory, network, filesystem, time |
| result hash | what came out |
| verdict | allow, deny, quarantine, release |
| receipt | TIBET chain node for the run |
| vectors | security/evidence vectors it satisfies |

The kernel asks:

```text
is this workload allowed?
which boundary runs it?
what proof did the boundary return?
does the receipt link back to the requested action?
```

## Rough RFC Model

AInternet extensions should follow a rough RFC model:

```text
show the primitive
show the code
show the vector
show the receipt
```

No heavyweight standards theater is required. A proposal is credible when another builder can run it and get the same result.

Recommended proposal structure:

| Section | Content |
|---|---|
| Problem | what primitive gap exists |
| Hook | which kernel primitive is extended |
| Code | minimal reference implementation |
| Vector | JSON test vector or conformance addition |
| Receipt | example TIBET chain |
| Security | how it fails closed |
| Interop | how a second implementation verifies it |

## Challenges and Bounties

Hard problems should be public enough for serious builders and red-teamers.

Good challenge shape:

```text
Here is the invariant.
Here is the vector set.
Here is the reference behavior.
Break it, or implement it independently.
```

Examples:

- Can you make MUX leak differential status without proof and relationship?
- Can you spam a route without a valid causal receipt?
- Can you replay an old action past freshness checks?
- Can you make a sandbox plugin release an object without a verdict receipt?
- Can you create a fake actor relation without a JIS proof chain?

Winning should mean improving the primitive, vector or implementation.

## Awesome-AInternet

Third-party work should be visible.

Candidate categories:

- receipt readers and trail visualizers
- JIS identity tools
- AINS registry browsers
- I-Poll clients
- MUX transport adapters
- Airlock/sandbox plugins
- Wayback/SBOM/CBOM viewers
- local Home Assistant-style integrations
- Matrix, SIP/PJSIP and voice bridges
- red-team and conformance tools

Inclusion rule:

```text
works locally
states which primitives it uses
emits or verifies receipts where relevant
does not ask users to trust transport as authority
```

## Conformance Before Claims

The preferred path for a serious plugin:

```text
prototype
receipt
vector
second implementation
awesome listing
```

The docs can praise a tool only after the boundary is clear.

## Related

- [Network Primitives](../network/primitives.md)
- [Build Your Network](../network/build.md)
- [Go Online](../network/federation.md)
- [TIBET](../protocols/tibet.md)
- [MCP Integration](../guides/mcp.md)
- [Stability Policy](../reference/stability.md)
