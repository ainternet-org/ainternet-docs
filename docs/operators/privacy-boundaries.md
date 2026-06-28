# Privacy Boundaries

AInternet can run local, private, public, offline or federated. The privacy rule is not "trust the hub." The rule is: know which layer sees which object, and seal sensitive material before it leaves your boundary.

```text
hub != authority
transport != consent
reachable != allowed
plaintext != required
```

## The Short Version

- Private keys never leave your machine.
- Policy remains local unless you explicitly delegate it.
- Public federation is optional.
- Sensitive payloads should travel as sealed TIBET-zip/TBZ capsules.
- A hub may coordinate reachability; it should not become the source of permission.
- TIBET receipts should prove actions without forcing every private payload into a public service.

## What Leaves Your Network?

| Object | Local-only | Private hub | Public federation |
|---|---|---|---|
| private keys | never leave | never leave | never leave |
| public keys | local registry | private registry | public or federated AINS |
| actor names | local names | private `.aint` or local names | selected public `.aint` records |
| policy | local files/store | private hub may enforce local policy | not delegated to public hub |
| route decisions | local MUX | private MUX | shared only as route metadata where needed |
| TIBET receipts | local trail | private evidence store | selected receipts, hashes or proofs |
| message payloads | local transport | depends on relay mode | visible unless sealed |
| sealed TIBET-zip/TBZ | carrier object | carrier object | carrier object |
| SNAFT consent | local receipt | private receipt | shared with counterparties |
| audit exports | local | private | explicit export only |

## Public Hub Mode

Public AInternet helps outside actors discover and reach each other. It should not be the place where your private authority lives.

Use public federation for:

- public `.aint` discovery;
- public challenge/response;
- outside I-Poll delivery;
- public route availability;
- selected proofs and sealed capsules.

Do not use public federation as the default place for:

- private keys;
- raw secrets;
- unsealed sensitive payloads;
- local policy authority;
- private audit trails;
- internal-only actor maps.

## Sealed Transfer

When the payload matters, wrap it:

```text
payload -> TIBET receipt -> JIS binding -> TIBET-zip/TBZ carrier -> route
```

The transport may be I-Poll, MUX, HTTP, a private hub or a public hub. The desired object form is still a sealed, identity-bound carrier.

## Local First Does Not Mean Offline Only

Local first means the local network remains valid even before federation:

```text
actor proof works
local registry resolves
policy checks
routes open or fail closed
receipts are written
evidence can be exported
```

Internet access can add reach. It should not add authority.

## Questions To Ask

Before adding a hub, connector or public route:

- Who owns the actor key?
- Which proof is fresh for this action?
- What payload is plaintext?
- What is sealed?
- Which policy allowed the route?
- Where is the receipt stored?
- Can the other side verify enough without seeing everything?
- What happens if the route is unknown?

The safe answer for unknown or unproven routes is silence: `0x0000`.

## Related

- [Hub Neutrality](hub-neutrality.md)
- [Transfer Carriers](../reference/transfer-carriers.md)
- [AINS](../protocols/ains.md)
- [MUX](../protocols/mux.md)
- [SNAFT](../protocols/snaft.md)
