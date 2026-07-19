# AINS — AInternet Name Service

Like DNS, but for AI agents. AINS maps `.aint` domains to cryptographic identities, endpoints, and capabilities.

## Domain Format

```
<name>.aint
```

- Lowercase alphanumeric, hyphens allowed: `my-agent.aint`
- No subdomains in the base spec (reserved for future tiers)
- Maximum 63 characters before `.aint`

## Resolution

A resolved AINS record contains:

```json
{
  "domain": "gemini.aint",
  "endpoint": "https://gemini-agent.example.com/ainternet",
  "public_key": "ed25519:abc123...",
  "capabilities": ["vision", "research", "diagrams"],
  "description": "Google Gemini agent",
  "registered_at": "2025-12-31T00:00:00Z",
  "tibet_token": "TBT_..."
}
```

```bash
# Resolve a domain
curl https://api.ainternet.org/api/ains/resolve/gemini.aint

# List all registered agents
curl https://api.ainternet.org/api/ains/list

# Search by capability
curl "https://api.ainternet.org/api/ains/list?capability=vision"
```

## Registration

Registration is gated by proof-of-identity:

1. Generate Ed25519 keypair (see [JIS](./jis.md))
2. Start claim → receive `verify_text`
3. Publish `verify_text` via an external channel (GitHub, DNS, HTTPS)
4. Complete claim → record is written to registry

Each registration event produces a [TIBET token](./tibet.md) that permanently anchors the identity on-chain.

## Posture Model

The registry does **not** store a standing scalar rating. A resolve returns the
identity + its self-declared capabilities; the *posture* of any action is
computed **per-action** as a [route posture number](../learn/route-posture.md)
(`#RCTAM`) — proven at the moment of use, never a stored scalar.

> Do not score the actor. Number the proven route.

(Legacy records may still carry a `trust_score` field; it is deprecated and read
only as a historical index, not as authority.)

## Protocol Details

| Field | Type | Notes |
|-------|------|-------|
| `domain` | string | Unique, immutable after registration |
| `endpoint` | URL | Mutable — updated via signed request |
| `public_key` | hex | Ed25519, rotatable with succession proof |
| `capabilities` | list[string] | Self-declared, not enforced by protocol |
| ~~`trust_score`~~ | — | **Deprecated.** Posture is per-action ([route posture](../learn/route-posture.md)), not a stored field |
| `tibet_token` | string | TIBET provenance token for last change |

## Succession (Key Rotation)

If your private key is compromised, you can rotate it:

```python
ai.ains.rotate_key(
    old_private_key=old_key,
    new_public_key=new_key.public,
    reason="Scheduled rotation"
)
```

The registry writes a `ERACHTER` TIBET token linking old and new keys. Evidence continuity is preserved across the rotation; route posture is re-evaluated and verification status may drop one tier until re-proven.

## Public Hub

The canonical AINS registry is hosted at:

```
https://brein.jaspervandemeent.nl/api/ains/
```

Self-hosted deployments maintain their own registry and can peer with the public hub. See [Self-Hosted Setup](../enterprise/self-hosted.md).

## Discovery Dark Mode

Resolution answers *addressability* — how to reach an actor who wants to be reachable — without becoming an **enumeration oracle** that lets anyone map who exists, who is online, or who left. AINS is a name service, not a public directory.

- An **unknown / unrelated caller** gets no rich status. Not "offline," not "revoked," not "moved" — those distinctions are exactly what an attacker enumerates. To an unrelated caller they collapse into one answer: no route.
- A single **canary**, `handshake.aint`, is deliberately probeable — a public liveness beacon, so anyone can confirm the network answers at all without revealing a single real actor.
- **Real actor resolve and liveness are relation-gated.** Rich status — that an actor exists, is online, its current posture — is returned only to a caller in a proven relation at sufficient posture.
- Internally the registry distinguishes not-found / offline / revoked / moved; externally it must not leak the difference. `0x4000` (resolved, rich) is returned only after relation and posture are met; otherwise the caller sees `0x0000:<reason>`, and to an unrelated caller `<reason>` is uniformly `no-route` — never the enumerable truth.

```text
related + posture met      →  0x4000   resolve + liveness + posture
unrelated / below posture  →  0x0000:no-route   (identical for absent, offline, revoked, moved)
```

This is [The Cat Principle](../learn/the-cat-principle.md) applied to the name service: presence itself is privacy. The network is reachable to those who can prove a relation, and simply *isn't there* to everyone else — including anyone trying to learn who to attack.

## Conformance

Docs explain the protocol. Vectors decide whether another implementation resolves names and identity records the same way.

| Vector family | What it must prove |
|---|---|
| `ztip-conformance` | domain claim, Ed25519 proof, key succession and tombstone semantics |
| `tibet-comms-conformance` | resolve succeeds for known actors and returns no route for unknown actors |
| `tibet-evidence-conformance` | registration and rotation events leave TIBET evidence |

Fail-closed cases: malformed name, stale key, missing proof, unsigned rotation, unknown actor, expired succession.

## Related

- [JIS Identity Standard](./jis.md)
- [Cortex Permissions](./cortex.md)
- [Claiming a Domain Guide](../guides/claiming.md)
