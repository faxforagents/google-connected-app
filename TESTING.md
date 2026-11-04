# Testing the Google connection

The package validator runs without network access or credentials.
Inspector and Gemini instructions below are for an authorized operator. They were not executed while building this package.
See [REQUIREMENTS.md](REQUIREMENTS.md) for source quotations and field requirements.

## Local package checks

```bash
sh scripts/validate.sh
```

Python 3 is the only runtime dependency.
The script rejects duplicate JSON keys, invalid worksheet fields, unsuitable listing copy, missing scenarios and an invalid icon.
It does not contact Google or transmit a fax.

## Public discovery

These GET requests need no credentials:

```bash
curl --silent --show-error --fail-with-body \
  https://mcp.faxforagents.com/.well-known/oauth-protected-resource
curl --silent --show-error --fail-with-body \
  https://mcp.faxforagents.com/.well-known/oauth-protected-resource/mcp
curl --silent --show-error --fail-with-body \
  https://api.faxforagents.com/.well-known/oauth-authorization-server
```

Check the resource equals `https://mcp.faxforagents.com/mcp` and the authorization server equals `https://api.faxforagents.com`.
Confirm authorization, token and registration URLs match `listing.json`.
Check `response_types_supported` includes `code` and `code_challenge_methods_supported` includes `S256`.
Check CIMD support and the advertised authorization-code and refresh grants.
On 2026-11-04, all three documents returned HTTP 200 and advertised these values.
No registration request or token exchange was performed.

## Inspector

Google's [MCP guide](https://developers.google.com/connected-apps/mcp) prescribes Inspector validation.
The [Inspector guide](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector) requires Node 22.19.0 or newer.
Use the current Inspector release and its [memory secret store](https://github.com/modelcontextprotocol/inspector/blob/main/docs/secret-storage.md).

```bash
MCP_INSPECTOR_SECRET_STORE=memory MCP_INSPECTOR_PERSIST_TOKENS=none \
  npx @modelcontextprotocol/inspector
```

1. Confirm Inspector reports memory secret storage before authenticating.
2. Add a server with Streamable HTTP transport and URL `https://mcp.faxforagents.com/mcp`.
   Use OAuth and a dedicated Sandbox account. Do not enter a bearer key as a saved header.
3. Inspect discovery and the OAuth flow. Confirm S256 and exact registered redirect matching.
   Verify CIMD where the client supports it and DCR in a separate session.
4. Initialize the connection and list tools. Compare all 15 names with `listing.json`.
   Inspect server instructions, argument types, required properties, descriptions and safety annotations.
5. Invoke `get_guide` and `get_fax_capabilities` first. Confirm the account environment is test.
   Run the applicable Sandbox cases in `review-cases.json` and inspect input/output payloads.
6. Check refresh and revocation using the dedicated review account.
   Confirm a revoked connection cannot read faxes until the operator grants new consent.
7. Close Inspector when finished. Store only redacted outcomes, not tokens, headers, private documents or raw authenticated telemetry.

This repository has no MCP server implementation to run locally.
For Google's local-server phase, use the service's own checkout and documented launch command, then repeat Inspector checks against that endpoint.
No local server command is invented here.

## Gemini Developer Mode

These steps follow Google's [Developer Mode usage guide](https://developers.google.com/connected-apps/mcp/dev-mode/usage).

1. Sign in to Gemini and open Settings, Gemini Apps Developer Mode, or visit `https://gemini.google.com/devmode`.
2. In Choose an app, select the registered Fax for Agents app if present.
   For a direct endpoint test, select + Create new.
3. In Connect to an MCP server, enter `https://mcp.faxforagents.com/mcp` in MCP Server URL and select Next.
   Additional settings, Show more contains pre-registered client credentials if a separately configured fallback requires them.
4. Read the security and privacy confirmation. Accept it only for the intended service, then select Connect.
5. Complete the account's authorization flow with Sandbox access.
   In Save your custom app, enter Fax for Agents, verify Available actions and select Connect.
6. Open Tool Schemas and confirm all 15 tools, their parameters and safety badges.
   In Authentication, choose Dynamic Client Registration for the DCR test. Select Save and wait for Saved.
7. Run every listing prompt and all eight review cases in the chat pane.
   Check Event Log for each request, response and error. Use the case expectations as pass criteria.
8. Check that sends and cancellation show the expected confirmation behavior.
   Reject a confirmation once and verify no action executes.
   Test sends only in Sandbox and only after the service's approval requirements are satisfied.
9. Test a different simulated date, time and language through Environment, then select Reset.
   This is a diagnostic check, not a claim of translated product support.
10. After a server schema change, select Sync schema in Tool Schemas and rerun the affected prompts.
    Re-sync tools in Connected Console separately before review. Developer Mode refresh does not establish a new published snapshot.

If Developer Mode or the app is unavailable, record that outcome and resolve access with Google.
Do not describe setup steps as completed tests.

## Registered preview and review

Follow [Google's registration guide](https://developers.google.com/connected-apps/gpc/perform-the-steps), steps 5 to 9.

1. Complete domain verification and OAuth setup from README.md.
   Copy all exact app-specific redirect URIs from the console and allowlist them before authentication.
2. Sync tools with an account allowed to access all intended tools. Resolve blocking console errors.
3. Confirm category fit, choose countries, and confirm the available language and product selections.
   Keep additional locale and location context disabled unless a tool demonstrably needs it.
4. Apply `tool_settings` from the worksheet, retaining stricter server confirmation annotations. Save.
5. In Test your app, select Add testers, then create or select a Gmail email list and select Save.
   Include the operator's account. Allow up to ten minutes for visibility.
6. In Gemini, type `@` and select Fax for Agents, or open Settings & help, Connected apps.
   Connect and run the cases with both explicit mentions and natural language.
7. Provide Google's representative with dedicated seeded reviewer access through a private channel.
   Disable 2FA on that test account. Include synthetic completed and inbound faxes plus these testing instructions.
8. Record each case as passed, failed or blocked after execution. Retain the date, client version and redacted evidence in private review records.
   Keep the shipped checklist's `not_run` values until real evidence exists.
9. After the cases pass, submit through Send for review. Publish after approval when the operator is ready.

The Live bypass scenario must not produce a live transmission.
Use a controlled account without a Live grant or allowed policy. Stop and mark it blocked if isolation cannot be established.
The synthetic malicious fax is test data. Its instructions must never authorize another tool action.
