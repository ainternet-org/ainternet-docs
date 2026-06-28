# Runtime Box Model

A runtime box is a bounded place where an AInternet actor can run.

The canonical RAINT runtime is Ignition-backed KVM/microVM. Containers can follow the same control-plane contract later as a lower-isolation compatibility tier, but they are not the RAINT baseline.

```text
identity -> consent -> route -> workload -> evidence -> destroy
```

That is the Redstone lesson.

## Why Boxes Exist

An AInternet network is not only names and messages. Actors eventually need places to do work:

- a hacker lab target;
- an AI runtime with tools;
- a device controller;
- a self-hosted bot page;
- a temporary project mesh;
- a partner workload;
- a risky artifact under Airlock;
- a function surface such as `summarize.aint` or `tibet-ping.aint`.

The box gives that work a boundary. The AInternet substrate gives it identity, route posture and audit.

## Box Types

| Box | Runtime | Use |
|---|---|---|
| AInternet-in-a-box | Ignition-backed KVM/microVM | friendly node: boot, bind identity, open named surfaces, audit locally |
| RAINT | Ignition-backed KVM/microVM | canonical runtime actor box |
| Function box | RAINT profile | one bounded function surface behind a `.aint` route |
| Agent box | RAINT profile | AI/runtime with tools, inbox/outbox and continuity |
| Hackbox | disposable RAINT profile | CTF, pentest, messy lab target |
| Device box | process or RAINT profile | local hardware or home automation actor |
| Partner box | RAINT / boxd profile | external actor with scoped access and budget |
| Container box | rootless container | later compatibility tier, weaker isolation, same control plane |

Build the friendly node first. A hackbox is the same box model plus adversary, scenario and flag gate. That makes the arena a strict specialization, not a separate substrate.

## The Invariant

Every box should carry the same minimum contract:

```text
box id
parent actor
runtime actor
JIS proof
TIBET allocation receipt
MUX surfaces
policy/consent window
materialized workload
evidence location
TTL or shutdown condition
destroy/tombstone receipt
```

The operator should be able to ask:

```text
who owns this box?
what can reach it?
which surfaces exist?
which actions are allowed?
what evidence will survive teardown?
how does it die?
```

If those questions are unclear, the runtime is only a process, not an AInternet box.

## Reference Lifecycle

```text
1. request
   caller asks for a box, purpose and scope

2. admit
   JIS proof and policy are checked

3. allocate
   CPU/RAM/network/GPU budget is reserved

4. materialize
   golden image, container image or sealed session state is mounted

5. bind
   runtime .aint is minted or loaded

6. grant
   consent, relation and allowed surfaces are recorded

7. start
   workload boots; only allowed surfaces become reachable

8. observe
   TIBET, continuityd, audit, SBOM/AI-SBOM/CBOM collect evidence

9. close
   TTL, operator stop, policy fail or idle reaper shuts the box down

10. release
    state is sealed or discarded; child actors are tombstoned
```

## RAINT As The Golden Reference

The P520 Redstone RAINT flow is the current reference because it proved the important control-plane shape on Ignition/KVM:

```text
knock from caller
mint short-lived raint-*.test.aint
prepare summoned-lane carrier
boot golden rootfs
bind JIS identity inside the guest
grant consent for a TTL window
expose handshake.aint and audit.aint
keep capture.this dark without clearance
route only signed MUX frames
destroy on TTL
write audit
```

This makes RAINT more than a demo. It is the model for how to give someone a fast disposable AInternet node without giving them your host.

The reusable factory split is:

| Part | Lifetime | Meaning |
|---|---|---|
| golden image | immutable, reusable, secret-free | OS, trust kernel, AInternet stack and boot contract |
| drop carrier | per session, read-only | identity ladder, consent grant, lane expectation and box manifest |
| overlay | ephemeral, writable | runtime scratch, reset on destroy |

The golden image must not contain keys, identities, flags or customer state. Those belong in the drop carrier or overlay.

## Profiles

### Unsynced

One box, no relation to peers.

Use it to prove:

```text
dark by default
no enumeration
handshake.aint works
audit.aint records
unknown surfaces return 0x0000
```

### Synced

Two fresh boxes with an explicit 2-of-2 relation.

Use it to prove:

```text
box A and box B can route only after relation
allowed surfaces are named
forged relation edges fail closed
TIBET records the sync lane
```

### Messy

A reproducible noisy box.

Use it to test real-world operator work:

```text
stale files
old packages
misleading logs
incomplete local apps
stale AINS entries
half-configured services
```

The mess belongs inside the box, not on the host.

## Surface Model

Do not expose raw ports as the authority. Expose named surfaces.

Examples:

| Surface | Meaning |
|---|---|
| `handshake.aint` | open test fixture for a granted box |
| `audit.aint` | read bounded evidence |
| `capture.this` | sealed target, dark without clearance |
| `pty.aint` | foothold lease, not a raw shell |
| `tool.<name>.waint` | delegated tool wrapper |
| `page.aint` | actor page or botpage surface |

The rule is:

```text
identity + consent + relation + surface policy = route
anything else = 0x0000
```

## Inside And Outside

There are two valid operating postures.

Outside mode:

```text
operator stays outside
signs MUX frames
broker verifies
guest sees only granted surfaces
```

Inside mode:

```text
operator receives a short-lived foothold lease
inside actor is child-bound to the parent RAINT
all child actions carry parentage and TTL
teardown tombstones the child identity
```

Inside access must not be an accidental SSH backdoor. It must be a named surface such as `pty.aint`, with identity, consent, TTL and audit.

## Containerized Boxes

A containerized AInternet box should use the same contract, with a weaker isolation tier. It is not RAINT. It is a compatibility path for workloads that do not need the KVM boundary.

Recommended container baseline:

```text
rootless
read-only root
cap-drop=ALL
no-new-privileges
pids/memory/cpu limits
network none by default
inbox read-only
outbox/state bounded
all network through MUX/I-Poll grants
```

The container image is material evidence. Record:

```text
image digest
SBOM
AI-SBOM if a model/runtime is mounted
CBOM capabilities
policy hash
TIBET start token
TIBET stop token
```

Container is a cell. AInternet is the control plane.

## Box Manifest

A portable runtime box should be describable as a manifest:

```yaml
kind: org.ainternet.runtime-box.v1
name: demo-node
box_kind: node
runtime: ignition-kvm
isolation: microvm
golden_ref: sha256:...
parent_actor: operator.local
surfaces:
  - handshake.aint
  - audit.aint
  - capture.this
ttl: 300
network:
  default: dark
  egress: denied
evidence:
  tibet: required
  audit: required
  sbom: recommended
  cbom: recommended
material:
  image: sha256:...
  golden_rootfs: sha256:...
policy:
  unknown_surface: 0x0000
  child_identity: parent-bound
```

The same shape can describe:

```text
local AI worker
browser botpage
device controller
temporary partner function
red-team RAINT
```

## What Not To Claim

Do not say:

```text
containers are as isolated as KVM
the public edge owns the runtime
the filename proves the artifact
reachability means consent
an open port is the API
```

Say instead:

```text
the box has a tier
the route has a posture
the object has a manifest
the action has a receipt
the actor has a key
```

## Related

- [Redstone RAINT Lab](redstone-raint-lab.md)
- [Build Your Network](../network/build.md)
- [Reaching a RAINT](../learn/reaching-a-raint.md)
- [Audit Cockpit](../operators/audit-cockpit.md)
- [Airlock](../protocols/airlock.md)
- [MUX](../protocols/mux.md)
