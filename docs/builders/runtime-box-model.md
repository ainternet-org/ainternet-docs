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

A portable runtime box is declared by one manifest. This is the knob that turns the enclave into a box factory.

The current contract fields are:

| Field | Required | Meaning |
|---|---:|---|
| `box_kind` | yes | `node`, `arena` or `function_cell` |
| `runtime` | yes | canonical: `ignition-kvm`; `container` is later compatibility tier |
| `isolation` | yes | `microvm` for `ignition-kvm`; `container` for container tier |
| `golden_ref` | yes | content hash/reference for the reusable golden image, never a filesystem path |
| `identity_ladder` | yes | ordered actor/surface ladder used during bind and route proof |
| `ttl` | yes | duration such as `20m`, `24h`, `7d`, or `persistent` for a node |
| `rate_limit` | no | `{mbit:int, pps:int}` |
| `audit_mode` | yes | evidence depth such as `A5` |
| `surfaces` | yes | named `.aint` / `.waint` surfaces the box may expose |
| `gate` | kind-dependent | required for `arena`; may carry posture/cortex requirements |
| `scenario` | no | arena/function scenario label |

Unknown fields should be treated as warnings. Missing or invalid required fields fail closed.

### Node

```yaml
box_kind: node
runtime: ignition-kvm          # RAINT baseline
isolation: microvm
golden_ref: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
identity_ladder:
  - node.local
ttl: persistent
rate_limit: { mbit: 100, pps: 5000 }
audit_mode: A5
surfaces:
  - audit.aint
  - tool.echo.waint
gate:
  required_posture: "#34358"
```

### Arena

```yaml
box_kind: arena
runtime: ignition-kvm
isolation: microvm
golden_ref: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
identity_ladder:
  - handshake.aint
  - vault-keeper.aint
ttl: 20m
rate_limit: { mbit: 100, pps: 5000 }
audit_mode: A5
surfaces:
  - handshake.aint
  - capture.this
gate:
  cortex_level: L4
  required_posture: "#34358"
scenario: external-ai-containment
```

The arena is a strict specialization:

```text
node + adversary + scenario + flag gate
```

### Function Cell

A function cell must expose a tool/function surface:

```yaml
box_kind: function_cell
runtime: ignition-kvm
isolation: microvm
golden_ref: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
identity_ladder:
  - function.local
ttl: 1h
rate_limit: { mbit: 25, pps: 1000 }
audit_mode: A5
surfaces:
  - tool.summarize.waint
  - audit.aint
```

## Build Gates

The box does not spawn because a manifest exists. It spawns only after three gates pass.

```text
box-manifest validate
  -> seal-gate on golden image
  -> host can-carry attestation
  -> spawn
```

### Manifest Gate

The manifest validator refuses unknown box kinds, unknown runtimes, missing fields, invalid TTLs and unsafe golden references. A `golden_ref` must be a content hash/reference, not `/srv/...`, `/var/...` or any other host path.

Kind-specific rules:

| Kind | Extra rule |
|---|---|
| `node` | should expose `audit.aint` |
| `arena` | must have a `gate` and a flag/capture surface |
| `function_cell` | must expose a `tool.*` or `.waint` function surface |

### Seal Gate

The golden image is reusable and must be secret-free. The seal must fail if golden contains:

- private keys;
- identity files;
- hardcoded secrets or passwords;
- `.key.json`, `id_ed25519`, `.pem`, `.key`;
- baked `.tza` envelopes;
- `capture.this` or flag material.

Those belong in the per-session drop carrier or the ephemeral overlay, never in golden.

### Can-Carry Gate

The host must prove it can carry the box before spawn:

```json
{
  "kvm": true,
  "compute_lane": "fma-avx2",
  "bridge": true,
  "nftables": true,
  "tooling": {
    "lttle": true,
    "ignitiond": true,
    "takeoff": true,
    "vmlinux": true
  },
  "mem_mib_free": 4096,
  "vcpu_free": 4
}
```

Missing evidence denies. A host without the guest kernel, bridge, nftables isolation or KVM does not carry an `ignition-kvm` RAINT.

## Spawn Chain

The intended spawn chain is:

```text
verify_ignition_host --json
  -> can_carry(manifest, host)
  -> redstone box spawn <manifest>
  -> allocate resources
  -> mount golden/drop/overlay
  -> boot Ignition/KVM
  -> bind runtime .aint
  -> expose named surfaces
  -> audit-out through tibet-audit
```

This is where AInternet-in-a-box and hackbox stay the same core. The manifest changes the workload and gate; the lifecycle stays identical.

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
