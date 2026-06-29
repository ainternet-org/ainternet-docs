# Pol — Infrastructure Health Checks

Pol runs structured health checks against JSON templates, generating TIBET-backed audit reports of your infrastructure state.

## How Pol Works

1. Define a **template** — a JSON file describing what to check and how
2. Run `pol_check` against the template
3. Pol executes each step (shell commands, wayback comparisons, endpoint pings)
4. Results are returned as structured data with TIBET provenance
5. Optionally generate an HTML report

## Check Statuses

| Status | Meaning |
|--------|---------|
| `valid` | All checks passed, within expected range |
| `drift` | Check passed but values shifted from baseline |
| `broken` | Check failed — remediation required |
| `blocked` | Check could not run (dependency failed) |
| `pending` | Awaiting human approval or external event |

## Template Format

```json
{
  "template_id": "api-health-v1",
  "description": "AInternet API health check",
  "steps": [
    {
      "id": "hub_reachable",
      "name": "Hub reachable",
      "type": "shell",
      "command": "curl -sf https://api.ainternet.org/health",
      "critical": true,
      "expected_exit": 0
    },
    {
      "id": "ains_resolves",
      "name": "AINS resolves root_idd.aint",
      "type": "shell",
      "command": "ainternet resolve root_idd.aint",
      "critical": true,
      "depends_on": ["hub_reachable"]
    },
    {
      "id": "wayback_seal_fresh",
      "name": "Latest Wayback seal < 24h old",
      "type": "wayback",
      "agent": "myagent.aint",
      "max_age_hours": 24,
      "critical": false
    }
  ]
}
```

## Check Types

| Type | Description | Parameters |
|------|-------------|-----------|
| `shell` | Run a shell command | `command`, `expected_exit`, `expected_output` |
| `wayback` | Verify seal freshness | `agent`, `max_age_hours` |
| `endpoint` | HTTP health check | `url`, `expected_status`, `timeout_ms` |
| `process` | Check process running | `name`, `min_count` |
| `disk` | Disk usage threshold | `path`, `max_percent` |
| `tibet` | Verify TIBET chain integrity | `chain_id`, `max_age_hours` |

## Running a Check

=== "Python SDK"

    ```python
    from tibet_pol import Pol

    pol = Pol(agent="myagent.aint")

    result = pol.check("api-health-v1")

    print(result.status)        # "valid", "drift", "broken"
    print(result.score)         # 0.0–1.0 (fraction of steps passed)
    print(result.tibet_token)   # Provenance token

    for step in result.steps:
        print(f"[{step.status}] {step.name}: {step.message}")
    ```

=== "MCP Tool"

    ```
    pol_check template_id="api-health-v1"
    ```

=== "CLI"

    ```bash
    ainternet pol check api-health-v1
    ```

## Diffing Two Runs

```python
diff = pol.diff(run_a="run_01J...", run_b="run_02K...")

for change in diff.changes:
    print(f"{change.step}: {change.before} → {change.after}")
```

Useful for detecting when a previously `valid` step starts `drifting`.

## Generating an HTML Report

```python
report = pol.report(run_id="run_01J...", output="health-report.html")
print(f"Report saved to {report.path}")
```

## Available Built-in Templates

```bash
ainternet pol templates
```

| Template | Description |
|----------|-------------|
| `ainternet-core` | Hub, AINS, I-Poll, Cortex |
| `airlock-ready` | KVM availability, snapshot freshness |
| `wayback-integrity` | Seal chain continuity |
| `network-basics` | DNS, TLS, port 443 |

## Quick Health Check

For a fast one-liner without a template:

```bash
# Check a single URL
ainternet pol quick https://api.ainternet.org/health

# Check a process
ainternet pol quick --process ainternet-hub
```

## TIBET Integration

Each Pol run creates:
- `ERIN` token when the check starts
- `ERAAN` token with full results when complete
- `ERACHTER` token if any step triggers remediation

```python
# Get audit trail for a run
chain = ai.tibet.get_chain(chain_id=result.chain_id)
```

!!! tip "Schedule regular checks"
    Use Pol with a cron job or the AInternet scheduler to maintain continuous
    health visibility with full audit history.

## Conformance

Docs explain the protocol. Vectors decide whether another implementation reports health and remediation evidence the same way.

| Vector family | What it must prove |
|---|---|
| `tibet-evidence-conformance` | check start, result, remediation and failure receipts reconstruct |
| `tibet-security-conformance` | remediation requires the configured operator posture |
| operator health vectors | process, URL, TLS and template checks agree across runners |

Fail-closed cases: missing receipt store, unauthorised remediation, stale template, failed evidence export, unknown process target.

## Related

- [TIBET Provenance](./tibet.md)
- [Wayback Snapshots](./wayback.md)
- [NIS2 Compliance](../enterprise/nis2.md)
