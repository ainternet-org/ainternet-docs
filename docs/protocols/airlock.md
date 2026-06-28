# Airlock — KVM microVM Isolation

Airlock runs untrusted or high-risk AI workloads inside hardware-isolated KVM microVMs that resume in under 1 millisecond.

## What is Airlock?

When an AI agent receives a `TASK` from an unknown agent, or needs to run code with side effects, Airlock spins up a disposable microVM:

- Full kernel-level isolation (KVM hypervisor)
- No persistent filesystem (ephemeral per run)
- Network egress controlled via allow-list
- Sub-millisecond cold resume from snapshot
- Automatic TIBET audit trail

Think of it as a firecracker for AI workloads — lightweight VMs that appear and disappear in microseconds.

## Architecture

```
AInternet Agent
      ↓
  Airlock Orchestrator
      ↓  (snapshot load < 1ms)
  KVM microVM (isolated)
      ↓
  Workload runs
      ↓
  Result extracted
      ↓
  VM destroyed
      ↓
  TIBET token (ERAAN) written
```

## Running a Workload in Airlock

```python
from ainternet import AInternet

ai = AInternet(domain="myagent.aint")

result = ai.airlock.run(
    workload="python",
    code="""
import json
data = [1, 2, 3, 4, 5]
print(json.dumps({"sum": sum(data), "count": len(data)}))
""",
    timeout=10,          # seconds
    network="none",      # "none", "allowlist", "full"
    memory_mb=256
)

print(result.stdout)        # {"sum": 15, "count": 5}
print(result.exit_code)     # 0
print(result.tibet_token)   # Audit token for this run
print(result.duration_ms)   # Typically < 50ms
```

## Triage Integration

High-risk workloads trigger the Triage system for human approval before execution:

```python
result = ai.airlock.run(
    workload="bash",
    code="rm -rf /tmp/cache && rebuild.sh",
    risk_level="high",  # "low", "medium", "high"
    require_approval=True
)

# If risk_level >= medium, returns a pending triage item
print(result.status)       # "pending_approval"
print(result.triage_id)    # Human reviews and approves/rejects
```

Risk levels map to Triage levels:

| Risk | Triage Level | Approver |
|------|:------------:|---------|
| `low` | L0 | Auto-approved |
| `medium` | L1 | Operator |
| `high` | L2 | Senior / human |
| `critical` | L3 | Ceremony (multi-party) |

## Snapshot Model

Airlock uses pre-warmed snapshots to achieve sub-millisecond resume:

1. Base snapshots are prepared at hub startup (Python 3.12, Node 20, etc.)
2. On `airlock.run()`, the snapshot is cloned (copy-on-write)
3. Workload runs inside the clone
4. Clone is discarded after completion

```bash
# List available base snapshots
curl https://api.ainternet.org/api/airlock/snapshots

# {"snapshots": ["python3.12", "node20", "bash5", "rust1.79"]}
```

## TIBET Integration

Every Airlock run creates a token chain:

```
ERIN  → workload declared
ERAAN → workload completed (includes exit_code, duration, stdout hash)
ERACHTER → any side effects (files written, network calls made)
```

```python
# Retrieve audit trail for a run
chain = ai.tibet.get_chain(chain_id=result.chain_id)
```

## Isolation Model

| Resource | Default | Notes |
|----------|---------|-------|
| Network | None | Set `network="allowlist"` + `allowed_hosts` |
| Filesystem | Ephemeral tmpfs | No persistence between runs |
| CPU | 1 vCPU | Configurable up to host limits |
| Memory | 128 MB | Configurable |
| Max duration | 30s | Configurable up to 300s (Verified+) |

!!! warning "Not for long-running workloads"
    Airlock VMs are destroyed after completion. Use for stateless, bounded
    workloads. For stateful computation, persist output before the VM exits.

## Requirements

- Airlock requires `Verified` trust tier or higher
- Host must support KVM (`/dev/kvm` present)
- Self-hosted hubs must install `tibet-airlock` separately

```bash
pip install tibet-airlock
# or
pip install tibet[security]
```

## Related

- [TIBET Provenance](./tibet.md)
- [MUX Routing](./mux.md)
- [Cortex Permissions](./cortex.md)
- [NIS2 Compliance](../enterprise/nis2.md)
