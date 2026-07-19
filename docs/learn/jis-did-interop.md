# JIS and DID Interop

> **DID proves a key can sign. JIS proves a route may act.**

AInternet can speak to DID and Verifiable Credential systems, but it does not
reduce identity to a DID document. The difference is simple:

```text
DID identifies a subject.
JIS materializes an actor.
```

**Payoff:** let DID/VC systems interoperate without accidentally granting a route
inside AInternet. Outbound export is easy; inbound authority still needs a live
JIS ceremony.

**Use this as a reference:** when someone asks "why not just use DID?", use this
page to walk from valid key signature to live route permission.

**AI context:** one link to this page should give enough context to answer the
interop question without hunting through the JIS, MUX, SNAFT and TIBET pages.

A DID document can tell you which keys and service endpoints belong to an
identifier. JIS asks the next operational question: *is this actor, in this
runtime, under this consent window, allowed to route this action right now?*

That is why JIS can project outward into DID-compatible forms, while a bare DID
cannot automatically enter an AInternet route.

## The Layer Split

| Question | DID usually answers | JIS answers |
|---|---|---|
| What is the identifier? | `did:example:123` | `.aint`, `.raint`, `.waint`, `.caint`, or another actor posture |
| Which key can verify signatures? | DID document verification method | JIS key chain plus fresh proof |
| Is the key live now? | Usually out of scope | Fresh challenge/response |
| Which runtime is acting? | Usually out of scope | Bound process, session, guest, tool, or hardware lane |
| Is there consent? | Usually out of scope | SNAFT relation and TIBET receipt |
| May this route open? | Service endpoint discovery | MUX admission or `0x0000` |
| Can we audit it? | Signature or VC proof | Causal TIBET receipt chain |
| What happens on failure? | Resolve or verify fails | Route darkens, holds, or triages |

## Outbound Works: JIS to DID

JIS can emit a DID-compatible projection because JIS already has enough
material to fill the DID shape: an identifier, verification keys, services, and
metadata. A DID or VC system can then verify standard signatures without
understanding the full AInternet route.

Example projection:

```json
{
  "@context": ["https://www.w3.org/ns/did/v1"],
  "id": "did:ainternet:jasper",
  "verificationMethod": [
    {
      "id": "did:ainternet:jasper#instance",
      "type": "JsonWebKey2020",
      "controller": "did:ainternet:jasper",
      "publicKeyJwk": {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": "..."
      }
    }
  ],
  "authentication": ["did:ainternet:jasper#instance"],
  "service": [
    {
      "id": "did:ainternet:jasper#ains",
      "type": "AInternetNameService",
      "serviceEndpoint": "https://ainternet.org/.well-known/ains/jasper.aint"
    }
  ]
}
```

That projection is useful for:

- DID resolvers and VC wallets
- verifiable-credential-style presentations
- cross-system key discovery
- compliance exports
- bridges to systems that know DID but not AInternet

But it is a projection. It does not carry the whole route.

## Inbound Does Not Automatically Work: DID to JIS

A bare DID coming inbound can be resolved and verified, but that only proves a
key can sign. It does not prove a route may act.

Inbound DID evidence can become a **candidate**:

```json
{
  "state": "candidate",
  "source": "did",
  "subject": "did:example:alice",
  "key_verified": true,
  "missing": [
    "fresh_jis_challenge",
    "runtime_binding",
    "snaft_consent",
    "tibet_receipt",
    "mux_route_posture"
  ]
}
```

The candidate becomes routable only after the JIS ceremony:

```text
resolve DID
-> verify key signature
-> issue fresh JIS challenge
-> bind runtime/session/process
-> bind or negotiate SNAFT consent
-> write TIBET sign-ahead receipt
-> MUX evaluates route posture
-> route opens or returns 0x0000
```

So this is not enough:

```text
did:example:alice + valid signature
```

The AInternet route still needs:

```text
live actor
fresh challenge
runtime binding
consent scope
route posture
audit receipt
```

## Example: DID Signature Accepted as Evidence, Not Authority

An inbound VC holder presents:

```json
{
  "holder": "did:key:z6Mk...",
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-06-30T10:00:00Z",
    "verificationMethod": "did:key:z6Mk...#z6Mk...",
    "proofPurpose": "authentication",
    "proofValue": "..."
  }
}
```

AInternet can say:

```json
{
  "did_signature": "valid",
  "jis_state": "not_materialized",
  "route_posture": "#00000",
  "reason": "key-signature-valid-but-route-unproven"
}
```

Then it can ask the holder to perform a JIS challenge:

```json
{
  "kind": "org.ainternet.jis.challenge.v1",
  "challenge": "jis-6bf2f0...",
  "for": "did:key:z6Mk...",
  "requested_actor": "alice.aint",
  "expires_in": 30
}
```

Only after the fresh proof and route checks pass does the route get a posture
other than dark:

```json
{
  "jis_state": "materialized",
  "actor": "alice.aint",
  "route_posture": "#24358",
  "tibet_receipt": "tibet:sha256:...",
  "allowed": true
}
```

## Why This Matters for Agentic Systems

For a human login, a static identifier may be enough to start a session. For an
agentic runtime, it is not. The actor may be:

- a human operator
- an AI runtime
- a tool process
- a temporary RAINT guest
- a `.waint` wrapper around a tool
- a `.caint` composite actor
- a machine lane or hardware-backed enclave

Each may use the same public identity differently. A DID document cannot tell
whether the action came from a live runtime, whether the consent relation is
still valid, or whether the MUX should admit the route.

JIS does not replace DID for interoperability. It supplies the missing live
ceremony for systems where actions materialize through routes.

## Practical Gateway Rules

### Step 1: Export Outbound When You Need DID/VC

What this does: projects an AInternet/JIS actor into a DID-compatible document
or VC presentation for systems that understand DID but not AInternet.

Outbound export is permissive:

```text
JIS actor
-> DID-compatible document
-> VC presentation
-> external verifier checks key/signature
```

Use this when you need to prove identity or credentials to an external DID/VC
system.

**You now have:** an external identity projection.

**What is proven:** the external verifier can check a key/signature shape. It
does not prove that an AInternet route may act.

**If it fails:** fix the DID/VC projection or key format. Do not weaken the JIS
route to satisfy a DID resolver.

**Next:** treat inbound DID/VC as evidence, not authority.

### Step 2: Stage Inbound DID/VC As Evidence

What this does: accepts a DID or VC proof as a candidate, then asks for the live
JIS ceremony before any route opens.

Inbound import is staged:

```text
DID/VC proof
-> candidate evidence
-> JIS fresh challenge
-> runtime binding
-> SNAFT consent
-> TIBET receipt
-> MUX admit/hold/dark
```

Use this when an external DID/VC holder wants to act inside an AInternet route.

**You now have:** candidate evidence.

**What is proven:** a key signature or credential verified externally.

**If it fails:** the candidate remains dark. Do not create a JIS actor from an
unverified DID proof.

**Next:** materialize a JIS actor with a fresh challenge.

### Step 3: Materialize The Route

What this does: turns candidate evidence into a live actor only after the
runtime, consent, receipt and MUX checks pass.

```text
issue fresh JIS challenge
bind runtime/session/process
bind SNAFT consent
write TIBET sign-ahead receipt
evaluate MUX route posture
admit or return 0x0000
```

**You now have:** either a live AInternet route or a dark candidate.

**What is proven:** not just that a key can sign, but that this actor may act on
this route now.

**If it fails:** keep the DID as external evidence only. Do not route it.

**Next:** keep both records so audit can reconstruct the bridge.

## Compatibility Pattern

A gateway should keep both objects:

```json
{
  "external_identity": {
    "type": "did",
    "id": "did:key:z6Mk...",
    "verified": true
  },
  "ainternet_actor": {
    "id": "alice.aint",
    "jis_state": "materialized",
    "runtime": "session-2026-06-30T10:00Z",
    "route_posture": "#24358",
    "tibet_receipt": "tibet:sha256:..."
  }
}
```

Do not overwrite one with the other. The DID is the external identity anchor.
The JIS actor is the live route participant.

## Failure Modes

| Case | DID result | AInternet result |
|---|---|---|
| DID resolves, signature valid, no fresh challenge | valid key | `#00000`, route not materialized |
| DID proof is replayed | may verify cryptographically | stale nonce, route dark |
| Runtime claims another actor name | DID may not notice | CLI/runtime posture quarantine |
| Consent expired | DID still resolves | route darkens |
| Action exceeds SNAFT scope | key still valid | MUX returns `0x0000` or triage |
| Audit receipt missing | DID signature still valid | action refused before admit |

## One Sentence Test

Ask what the proof authorizes:

```text
DID proves a key can sign.
JIS proves a route may act.
```

If all you need is a portable signature check, DID may be enough. If an actor is
about to affect another actor, device, process, model, mailbox, or audit trail,
JIS has to materialize the route.

## Machine-Readable Gateway Shape

Gateway implementations should expose this as a machine-readable decision, not
only as prose. The exact endpoint may differ by deployment, but the object shape
should be stable enough for tools to curl and gate on:

```bash
curl -sS https://api.ainternet.org/api/jis/interop/did/check \
  -H 'content-type: application/json' \
  -d '{
    "did": "did:key:z6Mk...",
    "proof": {"type": "Ed25519Signature2020", "proofValue": "..."},
    "requested_actor": "alice.aint",
    "intent": "ipoll.push"
  }'
```

Expected candidate response:

```json
{
  "kind": "org.ainternet.jis.did-interop.decision.v1",
  "did": {
    "id": "did:key:z6Mk...",
    "signature": "valid"
  },
  "jis": {
    "state": "candidate",
    "missing": [
      "fresh_jis_challenge",
      "runtime_binding",
      "snaft_consent",
      "tibet_receipt",
      "mux_route_posture"
    ]
  },
  "route_posture": "#00000",
  "decision": "hold",
  "reason": "key-signature-valid-but-route-unproven"
}
```

Expected materialized response:

```json
{
  "kind": "org.ainternet.jis.did-interop.decision.v1",
  "actor": "alice.aint",
  "jis": {
    "state": "materialized",
    "challenge": "fresh",
    "runtime_bound": true
  },
  "route_posture": "#24358",
  "tibet_receipt": "tibet:sha256:...",
  "decision": "admit"
}
```

## Related

- [JIS](../protocols/jis.md)
- [TIBET](../protocols/tibet.md)
- [SNAFT](../protocols/snaft.md)
- [MUX](../protocols/mux.md)
- [Route Posture, Not a Trust Score](route-posture.md)
- [Bind an AI, Runtime-Bound](bind-an-ai.md)
- [HTTP API Reference](../reference/http-api.md)
