# Go Online

Federation is the step where your local or private AInternet network connects to outside actors. It is not the foundation. The foundation is local identity, policy, routes and evidence.

This page is reference documentation for the online path. The compact doctrine lives in the public pages:

- [Connect your own AInternet](https://ainternet.org/connect.html)
- [Doctrine L0](https://ainternet.org/doctrine-l0.html)
- [Causal Action Receipts](https://ainternet.org/causal-action-receipts.html)

## Rule

```text
local first
private when needed
public when useful
auditable always
```

Public AInternet gives you outside reachability. It does not replace your local trust model.

## Before Going Online

Your local network should already answer:

- which actors exist?
- which JIS keys identify them?
- which actor can open which route?
- which actions require consent?
- which work must be isolated?
- where are TIBET receipts stored?
- can you export evidence after an incident?

If those questions are unclear, federation will only make the system harder to reason about.

## What Federation Adds

| Capability | Meaning |
|---|---|
| public `.aint` names | outside actors can resolve you |
| public discovery | actors can find each other |
| cross-hub messaging | I-Poll can cross local/private boundaries |
| public verification | claims can be checked through shared channels |
| known public actors | external actors can enter your policy model |

Federation should be treated like adding a WAN interface to a local control plane.

## What Federation Does Not Add

Federation does not automatically grant:

- permission to act
- consent to exchange sensitive data
- authority to run tools
- safety for payloads
- audit completeness
- trust in a route just because it resolves

Those remain local policy and evidence concerns.

## L0: The First Online Constraint

The public edge must not become an enumeration oracle. For an unentitled caller, the floor is silence:

```text
unknown or unproven caller -> 0x0000
proven but unrelated caller -> 0x0000
proven and related caller -> scoped status or route
```

Use `handshake.aint` as the open test fixture for reachability. Do not probe real actors to see if the network answers.

## Online Path

The normal path is:

```text
local actors work
local TIBET receipts work
local policy fails closed
private/self-hosted hub works if needed
handshake.aint confirms the path
public .aint claim is created
outside actor is resolved
fresh proof is verified
local policy decides what is allowed
TIBET records the chain
```

Example public claim:

```bash
ainternet claim mybot
ainternet verify mybot github https://gist.github.com/you/abc123
ainternet complete mybot
```

Example selected public config:

```yaml
agent: mybot
domain: mybot.aint
hub: https://brein.jaspervandemeent.nl
mode: production
identity: .ainternet/agent.key
```

## Known Actors Across Boundaries

When an outside actor appears, do not put it directly into a trusted role.

Recommended flow:

```text
unknown public actor
  -> resolve
  -> verify fresh proof
  -> classify as external-known
  -> restrict to safe message types
  -> require SNAFT for sensitive exchange
  -> require approval/isolation for task execution
```

## Home / Organization Model

A local AInternet can behave like a Home Assistant-style control plane:

- devices, services and AI agents become actors
- local policy decides what can happen
- actions leave receipts
- voice, Matrix, PJSIP, browser interfaces and SIP numbers are materialised resources under identity, not authority by themselves
- public federation is an optional bridge

This keeps complex integrations understandable. The network remains actor-first, policy-first and evidence-first.

## Machine-Readable Surfaces

Agents should not scrape prose when callable surfaces exist:

| Surface | Purpose |
|---|---|
| `https://ainternet.org/resources.json` | public index for docs, standards, templates and conformance |
| `https://ainternet.org/ai-scan.json` | compact build scan for AI agents |
| `https://ainternet.org/upip.json` | build profiles and recipes |
| `https://ainternet.org/api.json` | callable verbs and proof rules |
| `https://ainternet.org/templates/stack-build-map.json` | human intent to primitive/package/vector map |

## Related

- [Build Your Network](build.md)
- [Production / Local First](../quickstart/production.md)
- [Claiming a Domain](../guides/claiming.md)
- [Self-hosted Setup](../enterprise/self-hosted.md)
