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

## The Shape

The online path is a bridge between networks, not a landlord above them:

```text
your local AInternet
  -> outbound lane
  -> edge / hub / partner network
  -> outside actor
  -> local policy still decides
  -> TIBET records the chain
```

The edge may route. It must not become the authority for your identity, your consent, your payload or your audit trail.

## Connect Doctrine

When you connect your own AInternet, keep these layers separate:

```text
L0 silence          strangers get 0x0000
identity           your .aint / local actor key is the root
resolve            proven? related? scoped?
handshake.aint     the one open test fixture
edge lane          outbound-only, short-lived, signed
carrier            sealed .tza/TIBET-zip moves across the lane
local open         your side decrypts, checks policy and records evidence
```

This is the `connect.html` doctrine in operator form:

```text
inbound ports: zero
identity proof: fresh
edge visibility: envelope only
payload authority: local key and manifest
route authority: MUX + policy + consent
audit authority: local TIBET receipts
```

The outside network can deliver a sealed object. It cannot make that object safe, allowed or true by itself.

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

`handshake.aint` proves the path, not access to a peer:

```text
resolve handshake.aint        -> 0x4000  path fixture responds
resolve unknown-real-name     -> 0x0000  silence
resolve known-granted-actor   -> scoped status or route
```

Every other name has to be earned by proof and relation.

## Online Route Posture

For a connected network, route posture is the operator's location marker:

| You see | Meaning | Next step |
|---|---|---|
| `0x0000` | no entitlement, no disclosure, or not proven | prove identity or stop |
| `0x4000` on `handshake.aint` | the path fixture works | test your own node binding |
| proven identity, no relation | actor is real but not granted | negotiate or import relation |
| relation, no consent | route exists but action is not scoped | use SNAFT / operator approval |
| scoped route | named surface may carry this action | send sealed carrier and receipt |
| tombstone / successor | actor moved or retired | follow successor or stop retrying |

This is the user-facing promise:

```text
you are here
this is what is proven
this is the next safe move
```

If a step cannot say those three things, it is not ready to be a federation surface.

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
hub: https://your-hub.example
mode: production
identity: .ainternet/agent.key
```

The hub URL is configuration, not identity. A package should not silently phone a default third-party hub.

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

## Private-To-Private Connection

Public names are not required for federation. Two private AInternet networks can connect by exchanging known actor records and opening a scoped lane:

```text
network A exports partner record
network B imports partner record
both sides verify JIS proof
SNAFT records scope and duration
MUX opens only the named surfaces
sealed carriers move
each side writes its own TIBET receipts
```

This is useful for:

- household-to-family support;
- a lab and a staging network;
- a company and a contractor;
- two agents collaborating for a bounded task;
- temporary networks that will later be tombstoned.

When the relation ends:

```text
close lane
tombstone or expire relation
deny old route
keep the evidence
```

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
