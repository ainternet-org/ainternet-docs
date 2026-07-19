# A Computer Inside A Computer

AInternet nodes are easiest to understand when you can hold the whole machine in
your head. That is why the runtime-box pattern matters.

You boot a small computer inside your computer, give it a name, bind it to a key,
grant only the surfaces it may expose, and then watch what happens.

```text
host machine
  -> runtime box
     -> actor identity
     -> allowed surfaces
     -> audit trail
     -> teardown or persistence rule
```

That is not a cloud trick. It is a learning tool.

## Why This Pattern Exists

When something breaks in a distributed system, the first question is usually too
large:

```text
is the network broken?
is the code wrong?
is the key stale?
is the policy refusing?
is the route dark?
is the host doing something hidden?
```

A small box lets you reduce the problem until it is honest.

```text
one actor
one key
one route
one surface
one receipt
one place to inspect
```

If that works, add the next part. If it fails, the failure is small enough to
share.

## The Open Debug Habit

AInternet should be built in the open enough that a broken run is useful:

```text
I built this.
I broke this.
Here is the smallest reproduction.
Here is what the receipt says.
Here is what I expected.
Here is where the route went dark.
```

That habit is not a side issue. It is part of the security model. A route that
cannot be reduced, replayed, explained or refused in public is probably carrying
too much hidden state.

## What The Box Proves

A runtime box is not trusted because it boots. It is useful when it proves a
boundary-equivalent lane:

| Proof | What you can inspect |
|---|---|
| boot source pinned | which golden rootfs or image booted |
| runtime identity bound | which `.aint` or `.raint` is live |
| surfaces explicit | which names may route |
| policy and consent present | why the route may act |
| TIBET receipt written | how the action reconstructs |
| parent report survives | what remains after teardown |

Boot is only the start. The route is proven by the evidence around the boot.

## AInternet-in-a-box vs Hackbox

The clean path is:

```text
AInternet-in-a-box
  -> persistent friendly node
  -> local identity
  -> audit.aint and tool.*.waint surfaces
  -> build your own network
```

The adversarial path is a module:

```text
RAINT / arena
  -> disposable hackbox
  -> synthetic runtime identity
  -> handshake.aint, capture.this, pty.aint
  -> TTL destroy
```

The hackbox taught the stack how to behave under attack. The clean node is the
floor people should build from. Later, you can derive hackboxes, testboxes and
function boxes from the clean floor.

## The Surface Grant Is The Door

The box should not decide its own authority by hardcoded routes. The parent
broker signs what the box may expose.

```text
box manifest declares surfaces
broker signs surface grant
guest reads signed grant
MUX admits only granted surfaces
everything else darkens to 0x0000
```

That is why a clean node can structurally lack `capture.this`: the surface is
not in its signed grant. There is no flag endpoint to accidentally discover.

## Minimal Reproduction Form

When you report a bug or teach a new module, try to reduce it to this form:

```text
box kind:
runtime:
golden_ref or image digest:
command:
identity:
granted surfaces:
intended route:
observed route posture:
TIBET receipt id:
expected result:
actual result:
```

Example:

```yaml
box_kind: node
runtime: ignition-kvm
isolation: microvm
golden_ref: sha256:...
command: ["/sbin/node-init"]
identity_ladder: ["node.local"]
surfaces: ["audit.aint", "tool.echo.waint"]
intended_route: "node.local -> audit.aint"
observed_posture: "#00000"
expected: "audit.aint resolves"
actual: "surface grant missing audit.aint"
```

This is the small-form discipline: the least system that still shows the truth.

## How Nodes Reach Each Other

Two boxes do not become trusted because they share a host. They still need a
relation.

```text
box A resolves box B
box B answers a fresh JIS challenge
both sides bind a relation or consent scope
broker grants named surfaces
MUX routes only the granted names
TIBET records the edge
```

That is how a pair of RAINTs can become a live trace target for a pentest, and
also how two friendly AInternet-in-a-box nodes can exchange work without making
the host an authority.

## What This Teaches

The pattern teaches three things at once:

1. A node is a place where an actor can run.
2. A route is not open until evidence says it may act.
3. A failure is useful when it is small enough to reproduce.

That is the commons posture:

```text
build small
prove the route
share the failure
grow the network
```

## Machine-Readable

- `https://ainternet.org/resources.json` — runtime-box and conformance references
- `https://ainternet.org/api.json` — route explain, audit and MUX verbs
- `https://ainternet.org/templates/stack-build-map.json` — module-to-primitive map

## Related

- [Runtime Box Model](../builders/runtime-box-model.md)
- [Local Node Quickstart](../quickstart/local-node.md)
- [Build Posture](../network/build-posture.md)
- [Route Posture](route-posture.md)
- [Reaching a RAINT](reaching-a-raint.md)
