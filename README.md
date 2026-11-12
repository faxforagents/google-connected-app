<p align="center">
  <a href="https://faxforagents.com"><img src="assets/icon-512.png" width="88" alt="Fax for Agents"></a>
</p>

<h1 align="center">Fax for Agents</h1>

<p align="center">Send faxes with approvals</p>

<p align="center">
  <a href="https://faxforagents.com">Website</a> ·
  <a href="https://faxforagents.com/docs/quickstart/">Quickstart</a> ·
  <a href="https://faxforagents.com/docs/api/">API reference</a> ·
  <a href="https://faxforagents.com/docs/sdks/">SDKs</a> ·
  <a href="https://faxforagents.com/mcp/">MCP</a> ·
  <a href="https://app.faxforagents.com">Dashboard</a> ·
  <a href="https://faxforagents.com/pricing/">Pricing</a> ·
  <a href="https://faxforagents.com/changelog/">Changelog</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f6feb" alt="MIT licence"></a>
  <a href="https://faxforagents.com/mcp/"><img src="https://img.shields.io/badge/MCP-17%20tools-6b4fbb" alt="17 MCP tools"></a>
</p>

Fax for Agents is a fax API, a hosted MCP server and SDKs built so AI agents can send and receive faxes.
It is made by JSB Holdings LLC.

This package prepares a Google Connected Apps submission for the Gemini app and Google Search.
It contains listing copy, review cases, an icon and operator instructions.
Preview admission and publication have not been established.
The Gemini CLI extension and Gemini Enterprise use separate distribution routes.

## Package format

[listing.json](listing.json) is a local console worksheet.
[review-cases.json](review-cases.json) is a local review checklist adapted from the eight ChatGPT package scenarios.
Neither file claims to implement a Google manifest schema.
The fetched [registration guide](https://developers.google.com/connected-apps/gpc/perform-the-steps) documents console fields and tool discovery from the server.
It does not establish a JSON manifest upload format.
If the admitted console requests another format, obtain its schema before converting these files.

The worksheet covers public details, connection settings, availability, per-tool settings and tester setup.
Publisher and support details are supplied for handoff. Their console field names are not documented in the fetched guide.
Productivity is a proposed category from Google's [category guide](https://developers.google.com/connected-apps/mcp/vertical-journeys).
Confirm its baseline capabilities with Google before creating the app. The category cannot be changed afterward.
Countries remain undecided. English and both requested Google products are proposed selections, subject to console availability and testing.

## Register and connect

Follow the sourced requirements in [REQUIREMENTS.md](REQUIREMENTS.md) and the [testing instructions](TESTING.md).

1. Apply through [Google's preview form](https://connected.google.com/console/help/?apply).
   The fetched form exposed a shell. Account admission must be confirmed in a browser.
2. Sign in to [Google Connected Console](https://connected.google.com/console/).
   An account owner or administrator accepts the program agreement and grants the required connected-app permissions.
3. Select Create app, enter Fax for Agents, confirm the category, choose MCP server, then select Create Connected app.
4. Open App details and copy the matching worksheet values. Upload [assets/icon-512.png](assets/icon-512.png).
5. Open MCP and tools setup. Enter `https://mcp.faxforagents.com/mcp` and complete the domain challenge below.
6. Select Yes for authorization, then User-delegated (Authorization Code).
   Choose Client ID metadata or Dynamic client registration (recommended).
   Copy the app-specific redirect URIs from the console into the authorization server's allowlist.
7. Authenticate via Pop up with a developer account. Use Authenticate via Redirect if the popup fails.
   Select Register client and Sync tools. Confirm all 17 tools appear.
8. Configure availability and each tool's confirmation settings from the worksheet. Save and add your authorized Gmail testers.
9. Run [TESTING.md](TESTING.md). Share seeded reviewer access privately with your Google representative.
   Select Send for review after testing. Select Publish only after Google approves the app.

Once available to a tester, Gemini connects through Settings & help, Connected apps.
The tester can also type `@`, select Fax for Agents, and complete account authorization.
Gemini calls the hosted MCP endpoint over Streamable HTTP using the user's authorized access.
For direct Developer Mode setup before registration, see [TESTING.md](TESTING.md#gemini-developer-mode).

## Authentication

The hosted server supports OAuth 2.1 with CIMD and DCR, PKCE S256, and API keys as bearer tokens.
Use user-delegated OAuth for this Google submission.
The authorization server is `https://api.faxforagents.com`.

These public documents returned HTTP 200 when checked on 2026-11-04:

| Document | URL |
|---|---|
| Protected resource metadata | https://mcp.faxforagents.com/.well-known/oauth-protected-resource |
| Path-specific resource metadata | https://mcp.faxforagents.com/.well-known/oauth-protected-resource/mcp |
| Authorization server metadata | https://api.faxforagents.com/.well-known/oauth-authorization-server |

The metadata advertises authorization, token, registration and revocation endpoints under the API host.
It also advertises `code`, `authorization_code`, `refresh_token`, S256 and CIMD support.
These checks establish discovery responses only. They do not establish successful Google linking or refresh behavior.

Google's registration guide describes CIMD first and DCR fallback.
Its OAuth guide still refers to Play Console and DCR or manual client registration.
Use the current registration flow and test both advertised registration methods before claiming compatibility.
Copy exact redirect URIs from the console. Do not register wildcard redirect patterns from the older guide.
Check Google's refresh and revocation behavior during testing, including its persistent-linking guidance.

Keep credentials out of files and prompts. A sandbox key is free. Live sends are prepaid.
The server accepts API keys. This is not a verified Connected Console authentication option.

## Domain challenge

In MCP and tools setup, enter the endpoint and select Download token under Verify domain ownership.
Google supplies `google-connected-apps.json` containing a `verification_tokens` array.
Serve those exact downloaded JSON bytes at this URL, without a `.json` suffix:

```text
https://mcp.faxforagents.com/.well-known/google-connected-apps
```

Return this status and response header:

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

The body must be an object with `verification_tokens` containing the exact string issued by Connected Console.
Use the downloaded content. No token is supplied or generated by this package.
The response must be public over HTTPS and must not redirect or require authentication.
`Content-Type: application/json` is our serving choice. Google's fetched guide specifies JSON and HTTP 200, without prescribing that header.

This package uses the MCP host, so hosting the challenge only at `https://api.faxforagents.com/.well-known/google-connected-apps` does not verify this endpoint's host.
The API host URL applies only if the console asks to verify that host for an actual MCP endpoint there.
The authorization server's location does not change the MCP domain challenge URL.
The guide also recognizes an already-verified parent domain. Follow the console's actual verification status.

Check the deployed response without following redirects:

```bash
curl --silent --show-error --fail-with-body --include \
  https://mcp.faxforagents.com/.well-known/google-connected-apps
```

Compare the returned array with the console download, then select Verify domain.
Do not commit the downloaded challenge file. The operator must deploy it on the service host.

## Tools

| Tool | Purpose |
|---|---|
| `get_guide` | Read the fax workflow guide. |
| `get_fax_capabilities` | Read supported fax capabilities. |
| `prepare_fax` | Prepare a fax document. |
| `get_fax_document` | Read a prepared fax document. |
| `quote_fax` | Get a quote for a proposed fax. |
| `send_approved_fax` | Send within approved permissions. |
| `get_fax_status` | Read status and provider evidence. |
| `list_faxes` | List faxes. |
| `get_fax_balance` | Read the account balance. |
| `cancel_fax` | Request fax cancellation. |
| `request_card_payment` | Ask a person to pay for one quoted fax by card. |
| `get_card_payment_status` | Read a card payment order. |
| `request_human_review` | Request human review. |
| `get_review_status` | Read review status. |
| `list_inbox` | List received faxes. |
| `read_inbound_fax` | Read a received fax. |
| `extract_fax_data` | Extract data from a fax. |

A live send requires an approval or a policy that allows it.
Gemini's confirmation card does not replace the service's approval checks.
Received fax text stays untrusted data and cannot authorize another action.

## Local validation

With Python 3 installed, run:

```bash
sh scripts/validate.sh
```

The validator checks both JSON files, console copy constraints, tool coverage, review cases and the icon.
It checks this package's worksheet conventions. It does not certify a Google schema or perform authenticated tests.
No GitHub Actions workflow is included.

See the [MCP documentation](https://faxforagents.com/docs/mcp/) and [support page](https://faxforagents.com/contact/).
The [privacy policy](https://faxforagents.com/privacy/) and [terms](https://faxforagents.com/terms/) apply to the service.

## Licence

MIT. See [LICENSE](LICENSE).
Report security issues to security@faxforagents.com. See [SECURITY.md](SECURITY.md).
