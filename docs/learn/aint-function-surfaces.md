# .aint Function Surfaces

An `.aint` name is not only a domain-like label. In a running AInternet, it can also name a function surface: a capability-addressed operation such as `handshake.aint`, `audit.aint`, `capture.this`, `pty.aint`, or `tibet-ping.aint`.

The useful distinction is:

```text
actor posture tells who is acting
surface name tells what is being asked
MUX decides whether the route exists
TIBET records what happened
```

This makes AInternet's tool layer feel MCP-like, but with identity, permission and provenance in the substrate.

## Actor Posture Is Not a Tool Category

Do not create a separate category called "tooling aints" unless the actor really is a tool runtime. First ask what posture the name carries.

| Posture | Meaning | Examples |
|---|---|---|
| `.aint` | sovereign actor | `jasper.aint`, `richard.test.aint` (human, agent, device) |
| `.raint` | runtime enclave/session | `raint-51fc8ee7.test.aint`, an enclave, a sandbox container context |
| `.waint` | wrapped actor/tool | `tibet-ping.codex.waint`, a sub-tool/worker acting on behalf of an actor |
| `.paint` | published or provisional surface | a public page, botpage, claimable signboard |
| `.saint` | system/service actor | `vault-keeper.aint`, persistent registry, arena infrastructure |
| `.maint` | maintenance posture | doctor, updater, key rotation, repair lane |
| `.taint` | test or adversarial posture | quarantine, poison lane, red-team probe, fuzz target |

The suffix is the posture. It says what kind of right is active right now. It does not automatically say what function is being called.


## Surface Names Are Verbs

A surface is the named operation exposed by an actor or runtime.

Examples:

| Surface | Meaning |
|---|---|
| `handshake.aint` | liveness under a verified knock |
| `audit.aint` | read the causal trail allowed to this actor |
| `capture.this` | sealed flag or protected resource |
| `pty.aint` | explicit inside foothold lease |
| `tibet-ping.aint` | reachability and route posture probe |
| `continuityd.aint` | continuity status or heartbeat surface |
| `tools.list.aint` | list callable surfaces visible to this actor |

The same surface name can appear under different actors:

```text
raint-123.test.aint exposes tibet-ping.aint
maint-doctor.aint calls tibet-ping.aint
taint-probe.aint fuzzes tibet-ping.aint
paint-docs.aint explains tibet-ping.aint
```

The surface is stable. The actor and posture around it can change.

## `tibet-ping.aint`

`tibet-ping.aint` should usually be treated as a function surface, not as a sovereign actor.

It asks:

```text
can this identity reach this route under this consent and policy?
```

It should not mean:

```text
the target is trusted
the action is allowed
the peer has consented to every later action
the route will stay open forever
```

A good result is shaped like:

```text
reachable: yes/no
route: allowed/dark/held
identity: verified/unverified
consent: present/missing/expired
receipt: tibet event id
```

That is why `tibet-ping.aint` belongs near MUX and TIBET, not near plain ICMP. It proves route posture, not raw network reachability.

## MCP-Style Tools

MCP-style tools can be represented as `.aint` surfaces when the call needs AInternet semantics:

```text
tool discovery    -> tools.list.aint
tool call         -> <tool-name>.aint
permission check  -> MUX/Cortex/SNAFT
trace             -> TIBET
identity          -> JIS
```

The difference from ordinary MCP is the substrate:

| Ordinary tool call | `.aint` function surface |
|---|---|
| caller is session-local | caller is an identity-bound actor |
| permission is app-defined | permission is route and policy material |
| trace is optional | receipt is part of the action |
| unavailable may be an error | unauthorized can be indistinguishable from nonexistent |

If a tool only exists inside one app and does not need network identity, consent or provenance, it may not need its own `.aint` surface. Keep it local. Promote it to a surface when routing, delegation, audit or cross-actor consent matters.

## Wrapper And Adapter Actors

Sometimes an existing system needs an AInternet wrapper:

```text
mcp.adapter.aint
postgres.adapter.aint
homeassistant.adapter.aint
matrix.adapter.aint
voice.adapter.aint
```

These are actors or runtimes when they hold keys, enforce policy, or issue receipts. They expose function surfaces for the work they perform.

Example:

```text
mcp.adapter.aint exposes tools.list.aint
mcp.adapter.aint exposes browser.open.aint
mcp.adapter.aint exposes memory.search.aint
```

The adapter is the actor. The surface is the verb.

## Dark By Default

Function surfaces obey the same dark rule as every other route.

```text
authorized actor + valid relation + allowed intent -> route
anything else -> no useful signal
```

This matters for tool discovery. `tools.list.aint` should list what the caller is allowed to see, not everything the runtime can do. A missing tool, a forbidden tool and a nonexistent tool may intentionally look the same to an untrusted actor.

## Naming Rule

Use the smallest truthful name:

```text
<actor posture> owns keys, leases, authority or runtime state
<surface name> names the callable function
<receipt> proves what happened
```

So:

```text
raint-51fc8ee7.test.aint exposes tibet-ping.aint
```

is usually better than:

```text
tibet-ping-runtime-service-tool.aint
```

unless `tibet-ping` itself is a long-lived actor with its own key, policy and audit responsibility.

## The Line To Keep

An `.aint` function is not just a tool endpoint. It is a callable surface whose existence is decided by identity, consent, relation and policy, and whose use leaves a receipt.
