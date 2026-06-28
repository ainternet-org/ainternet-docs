# Doc Posture

Documentation is part of the system. If a page tells someone to build, route, seal, federate or operate AInternet, the page itself needs a posture: what it expects from the reader, what it gives back, and how a reviewer can tell whether it is safe to publish.

The rule is the same as route posture:

```text
Do not score the document.
Declare what route the document can carry.
```

## Push and Pull

Every public page has two directions:

| Direction | Question |
|---|---|
| pull posture | What does this page require from the reader? |
| push posture | What can this page safely deliver to the reader? |

Example:

```yaml
doc_posture:
  reader: builder
  mode: local-first
  pull:
    prior_knowledge: "basic shell + Python"
    network_required: false
    secrets_required: false
  push:
    outcome: "three local actors and one signed route"
    evidence: "doctor output + TIBET receipt"
    next_step: "add policy or federate"
  guardrails:
    - "no public hub required"
    - "no private keys pasted into docs"
    - "sensitive payloads use TIBET-zip/TBZ"
```

If the pull posture is too high, the page belongs later in the journey. If the push posture is vague, the page needs a better outcome.

## The Axes

Doc posture is not one number. It is a declaration across the axes that matter for builders.

| Axis | Meaning | A good page answers |
|---|---|---|
| readability | Can the reader follow the page? | Where am I, what is next, what do I not need yet? |
| reliability | Is the page grounded? | Which source, package, vector, API or command backs this? |
| richness | Does it explain the shape? | Why this primitive, what edges matter, what fails closed? |
| workability | Can it be used? | Can I copy the command, run it, and compare output? |
| noise filtering | Does it remove wrong paths? | What should I not do, what is legacy, what is optional? |

## Suggested Header

Use this on tutorial, operator and builder pages when it helps:

```yaml
doc_posture:
  reader: operator | builder | implementer | auditor
  mode: local-first | private-hub | public-federation | lab
  pull:
    tools: [python, shell]
    network_required: false
    secrets_required: false
  push:
    outcome: "local node running"
    evidence: "doctor output"
    next_step: "add actor"
  guardrails:
    - "public federation is optional"
```

Not every page needs the same shape. A Learn page may push understanding. A Quickstart page must push a runnable result. A Reference page must push a stable contract.

## Page Families

| Page type | Required posture |
|---|---|
| Learn | clear concept, honest boundaries, links to runnable path |
| Quickstart | copy/paste commands, expected output, rollback/cleanup |
| Reference | stable fields, auth, privacy, error behavior, compatibility notes |
| Operator | local-first commands, evidence to inspect, failure modes |
| Builder | extension points, plugin shape, conformance vectors |
| Lab | measured results, hardware/software assumptions, no production claim |

## Publish Gate

Before a page is pushed to the commons, check:

- Does it say whether public AInternet is optional or required?
- Does it say what data leaves the local machine?
- Does it avoid static trust-score language?
- Does it distinguish identity, transport, policy and consent?
- Does it have at least one next action?
- If it has commands, are they copy/paste safe?
- If it makes a technical claim, is there a source, vector or measurement?
- If it handles secrets, does it say what never leaves?

## Examples

Weak:

```text
Install the full stack and connect to the hub.
```

Better:

```text
Install the local node profile, create three local actors, send one signed local message, inspect the TIBET receipt, then federate only when useful.
```

Weak:

```text
This actor is trusted.
```

Better:

```text
This route is allowed because the current route posture satisfies policy and the action leaves a receipt.
```

## Related

- [Privacy Boundaries](privacy-boundaries.md)
- [Machine Posture](machine-posture.md)
- [Route Posture](../learn/route-posture.md)
- [Local Node Quickstart](../quickstart/local-node.md)
