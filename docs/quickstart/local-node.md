# Build Your First AInternet Node

A follow-along path, not a catalog. You start with nothing; you end with a
local node you can ping. Each step has a copy-paste block and a **You now have**
checkpoint, so you always know where you are.

This is the smallest coherent loop:

```text
identity -> node up -> self-ping
```

**Payoff:** your first local ping arrives. The function is familiar; the new
part is that identity, route posture and evidence are visible while it happens.

**Use this as a reference:** when you later forget the exact order for "make a
local actor, bring up the node, ping it, check evidence", this page is the
repeatable path.

**AI context:** one link to this page should be enough for an assistant to know
the goal, commands, checkpoints, failure behavior and next docs.

Proving evidence, holding or rejecting work, adding agents, and federating with
another network are separate handbooks in this same shape.

!!! warning "Before you start"
    **Placeholders.** Anything in `<angle-brackets>` or ending in `.example` is
    yours to replace, for example `<node-name>` or `peer.example.aint`. Nothing
    with a placeholder is meant to run unchanged.

    **Verify the verb.** Some commands below describe the intended CLI shape.
    Exact verb names and flags can differ by installed version. Lines marked
    `verify with --help` should be checked once against your install.

## Step 0: Prerequisites

What this does: confirms you have the runtime the packages need.

```bash
python3 --version      # 3.10+ expected
pip --version
```

**You now have:** a Python toolchain ready to install into.

## Step 1: Install The Substrate

What this does: puts the smallest identity and provenance floor on the machine.

`tibet[zero-state]` is the T-1 substrate: identity, provenance, genesis and
causal time. `tibet[network]` adds the lane tools you will self-ping with.

```bash
# identity/provenance floor: tibet-core, jis-core, genesis, causal time
pip install -U "tibet[zero-state]"

# local lane tools: ping, overlay, MUX
pip install -U "tibet[network]"

# node/actor surface: init, actors, doctor
pip install -U "ainternet[node]"
```

**You now have:** the software on the machine.

One distinction matters:

```text
installed != running
```

Nothing is up yet. You have installed the floor, not proven a route.

## Step 2: Become An Actor

What this does: gives you a name, so others can route to you, and a key, so you
can prove it is you. This is the moment you exist as an AInternet actor.

```bash
# initialize a local-only node
ainternet node init --local

# create your local actor; replace <node-name>
ainternet actor create <node-name>.example.aint --role operator
```

If your installed CLI exposes a different actor verb, check:

```bash
ainternet actor --help
```

**You now have:** an actor: a `.aint` name bound to a JIS key.

What just happened:

```text
name routes
key proves
```

Your private key stays on this machine and never leaves it.

Expected local shape:

```text
~/.ainternet/
  node.yaml
  actors/
  keys/
  receipts/
  routes/
```

The actor record is yours to inspect and complete:

```text
~/.ainternet/actors/<node-name>.example.aint.yaml
```

It should carry identity, endpoints, receipt roots, and later succession or
tombstone fields. Do not commit private keys.

## Step 3: Bring The Node Up Locally

What this does: checks whether the local planes can carry a route.

```bash
ainternet node doctor
```

If your installed build uses a different health command, check:

```bash
ainternet node --help
```

The doctor should check at least:

```text
identity plane      JIS available
evidence plane      TIBET available
local registry      present
receipt store       writable
MUX                 local route gate available
carrier tools       TIBET-zip / TBZ available
```

**You now have:** a node that can prove its own local planes.

The rule:

```text
red plane -> fail closed
```

If doctor is unhappy, stop here and fix it. A node that cannot prove its own
health should not carry routes.

## Step 4: Close The Smallest Loop

What this does: pings your own node over its local lane. This closes the loop:
identity exists, the node is up, and the lane carries on your machine without
depending on the public hub.

First find the local MUX surface your node uses:

```bash
ainternet node doctor
```

Then self-ping it:

```bash
# replace <port> with the local MUX port reported by your node
tibet-ping stack --mux http://127.0.0.1:<port>
```

Later, the peer form targets another actor:

```bash
tibet-ping peer.example.aint
```

**You now have:** a running node that answers its own ping. The smallest loop is
closed.

!!! note "Doctrine L0"
    A successful ping proves **reachability, not authority**.

    You have shown that the lane carries. You have not shown that you are
    allowed to act across it. Never escalate "I can reach it" into "I may act on
    it." That separation is the point of the floor you just built.

## Step 5: Read The First Posture

What this does: shows where the route stands. A route posture is not a rating of
the actor; it is a coordinate into what this route has proven.

```bash
ainternet route explain <node-name>.example.aint <node-name>.example.aint
```

If that exact verb is not present yet, use the available route or doctor output
and compare it to the expected shape:

```text
resolve       actor name resolves to a JIS key
challenge     fresh proof can be requested
relation      local self-relation or parent relation exists
policy        local action is allowed or held
route         local MUX lane exists
evidence      TIBET receipt path is available
posture       #... or #00000
```

**You now have:** a map marker. You can see whether the node is dark, holding, or
admitted for this smallest action.

## Step 6: Keep One Receipt

What this does: checks that the node can leave evidence for what it just did.

```bash
ainternet audit trail --actor <node-name>.example.aint
```

Expected shape:

```text
actor
intent or probe
route or denial
posture
receipt id
causal position
```

**You now have:** the start of an audit trail. The ping is no longer only an
event you saw in the terminal; it is something you can reconstruct.

## Where This Leaves You

You went from an empty machine to:

```text
an identity
a local node
a proven lane to yourself
the first audit surface
```

That is the bare-necessity floor. Everything else builds on it.

## Next Handbooks

Each next capability should follow this same shape: command, checkpoint, proof.

| Next capability | What you prove |
|---|---|
| Prove what happened | read and verify the TIBET evidence chain |
| Hold or reject unknown work | SNAFT, Cortex and Airlock fail closed |
| Let an agent operate it | I-Poll or MCP surfaces under your `.aint` identity |
| Add another actor | local relation and MUX route between two names |
| Federate later | outside reachability remains subordinate to local policy |

If you want the intuition behind the runtime-box pattern before going deeper,
read [A Computer Inside A Computer](../learn/computer-inside-computer.md).

If you want the same local loop in a bounded microVM first, use
[AInternet-in-a-Box](../builders/ainternet-in-a-box.md). The box path is the
same state machine with an extra clean boundary around it.

Read in this order when you are ready:

1. [Build Your Network](../network/build.md)
2. [Build Posture](../network/build-posture.md)
3. [Network Primitives](../network/primitives.md)
4. [Messaging](../guides/messaging.md)
5. [Permissions](../guides/permissions.md)
6. [Go Online](../network/federation.md)

## Machine-Readable Companion

If an AI agent is helping you build the node, point it at:

| Surface | Use |
|---|---|
| `https://ainternet.org/upip.json` | local-node profile and recipes |
| `https://ainternet.org/resources.json` | docs, templates and conformance index |
| `https://ainternet.org/api.json` | route, actor, audit and MUX verbs |

Pin local copies when running offline.

## Related

- [Build Your Network](../network/build.md)
- [AInternet-in-a-Box](../builders/ainternet-in-a-box.md)
- [Build Posture](../network/build-posture.md)
- [Route Posture](../learn/route-posture.md)
- [Privacy Boundaries](../operators/privacy-boundaries.md)
- [Transfer Carriers](../reference/transfer-carriers.md)
