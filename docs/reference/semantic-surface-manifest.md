# Semantic Surface Manifest

Once AInternet objects move as sealed TIBET carriers, the filename becomes a
surface. It may help a human, but it is not the truth.

```text
file-voor.claude
log-2026.jasper.aint-lane5.log_storageQ2
payload.drop_lane5
```

All of these can be valid surfaces. The sealed manifest is the authority.

## The Two Laws

1. **Surface carries no authority.** A reader may parse the name, extension or
   facets for convenience, but must verify the object by magic bytes, signature
   and manifest.
2. **Surface is still a useful index.** Humans and audit tools may use surface
   facets to find, bucket, route or stash an object.

In short:

```text
surface = greeting and index
manifest = truth
```

## Magic Bytes, Not Filenames

A `.tza` extension is not proof. A file without a `.tza` extension can still be a
sealed carrier. A file named `report.tza` can be a plain ZIP or junk.

Readers should verify:

```text
magic bytes: TBZ\x84
signature:   valid
manifest:    present and consistent
```

If the surface implies a sealed carrier but the magic bytes do not confirm it,
the object should be treated as untrusted surface only.

## SSM Posture Card

An SSM card is read bottom-up:

```text
[SSM POSTURE: TZA#89421]
 |||||
 |||||_ Surface  : liquid semantics, advisory facets
 ||||__ Seal     : byte-identical cryptographic lock
 |||___ Causal   : frozen at a Lamport tick
 ||____ Origin   : created by a proven route posture
 |_____ Manifest : TIBET-zip inviolable core
```

The manifest is the ground. Everything above it describes how the object was
named, sealed, caused and originated.

## Surface Facets

A surface name is a free stem plus optional facet tokens. Tokens may be separated
with `.`, `-`, `_`, `/` or spaces. They are advisory.

| Context | Facet shape | Example |
|---|---|---|
| save | `.<class>_<bucket><period>` | `report.log_storageQ2` |
| send | `.for_<recipient.aint>` | `notes.for_claude.aint` |
| share | `.share_<scope>` | `deck.share_public` |
| drop | `.drop_<lane>` | `payload.drop_lane5` |
| work in progress | `.wip` / `.draft.<period>` | `idea.for_claude.draft.q3` |

Common hint vocabulary:

```text
Q1..Q4
20xx
lane5 / lane-5 / lane_5
*.aint
log, wip, draft, backup, archive, snapshot, inbox, outbox, share, storage, cold, hot
```

These facets can help a person and `tibet-audit` find the object. They must not
grant authority.

## Manifest Facts

SSM reads material facts from the sealed manifest. The current recommended keys
are:

| Key | Meaning |
|---|---|
| `lamport_tick` | causal anchor for this object |
| `route_posture` | origin route posture, for example `#24358` |
| `audit_mode` | evidence mode such as `A2`, `A5` or `A7` |
| `seal_algo` | sealing algorithm or suite |
| `tza_id` | stable sealed-object identifier, when available |

Missing facts must degrade honestly. If a manifest does not contain
`route_posture`, the card should say the origin route is not recorded. The
surface must never fill that gap with authority.

Example manifest excerpt:

```json
{
  "material_facts": [
    {"key": "lamport_tick", "value": "184467"},
    {"key": "route_posture", "value": "#24358"},
    {"key": "audit_mode", "value": "A5"},
    {"key": "seal_algo", "value": "Ed25519+PCLMULQDQ"},
    {"key": "tza_id", "value": "89421"}
  ]
}
```

## Surface Drift

Surface drift means the name hints one thing and the manifest proves another.

Examples:

```text
surface says Q2, manifest causal tick belongs to Q3
surface says lane5, manifest route posture records a different lane
surface says .tza, magic bytes say PKZIP
```

Audit tools may flag the drift. The manifest wins.

## Audit Behavior

`tibet-audit` may index by surface:

```text
show Q2 logs for jasper.aint
show lane5 drops
show drafts for claude.aint
```

But verification must follow the sealed core:

```text
verify magic bytes
verify signature
verify manifest facts
verify TIBET receipt chain
verify route posture where required
```

## Minimal Reader Rules

```text
read surface facets as hints
verify magic bytes before treating an object as sealed
verify manifest before trusting any object claim
flag drift, but keep the manifest authoritative
fail closed when required evidence is absent
```

## Related

- [Transfer Carriers](transfer-carriers.md)
- [Route Posture API](route-posture-api.md)
- [TIBET](../protocols/tibet.md)
- [Keys Never Leave Your Machine](../learn/keys-never-leave.md)
