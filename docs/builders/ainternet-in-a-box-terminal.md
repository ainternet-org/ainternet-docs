# AInternet-in-a-Box Terminal Path

This is the same path as the TUI, written as commands. Use it when you want to
change paths, inspect the engine under the cockpit, run offline, or build the
same posture from `ainternet[full]` on a normal host.

The terminal path is canonical:

```text
command -> proof -> posture -> receipt
```

**Payoff:** do by hand what the TUI does for you: prove a clean box, bind an
actor, verify the grant, self-ping, and write the first receipt.

**Use this as a reference:** this is the low-frequency task page. If you only set
up a clean node twice a year, copy-paste from here instead of trusting memory.

**AI context:** this page contains the runnable path without requiring the TUI
or a search across the docs tree.

The TUI may make this easier. It must not make it different.

!!! warning "Before you start"
    Replace anything in `<angle-brackets>` or ending in `.example`.
    Verify command names with `--help` when your installed package differs.

## Step 0: Install Or Enter The Box

If you are using the packaged CLI on a host:

```bash
pip install -U "ainternet[full]"
ainternet --help
```

If you are already inside AInternet-in-a-box, start with the box doctor:

```bash
ainternet box doctor
```

**You now have:** a CLI surface. You have not proven the box yet.

**What is proven:** only that the command surface exists.

**If it fails:** fix the package install or enter the box before continuing.

**Next:** prove the boot source and boundary.

## Step 1: Prove The Golden

```bash
ainternet box proof --boot --output json
ainternet box proof --boundary --output json
```

Expected facts:

```text
boot_source: golden-rootfs
golden_hash: sha256:...
boundary_class: microvm-equivalent
secret_free: true
```

**You now have:** a clean boot proof.

**What is proven:** this runtime came from the expected golden rootfs and carries
the expected boundary class.

Failure mode:

```text
missing proof -> hold
bad proof     -> dark
```

**Next:** create the local actor.

## Step 2: Create The Local Actor

```bash
ainternet node init --local
ainternet actor create <node-name>.example.aint --role node
ainternet actor prove <node-name>.example.aint --output json
```

Expected facts:

```text
actor: <node-name>.example.aint
identity: JIS Ed25519
fresh_challenge: pass
private_key_location: local
```

**You now have:** a node actor. The name routes; the key proves.

**What is proven:** the local actor can answer a fresh JIS challenge.

**If it fails:** do not continue to grants or routing. No JIS proof means no
actor route.

**Next:** verify the broker-signed grant.

## Step 3: Verify The Broker-Signed Grant

```bash
ainternet box grant show --output json
ainternet box grant verify --output json
```

For a clean node, the allowed surfaces should be:

```text
audit.aint
tool.*.waint
```

The default must be:

```text
unknown_surface: 0x0000
```

**You now have:** positive authority for named surfaces only.

**What is proven:** the parent broker signed the exact surfaces this box may
materialize.

Failure mode:

```text
bad signature      -> dark
wrong mode/session -> dark
expired grant      -> dark
unknown surface    -> 0x0000
```

**Next:** self-ping the local MUX.

## Step 4: Self-Ping The Local MUX

Find the local MUX port:

```bash
ainternet node doctor --output json
```

Then ping:

```bash
tibet-ping stack --mux http://127.0.0.1:<port>
```

Read the route:

```bash
ainternet route explain <node-name>.example.aint <node-name>.example.aint --intent self.ping --output json
```

**You now have:** a local route candidate and its posture.

**What is proven:** the lane carries locally and the posture can be inspected.

Keep the doctrine line in your head:

```text
reachable != authorized
```

**If it fails:** stay local and repair the MUX or node planes. Do not connect a
peer yet.

**Next:** write the first receipt.

## Step 5: Write A Receipt

```bash
ainternet send <node-name>.example.aint audit.aint --type PUSH --content "hello"
ainternet audit trail --actor <node-name>.example.aint --output json
```

Expected facts:

```text
message_id
route_posture
tibet_receipt_id
causal_seq
delivery_state
```

**You now have:** an action with reconstructable evidence.

**What is proven:** delivery, route posture and TIBET receipt are connected.

If the receipt is missing, the action is not complete.

**Next:** test an ungranted surface.

## Step 6: Test The Dark Route

```bash
ainternet route explain <node-name>.example.aint capture.this --intent probe --output json
```

Expected clean-node result:

```text
route: 0x0000
reason: surface-not-in-signed-grant
```

**You now have:** a denial proof. The box did not hide `capture.this`; it never
received a signed grant for it.

**What is proven:** the clean node fails closed for surfaces outside the signed
allowlist.

**If it fails:** a clean node exposing `capture.this` is not in the clean
posture. Stop and inspect the grant.

**Next:** add a bounded tool.

## Step 7: Add One Tool

```bash
ainternet tool create tool.echo.waint --under <node-name>.example.aint
ainternet tool invoke tool.echo.waint --input "hello"
ainternet audit trail --actor tool.echo.waint --output json
```

**You now have:** a bounded tool surface under your node.

The tool may only act through the signed `tool.*.waint` surface and its receipts.

**What is proven:** local tools can be wrapped as actors instead of inheriting
ambient local authority.

**If it fails:** check the tool actor, the signed grant and the audit receipt.

**Next:** connect a peer only after the local loop is green.

## Step 8: Connect A Peer

Do this only after the local loop is green.

```bash
ainternet peer resolve peer.example.aint --output json
ainternet route challenge <node-name>.example.aint peer.example.aint --output json
ainternet route open <node-name>.example.aint peer.example.aint --intent ipoll.push --output json
```

Expected rule:

```text
resolution is not consent
challenge is not delivery
route-open is not complete without a receipt
```

**You now have:** a peer lane only if the route is proven.

**What is proven:** peer reachability is subordinate to challenge, consent,
posture and receipt.

**If it fails:** keep the node local. Resolution alone is not consent.

## Conformance

Use vectors to test the route instead of trusting this page:

```bash
pip install -U "tibet[conformance]"
tibet-comms-conformance
tibet-evidence-conformance
tibet-security-conformance
```

The page is a runbook. Vectors decide compatibility.

## Machine-Readable Companion

```bash
curl -fsS https://ainternet.org/upip.json
curl -fsS https://ainternet.org/resources.json
curl -fsS https://ainternet.org/api.json
```

## Related

- [AInternet-in-a-Box](ainternet-in-a-box.md)
- [Surface Grant](../reference/surface-grant.md)
- [Local Node](../quickstart/local-node.md)
- [Route Posture](../learn/route-posture.md)
