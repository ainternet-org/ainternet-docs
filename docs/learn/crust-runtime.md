# CRUST Runtime

CRUST is the zero-residue runtime floor for AInternet-in-a-box.

It lets a box carry executable runtime capsules as sealed `.tza` artifacts,
open them into anonymous memory, seal the memory view, and run without a
plaintext executable path on disk.

```text
sealed carrier may rest on disk
plaintext runtime must live only in sealed memory
```

Short version:

```text
musl/static = bring your own floor
memfd       = run without a path
seals       = make the memory view immutable
TIBET       = remember the act
```

## Why It Exists

Classic boot paths quietly trust the host:

```text
host libc
host package manager
host temp directory
host writable filesystem
host runtime updates
```

A sovereign AI box should be able to boot offline, on ordinary hardware, and
still know which runtime it is using. CRUST carries the runtime floor with the
box.

The musl/static floor reduces dependence on host distribution drift. The memfd
floor means the opened executable does not need a filesystem path.

## Runtime Flow

The executable path has this shape:

```text
sealed .tza capsule on disk
  -> verify carrier/hash/signature
  -> open/decompress into anonymous memory
  -> create memfd
  -> write plaintext executable bytes once
  -> apply seals: no write, no grow, no shrink
  -> execute from fd
  -> close/power loss vaporizes the plaintext runtime
```

Linux may report a live process like this:

```text
/proc/<pid>/exe = /memfd:tibet_phantom_run (deleted)
```

For a memfd, `(deleted)` does not mean an on-disk file was deleted. It means the
inode has no directory entry. The runtime is anonymous memory, not a host path
that used to be trusted.

## Data Spooler Variant

The same pattern applies to data:

```text
sealed .tza carrier
  -> identity-gated decrypt
  -> plaintext in locked memory
  -> memfd read-only handoff
  -> actor consumes fd, not path
  -> fd close/power loss vaporizes plaintext
```

CRUST closes the disk flank. It does not hide plaintext from the process that is
legitimately using it. If an actor has the data in memory, an attacker inside
that actor can read it. That is the honest physical floor.

So the complete rule is:

```text
CRUST prevents runtime/spooler disk spill.
Containment prevents actor self-spill.
TIBET records the route.
```

Memfd without containment is only half a door.

## What CRUST Is Not

CRUST is not:

- encryption by itself;
- a replacement for SNAFT or MUX authority;
- a replacement for namespaces, seccomp, bwrap or microVM containment;
- a promise that a compromised process cannot read its own memory;
- a claim that all host risk disappears.

CRUST is the runtime and spool floor. SNAFT decides authority. MUX routes
surfaces. Containment limits the actor. TIBET records the event.

## Evidence Surfaces

A box should make CRUST visible without forcing the operator to know kernel
internals.

| Surface | What it should show |
|---|---|
| `box status` | CRUST deep mode, capsules, live memfd path evidence |
| RAM-BOM | live memfd capsules and executable memory digests |
| System-BOM | honest partial/full sensor posture |
| Manifests | hashes for carried capsules and decompressed binaries |
| Receipts | boot, spool, seal and launch evidence |
| Cockpit/TUI | "running from anonymous RAM; no executable disk path" |

## Conformance Vectors

| ID | Test | Pass condition |
|---|---|---|
| CRUST-V1 | Boot deep-mode runtime | status shows CRUST deep mode and live memfd evidence |
| CRUST-V2 | No executable path | `/proc/<pid>/exe` resolves to a memfd-style path, not `payload/bin/...` |
| CRUST-V3 | Immutable fd | seals prevent write/grow/shrink after population |
| CRUST-V4 | Disk trace | plaintext executable/data is not written to a disk path |
| CRUST-V5 | RAM-BOM digest | executable memory segments can be hashed and marked as memfd capsules |
| CRUST-V6 | Actor spill test | receiving actor cannot write plaintext to host disk without grant |
| CRUST-V7 | Honest boundary | docs and UI state the in-process memory floor clearly |

## Publication Path

The IAB doctrine can later become a standalone spec or citable artifact:

```text
CRUST: Zero-Residue Runtime Capsules for Local-First AI Systems
```

Until then, treat CRUST as part of the AInternet running substrate: small,
auditable, local-first, and dark until a grant says otherwise.


## Related

- [What We Push Is What You Download](what-we-push-is-what-you-download.md) — the sealed carrier and its RAM-BOM / System-BOM evidence.
- [Runtime Is The Firewall](runtime-is-the-firewall.md) — enforcement on top of the sealed floor.
- [The Running Substrate](the-running-substrate.md) — where CRUST sits in the two-height model.
- [A Computer Inside a Computer](computer-inside-computer.md) — box-in-box isolation, plainly.
