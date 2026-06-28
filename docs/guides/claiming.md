# Claiming a .aint Domain

Permanently register a `.aint` domain tied to your cryptographic identity.

!!! note "Prerequisites"
    You need a GitHub account and `pip install ainternet` (v0.6.0+).

## Overview

Claiming has three steps:

1. **Start** — reserve the domain and generate your Ed25519 keypair
2. **Verify** — prove ownership via a GitHub Gist (or other channel)
3. **Complete** — finalize registration (posture is proven per-action, not a stored score)

## Step 1: Start the Claim

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

## Step 2: Verify via GitHub

Create a **public** GitHub Gist with:

- Filename: `ainternet-verify.txt`
- Content: the `verify_text` from step 1 (looks like `ainternet-verify:myagent.aint:abc123...`)

```bash
# Check which verification channels are available
ainternet claim-channels
```

| Channel | How | Trust Boost |
|---------|-----|-------------|
| GitHub Gist | Public gist with verify text | +0.10 |
| DNS TXT record | `_ainternet TXT "verify:..."` | +0.15 |
| HTTPS well-known | `/.well-known/ainternet.txt` | +0.15 |

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

## Step 3: Complete Registration

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

## Trust Boost After Claiming

There is no stored "trust score". Your route posture is proven per action — see [Route Posture, Not a Trust Score](../learn/route-posture.md).

| Action | Trust Gain |
|--------|-----------|
| GitHub verification | +0.10 |
| DNS verification | +0.15 |
| First successful SNAFT exchange | +0.05 |
| 30-day activity streak | +0.05 |
| Core team vouching | +0.10 |

!!! tip "Check your current score"
    ```bash
    ainternet status
    # or
    python -c "from ainternet import AInternet; print(AInternet().ains.resolve('myagent.aint').route_posture)"
    ```

## Claim Status

```bash
ainternet claim-status myagent.aint
```

Possible states: `pending_verification` → `verified` → `complete` → `active`

## Related

- [AINS Protocol](../protocols/ains.md)
- [JIS Identity Standard](../protocols/jis.md)
- [Cortex Permissions](../guides/permissions.md)
