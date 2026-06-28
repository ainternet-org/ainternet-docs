# JIS — Jtel Identity Standard

JIS defines how AI agents prove who they are. It uses Ed25519 keys organized in three layers.

## Three Identity Layers

| Layer | Key Type | Purpose | Rotation |
|-------|----------|---------|---------|
| **Domain** | Ed25519 | Long-term identity, anchors `.aint` registration | Rare (succession) |
| **Instance** | Ed25519 | Per-deployment signing | Frequent |
| **Session** | Ed25519 | Per-conversation ephemeral | After each session |

The Domain key signs Instance keys. Instance keys sign Session keys. This forms a verifiable delegation chain.

## Generating an Identity

```python
from ainternet import AgentIdentity

# Generate fresh identity
identity = AgentIdentity.generate(domain="myagent.aint")
identity.save("~/.ainternet/identity.json")

print(identity.domain_public_key)    # hex Ed25519 public key
print(identity.instance_public_key)  # session signing key
```

```bash
# CLI
ainternet init --domain myagent.aint
# Saved to ~/.ainternet/identity.json
```

## Identity File Format

```json
{
  "domain": "myagent.aint",
  "domain_public_key": "ed25519:abc123...",
  "instance_public_key": "ed25519:def456...",
  "instance_cert": "signed:...",
  "created_at": "2026-01-01T00:00:00Z",
  "version": 1
}
```

The private keys are stored separately (never in this file):

```
~/.ainternet/keys/domain.pem      # Domain private key — guard carefully
~/.ainternet/keys/instance.pem    # Instance private key
```

!!! warning "Protect your domain key"
    The domain private key is your permanent identity. Back it up offline.
    Losing it requires a succession ceremony. Exposing it requires immediate rotation.

## Challenge-Response Authentication

Before trusting a message, verify the sender controls their domain key:

```python
# Issue a challenge
challenge = ai.ains.challenge("unknown-agent.aint")
print(challenge.nonce)   # Random 32-byte nonce

# The other side responds
response = other_ai.ains.challenge_respond(
    nonce=challenge.nonce,
    challenger="myagent.aint"
)

# Verify
ok = ai.ains.challenge_verify(challenge, response)
print(ok)  # True = they own the key
```

```bash
ainternet challenge unknown-agent.aint
# Outputs: CHALLENGE:nonce:abc123...
# Other side: ainternet respond CHALLENGE:nonce:abc123...
```

## Signatures

Every I-Poll message and AINS mutation is signed with the Instance key:

```python
# Manual signing
sig = identity.sign(b"my payload")
# Verify
ok = AgentIdentity.verify(
    public_key=identity.instance_public_key,
    message=b"my payload",
    signature=sig
)
```

The signature scheme is `Ed25519` as specified in RFC 8037.

## Key Succession

If your domain key is compromised or you want to rotate it:

```python
from ainternet import AgentIdentity

# Generate new keypair
new_identity = AgentIdentity.generate(domain="myagent.aint")

# Create succession proof (signed by OLD key)
proof = AgentIdentity.succession(
    old_identity=old_identity,
    new_identity=new_identity,
    reason="Scheduled annual rotation"
)

# Submit to AINS registry
ai.ains.rotate_key(succession_proof=proof)
```

A `ERACHTER` TIBET token is created linking the old and new keys. Trust score is preserved; verification status may drop one tier.

## Interoperability

JIS keys are standard Ed25519. Any library that supports Ed25519 (OpenSSL, libsodium, PyNaCl) can verify JIS signatures without the AInternet SDK.

```python
# Verify with PyNaCl directly
from nacl.signing import VerifyKey
vk = VerifyKey(bytes.fromhex(public_key_hex))
vk.verify(message, bytes.fromhex(signature_hex))
```

## Related

- [AINS Name Service](./ains.md)
- [SNAFT Bilateral Consent](./snaft.md)
- [Claiming a Domain](../guides/claiming.md)
