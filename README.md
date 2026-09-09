# TCCC Evaluation Suite — Android / APK

**Release:** v2.21.0  
**Android versionCode:** 22100  
**Role:** Offline field evaluation + local readiness/performance-improvement management

v2.21.0 is the merged baseline that combines the v2.20.0 RCA/performance-intelligence work with the MAJCOM/base data-management capabilities found in the uploaded v2.19.3 APK.

## What v2.21.0 does

### 1. Field evaluation
- Tier 1–4 TCCC evaluator with PASS / FAIL / NT / N/O.
- Critical failures override percentage performance.
- Field Mode minimizes cognitive load; Review Mode exposes documentation/provenance.
- Critical FAIL requires structured failure mode + primary contributor.
- Noncritical FAIL remains fast and can be classified later.
- A2 is remediation-only after a finalized A1 FAIL and captures remediation reason/action.
- Next Unresolved, timer recovery, NT justification, touch-target, modal, CSV, PDF, and finalization safeguards remain in place.

### 2. Structured location management
New/edit class captures:
- supported MAJCOM / command,
- home installation,
- unit / organization,
- local site code,
- training location (same as home, another installation, or custom expeditionary location),
- exercise / event,
- course type,
- scenario/version/difficulty/profile,
- lead evaluator and evaluator ID.

The installation selector uses stable IDs from `www/installations.js`. Installation `hostCommand` is kept separate from the class's supported/operational MAJCOM so tenant/joint relationships are not lost.

Legacy classes that only contain a free-text location are migrated where possible using catalog names/aliases; otherwise the original location is retained as custom data.

### 3. Program Management Intelligence
The home dashboard can scope all locally stored classes by:
- MAJCOM / command,
- home installation,
- tier,
- course type.

It reports:
- classes and students,
- first-attempt qualification,
- final qualification,
- remediation rate,
- remediation success,
- critical-failure rate,
- RCA classification completeness,
- MAJCOM summaries,
- installation summaries,
- highest normalized competency gaps,
- primary root causes,
- location/RCA data-quality gaps.

Criterion gaps use `FAIL / (PASS + FAIL)` rather than raw miss count.

### 4. Downstream data exports
- Existing individual and class exports retain RCA/remediation details and now carry structured location metadata.
- **Management Summary CSV** provides aggregate MAJCOM/base metrics for the current local scope.
- **Enterprise Detail CSV** uses `TCCC_ANALYTICS_2.0` and combines location, scenario, remediation, RCA, and criterion-level performance fields.
- Cross-class Enterprise Detail excludes student names; local student ID and optional training ID are included for downstream linkage. Evaluator-entered free-text fields still require appropriate data governance.

## Installation catalog
`www/installations.js` currently contains **73 active-duty installation records** and **11 command categories**, including multi-command relationships for tenant/joint use cases. The catalog has its own version/date so future display-name or command-relationship updates can be managed without fragmenting historical analytics.

## Architecture boundary
This APK is **not** the DAF enterprise system of record. v2.21.0 intentionally stops at offline collection, local class/program management, and export-ready structured data.

The planned DAF backend should own:
- authoritative identities and RBAC,
- synchronization,
- central storage/retention,
- server-side integrity,
- cross-device longitudinal records,
- MAJCOM/DAF enterprise dashboards,
- evaluator inter-rater reliability/calibration analytics.

## Build test APK
1. Put the contents of this repository at the root of the APK GitHub repository.
2. Open **Actions**.
3. Run **Build TCCC Test APK**.
4. Download `TCCC-v2.21.0-test.apk` from the workflow artifact.

The workflow validates the source tree, TCCC criteria, installation catalog, Android branding resources, hardening, and version before Gradle builds.

## Signed release
Use **Build TCCC Release APK** after the repository signing secrets are configured. Do not commit a keystore or passwords.

## Repository layout
- `.github/workflows/` — TEST and signed RELEASE APK workflows
- `www/` — evaluator, analytics, TCCC content, installation catalog, branding
- `native-android-res/` — controlled launcher/splash resources
- `scripts/` — content/release validation and Android preparation/hardening
- `COMPARISON_2.20.0_vs_UPLOADED_2.19.3.md` — exact merge basis
- `CHANGELOG-v2.21.0.md` — release changes

## Clinical/content note
The Tier 1–4 `tiers.js` data in the uploaded v2.19.3 APK and the v2.20.0 baseline was byte-for-byte identical and is preserved. The approved tourniquet-conversion criterion remains **“Wound could be closely monitored.”**

**Contact: John Garcia**
