# Installation Catalog Maintenance

Runtime catalog: `www/installations.js`

Current catalog version: `2026.09.08`

## Design

Each installation has a stable `id`, display `name`, `hostCommand`, optional command associations, state/region, country, aliases, and active/component flags.

The New Class form filters on the `commands` array, not the display name. This allows known tenant relationships such as:

- Dyess: AFGSC host + AMC relationship
- JB Pearl Harbor-Hickam: PACAF host + AMC relationship
- Ramstein: USAFE-AFAFRICA host + AMC relationship
- Kadena: PACAF host + AFSOC relationship
- RAF Mildenhall: USAFE-AFAFRICA host + AFSOC relationship

## Update rules

1. **Never change an existing stable ID merely because a base display name changes.** Change `name` and preserve the former name in `aliases`.
2. Add a new ID only for a genuinely distinct installation/location.
3. Mark a closed/deactivated location `active: false` instead of deleting historical IDs if old records may still contain them.
4. Update `catalogVersion` and `lastVerified` whenever the command mapping changes.
5. Run `npm run validate` before committing.
6. For command reassignment, update both `hostCommand` and `commands` when appropriate.

## Current-source baseline checked 8 Sep 2026

- PACAF official Units / Bases page
- ACC/AETC official reassignment announcements for Holloman (4 Jun 2026) and Luke (17 Jul 2026)
- AMC current fact sheet
- AFGSC current Units / 2026 fact sheet
- AFMC current host-base fact sheet
- USAFE-AFAFRICA current fact sheet
- AFSOC current unit/heritage information

This catalog is a software-maintenance dataset, not an authoritative personnel-assignment source. Verify future organizational changes against current official DAF sources before editing.
