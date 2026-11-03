# Getting a Meta access token

AdSonar uses Meta's **official** Ad Library API, so every user needs their own Meta developer
access. This takes about 15 minutes of work, plus up to 48 hours for identity confirmation.

## 1. Confirm your identity
Go to <https://www.facebook.com/ID> and follow the steps (government-issued ID required).
Meta needs to approve this before the Ad Library API will accept your token.

## 2. Create a developer app
1. Open <https://developers.facebook.com/apps> and click **Create app**.
2. Choose the **Other** use case, then the **Business** app type.
3. Give it any name (e.g. "My AdSonar"), and finish creation.

## 3. Accept the Ad Library API terms
Visit <https://www.facebook.com/ads/library/api> and click **Get started**. Accept the terms when prompted.

## 4. Generate a token
1. Open the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. Select your app in **Meta App**.
3. Click **Generate Access Token** and log in.
4. Copy the token.

This token expires after about an hour. To get a ~60-day token:
1. Paste it into the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/).
2. Click **Debug**, then **Extend Access Token** at the bottom.
3. Copy the new long-lived token.

## 5. Save it
```bash
cp .env.example .env
```
Then put the token in `.env`:
```
META_ACCESS_TOKEN=EAAB...
```

## 6. Check it works
```bash
adsonar -q "coffee" -c GB -n 5 -o output/check.json
```

## Common errors

| Message | Cause | Fix |
|---------|-------|-----|
| `code=190` Invalid OAuth access token | Token expired or mistyped | Generate a new token (step 4) |
| `code=10` / `code=200` permission error | Identity not confirmed or API terms not accepted | Complete steps 1 and 3, then make a new token |
| `code=100` invalid parameter | A filter value is wrong (e.g. bad country code or field) | Check the option values in `adsonar --help` |
| `code=613` / `code=4` rate limit | Too many calls | AdSonar retries automatically; for big jobs, lower `--max-items` or run later |
| 0 ads returned for a commercial search | Meta only returns non-political ads delivered in the EU/UK | Use EU countries or `GB` with `-c` |
