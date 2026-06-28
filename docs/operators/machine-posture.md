# Machine Posture

"AI-ready" usually means a machine can run a model fast enough. AInternet needs a harder question:

```text
Which proven routes may this machine carry?
```

A laptop may be fine for local inference and still not be allowed to carry a sealed multi-actor business transaction. A workstation may carry hardware-backed encryption, TPM key custody, protected DMA and audit-grade route posture. Machine posture describes that difference.

## Not A Trust Score

Machine posture does not say a computer is morally trusted. It says which routes the machine can bear under current evidence.

Examples:

```text
safe for local inference
encrypts at line rate with AES-NI
can hold sealed multi-actor runtime
cannot support A5 sign-ahead under load
supports protected DMA hot-transfer lane
```

## What Is Checked

| Area | Example signals |
|---|---|
| CPU | AES-NI, PCLMULQDQ, FMA3, AVX2/AVX-512 |
| Memory | protected DMA, pinned buffers, userfaultfd capability |
| Identity | local JIS key custody, TPM2 availability |
| Kernel | KVM, IOMMU, namespace/cgroup support |
| GPU | local GPU, DMA path, P2P/topology where available |
| Audit | local TIBET trail, sign-ahead capability, durable receipts |
| Network | local/private/public route mode, MUX guard |

Unknowns should stay unknown. A machine must not claim a lane it did not prove.

## Route Carrying

Machine posture combines with route posture:

```text
route posture proves what the route is
machine posture proves whether this box may carry it
```

Example:

```text
route: #54359
payload: hot_transfer
machine: supports pinned DMA + protected route + sign-ahead
verdict: can carry
```

If a required capability is missing, the route should hold, degrade or go dark rather than pretend.

## Operator Output

A useful machine posture command should explain both allowed and missing pieces:

```text
machine posture
  ok   AES-NI: line-rate encryption available
  ok   FMA3: local inference compute lane available
  ok   IOMMU: protected DMA boundary available
  hold AVX-512: not present, A5 sign-ahead under load not claimed
  ok   TPM2: local key custody available

can carry:
  #34358 hot_transfer: yes
  #54359 composite hot_transfer: yes, if relation and receipt are fresh
  #00000 unknown route: no, dark route
```

## Related

- [Route Posture](../learn/route-posture.md)
- [Operator Tooling](tooling.md)
- [The Running Substrate](../learn/the-running-substrate.md)
- [Route Posture API](../reference/route-posture-api.md)
