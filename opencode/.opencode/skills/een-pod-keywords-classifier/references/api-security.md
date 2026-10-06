# Partner Web Service security

## Secrets

Use `EEN_API_KEY` as the runtime environment variable for the organisation API key.

Never:
- hard-code the key;
- commit it;
- echo it;
- include it in exception output;
- put it in a prompt/reference file;
- write it to synchronisation JSON/CSV files.

## Network access

Access also depends on IP whitelisting.

Treat HTTP 401/403 as an access/authentication/whitelisting issue. Do not retry aggressively and do not propose bypass techniques.

## Logging

Log only endpoint path, non-secret filter parameters, HTTP status, item/page counts and timestamps.

Do not log request headers containing `X-API-KEY`.

## Data handling

An authenticated organisation may receive non-public profile data that it is entitled to access.

Do not automatically republish private/non-published profile content. Distinguish:
- analysis for the authorised user;
- public-profile content;
- data that should remain internal.

The presence of an API field is not permission to make it public.
