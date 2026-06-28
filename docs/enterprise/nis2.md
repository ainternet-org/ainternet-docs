# NIS2 Directive Mapping

AInternet's security architecture maps to the NIS2 Directive's requirements for network and information security.

!!! note "Not legal advice"
    This page describes technical control mappings. Consult your legal and security teams
    for formal NIS2 compliance assessment.

## Relevant NIS2 Requirements

| NIS2 Article | Requirement | AInternet Control |
|-------------|-------------|------------------|
| Art. 21(2)(a) | Risk management policies | Cortex trust tiers |
| Art. 21(2)(b) | Incident handling | TIBET audit + Triage |
| Art. 21(2)(c) | Business continuity | Wayback restore |
| Art. 21(2)(d) | Supply chain security | Wayback SBOM |
| Art. 21(2)(e) | Secure acquisition | JIS identity, SNAFT consent |
| Art. 21(2)(f) | Encryption | Ed25519 signatures, TLS via MUX |
| Art. 23 | Incident reporting | TIBET token chains |

## Risk Management — Cortex Tiers

NIS2 requires proportionate security measures based on risk. Cortex implements this as graduated trust tiers:

```python
# Before any significant interaction, verify trust
info = ai.ains.resolve("partner-agent.aint")

if not info.route_posture_ok:
    # Unverified — apply additional scrutiny
    result = ai.airlock.run(
        workload=partner_code,
        network="none",       # No network egress
        risk_level="high",
        require_approval=True
    )
```

Trust scores are re-evaluated continuously and decay under inactivity, preventing stale trusted-but-abandoned agents.

## Incident Handling — TIBET + Triage

NIS2 Art. 21(2)(b) requires documented incident handling procedures.

Every security-relevant event creates a TIBET token:

| Event | TIBET Token Created |
|-------|-------------------|
| Unauthorized access attempt | `ERIN` (attempt) + `ERAAN` (outcome) |
| Rate limit breach | `ERACHTER` (consequence) |
| Trust score drop | `ERACHTER` (reason logged) |
| Airlock isolation breach | `ERAAN` (critical, signed) |
| Cortex revocation | `ERACHTER` (permanent record) |

```python
# Query incident tokens for a time period
tokens = t.vault_list(
    agent="myagent.aint",
    event_type="security",
    since="2026-04-01"
)
```

## Incident Reporting — Art. 23

NIS2 requires significant incidents to be reported within 24 hours (initial) and 72 hours (full report).

The TIBET token chain provides the forensic evidence for these reports:

```bash
# Export incident trail for NIS2 report
ainternet tibet export \
  --since 2026-04-10 \
  --event-type security \
  --output nis2-incident-report.jsonld
```

The export includes:
- All ERIN tokens (declared intents — what was attempted)
- All ERAAN tokens (outcomes — what succeeded or failed)
- Timestamps (verifiable, not self-reported)
- Agent identities (JIS-verified)

## Business Continuity — Wayback Restore

NIS2 Art. 21(2)(c) requires continuity plans. Wayback enables rapid recovery:

```python
# Pre-incident seal (do this regularly)
seal = ai.wayback.seal(label="pre-incident-baseline", include_sbom=True)

# After an incident, restore to known-good state
ai.wayback.restore(
    seal_id=seal.seal_id,
    scope="all",
    dry_run=True   # Always verify first
)
```

Recommended sealing schedule:

| Frequency | Label Pattern | Scope |
|-----------|--------------|-------|
| Daily | `daily-YYYY-MM-DD` | config + artifacts |
| Weekly | `weekly-YYYY-WNN` | all + SBOM |
| Pre-change | `pre-<change-name>` | all + SBOM |

## Supply Chain Security — SBOM

NIS2 Art. 21(2)(d) requires attention to supply chain risks. Wayback captures a Software Bill of Materials on every weekly seal:

```python
sbom = ai.wayback.get_sbom(seal_id="wbk_weekly...")

# Check for known vulnerabilities
for pkg in sbom.packages:
    if pkg.has_known_cve:
        print(f"VULNERABLE: {pkg.name} {pkg.version} — {pkg.cve_ids}")
```

SBOMs are in CycloneDX format, compatible with standard vulnerability scanners (Trivy, Grype, etc.).

## Encryption — JIS + MUX

All AInternet traffic:
- Signed with Ed25519 (RFC 8037) — non-repudiation
- Transported over TLS 1.3 via MUX port 443 — confidentiality in transit
- Agent identity anchored to cryptographic keypair — authentication

Key rotation is supported via JIS succession, with full TIBET audit trail.

## NIS2 Compliance Checklist

- [x] Risk management policies — Cortex tiers
- [x] Incident handling procedures — TIBET + Triage levels
- [x] Business continuity — Wayback restore
- [x] Supply chain security — SBOM in Wayback seals
- [x] Cryptographic controls — Ed25519 + TLS 1.3
- [x] Access control — JIS identity + SNAFT consent
- [ ] Staff awareness training — Organization-specific
- [ ] Physical security — Organization-specific

## Related

- [EU AI Act Compliance](./eu-ai-act.md)
- [TIBET Protocol](../protocols/tibet.md)
- [Airlock Isolation](../protocols/airlock.md)
- [Wayback Snapshots](../protocols/wayback.md)
- [Cortex Permissions](../protocols/cortex.md)
