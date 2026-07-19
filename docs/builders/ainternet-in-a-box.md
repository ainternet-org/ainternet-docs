# AInternet-in-a-Box

AInternet-in-a-box is the friendly way to build a clean AInternet node inside a
bounded microVM before you expose anything to the outside world.

It is the same substrate as the terminal path: JIS identity, TIBET receipts,
SNAFT consent, a broker-signed surface grant, MUX routing and fail-closed audit.
The TUI is only a guided cockpit over those steps. It is not a hidden installer
with its own authority.

```text
TUI screen -> command -> proof -> posture -> receipt
```

**Payoff:** boot a clean local AInternet box and see the first self-ping and
receipt land. The user-facing function is simple; the primitives underneath are
JIS, TIBET, SNAFT, MUX, surface grants and route posture.

**Use this as a reference:** when you need to rebuild a clean box, verify a
surface grant, or remember why `capture.this` is absent on a node, follow this
page in order.

**AI context:** this page is intentionally single-link readable. An assistant
should not need to scrape five other pages before it can explain or guide the
box setup.

!!! warning "Before you start"
    Anything in `<angle-brackets>` or ending in `.example` is yours to replace.
    Some commands below are intended CLI shapes while the package finalizes the
    public verbs. Check the installed command with `--help` before depending on it.

## What This Builds

You start with a clean golden rootfs and end with a node that can prove:

```text
clean boot
local identity
signed surface grant
dark-by-default MUX
self-ping
first TIBET receipt
```

The recognizable result is small on purpose:

```text
I can reach my own node and prove what happened.
```

The same route can later be run without the TUI. See
[AInternet-in-a-Box Terminal Path](ainternet-in-a-box-terminal.md).

## Coming Box Shape

AInternet-in-a-box is moving toward a packaged local sovereign node:

```text
download sealed release
  -> verify genesis and hashes
  -> compose the local actor pool
  -> seal human and machine posture
  -> ready to go dark
  -> boot live cockpit
```

The goal is not a dashboard on top of scripts. The goal is a box that can say:

```text
this is who I am
this is what I may do
this is what I can carry
this is what I can prove
this is where I stop
```

### Pre-Boot Compose

Before the box goes live, the operator can compose the local pool:

- enroll the human root;
- add local API actors such as Ollama-backed models;
- add online API actors with key references, not pasted secrets;
- prepare CLI actors such as Codex, Claude Code or Gemini CLI;
- set SNAFT posture;
- review System-BOM and runtime evidence;
- seal the pool.

This is the light side of the console. It is the place for setup.

### Ready To Go Dark

After the pool is sealed, the same surface crosses a one-way threshold:

```text
ready to go dark?
```

This is not just a launch button. It is the warning that compose is ending. Once
the box is live, the operator does not keep freely filling in actors and
providers. Mutations become ceremonies, triage items or new sealed changes.

### Live Cockpit

After boot, the console becomes a cockpit:

- show which actors and lanes are alive;
- show which surfaces are dark;
- show triage and blocked actions;
- attach to runtime PTYs only where a grant exists;
- read evidence, receipts and route posture;
- avoid free-form setup controls that would bypass the sealed posture.

The same surface changes state. It does not become a second authority.

### Local Helper Actor

The box may include a local helper actor when the host can carry it:

```text
local-helper.aint
  -> local model
  -> no shell
  -> no host filesystem write
  -> no egress by default
  -> reads selected docs/status/evidence
  -> suggests next safest command
```

The helper is useful because it is constrained. It can explain the box state,
but it cannot invent authority.

## Step 0: Verify The Clean Box

What this does: checks that the box booted from the clean golden and that the
boundary is equivalent to the expected microVM posture.

```bash
ainternet box doctor
ainternet box proof --boot
ainternet box proof --boundary
```

The TUI should show:

```text
boot source        golden-rootfs
golden hash        sha256:...
boundary class     microvm-equivalent
mode               node
unknown surface    0x0000
```

**You now have:** a clean room to configure. You do not have a route yet.

**What is proven:** the boot source, golden hash and boundary class are visible
before identity or networking starts.

If the boot proof or boundary proof is absent, stop. The box must fail closed
before identity or networking is configured.

**Next:** bind the box to a local node actor.

## Step 1: Become A Node Actor

What this does: creates or imports the local `.aint` actor that this box will
operate as.

```bash
ainternet node init --local
ainternet actor create <node-name>.example.aint --role node
ainternet actor prove <node-name>.example.aint
```

The TUI should show the same facts:

```text
actor name      <node-name>.example.aint
identity        JIS Ed25519
private key     local only
fresh proof     pass
```

**You now have:** a local actor identity. The name routes; the key proves.

**What is proven:** this runtime can answer a fresh JIS challenge for the actor
name it claims.

No private key should leave the box. If a fresh JIS challenge cannot be answered,
the route stays dark.

**Next:** inspect what this actor is allowed to expose.

## Step 2: Review The Surface Grant

What this does: verifies what the parent broker actually allowed this box to
expose.

```bash
ainternet box grant show
ainternet box grant verify
```

The clean node grant should contain:

```text
audit.aint
tool.*.waint
```

It should not contain:

```text
capture.this
```

**You now have:** a signed allowlist of surfaces. You still do not have open
authority beyond that allowlist.

The point is visible zero-trust:

```text
you cannot route what you were not granted
```

If the grant is missing, unsigned, expired, for the wrong session, or for the
wrong mode, no MUX surfaces should materialize.

**What is proven:** the broker signed exactly which surfaces may exist for this
box and this mode.

**Next:** prove that one granted local lane carries.

## Step 3: Close The Local Loop

What this does: proves the local lane carries before any peer or public hub is
involved.

```bash
tibet-ping stack --mux http://127.0.0.1:<port>
ainternet route explain <node-name>.example.aint <node-name>.example.aint --intent self.ping --output json
```

The TUI should show reachability separately from authority:

```text
reachable        yes
route posture    #...
receipt path     available
```

**You now have:** a local route candidate. Reachability is not authority.

**What is proven:** local MUX can carry a self-route, and the route posture is
visible to the operator.

If the self-ping fails, do not federate. Fix the local loop first.

**Next:** write evidence for a harmless local action.

## Step 4: Write The First Receipt

What this does: creates a harmless local action and proves it with TIBET.

```bash
ainternet send <node-name>.example.aint audit.aint --type PUSH --content "hello"
ainternet audit trail --actor <node-name>.example.aint
```

Expected trail shape:

```text
actor
intent
surface
route posture
receipt id
causal position
```

**You now have:** an action that can be reconstructed after the terminal scroll
is gone.

**What is proven:** the action has a TIBET receipt and a causal position, not
only a terminal printout.

No receipt means the action is not complete.

**Next:** prove a denied surface, not only an allowed one.

## Step 5: Prove A Dark Surface

What this does: tests that a missing grant really stays dark.

```bash
ainternet route explain <node-name>.example.aint capture.this --intent probe --output json
```

Expected node behavior:

```text
capture.this -> 0x0000
```

**You now have:** proof that the clean node cannot expose an arena flag surface
unless the broker signs it into the grant.

This is not a hidden check. It is structural: the surface is absent from the
signed grant.

**What is proven:** denial is part of the route model. Unknown or ungranted
surfaces collapse to `0x0000`.

**Next:** add one bounded local tool under the node.

## Step 6: Add A Local Tool

What this does: shows how a tool can live under the node without becoming a
raw, unbounded process.

```bash
ainternet tool create tool.echo.waint --under <node-name>.example.aint
ainternet tool invoke tool.echo.waint --input "hello"
ainternet audit trail --actor tool.echo.waint
```

**You now have:** a tool actor whose route is bounded by identity, grant,
posture and receipt.

**What is proven:** tools are actors or wrappers under a grant, not raw local
programs with ambient authority.

If the tool is not under a signed relation or does not fit `tool.*.waint`, it
holds or darkens.

**Next:** connect another AInternet only after the local route is green.

## Step 7: Connect Later

Only after the local loop is green should you connect to another AInternet.

```bash
ainternet peer resolve peer.example.aint
ainternet route challenge <node-name>.example.aint peer.example.aint
ainternet route open <node-name>.example.aint peer.example.aint --intent ipoll.push
```

**You now have:** a peer route only if resolution, challenge, relation, policy,
MUX and TIBET all agree.

**What is proven:** the outside lane is subordinate to your local identity,
policy and receipts.

AInternet.org can be a hub. It is not the landlord. Your local node remains the
authority for its own keys, grants, receipts and dark routes.

**Next:** move from this guided path to the terminal mirror or to federation.

## TUI Contract

The TUI should read from the same walkthrough manifest used by docs:

```text
plans/ainternet-in-a-box-walkthrough.v1.yaml
```

Each screen mirrors one rung:

```text
label
commands
proofs
failure mode
next step
```

The TUI must fail closed when proof is absent. It should never mark a step done
because a package is installed.

## Machine-Readable Companion

For automation and AI-assisted setup:

```bash
curl -fsS https://ainternet.org/upip.json
curl -fsS https://ainternet.org/resources.json
curl -fsS https://ainternet.org/api.json
```

Pin local copies when running offline.

## Related

- [AInternet-in-a-Box Terminal Path](ainternet-in-a-box-terminal.md)
- [Runtime Box Model](runtime-box-model.md)
- [Actor Seal](../learn/actor-seal.md)
- [CRUST Runtime](../learn/crust-runtime.md)
- [A Computer Inside A Computer](../learn/computer-inside-computer.md)
- [Surface Grant](../reference/surface-grant.md)
- [Local Node](../quickstart/local-node.md)
