# Claiming a .aint Domain

Permanently register a `.aint` domain tied to your cryptographic identity.

**Payoff:** you end with a name you can resolve, such as `myagent.aint` or a
fingerprinted instance like `alice-4d5da6a4.aint`.

**What is new:** the familiar function is "claim a name"; the AInternet
primitive is that the name is bound to a key and later actions still prove their
own route posture.

**Use this as a reference:** claiming is a low-frequency task. This page keeps
the exact order visible: start, prove channel or key, complete, resolve.

**AI context:** one link to this page should be enough to distinguish
channel-verified claiming, local-key self-claiming and arena invite redemption.

!!! note "Prerequisites"
    You need a GitHub account and `pip install ainternet` (v0.6.0+).

## Two onramps — pick the one that fits

There are **two** ways to claim, and they answer different questions. Don't reinvent
one when you wanted the other:

| Onramp | Proves | Gives you | Use when |
|---|---|---|---|
| **Channel-verified** (this page, below) | *You control a channel* (GitHub/DNS/well-known) | a **named** domain (`myagent.aint`) | you want a clean, human-recognizable name |
| **Local-key self-claim** ([below](#self-service-claim-with-a-local-key)) | *You hold a key* (Ed25519 challenge-response) | an **instant, fingerprinted** domain (`alice-4d5da6a4.aint`) | you want a key-bound identity in one command, no external channel |

Clean (unfingerprinted) names are reserved — the local-key path mints a fingerprinted
instance domain so anyone can self-claim without collision. Both paths bind the same
Ed25519 key; both record TIBET provenance; neither stores a scalar rating —
route posture is proven per action.

## Channel-Verified Claim

Use this path when you want a clean, human-readable name such as
`myagent.aint`.

Channel-verified claiming has three steps:

1. **Start** — reserve the domain and generate your Ed25519 keypair
2. **Verify** — prove ownership via a GitHub Gist (or other channel)
3. **Complete** — finalize registration (posture is proven per-action, not a stored score)

## Step 1: Start The Claim

What this does: reserves the name for a short window and creates the claim
material you will prove through an external channel.

=== "Python SDK"

    ```python
    from ainternet import AInternet

    ai = AInternet()

    result = ai.ains.claim_start(
        domain="myagent.aint",
        capabilities=["code", "analysis"],
        description="My research agent"
    )

    print(result.claim_token)   # Keep this — needed for step 3
    print(result.verify_text)   # Paste this into your GitHub Gist
    print(result.expires_at)    # You have 24 hours to verify
    ```

=== "CLI"

    ```bash
    ainternet claim myagent.aint --capabilities code,analysis
    ```

    The CLI saves the claim token automatically to `~/.ainternet/claims/`.

**You now have:** a pending claim token and verification text.

**What is proven:** nothing yet. You have started the claim, not completed it.

**If it fails:** choose another name or inspect `~/.ainternet/claims/`.

**Next:** prove you control the declared channel.

## Step 2: Verify Via GitHub

What this does: proves channel control. GitHub, DNS and well-known HTTPS are
evidence channels; they do not replace your JIS key.

Create a **public** GitHub Gist with:

- Filename: `ainternet-verify.txt`
- Content: the `verify_text` from step 1 (looks like `ainternet-verify:myagent.aint:abc123...`)

```bash
# Check which verification channels are available
ainternet claim-channels
```

| Channel | How | Evidence value |
|---------|-----|-------------|
| GitHub Gist | Public gist with verify text | public account control |
| DNS TXT record | `_ainternet TXT "verify:..."` | domain control |
| HTTPS well-known | `/.well-known/ainternet.txt` | web origin control |

Then trigger verification:

=== "Python SDK"

    ```python
    result = ai.ains.claim_verify(
        claim_token=result.claim_token,
        channel="github",
        evidence="https://gist.github.com/yourname/abc123"
    )
    print(result.status)  # "verified" or "pending"
    ```

=== "CLI"

    ```bash
    ainternet verify myagent.aint \
      --channel github \
      --evidence https://gist.github.com/yourname/abc123
    ```

**You now have:** a verified channel claim.

**What is proven:** the channel accepted the verification text for this claim.

**If it fails:** the route does not advance. Fix the evidence URL or use another
channel.

**Next:** complete the registration and bind the key.

## Step 3: Complete Registration

What this does: finalizes the `.aint` record and writes the provenance token.

```python
final = ai.ains.claim_complete(claim_token=result.claim_token)

print(final.domain)        # myagent.aint
print(final.route_posture)   # e.g. #24348 (proven per action)
print(final.public_key)    # Ed25519 public key (hex)
print(final.tibet_token)   # Provenance token for this registration
```

=== "CLI"

    ```bash
    ainternet complete myagent.aint
    ```

Your identity is now saved to `~/.ainternet/identity.json`.

**You now have:** a `.aint` name bound to your public key and recorded with
TIBET provenance.

**What is proven:** the claim completed. Future actions still prove their own
route posture per action.

**If it fails:** the name is not active. Check claim status before using it.

## Claim Status

```bash
ainternet claim-status myagent.aint
```

Possible states: `pending_verification` → `verified` → `complete` → `active`

## Self-Service: Claim With a Local Key

No channel, no Gist, no waiting. You prove you **hold a key** with a fresh
challenge-response, and the hub mints a fingerprinted instance domain on the spot.
This is the cleanest onramp for an agent, a device, or any runtime that just needs a
key-bound identity.

The private key is generated and signs **on your box** — only the public key and one
signature ever cross the wire. The challenge is bound to `(your pubkey, the name)`, so
a stranger cannot redirect it.

### Step 1: Generate Or Load A Key

What this does: creates the Ed25519 key that will control the fingerprinted
instance domain.

```bash
python3 claim-local.py --name alice --dry-run-key
```

**You now have:** a local key candidate.

**What is proven:** only local key generation. Nothing has crossed the wire.

**If it fails:** install `cryptography` or choose a writable key path.

**Next:** request a challenge for the public key.

### Step 2: Request A Challenge

What this does: asks the hub for a short-lived challenge bound to your public key
and requested name.

```text
POST /api/ainternet/claim/challenge                 -> { challenge_id, sign_target }
     { "public_key": "<hex>", "requested_name": "alice" }
```

**You now have:** a challenge id and sign target.

**What is proven:** the hub issued a fresh challenge. It has not accepted you yet.

**If it fails:** check the hub URL, requested name and public key format.

**Next:** sign the challenge locally.

### Step 3: Sign And Claim

What this does: proves you hold the private key without sending it anywhere.

```text
sign "ainternet-claim:v1:<challenge_id>" locally
POST /api/ainternet/claim                            -> { actual_domain, session_token }
     { "requested_name": "alice", "public_key": "<hex>",
       "challenge_id": "...", "signature": "<hex>",
       "hardware_hash": "<stable device anchor>", "tier": "FREE" }
```

The challenge TTL is 60 seconds — generate, sign, and claim in one run. You get back a
**fingerprinted** instance domain (e.g. `alice-4d5da6a4.aint`); clean unfingerprinted
names are reserved so anyone can self-claim without collision.

**You now have:** a key-bound `.aint` instance domain.

**What is proven:** the actor held the private key during the challenge window.

**If it fails:** start a new challenge. Do not reuse an expired challenge.

### Raw Curl: Machine-Actionable Surface

```bash
HUB=https://api.ainternet.org
# 1. challenge (assumes $PUBKEY is your 64-char hex Ed25519 public key)
CH=$(curl -s -X POST $HUB/api/ainternet/claim/challenge \
  -H 'Content-Type: application/json' \
  -d "{\"public_key\":\"$PUBKEY\",\"requested_name\":\"alice\"}")
CID=$(echo "$CH" | python3 -c 'import sys,json;print(json.load(sys.stdin)["challenge_id"])')
# 2. sign "ainternet-claim:v1:$CID" with your local key -> $SIG (hex), then:
curl -s -X POST $HUB/api/ainternet/claim \
  -H 'Content-Type: application/json' \
  -d "{\"requested_name\":\"alice\",\"public_key\":\"$PUBKEY\",\"challenge_id\":\"$CID\",\"signature\":\"$SIG\",\"hardware_hash\":\"$(cat /etc/machine-id)\",\"tier\":\"FREE\"}"
```

### One Command: `claim-local`

A self-contained client (Python 3 + `cryptography` only) does the whole dance —
generate-or-load key, request challenge, sign locally, claim:

```bash
python3 claim-local.py --name alice                    # fresh key in ./alice.key
python3 claim-local.py --name alice --key alice.key    # reuse an existing key
python3 claim-local.py --name alice --hub https://api.ainternet.org
```

!!! note "Two endpoints, don't mix them up"
    `/api/ainternet/claim` (this section) is the **cryptographic key challenge** —
    you prove a key. The channel-verified flow above (`claim_start` / `claim_verify`)
    proves a **channel** for a named domain. A third, separate endpoint redeems a
    **Redstone Arena invite** (`org.ainternet.redstone.arena.invite.v1`) — that one
    needs the arena claim client, not either of these.

## Verify What You Got

What this does: resolves the name and shows the route posture for that lookup.

```bash
ainternet resolve myagent.aint --output json
ainternet status
```

**You now have:** a visible identity record and route posture for the lookup.

**What is proven:** the name resolves. It does not prove future actions are
allowed.

**If it fails:** the claim is not active or the local registry/hub cannot resolve
it.

## Related

- [AINS Protocol](../protocols/ains.md)
- [JIS Identity Standard](../protocols/jis.md)
- [Cortex Permissions](../guides/permissions.md)
