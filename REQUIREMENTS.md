# Verified platform requirements

Checked on 2026-11-04 against the public pages linked below.
Quoted excerpts retain the source wording. The accompanying descriptions explain how this package applies them.
Google documents are attributed to Google and published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
This worksheet is not a Google schema or a claim of approval.

## Preview and account access

Source: [Connected Apps Platform](https://developers.google.com/connected-apps).

> Developers interested in joining can apply for preview.

Apply through the linked preview form before assuming access or a launch date.
The unauthenticated form fetch returned a shell, without usable application fields.

Source: [Console prerequisites](https://developers.google.com/connected-apps/gpc/prerequisites).

> Each connected app supports a single global MCP server endpoint.

Use a public HTTPS endpoint with Streamable HTTP.
An admitted developer account needs connected-app permissions and owner or administrator acceptance of the program agreement.
If the service restricts source IPs, maintain Google's documented fetcher and agent allowlists.
Use the current lists linked from the prerequisites page.

## Public details

Source: [Console prerequisites](https://developers.google.com/connected-apps/gpc/prerequisites), public-facing metadata section.
Source: [Registration guide](https://developers.google.com/connected-apps/gpc/perform-the-steps), steps 1 and 2.

> Include only a single capability per entry.

| Console input | Verified constraint | Worksheet value |
|---|---|---|
| Connected app name | Display name used for mentions | Fax for Agents |
| Description | One sentence with fewer than 30 words | `app_details.description`, 16 words |
| Icon | JPEG or PNG, 512 by 512 pixels, at most 1,024 KB | `assets/icon-512.png` |
| Capabilities | At least three added tasks, no numbered prefixes, one capability per entry | Six entries in `app_details.capabilities` |
| Example prompts | At least three, two starting with the app mention, one mentioning the name later | Three entries in `app_details.example_prompts` |
| Prompt formatting | No numbered prefixes or outer quotation marks in console text | Copy JSON string values without JSON quotation marks |
| Terms of Service URL | Public HTTP or HTTPS URL | `app_details.terms_of_service_url` |
| Policy URL | Public privacy-policy HTTP or HTTPS URL | `app_details.privacy_policy_url` |
| Website URL | Optional attribution link | `app_details.website_url` |
| Category | Selected at creation, defines baseline capabilities, cannot be changed later | Proposed Productivity, pending operator confirmation |
| Connection type | One selection per app, permanent after creation | MCP server |
| Localization | Optional language-tagged values for translated text | English copy only, no translation claims |

No additional icon dimensions were prescribed on these fetched pages.
Publisher and support values are supplied at the user's request. The public field guide does not identify dedicated controls for them.

## Category fit

Source: [Recommended user journeys by category](https://developers.google.com/connected-apps/mcp/vertical-journeys).

> For: task and project managers, notes and knowledge bases, cloud storage, meeting-notes tools

That description belongs to Productivity. It does not establish fax-service eligibility or list every console option.
The operator must confirm the category and its baseline capabilities with Google before creating the app.
Do not claim the fax service implements unrelated task-management or storage journeys.

## Domain and authentication

Source: [Registration guide](https://developers.google.com/connected-apps/gpc/perform-the-steps), steps 3 and 4.
Source: [Troubleshooting](https://developers.google.com/connected-apps/gpc/troubleshooting), domain verification and client registration entries.

> without a `.json` extension in the URL path

Serve the console's downloaded JSON directly at the MCP domain's `/.well-known/google-connected-apps` path.
It must return HTTP 200 over public HTTPS, without redirects, with the issued string inside `verification_tokens`.
See [README.md](README.md#domain-challenge) for the exact host, response header choice and body handling.

Select user-delegated authorization and CIMD or DCR registration.
Google checks CIMD first and falls back to DCR.
Copy all six exact app-specific redirect URIs from the console and allowlist them on the authorization server.
Authenticate the developer account before syncing tools. Use redirect authentication if popup authentication fails.
Pre-registered client credentials and custom authorization/token endpoint controls exist as conditional alternatives.
The worksheet leaves custom endpoint overrides unset because discovery is available.

Source: [OAuth implementation guide](https://developers.google.com/connected-apps/mcp/oauth).

> PKCE is mandatory for all OAuth 2.1 and optional for OAuth2.0.

Validate discovery and `code` response support.
Check authorization and token URLs, DCR, S256, declared scopes and refresh grants.
The guide still references Play Console. The newer registration guide explicitly describes CIMD support.
The OAuth guide's refresh section calls for preserving refresh tokens for persistent linking.
Test refresh and revocation against the service before claiming compatibility. Do not infer them from metadata alone.

## Tools, testing and release

Source: [MCP developer guide](https://developers.google.com/connected-apps/mcp).

> Connect to the local server using the MCP Inspector tool (`npx @modelcontextprotocol/inspector`).

The guide recommends explicit server instructions, typed schemas and safety annotations.
It prescribes Inspector validation, public hosting and Gemini Developer Mode verification before publication.
This package connects to an existing hosted service. Server-local validation belongs with that service's source checkout.
The authenticated checks in [TESTING.md](TESTING.md) remain unrun.

Source: [Registration guide](https://developers.google.com/connected-apps/gpc/perform-the-steps), steps 5 to 9.

Configure countries, languages and Google products after tool sync.
Each tool has an enable control, optional locale or location context, and a user-confirmation control.
Google preselects confirmation for `destructiveHint: true`.
The worksheet requests no contextual signals and proposes confirmations for sending, cancellation and human-review requests.
Keep stricter synced annotations. These selections do not replace backend authorization.

Provide a dedicated seeded reviewer account privately to Google's representative, with synthetic sample data, testing instructions and 2FA disabled.
Add Gmail testers, including the operator, through Manage testers. Visibility can take ten minutes.
Test prompts, account linking, tool execution and confirmation behavior before review.
Submit through Send for review. Approval enables Publish.
The published tool snapshot requires a new version for subsequent updates.

## Developer Mode and Inspector

Source: [Developer Mode overview](https://developers.google.com/connected-apps/mcp/dev-mode).

> Authentication: Configures how Gemini establishes client and user credentials with your MCP server under Dynamic Client Registration.

Source: [Developer Mode usage](https://developers.google.com/connected-apps/mcp/dev-mode/usage).

> In the Choose an app dialog, click + Create new.

Use the registered app or enter the HTTPS endpoint as a custom MCP app.
Inspect Tool Schemas and Event Log. Use Sync schema after server changes.
The Authentication tab supports DCR and manual client registration.
See [TESTING.md](TESTING.md#gemini-developer-mode) for the complete sequence.

Source: [MCP Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector).

> The Inspector requires Node 22.19.0 or newer and runs directly through `npx`.

Source: [Inspector secret storage](https://github.com/modelcontextprotocol/inspector/blob/main/docs/secret-storage.md).

> Don't write secrets to disk at all: `MCP_INSPECTOR_SECRET_STORE=memory`, and re-enter them each session.

The documented Inspector command in TESTING.md selects memory storage and disables token persistence.
Do not save authorization headers or raw authenticated traces to package files.

## Format boundary

The [console overview](https://developers.google.com/connected-apps/gpc) and registration guide describe form entry and server tool discovery.
No uploadable Google manifest schema was verified.
The files named `listing.json` and `review-cases.json` use local preparation structures.
Their validation cannot establish platform acceptance.
