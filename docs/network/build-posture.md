# AInternet Build Posture

The local-node build, expressed in the TIBET-MUX `#RCTAM` route-posture grammar.

This page is the connective layer between [Build Your Network](build.md), the model, and [Local Node Quickstart](../quickstart/local-node.md), the runnable path. It maps each build step onto the posture coordinate it is allowed to assert, the command that earns it, the thing you still have to place, and the vector that proves it.

The rule:

```text
A step is not done when the tool is installed.
A step is done when its posture digit lights and a vector proves the digit.

tools installed != route proven
```

## Prerequisites

Start from the local node path:

```bash
pip install -U "ainternet[node]"
ainternet node init --local
```

Equivalent substrate:

```text
tibet[zero-state] + tibet[network] + tibet[continuity]
```

This page assumes a tiny local network:

```text
operator.local -> agent.local -> audit.local
```

Public `.aint` federation is not required. Internet access is not required. A public hub is not required.

## Coordinate

Route posture does not score an actor. It numbers the proven route for one action.

Source anchors: [Route Posture API](../reference/route-posture-api.md), [MUX](../protocols/mux.md), [Route Posture](../learn/route-posture.md).

```text
#RCTAM
 │││││
 ││││└─ M  MUX-known / exception posture
 │││└── A  audit / evidence origin
 ││└─── T  timing / hardware lane
 │└──── C  consent / relation class
 └───── R  route family / actor class
```

Current digit families in `tibet-mux`:

| Digit | Means | Current anchor values |
|---|---|---|
| **R** | route family / actor class | `1` direct `.aint`, `2` `.saint`, `3` `.raint`, `4` `.waint`, `5` `.caint` |
| **C** | consent / relation | `2` fresh JIS challenge, `4` active parent relation, `5` 2-of-2 DAG relation |
| **T** | timing / hardware lane | `3` scheduler-free cadence, `4` DMA graph, `5` DMA descriptor ring |
| **A** | audit / evidence origin | `3` receipted, `5` sign-ahead, `7` durable |
| **M** | MUX posture | `8` known partituur, `9` verified partituur |

Open end: the code has a digit table, but the public reference still needs a normative `verify_at` table so a second implementer computes the same `#RCTAM`. Until that lands, examples are examples, not a cross-implementation contract.

Three states to internalize before building:

```text
#00000   DARK    unknown / unproven / unconsented / malformed -> collapse here
#24008   HOLD    relation + MUX known, but A=0 audit not bound yet -> policy refuses
#24358   ADMIT   audit surface bound sign-ahead -> action admitted
```

## Proving Order

The digits read `R C T A M`. You prove them in lifecycle order:

```text
resolve -> challenge -> verify JIS -> relation -> Cortex policy -> SNAFT scope -> open MUX/I-Poll -> TIBET receipt
   R          R             R            C            C              C                M                A
```

The audit digit is proven late in time, but a sign-ahead posture binds audit before the action is admitted. That is why `#24008` is a useful HOLD state: the route is known, but the evidence origin is still not bound.

Build toward audit being bound at or before route-open, not after delivery.

## MUX Intent Floors

| MUX intent | Auth tier | Posture floor it implies |
|---|---|---|
| `ains_resolve`, `cortex_check` | none | works while `#00000`; no route opened |
| `ipoll_pull`, `snaft_accept`, `ains_register` | JIS | `R` lit, at least identity-proven |
| `ipoll_push`, `snaft_propose`, `pol_check` | registered+ | `C` lit, known relation required |
| `airlock_run`, `wayback_seal` | verified+ | `A` and `M` lit, toward `#24358` |

## Build Ladder

Each rung has:

```text
posture target -> do -> place yourself -> prove
```

### Rung 0: Bootstrap, target `#00000`

Tools are present, nothing is proven. This rung cannot light a digit by design.

Do:

```bash
pip install -U "ainternet[node]"
ainternet --version
ainternet node doctor
```

Place yourself:

- Pin the dependency set.
- Decide local MUX port now: use `8443` local, reserve `443` for federation.
- Keep federation off.

Prove:

- `ainternet node doctor` must later report all planes green.
- A red identity or evidence plane fails closed.

### Rung 1: Actor Identities, target `#10000` or actor-family equivalent

JIS key per actor. The actor can answer a fresh challenge.

Do:

```bash
ainternet node init --local
ainternet actor create operator.local --role operator
ainternet actor create agent.local --role agent
ainternet actor create audit.local --role evidence
```

Place yourself:

- Author the actor records under `~/.ainternet/actors/`.
- Include identity, receipt root, endpoints, successor and tombstone fields.
- Keep private keys under `~/.ainternet/keys/`; never commit them.

Prove:

- `ztip-conformance`: identity and fresh proof.

### Rung 2: Local Registry And Resolve, R stays lit

Names resolve to identity and endpoints. Resolving is allowed while a route is still dark, because it does not open anything.

Do:

```bash
ainternet route explain agent.local audit.local
```

Place yourself:

- Use per-actor files under `actors/` as source of truth.
- Treat `registry` as the resolved view, not a second competing file.

Prove:

- Resolve returns a JIS key for each known actor.
- Unknown names produce no route.

### Rung 3: Challenge And Relation, target relation posture such as `#14000` or `#24000`

Fresh proof verified, and a known mutual relation. This is the jump from reachable to recognized.

Do:

```bash
ainternet route challenge agent.local audit.local
ainternet ping agent.local
```

Read the result:

```text
reachable != allowed
alive != consented
route exists != action approved
```

Place yourself:

- Define what counts as a relation: mutual registry entry, signed introduction, or parent relation.
- If `route challenge` is not implemented in your installed build, implement against the [Route Posture API](../reference/route-posture-api.md) contract.

Prove:

- `tibet-comms-conformance`: challenge/relation; null-route on failure.

### Rung 4: Policy, Consent And Lane, HOLD until audit binds

Cortex decides what is allowed. SNAFT negotiates scope when both sides must agree. The lane cadence lights `T`. Even with a known route, a sign-ahead policy holds until audit is bound.

Do:

```bash
ainternet route explain agent.local audit.local
```

Expected shape:

```text
policy: PUSH allowed
posture: holds until audit surface binding
decision: hold if required_posture is not met
```

Place yourself:

- Author `policy.yaml`.
- Use `default: deny`.
- Set `required_posture` per intent.
- Decide the SNAFT consent-record shape: scope, accept/reject and TIBET link.

Prove:

- `tibet-security-conformance`: Cortex, SNAFT, no fail-open.

### Rung 5: Open Route And Bind Audit, target `#24358`-style ADMIT

MUX/I-Poll carries the named surface. The audit surface binds sign-ahead. The action is admitted. A TIBET receipt is written.

Do:

```bash
ainternet send agent.local audit.local --type PUSH --content "hello"
ainternet audit trail --actor agent.local
```

The result must include:

```text
message id
route posture
TIBET receipt id
delivery state
```

Place yourself:

- Bind audit before admit, or the route stays in HOLD.
- Wire receipt write into the route-open path, not after delivery.
- Expose posture compose/smoke functions if your build does not expose route audit yet.

Prove:

- `tibet-evidence-conformance`: TIBET trail reconstructable end-to-end.

### Rung 6: Material Evidence And Isolation

Once actions affect state, add Wayback, SBOM, AI-SBOM, CBOM and Airlock. The route posture does not encode CPU features directly; it references a capability receipt.

Do:

```bash
ainternet wayback seal --label pre-deploy --sbom
ainternet pol check ainternet-core
```

Place yourself:

- Choose the Airlock boundary: firejail, nsjail, gVisor, container or an equivalent local boundary.
- Define the safe default ladder:

```text
unknown -> quarantine
risky -> isolate
unsafe -> deny
approved -> execute + receipt
```

- For compute-sensitive lanes, author a bifurcation receipt:

```text
org.ainternet.airlock.bifurcation.v1
two cells, byte-identical verdict, else hold or darken
```

Prove:

- `tibet-evidence-conformance`
- `tibet-security-conformance`

### Rung 7: Federate Subordinate

Only after the local loop is green. The outside lane is subordinate:

```text
reachability != authority
resolution != consent
edge routing != local receipts
```

Do:

```bash
ainternet claim myagent
```

Place yourself:

- Retire or succeed actors explicitly before any key leaves.
- Use tombstone and successor fields.

Prove:

- Multi-hop compose: declared vs observed fold.
- Dark contagion honored.

## Target On-Disk Structure

`ainternet node init --local` should create or expect this shape:

```text
~/.ainternet/
├── node.yaml
├── policy.yaml
├── actors/
│   ├── operator.local.yaml
│   ├── agent.local.yaml
│   └── audit.local.yaml
├── keys/
├── receipts/
└── routes/
```

`node.yaml` target shape:

```yaml
node:
  mode: local
  federation: off
hub:
  bind: 127.0.0.1
  mux_port: 8443
posture:
  floor: "#10000"
  dark: "#00000"
policy:
  default: deny
evidence:
  receipts: ./receipts
  require: true
```

`policy.yaml` target shape:

```yaml
default: deny
intents:
  ipoll_pull:  { required_posture: "#10000" }
  ipoll_push:  { required_posture: "#24358" }
  airlock_run: { required_posture: "#24358" }
actors:
  agent.local:
    can:    [receive:PUSH, receive:PULL]
    cannot: [execute:shell, access:secrets]
```

`actors/agent.local.yaml` target shape:

```yaml
actor: agent.local
role: agent
identity: jis:ed25519:<pubkey>
receipt_root: receipts/agent.local/root.tibet
endpoints:
  ipoll: http://127.0.0.1:8080/ipoll
  mux: tcp://127.0.0.1:8443
capabilities: [answer, summarize, task.receive]
successor: null
tombstone: null
```

## API Contract To Stand Up

If your installed `ainternet` build does not serve these yet, this is the local node contract to implement.

HTTP:

```text
GET  /api/mux/route/explain?from=A&to=B&intent=...
POST /api/mux/route/challenge
POST /api/mux/route/open
POST /api/mux/route/close
GET  /api/mux/route/audit/{route_id}
POST /api/mux
```

Explain response shape:

```json
{
  "from": "agent.local",
  "to": "audit.local",
  "intent": "ipoll.push",
  "route_posture": "#24358",
  "expanded_posture": {
    "family": "aint",
    "consent": "active_relation",
    "timing": "cadence_locked",
    "audit": "sign_ahead",
    "mux": "known"
  },
  "causal_seq": 42,
  "transition_reason": "audit_surface_binding"
}
```

Posture compose and smoke:

```python
DARK = "#00000"

def compose(hops: list[str]) -> str:
    """Meet / per-digit minimum; a dark hop darkens the whole route."""
    if DARK in hops:
        return DARK
    return "#" + "".join(str(min(int(h[1 + i]) for h in hops)) for i in range(5))

def smoke(declared: str, observed: str) -> tuple[str, str]:
    """Compare declared route against observed fold."""
    if observed == DARK:
        return "deny", "route dark"
    for i, name in enumerate("RCTAM"):
        if int(observed[1 + i]) < int(declared[1 + i]):
            return "hold", f"digit {name} fell back ({declared} -> {observed})"
    return "admit", "observed meets declared"
```

CLI mirror:

```bash
ainternet route explain agent.local audit.local
ainternet route challenge agent.local audit.local
ainternet route close <route-id>
```

## Dependencies

| Need | Why |
|---|---|
| Python 3.10+ and pip | runtime |
| `ainternet[node]` or `tibet[zero-state]+[network]+[continuity]` | local node profile |
| Ed25519 library such as PyNaCl or `cryptography` | JIS keys |
| Rust and cargo | TBZ / TIBET-zip carriers |
| TLS cert and key | MUX over TLS; self-signed for local `:8443`, real cert for federation |
| Airlock sandbox runtime | firejail, nsjail, gVisor, container or equivalent |
| `jq` | optional JSON scripting |
| `tibet-overlay` | optional NAT traversal without inbound ports |

## Machine-Readable Build Surfaces

Builders and AI agents should load these instead of reverse-engineering the prose:

| Surface | Use |
|---|---|
| `https://ainternet.org/upip.json` | profiles and runnable build recipes |
| `https://ainternet.org/resources.json` | docs, standards, templates and conformance index |
| `https://ainternet.org/api.json` | callable verbs and required proof rules |
| `https://ainternet.org/templates/stack-build-map.json` | intent-to-primitive/package/vector mapping |

For local-only work, mirror those files into your node and treat the local copy as the source of truth.

## Open Ends Register

| # | Gap | Where | What to decide or build | Ties to |
|---|---|---|---|---|
| 1 | Digit value table not fully public-normative | route posture reference | fix values and `verify_at` in public spec | second implementer parity |
| 2 | Actor record shape | `actors/*.yaml` | identity, endpoints, successor, tombstone | rungs 1, 7 |
| 3 | Registry representation | build doc vs local node | choose `actors/` as source of truth | rung 2 |
| 4 | `node.yaml` contents | local node | posture floor and default-deny | rungs 0-4 |
| 5 | Cortex policy shape | `policy.yaml` | `required_posture` floor per intent | rung 4 |
| 6 | SNAFT consent-record shape | consent store | scope, accept/reject, TIBET link | rung 4 |
| 7 | Route endpoints | `/api/mux/route/*` | serve them or implement locally | rungs 3-5 |
| 8 | Posture compose exposure | library/CLI | expose `compose` and `smoke` | rungs 5, 7 |
| 9 | Airlock boundary | isolation | choose sandbox and bifurcation receipt | rung 6 |
| 10 | Key succession | `keys/`, `actors/` | rotation and tombstone flow | rung 7 |

## Test Gate

```text
if it cannot be tested by vectors, it is still a claim
```

| Layer | Vector family | Rung |
|---|---|---|
| actor identity and fresh proof | `ztip-conformance` | 1 |
| reachability, MUX, I-Poll, null-route | `tibet-comms-conformance` | 3 |
| TIBET trail, Wayback, SBOM/AI-SBOM/CBOM | `tibet-evidence-conformance` | 5-6 |
| Cortex, SNAFT, Airlock, no-fail-open | `tibet-security-conformance` | 4, 6 |

The local loop is green when one `PUSH` from `agent.local` to `audit.local` reaches the required posture, writes a TIBET receipt, and the trail reconstructs who, what, route, policy and result.

## Related

- [Build Your Network](build.md)
- [Local Node Quickstart](../quickstart/local-node.md)
- [Route Posture API](../reference/route-posture-api.md)
- [Doc Posture](../operators/doc-posture.md)
- [Go Online](federation.md)
