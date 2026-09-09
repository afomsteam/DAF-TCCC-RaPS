# TCCC Evaluation Suite v2.21.0 — Validation Report

Validation performed before packaging the complete GitHub repository.

## Passed checks

- JavaScript syntax: `app.js`, `tiers.js`, `branding.js`, `installations.js`, `version.js`, Android preparation/hardening scripts.
- Tier content validator:
  - Tier 1: 33 criteria / 17 critical / 2 timers
  - Tier 2: 71 / 16 / 2
  - Tier 3: 124 / 28 / 7
  - Tier 4: 124 / 30 / 9
- Release hardening suite: **55/55 checks passed**.
- Installation catalog: **73 unique installation IDs / 11 command categories**; command references and multi-command relationships validated.
- `tiers.js` SHA-256 is identical across uploaded v2.19.3, v2.20.0 baseline, and v2.21.0.
- GitHub Actions YAML parsed successfully.
- Workflow preflight paths verified, including `www/installations.js`, native Android branding, and Android hardening scripts.
- Static HTML local resource references resolve.
- No program email address, `mailto:`, `tel:`, or prior phone-number string remains in the application bundle.
- Native branding script executed against a generated-like Android resource tree.
- Android hardening script executed against representative Gradle/manifest files and produced:
  - `versionName "2.21.0"`
  - `versionCode 22100`
  - `android:allowBackup="false"`
  - `android:usesCleartextTraffic="false"`
  - INTERNET permission removed.

## Data-model smoke test

A synthetic legacy class containing only the free-text location `Hickam AFB` was loaded through the v2.21.0 migration path. The app:

- mapped the location to `Joint Base Pearl Harbor-Hickam (Hickam)`,
- inferred PACAF as the supported command,
- rendered the PACAF and installation management rows,
- calculated 0% first-pass and 100% final qualification after A2 remediation,
- rendered 100% remediation success,
- aggregated the structured `Cue recognition` RCA contributor, and
- reported complete location/RCA data quality for the synthetic record.

## Browser/Android build boundary

A full GitHub-hosted Gradle APK build was not reproduced in this container because the GitHub runner/toolchain environment is external. The repository therefore includes CI preflight checks that explicitly verify every required source/branding file before Capacitor/Gradle execution. The source-side Android preparation, branding, hardening, and version-patching paths were executed locally against a representative generated Android tree.
