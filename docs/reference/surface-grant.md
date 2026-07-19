# Surface Grant

A surface grant is the signed allowlist that tells a runtime box which AInternet
surfaces may materialize.

It is not a list of ports. It is not a UI preference. It is parent-broker
authority, signed before the guest exposes anything.

```text
signed surface present -> candidate route
signed surface absent  -> 0x0000
```

## Why It Exists

A clean AInternet-in-a-box and an arena hackbox may share the same daemons. The
difference is not a secret code path. The difference is the grant:

| Mode | Surfaces |
|---|---|
| node | `audit.aint`, `tool.*.waint` |
| arena | `audit.aint`, `handshake.aint`, `capture.this`, `tool.*.waint` |

So a probe to `capture.this` on a node fails for a simple reason:

```text
capture.this is not in the signed grant
```

That is Kerckhoffs-friendly. The system may be inspected, and the route still
cannot materialize without the signature.

## Public Shape

The grant is a JSON object signed by the parent broker.

```json
{
  "kind": "org.ainternet.redstone.surface-grant.v1",
  "grant_id": "sg-node-example-001",
  "issued_at": 1782452628,
  "expires_at": null,
  "issuer": {
    "aint": "mama.example.aint",
    "role": "parent-broker",
    "key_id": "sha256:<broker-pubkey-hash>"
  },
  "subject": {
    "session_id": "node-example-001",
    "mode": "node",
    "identity_flavor": "node.local",
    "runtime_aint": null,
    "box_manifest_hash": "sha256:<manifest-hash>",
    "boot_source": "golden-rootfs"
  },
  "policy": {
    "default": "0x0000",
    "unknown_surface": "0x0000",
    "on_expired": "darken",
    "egress_default": "deny",
    "sign_ahead_required": true
  },
  "surfaces": [
    {
      "name": "audit.aint",
      "match": "exact",
      "verbs": ["read"],
      "requires": ["jis-bound", "tibet-continuity"],
      "posture_floor": "#20000"
    }
  ],
  "tibet": {
    "receipt_required": true,
    "parent_report": "required",
    "audit_mirror": "audit-out/<session>/surface-grant.json"
  },
  "sig": "ed25519:<hex>"
}
```

The values above are examples. Anything in `<angle-brackets>` or ending in
`.example` is a placeholder.

## Canonical Signature

The signature covers the canonical grant object with `sig` removed.

Current canonical form:

```text
US 0x1f joined top-level sorted keys
compact JSON per value
sort keys inside JSON values
exclude only sig
```

In Python terms:

```python
US = "\x1f"

def canonical(frame):
    return US.join(
        "%s=%s" % (
            k,
            json.dumps(frame[k], separators=(",", ":"), sort_keys=True, ensure_ascii=False),
        )
        for k in sorted(frame)
        if k != "sig"
    ).encode("utf-8")
```

The signature field is:

```text
ed25519:<hex signature over canonical bytes>
```

Arrays are order-significant. The broker should sort surface entries by `name`,
then `match`, before signing.

## Surface Entries

Exact surface:

```json
{
  "name": "audit.aint",
  "match": "exact",
  "verbs": ["read"],
  "requires": ["jis-bound", "tibet-continuity"],
  "posture_floor": "#20000"
}
```

Tool wildcard:

```json
{
  "name": "tool.*.waint",
  "match": "glob",
  "verbs": ["invoke", "read-status"],
  "requires": ["jis-bound", "snaft-scope", "tibet-receipt"],
  "posture_floor": "#24358"
}
```

Allowed match modes:

| Match | Meaning |
|---|---|
| `exact` | byte-exact surface name |
| `glob` | `*` wildcard only, no regex |

## Guest Verification

The guest should verify:

```text
kind is exact
signature verifies
issuer key hash matches the public key
subject session matches this runtime
subject mode matches node or arena
grant is not expired
policy default is 0x0000
unknown_surface is 0x0000
```

Only after those checks may surfaces materialize.

## Failure Behavior

| Case | Result |
|---|---|
| missing grant | dark / no surfaces |
| bad signature | dark / no surfaces |
| wrong mode | dark / no surfaces |
| wrong session | dark / no surfaces |
| expired arena grant | dark / no surfaces |
| unknown surface | `0x0000` |
| `capture.this` on node | `0x0000` |
| required proof missing | `0x0000` and a refusal receipt when audit is available |

No failure should open a fallback route.

## CLI Inspection

Intended command shape:

```bash
ainternet box grant show --output json
ainternet box grant verify --output json
ainternet route explain <node-name>.example.aint capture.this --intent probe --output json
```

The expected clean-node result for `capture.this` is:

```text
0x0000
```

## Conformance

The surface-grant vector family should include:

```text
valid node grant
valid arena grant
bad signature
wrong mode replay
wrong session replay
permissive default refused
capture.this absent on node
```

Docs explain the contract. Vectors decide whether an implementation is compatible.

## Machine-Readable Companion

```bash
curl -fsS https://ainternet.org/api.json
curl -fsS https://ainternet.org/resources.json
```

## Related

- [AInternet-in-a-Box](../builders/ainternet-in-a-box.md)
- [AInternet-in-a-Box Terminal Path](../builders/ainternet-in-a-box-terminal.md)
- [MUX](../protocols/mux.md)
- [JIS](../protocols/jis.md)
- [TIBET](../protocols/tibet.md)
