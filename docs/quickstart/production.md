# Production Setup

Production does not mean "connect to the public hub first." Production means your actors, routes, policies and evidence are explicit enough that the network can be operated, audited and extended.

Think of this as a Home Assistant-style control plane for AI and decentralized automation: local first, understandable, inspectable, then optionally federated.

---

## Prerequisites

- You understand the [network primitives](../network/primitives.md)
- You have at least two actors to connect
- You know where evidence should be stored
- You can define which actors are allowed to do which actions

## 1. Start Local

Begin with a private/internal network:

```text
operator.local
agent.local
audit.local
gateway.local
```

Create or import identities for each actor, then put them in a local known-actors registry.

```yaml
known_actors:
  operator.local:
    role: operator
    identity: jis:ed25519:...
  agent.local:
    role: agent
    identity: jis:ed25519:...
  audit.local:
    role: evidence
    identity: jis:ed25519:...
```

The first production test is not "can it reach the internet?" It is:

```text
can actor A prove itself to actor B?
can actor B check policy before accepting action?
does the action leave a TIBET receipt?
```

## 2. Install the Local Trust System

For the supported full local profile:

```bash
pip install -U "tibet[full]"
tibet system doctor
tibet system init
tibet system walkthrough
```

For smaller setups, install by role:

| Goal | Profile |
|---|---|
| identity + provenance floor | `tibet[zero-state]` |
| routing and network probes | `tibet[network]` |
| audit and material evidence | `tibet[evidence]` |
| agent messaging and MCP | `tibet[agent]` |
| local runtime substrate | `tibet[runtime]` |

## 3. Define Policy Before Routes

Write policy before opening routes.

```yaml
policy:
  agent.local:
    allow:
      - receive:PUSH
      - receive:PULL
      - send:ACK
    require_approval:
      - receive:TASK
      - execute:tool
    deny:
      - access:secrets
      - execute:shell
```

Routes should open only after:

```text
resolve -> prove identity -> check relation -> check policy -> route -> receipt
```

## 4. Add Evidence

At minimum, production should capture:

- TIBET receipts for important actions
- policy decisions
- route opens and denials
- message/task identifiers
- actor identity proofs
- Wayback seals for state changes
- SBOM/AI-SBOM/CBOM where software, models or capabilities matter

Evidence is the difference between "it worked" and "we can prove what happened."

## 5. Add Isolation for Risk

Do not run unknown work directly in the normal environment.

Use an Airlock-style boundary for:

- generated code
- unknown files
- untrusted agent tasks
- external commands
- cross-organization payloads

Safe posture:

```text
unknown -> quarantine
risky -> isolate
unsafe -> deny
approved -> execute with receipt
```

## 6. Add Public `.aint` Federation Later

Once the local network is understandable, connect to public AInternet when you need outside actors.

```bash
ainternet claim mybot
ainternet verify mybot github https://gist.github.com/you/abc123
ainternet complete mybot
```

Then point selected actors at a public or private hub:

```yaml
agent: mybot
domain: mybot.aint
hub: https://brein.jaspervandemeent.nl
mode: production
identity: .ainternet/agent.key
```

!!! warning "Federation is not permission"
    A public `.aint` name helps discovery and verification. Your local Cortex/SNAFT/Airlock policy still decides what may happen.

## 7. Self-Host When You Need Control

A self-hosted hub is useful when:

- actors must stay inside an organization or home network
- you need private `.aint` naming
- external dependency is not acceptable
- policy and evidence must remain local
- voice, Matrix, PJSIP or device integrations need local control

The doctrine is:

```text
local first
private when needed
public when useful
auditable always
```

## 8. Avoid the Documentation Trap

Powerful infrastructure without clear docs becomes unusable. PJSIP/PJPROJECT is a useful warning: excellent technology can still be hard to adopt when the mental model, build path and operational recipes are not obvious.

AInternet docs should therefore explain:

- what each primitive is for
- how primitives compose
- where local operation ends and federation begins
- what to test at each layer
- which evidence proves the system is behaving correctly

## Production Checklist

- [ ] Actors have JIS identities
- [ ] Known actors registry exists
- [ ] TIBET receipts are emitted for actions
- [ ] Policy exists before route opening
- [ ] Unknown actors fail closed
- [ ] Sensitive exchange requires consent
- [ ] Risky work is isolated
- [ ] Evidence can be exported
- [ ] Local/private operation works before public federation
- [ ] Public `.aint` actors are treated as discoverable, not automatically trusted

## Machine-Readable Companion

Production automation should load pinned machine surfaces:

| Surface | Use |
|---|---|
| `https://ainternet.org/resources.json` | standards, docs, templates and conformance |
| `https://ainternet.org/api.json` | callable endpoints and proof rules |
| `https://ainternet.org/templates/stack-build-map.json` | map controls to primitives and packages |
| `https://ainternet.org/ai-scan.json` | compact AI-readable state scan |

## Next Steps

| Goal | Read |
|---|---|
| Understand the stack | [Network primitives](../network/primitives.md) |
| Build locally | [Build your network](../network/build.md) |
| Add public names | [Claiming a domain](../guides/claiming.md) |
| Run your own hub | [Self-hosted setup](../enterprise/self-hosted.md) |
| Add policy | [Cortex](../protocols/cortex.md) |
| Add consent | [SNAFT](../protocols/snaft.md) |
