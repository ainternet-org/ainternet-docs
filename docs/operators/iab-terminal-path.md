# IAB Terminal Path

`jasper.aint` owns the box first. Every AI actor that follows is anchored under
that human root, with its own `.aint`, its own runtime shape, and its own
receipts. This page is the terminal-first path for operators who want to see the
exact box verbs behind the pre-boot console and cockpit.

The CLI is the contract. The TUI and web console are lenses over the same
verbs.

```text
identity -> posture -> runtime -> grant -> bind -> seal -> launch
```

Do not compress this into a giant `&&` command. Boot, provision, actor binding
and launch are phase boundaries. Each phase says what is proven and what is
still missing.

---

## 1. Verify And Enter The Release

```sh
gh release download v0.2.0-dev -R ainternet-org/ainternet-in-a-box --clobber
python3 unpack-tza.py ainternet-in-a-box-0.2.0-dev.tza
cd ainternet-in-a-box-0.2.0-dev
./box version
```

Representative output:

```text
carrier   : TBZ magic + manifest parsed
payload   : sha256 ✓
genesis   : signature ✓ against pinned key · channel=dev · manifest pinned ✓
verified sovereign box -> /iab/ainternet-in-a-box-0.2.0-dev
ainternet-in-a-box · 0.2.0-dev · build <build-id>
```

This proves the carrier, payload hash and pinned genesis signature. It does not
prove the host can run the box, that a root exists, or that any actor can carry.

Next:

```sh
./box up
```

---

## 2. Boot The Floor

```sh
./box up
```

Representative output:

```text
Continuity Boot: branch=none previous_close=missing reason=no-identity
✓ kvm + payload + broker + tools present
✓ crust deep mode — ignitiond/lttle/cow-seed-store run from SEALED memfd
✓ bridge ltbr-box + host attestation + certs
✓ golden seeded as store image
ignitiond up (...) — the box's own VMM
broker: signing this box's own surface grant + spawning single-root golden...
```

This proves the host floor can start the box path and the CRUST deep-mode
capsules. It does not prove an operator identity or a provisioned actor pool.

Next:

```sh
./box enroll jasper.aint --human
```

---

## 3. Enroll The Human Root

```sh
./box enroll jasper.aint --human
```

Representative output:

```text
✓ minted actor key -> certs/jasper.aint.key
✓ minted seal key -> certs/jasper.aint.seal.key
✓ node-identity.json -> aint=jasper.aint · type=human

a root owns the box. AI actors run ON BEHALF OF it.
```

This proves the box has a human root identity. It does not prove any actor,
runtime, model, provider keyref or egress route.

Next: choose an actor shape.

---

## 4. Native CLI Actor With External Egress

Codex is a native CLI actor. The binary runs locally, but the runtime traffic
goes to OpenAI, so the actor locality is **external**.

Declare and bind the actor under the human root:

```sh
./box actor new codex.aint --kind codex --alias "Codex" --ai
./box pop --agent codex.aint
```

Representative output:

```text
✓ declared: codex.aint   mode=cli   provider=codex   type=ai

popped:  raint-....test.aint
bound:   codex.aint  ⊆  jasper.aint
key certs/codex.aint.key · grant actors/codex.aint.json (root-signed)
```

Prepare the runtime supply chain:

```sh
./box runtime prefetch codex
./box runtime stage codex
./box runtime status
./box runtime switch codex 0.144.6
```

This proves the Codex runtime was mirrored, staged and selected for the next
bind. It does not prove egress is allowed.

Open the egress gate deliberately:

```sh
./box provision set-snaft NORMAL
./box grant egress codex.aint
```

Use the declared actor `.aint` for the grant. Do not aim an egress grant at the
runtime `.waint` work surface; `.waint` appears after bind, not as the actor
declaration.

Bind and seal on clean exit:

```sh
./box bind codex
```

Representative output:

```text
⟳ codex.waint bound · grant sha256:...
surfaces pty.aint,audit.aint,tool.local-shell.waint,net.egress.waint
exit /quit or Ctrl-D to seal (Ctrl-C = crash -> reseed)
```

Clean close emits a receipt:

```json
{
  "actor": "codex.waint",
  "closed": true,
  "event": "actor-exit-clean",
  "exit_code": 0,
  "result": "0x4000"
}
```

Sandbox is the default floor. `--no-sandbox` is the explicit development escape,
not a normal operator flag.

---

## 5. Local Or LAN API Actor

An API/local actor is a request-envelope runtime. It can ask a model endpoint;
it does not get a shell, filesystem access or external egress by default.

Loopback example:

```sh
./box actor onboard qwen.aint --kind api --provider ollama --endpoint http://127.0.0.1:11434
```

Private LAN example:

```sh
./box actor onboard qwen.aint --kind api --provider ollama --endpoint http://192.168.x.x:11434
```

Loopback and private LAN are different postures. `127.0.0.1` is local to the
box. A `192.168.x.x` endpoint is useful, but it is not automatically
`LOCAL_ONLY`; treat it as explicit route/grant work.

Representative START output:

```text
actor onboard: qwen.aint — the START flow (Seed · Triage · Anchor · Restrict · Trail)

[1/5] SEED
✓ declared: qwen.aint mode=api provider=ollama endpoint=http://127.0.0.1:11434
surfaces: tool.infer.ollama + lane.read/say (NO shell/fs/egress)

models for ollama (qwen.aint) — pick a number:
  [ 1] gemma4:26b
  [11] qwen2.5:7b

✓ model = gemma4:26b — written to the declaration

[3/5] ANCHOR
✓ qwen.aint is UP (light bind · no VM — a thin bound runtime under jasper.aint)

[4/5] RESTRICT
surfaces: ['tool.infer.ollama', 'lane.read.master', 'lane.say.master']
```

Test and open TCLI:

```sh
./box actor test qwen.aint
./box actor cli qwen.aint
```

Representative TCLI output:

```text
opening tcli as qwen.aint — /quit to seal
qwen.aint · bound actor runtime
  on behalf of jasper.aint
  provider/model local/gemma4:26b (locked)
  runtime request envelope · no shell/fs/egress unless granted
  audit /var/lib/ainternet-box/actors/qwen.aint.tcli-state/tcli/audit.tza.jsonl
  /models · /whoami · /trail · /clear · /verify · /seal · /help · /quit
qwen.aint› /quit
  ✓ session sealed (qwen.aint) · audit-head no-audit
```

This proves the actor opens through TCLI, acts on behalf of the human root, uses
the locked provider/model, and seals on `/quit`.

---

## 6. Evidence: System-BOM And TIBET-BOM

```sh
./box sys-bom
./box bom
```

Representative System-BOM:

```text
System-BOM · iab-node · verdict partial (5/7 present)
  ✗ gpu  ✓ hw  ✓ mux  ✓ net  ✓ ram  ⚠ role  ✓ static
  hw    : TPM present · SecureBoot off · bare-metal · entropy 256
  mux   : 1 active enclave(s)
  gpu   : driver none
  next  : role · gpu · receipt · tui · policy
  sha256: ...

sealed a local result into your inbox — kind system-bom
```

Representative TIBET-BOM:

```text
TIBET-BOM LEDGER VALIDATOR
Chain        : INTACT (24 events)
Ticks        : 24 total · 24 attested labour
Anchors OK   : YES
Labour OK    : YES
Envelope OK  : YES
VERDICT      : [INTACT]
composition  : cli-session.grant x6, cli-session.seal x6, ...
```

System-BOM says what sensors are present or partial. TIBET-BOM says whether the
receipt chain is intact. These are different truths; a partial system can still
have an intact ledger.

---

## 7. Seal Human And Machine Posture

Human posture:

```sh
./box provision seal --human-posture
```

Machine posture:

```sh
./box provision seal --machine-posture
```

Full provision fold:

```sh
./box provision seal
./box provision status --json
```

The machine posture command is `./box provision seal --machine-posture`. The
older shape `./box seal machine-posture` is not a box command.

Representative machine seal:

```json
{
  "result": "0x4000",
  "sealed": "machine",
  "root": "jasper.aint",
  "pool": 1,
  "can_carry": "0/1",
  "gaps": []
}
```

Partial seals are useful evidence. They are not the same as final launch
readiness.

---

## 8. Ready To Go Dark

The operator should read this as a threshold, not as a casual launch button:

```text
ready to go dark?
```

Meaning:

- pre-boot compose ends;
- the sealed pool becomes the boundary;
- free setup fields disappear;
- the box boots as a dark runtime;
- later changes go through ceremony, triage, relation or explicit dev escape;
- the cockpit becomes telemetry-first: actors, lanes, I-Poll, TIBET, System-BOM,
  refusals and seals.

Command shape:

```sh
./box launch --json
./box launch
```

A launch command must not boot through a false green. If the fold is missing a
required fact, it should return `0x0000:<reason>` and name the next safe step.

---

## Common Refusals

External CLI under local-only posture:

```json
{
  "result": "0x0000:egress-not-permitted",
  "aint": "codex.waint",
  "carry_decision": "needs_egress_grant",
  "egress_target": "api.openai.com",
  "locality": "external"
}
```

Correct next steps:

```sh
./box provision set-snaft NORMAL
./box grant egress codex.aint
```

Wrong actor target:

```text
granting egress to the runtime .waint work surface instead of the declared .aint actor
```

Representative refusal:

```json
{
  "result": "0x0000:no-such-actor",
  "hint": "declare the actor or pass --to <target>"
}
```

Unsealed session:

```json
{
  "result": "0x0000:reseed-required",
  "unsealed_sessions": ["codex_waint-..."]
}
```

Refusal is evidence. The UI should show it, not smooth it away.

---

## Short Phase Path

This is the smallest readable path. Keep it phased.

```sh
# release
gh release download v0.2.0-dev -R ainternet-org/ainternet-in-a-box --clobber
python3 unpack-tza.py ainternet-in-a-box-0.2.0-dev.tza
cd ainternet-in-a-box-0.2.0-dev
./box version

# floor and root
./box up
./box enroll jasper.aint --human

# external CLI actor
./box actor new codex.aint --kind codex --alias "Codex" --ai
./box pop --agent codex.aint
./box runtime prefetch codex
./box runtime stage codex
./box runtime status
./box runtime switch codex 0.144.6
./box provision set-snaft NORMAL
./box grant egress codex.aint
./box bind codex

# local/API actor
./box actor onboard qwen.aint --kind api --provider ollama --endpoint http://127.0.0.1:11434
./box actor test qwen.aint
./box actor cli qwen.aint

# evidence and seal
./box sys-bom
./box bom
./box provision seal --human-posture
./box provision seal --machine-posture
./box provision seal
./box provision status --json
./box launch --json
./box launch
```

## Related

- [Tooling](tooling.md) — operator tools and route posture checks.
- [Machine Posture](machine-posture.md) — what the hardware and runtime floor can carry.
- [Audit Cockpit](audit-cockpit.md) — evidence as a cockpit, not a loose log.
- [Bind an AI, Runtime-Bound](../learn/bind-an-ai.md) — why actor binding is per-action, not a bearer key.
- [Actor Seal](../learn/actor-seal.md) — clean close as continuity proof.
