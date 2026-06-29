# Redstone RAINT Lab

This is the practical lab for the running AInternet substrate. A RAINT is a short-lived runtime actor: it boots, binds identity, receives a consent window, exposes only verified MUX surfaces, records its own audit trail, and disappears when its lease ends.

The lab is not an install guide for a Python package. It is a way to see the primitives working together:

```text
JIS identity -> TIBET receipt -> MUX decision -> surface route -> audit -> TTL destroy
```

Use this page when you want to run the live path, inspect what is dark, and understand how a local or self-hosted AInternet node behaves under pressure.

For the reusable pattern behind this lab, see [Runtime Box Model](runtime-box-model.md). The RAINT lab is the KVM/microVM reference implementation of that model.

## What This Proves

| Property | Expected behavior |
|---|---|
| Identity before route | A call is signed and verified before any surface is reached. |
| Dark by default | Unknown or unauthorized surfaces return no useful wire signal. |
| Auditability | Allowed and denied actions appear in the RAINT audit trail. |
| Bounded runtime | The RAINT has a TTL and is destroyed after the window. |
| Bilateral relation | Two RAINTs do not talk until a 2-of-2 relation exists. |
| Foothold discipline | `pty.aint` is a lease, not a raw shell. |

## Start a Fresh RAINT

On the Redstone host:

```bash
redstone doctor
redstone richard start richard.test.aint
```

The start command prints a live RAINT name:

```text
raint-51fc8ee7.test.aint
```

It also prints the consent window. In the current arena profile this is intentionally short. If the window closes, start a new RAINT instead of trying to revive the old one.

## Attach by Identity

From the operator side, attach to the RAINT by name:

```bash
ainternet attach raint-51fc8ee7.test.aint
```

This is not a host shell and not a guest shell. It is a client over verified surfaces. Underneath, attach asks the broker for the RAINT's own surface and keeps the consent window in view.

Expected public surfaces:

```text
handshake.aint -> alive, 0x4000
audit.aint     -> causal trail
```

Unknown surfaces and forbidden surfaces stay dark.

## Signed Frame Mode

The broker-facing frame path is:

```bash
ainternet attach raint-51fc8ee7.test.aint --frames --key <richard-ed25519-key>
```

Each surface call uses:

```text
broker challenge
fresh nonce
lane id
consent receipt hash
signed MUX frame
broker verification
surface route
```

The guest trusts the broker grant, not the caller directly. This keeps the HTTP carrier from becoming the authority.

## Dark Surface: `capture.this`

Probe the sealed surface without a clearance:

```text
capture.this
```

Expected behavior:

```text
0x0000 semantics: no useful response body, no hint, no oracle
```

The audit can record the probe. The caller does not get a reason from the guest surface.

Open it only with an L4 clearance claim signed by `vault-keeper.aint`:

```bash
ainternet attach raint-51fc8ee7.test.aint \
  --frames \
  --key <richard-ed25519-key> \
  --cap-key <vault-keeper-ed25519-key>
```

Expected decision:

```text
verified-capture-l4
```

The broker verifies the clearance claim and issues a short-lived surface grant. The guest accepts only that broker-signed grant and opens the sealed TBZ envelope.

## Relation Between Two RAINTs

Start two fresh RAINTs:

```bash
redstone richard start richard.test.aint
redstone richard start attach.test.aint
redstone raints
```

Before a relation exists, cross-RAINT route attempts fail closed:

```text
route <peer> handshake.aint
-> 0x0000, source-relation-not-bound
```

In `ainternet attach`, form the relation:

```text
relate raint-99eda9fc.test.aint handshake.aint,audit.aint
```

This forms a 2-of-2 signed relation contract:

```text
org.ainternet.redstone.relation.v1
sync-lane-...
surfaces: handshake.aint, audit.aint
```

Then route over the relation:

```text
route raint-99eda9fc.test.aint handshake.aint
route raint-99eda9fc.test.aint audit.aint read-audit
```

Expected behavior:

```text
handshake.aint -> peer guest returns 0x4000
audit.aint     -> peer audit is returned
capture.this   -> 0x0000, surface-not-in-relation
```

The denial reason shown by attach is control-plane feedback to the authenticated operator. It is not a guest surface leak and does not change true-dark wire behavior.

## Inside Position: `pty.aint`

`pty.aint` is the first inside foothold surface. It is not an SSH server and not a raw shell.

Before a grant:

```bash
curl --noproxy "*" -sS -m 2 http://172.16.0.2:8080/resolve/pty.aint
```

Expected wire behavior:

```text
curl 52
http=000
bytes=0
```

Open a short-lived lease:

```bash
python3 raint_broker.py \
  --pty-open raint-51fc8ee7.test.aint \
  --pty-subject richard.test.aint \
  --pty-ttl 60
```

Expected result:

```json
{
  "kind": "org.ainternet.redstone.pty.open-result.v1",
  "surface": "pty.aint",
  "guest": {
    "result": "0x4000",
    "session": {
      "kind": "org.ainternet.redstone.pty.session.v1",
      "mode": "foothold-lease",
      "shell": false
    }
  }
}
```

A future interactive PTY must hang behind this lease. The invariant is simple:

```text
no lease -> no foothold
lease -> identity, consent, TTL, audit
no raw port bypass
```

## Inspect Audit

Inside attach:

```text
audit
```

Or from the carrier during a lab run:

```bash
curl --noproxy "*" -sS http://172.16.0.2:8080/audit
```

Useful phases to look for:

```text
jis_bound
consent_granted
mux_surface_ready
mux_frame_decision
capture_grant_verified
relation_formed
relation_route_decision
pty_grant_verified
```

The audit is the place where denied probes can exist without becoming an oracle to the caller.

## Clean Up

Stop every active RAINT when the lab is done:

```bash
redstone richard stop raint-51fc8ee7.test.aint
redstone raints
```

Expected final state:

```json
{
  "active": {}
}
```

## The Line To Keep

You are not opening ports. You are asking whether a route may exist.

```text
identity + consent + relation + surface policy = route
anything else = 0x0000
```

That is the core Redstone lesson: a small AInternet can be one household, one runtime, one AI, two RAINTs in a lab, or a continent-scale mesh. The primitive is the same.

## Related

- [Runtime Box Model](runtime-box-model.md)
- [Build Posture](../network/build-posture.md)
- [Reaching a Raint](../learn/reaching-a-raint.md)
- [Airlock](../protocols/airlock.md)
