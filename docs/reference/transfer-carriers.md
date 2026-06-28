# Transfer Carriers

AInternet can move over many transports. The preferred object form is still a sealed carrier.

```text
transport may vary
carrier should prove
```

For sensitive or important exchange, use TIBET-zip/TBZ rather than raw files, ad-hoc JSON or transport-specific blobs.

## Preferred Carrier

```text
tibet-zip / TBZ / .tibet.zip / .tza family
```

The carrier should be:

- magic-byte identifiable;
- bound to JIS identity where needed;
- linked to TIBET receipts;
- safe to route through MUX;
- inspectable by audit tooling;
- usable local, private, offline or federated.

## Transport Is Not Authority

The same sealed object may move through:

- local filesystem;
- I-Poll;
- MUX;
- private hub;
- public federation;
- CMail;
- offline handoff.

The authority comes from the object, signatures, consent, policy and receipts, not from the transport that carried it.

## Carrier Lifecycle

```text
payload
  -> hash / manifest
  -> JIS binding
  -> TIBET receipt
  -> TIBET-zip/TBZ seal
  -> route or handoff
  -> receipt on receive / open / reject
```

## Plaintext Rules

Plaintext may be fine for local demos and public test messages. It is not the default for sensitive work.

| Situation | Carrier |
|---|---|
| local hello-world | plaintext ok |
| public test message | plaintext ok |
| private data | sealed TIBET-zip/TBZ |
| model/runtime state | sealed carrier + manifest |
| business transaction | sealed carrier + consent + receipt |
| cross-organization task | sealed carrier + SNAFT scope |

## Magic Bytes, Not Filenames

Do not trust a filename extension. A carrier should be identified by structure and magic bytes. This lets MUX, continuityd and audit tooling recognize the object even when it is copied, renamed or moved across transports.

The filename still has value as a human surface. It can say who the object is
for, which lane it was dropped on, or which quarter a log belongs to. That
surface is an index, not authority. The sealed manifest remains the truth. See
[Semantic Surface Manifest](semantic-surface-manifest.md).

## Related

- [Privacy Boundaries](../operators/privacy-boundaries.md)
- [Semantic Surface Manifest](semantic-surface-manifest.md)
- [The Running Substrate](../learn/the-running-substrate.md)
- [TIBET](../protocols/tibet.md)
- [SNAFT](../protocols/snaft.md)
