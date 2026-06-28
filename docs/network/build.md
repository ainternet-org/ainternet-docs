# Build Your Network

This guide is for building a decentralized zero-trust AInternet-style network. It starts local. Public `.aint` federation is optional and comes later.

## Target Shape

A minimal useful network has:

```text
one operator actor
one agent or service actor
one evidence location
one local registry of known actors
one signed action trail
one route or message path
one policy decision before action
```

That is enough to learn the architecture without depending on the public hub.

The same model can scale down or up:

```text
one human + one AI
one household + a few devices
one temporary project mesh
one organization hub
one federated partner network
```

## 1. Create Actor Identities

Start with actors, not packages.

Example actors:

| Actor | Role |
|---|---|
| `operator.local` | human/operator authority |
| `agent.local` | AI or automation actor |
| `audit.local` | evidence and report node |
| `gateway.local` | route and policy boundary |

Each actor needs a JIS identity and a fresh proof mechanism.

```text
actor name -> JIS public key -> current instance key -> proof challenge
```

For a private network, keep the initial actor registry local:

```yaml
known_actors:
  operator.local:
    key: jis:ed25519:...
    role: operator
  agent.local:
    key: jis:ed25519:...
    role: agent
  audit.local:
    key: jis:ed25519:...
    role: evidence
```

## 2. Add TIBET Receipts

Every meaningful action should produce evidence.

The minimum event chain:

```text
intent declared
policy checked
route opened or denied
message/action completed
result linked back to intent
```

This is the difference between an auditable network and a chat system with logs.

## 3. Add a Local Name Registry

You do not need public `.aint` names at the start. You need a registry that resolves actor names to identity and endpoints.

```yaml
registry:
  agent.local:
    identity: jis:ed25519:...
    endpoints:
      ipoll: http://agent.local:8080/ipoll
      mux: tcp://agent.local:9443
    capabilities:
      - answer
      - summarize
      - task.receive
```

Later this can map cleanly to AINS:

```text
agent.local -> private registry
agent.company.aint -> private/federated AINS
agent.aint -> public AInternet
```

## 4. Open Routes Only After Proof

The route opening sequence should be explicit:

```text
resolve actor
challenge actor
verify JIS response
check known relation
check Cortex policy
open MUX route or I-Poll delivery
write TIBET receipt
```

This prevents a common failure mode: treating network reachability as trust.

## 5. Add Message Semantics

When you introduce I-Poll, use typed messages:

| Message | Required checks |
|---|---|
| `PUSH` | identity, route policy |
| `PULL` | identity, route policy, read permission |
| `SYNC` | identity, relation, scope |
| `TASK` | identity, relation, policy, cost/risk gates |
| `ACK` | links to original message/action |

A `TASK` should usually create a stronger evidence trail than a `PUSH`, because it can cause work.

## 6. Add Policy and Consent

Use Cortex to decide what is allowed:

```yaml
policy:
  agent.local:
    can:
      - receive:PUSH
      - receive:PULL
    cannot:
      - execute:shell
      - access:secrets
```

Use SNAFT when the exchange needs agreement from both sides:

```text
agent asks for sensitive context
operator proposes scope
agent accepts or rejects
TIBET records the consent chain
message route opens only for that scope
```

## 7. Add Evidence and State Snapshots

Once actions affect state, add material evidence:

| Tooling layer | Purpose |
|---|---|
| TIBET trail | causal action chain |
| Wayback | point-in-time state seal |
| SBOM | software materials |
| AI-SBOM | AI/model/tool materials |
| CBOM | capabilities and authorities |
| Pol | health checks with receipts |

Evidence should be queryable by actor, action, route, object and time.

## 8. Add Isolation

Route risky work through Airlock or an equivalent boundary:

- unknown artifact
- untrusted code
- generated script
- command with filesystem/network effects
- cross-organization task

Safe default:

```text
unknown -> quarantine
risky -> isolate
unsafe -> deny
approved -> execute with receipt
```

## 9. Choose an Install Profile

Use profiles based on the job:

| Profile | Use when |
|---|---|
| `tibet[zero-state]` | you need identity and provenance primitives |
| `tibet[network]` | you need route probes, overlay and mesh primitives |
| `tibet[evidence]` | you need audit, SBOM, CBOM, reports and snapshots |
| `tibet[agent]` | actors need AInternet/I-Poll/MCP surfaces |
| `tibet[runtime]` | you want local operation without every enterprise layer |
| `tibet[full]` | you want the supported complete local trust-system profile |

After a full install, the intended local path is:

```bash
pip install -U "tibet[full]"
tibet system doctor
tibet system init
tibet system walkthrough
```

The command installs the tools. The network is the actor registry, policies, receipts, routes and evidence you define.

## 10. Federate When Useful

Connect to public AInternet when you need:

- public `.aint` names
- outside discovery
- agent-to-agent communication beyond your network
- public verification or claim paths
- inter-organization messaging

Federation should preserve your local rules:

```text
public actor resolves
fresh proof verified
local policy checks relation
SNAFT scope negotiated if needed
route opens or fails closed
TIBET records the chain
```

## 11. Retire or Succeed Actors Explicitly

Networks change. Devices leave, agents are replaced, projects end, keys rotate.

Do not silently delete identity history. Use tombstone or succession semantics:

```text
actor retired -> tombstone record + TIBET reason
actor replaced -> successor pointer + fresh proof
route closed -> MUX denies old path
relation renewed -> consent/policy is checked again
```

This keeps temporary networks temporary without losing auditability.

## Bare Necessity vs Production

| Bare necessity | Production needed |
|---|---|
| JIS identity | key succession procedure |
| TIBET receipts | signed export/report flow |
| known actors | role and permission model |
| local registry | private or public AINS |
| one route/message | MUX/I-Poll policy gates |
| one evidence trail | Wayback/SBOM/CBOM/Pol |
| manual checks | conformance vectors in CI |

## Test What You Built

Do not stop at a diagram. Each layer should map to a conformance family:

| Layer | Conformance |
|---|---|
| actor identity and fresh proof | `ztip-conformance` |
| reachability, MUX, I-Poll and null-route behavior | `tibet-comms-conformance` |
| TIBET trail, Wayback, SBOM, AI-SBOM, CBOM and reports | `tibet-evidence-conformance` |
| Cortex, SNAFT, Airlock, quarantine and no-fail-open | `tibet-security-conformance` |

The rule is:

```text
if it cannot be tested by vectors, it is still a claim
```

## Related

- [Network Primitives](primitives.md)
- [Build on AInternet](../builders/extending.md)
- [Production Setup](../quickstart/production.md)
- [Self-hosted Setup](../enterprise/self-hosted.md)
- [TIBET](../protocols/tibet.md)
- [Cortex](../protocols/cortex.md)
- [SNAFT](../protocols/snaft.md)
