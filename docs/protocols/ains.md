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

The registry does **not** store a standing "trust score". A resolve returns the
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

## Related

- [JIS Identity Standard](./jis.md)
- [Cortex Permissions](./cortex.md)
- [Claiming a Domain Guide](../guides/claiming.md)
