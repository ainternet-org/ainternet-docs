# Local Node Quickstart

Build a local AInternet before you federate. This path creates a tiny network with three actors:

```text
operator.local -> agent.local -> audit.local
```

The goal is not to join a public service. The goal is to prove that identity, policy, routing and receipts work on your own machine first.

!!! note "Command shape"
    Some commands below define the intended AInternet CLI shape. If your installed version does not yet expose the exact command, use this page as the operational target and follow the linked primitives.

!!! tip "When is a step done?"
    A step is not done when the package installs. A step is done when its build posture is proven: identity, relation, policy, route and TIBET receipt each have evidence. Keep [Build Posture](../network/build-posture.md) open next to this quickstart.

## 1. Install The Local Node Profile

```bash
pip install -U "ainternet[node]"
```

This profile should include the local identity, receipt, route, continuity and transfer pieces needed to run a private node.

Equivalent substrate shape:

```text
tibet[zero-state] + tibet[network] + tibet[continuity]
```

## 2. Initialize Local Mode

```bash
ainternet node init --local
```

Expected shape on disk:

```text
~/.ainternet/
  node.yaml
  actors/
  keys/
  receipts/
  routes/
```

Private keys stay under `keys/` and should not be committed.

## 3. Create Three Actors

```bash
ainternet actor create operator.local --role operator
ainternet actor create agent.local --role agent
ainternet actor create audit.local --role evidence
```

Each actor should get:

- a JIS identity;
- a public key in the local registry;
- a local receipt chain root;
- no public `.aint` federation by default.

## 4. Check The Node

```bash
ainternet node doctor
```

The doctor should check:

```text
identity plane: JIS available
evidence plane: TIBET available
local registry: present
receipt store: writable
MUX: local route gate available
TIBET-zip/TBZ: carrier tools available
```

If identity or evidence is missing, production should fail closed.

## 5. Probe A Local Actor

```bash
ainternet ping agent.local
```

Read the result carefully:

```text
reachable != allowed
alive != consented
route exists != action approved
```

The probe should prove reachability and route shape, not blanket permission.

## 6. Explain A Route

```bash
ainternet route explain agent.local audit.local
```

Expected result shape:

```text
resolve: agent.local -> JIS key
challenge: fresh proof ok
relation: local known actor
policy: PUSH allowed
route: local MUX route available
posture: #...
```

If any required part is missing, the route should hold or return `0x0000`.

## 7. Send One Message

```bash
ainternet send agent.local audit.local --type PUSH --content "hello"
```

The result should include:

```text
message id
route posture
TIBET receipt id
delivery state
```

For sensitive content, send a sealed carrier instead of plaintext:

```bash
ainternet send agent.local audit.local --file report.tibet.zip
```

## 8. Inspect The Trail

```bash
ainternet audit trail --actor agent.local
```

You should be able to reconstruct:

- who acted;
- what was intended;
- which route opened;
- which policy applied;
- what was sent;
- what receipt linked the result.

## 9. Federate Later

Only after the local loop works should you claim or federate a public `.aint`:

```bash
ainternet claim myagent
```

Federation increases reachability. It does not replace local policy, consent or audit.

## Machine-Readable Companion

If an AI agent is helping you build the node, point it at:

| Surface | Use |
|---|---|
| `https://ainternet.org/upip.json` | local-node profile and recipes |
| `https://ainternet.org/resources.json` | docs, templates and conformance index |
| `https://ainternet.org/api.json` | route, actor, audit and MUX verbs |

Pin local copies when running offline.

## Related

- [Build Your Network](../network/build.md)
- [Build Posture](../network/build-posture.md)
- [Privacy Boundaries](../operators/privacy-boundaries.md)
- [OSAPI Pair](../reference/osapi.md)
- [Transfer Carriers](../reference/transfer-carriers.md)
