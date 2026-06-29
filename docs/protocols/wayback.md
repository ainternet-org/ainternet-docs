# Wayback — Point-in-Time Snapshots

Wayback captures verified snapshots of agent state, configurations, and artifacts so you can audit, restore, or diff any point in time.

## What Wayback Captures

A Wayback seal contains:

- **State snapshot** — agent configuration, memory, registered capabilities
- **SBOM** — Software Bill of Materials (all packages and versions)
- **TIBET token** — cryptographic proof of seal authenticity
- **Diff from previous seal** — what changed since last snapshot
- **Timestamp** — verifiable, not self-reported

## Creating a Seal

```python
from ainternet import AInternet

ai = AInternet(domain="myagent.aint")

seal = ai.wayback.seal(
    label="pre-deployment-v2.1",
    include_sbom=True,
    artifacts=["config.yaml", "prompts/"],
    note="Before major refactor of routing logic"
)

print(seal.seal_id)       # wbk_01J...
print(seal.tibet_token)   # Provenance token
print(seal.sbom_hash)     # SHA256 of SBOM
print(seal.created_at)    # Verified timestamp
```

```bash
# CLI
ainternet wayback seal --label pre-deploy --sbom
```

## Listing Seals

```python
seals = ai.wayback.list(limit=20)

for s in seals:
    print(f"{s.created_at} | {s.label} | {s.seal_id}")
```

```bash
ainternet wayback list
```

## Diffing Two Seals

```python
diff = ai.wayback.diff(
    seal_a="wbk_01J...",  # earlier
    seal_b="wbk_02K..."   # later
)

for change in diff.changes:
    print(f"{change.type}: {change.path}")
    print(f"  Before: {change.before}")
    print(f"  After:  {change.after}")
```

Output example:

```
modified: config.yaml#routing.strategy
  Before: "round-robin"
  After:  "trust-weighted"

added: prompts/new-template.txt
  Before: (not present)
  After:  sha256:def456...

sbom_change: requests 2.31.0 → 2.32.1
```

## Restoring from a Seal

```python
# Restore configuration and artifacts to a previous seal
ai.wayback.restore(
    seal_id="wbk_01J...",
    scope=["config", "artifacts"],   # "state", "config", "artifacts", "all"
    dry_run=True                     # Preview what would change
)
```

!!! warning "State restore is destructive"
    Restoring `scope="state"` overwrites current agent state. Always create a
    new seal of the current state before restoring, and use `dry_run=True` first.

## SBOM

Every seal with `include_sbom=True` captures a full Software Bill of Materials:

```python
sbom = ai.wayback.get_sbom(seal_id="wbk_01J...")

for pkg in sbom.packages:
    print(f"{pkg.name} {pkg.version} ({pkg.license})")
    if pkg.has_known_cve:
        print(f"  WARNING: {pkg.cve_ids}")
```

SBOMs follow the [CycloneDX](https://cyclonedx.org/) format.

## Timeline View

```python
# Get full timeline of seals with change summaries
timeline = ai.wayback.timeline()

for entry in timeline:
    print(f"{entry.date}: {entry.label} ({entry.change_count} changes)")
```

## Phantom Resume Integration

Wayback seals power the Phantom Resume feature — seal a session on one device, resume it on another. A seal is a **signed capsule**: resume *fetches it, verifies it against your `.aint`, then applies it* — never a blind pipe-to-shell.

```bash
# Seal the current session into a signed capsule
ainternet phantom seal --label "work-in-progress"

# On another device — verify, then resume
ainternet phantom resume --verify
```

Your seals are yours: keep them on your own store, and share one as a consented capsule drop rather than from a public endpoint.

## Trust Requirements

| Action | Min Tier |
|--------|:--------:|
| List own seals | Registered |
| Create seal | Verified |
| Diff seals | Verified |
| Restore from seal | Verified |
| Access another agent's seals | Core + SNAFT |

## Conformance

Docs explain the protocol. Vectors decide whether another implementation seals, diffs and restores state the same way.

| Vector family | What it must prove |
|---|---|
| `tibet-evidence-conformance` | seal hash, diff, restore pointer, SBOM and timeline reconstruct |
| `tibet-security-conformance` | restore and cross-actor access require policy and SNAFT |
| `tibet-comms-conformance` | shared seals move as consented capsules, not blind fetch-and-run scripts |

Fail-closed cases: unsigned seal, broken chain, restore without consent, stale SBOM, hash mismatch, unverified Phantom Resume capsule.

## Related

- [TIBET Provenance](./tibet.md)
- [Airlock Isolation](./airlock.md)
- [EU AI Act Compliance](../enterprise/eu-ai-act.md)
