# Security

## Protecting your access token
- Keep `META_ACCESS_TOKEN` in a `.env` file or your shell environment. `.env` is git-ignored; never commit it.
- Don't share your token with other people or customers. Every user needs their own Meta developer account and token.
- If a token leaks, revoke it in the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/) and generate a new one.

## Reporting a vulnerability
Email vijay.singh@expeditets.com with details. Please don't open a public issue.
