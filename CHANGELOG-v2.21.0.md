# TCCC Evaluation Suite v2.21.0

## Management + RCA integration release

v2.21.0 merges the strongest capabilities of the uploaded v2.19.3 APK and the v2.20.0 performance-intelligence baseline.

### Added
- Offline active-duty installation catalog with stable installation IDs.
- Supported MAJCOM/command selector that filters home-installation choices.
- Show-all option for tenant/joint relationships.
- Structured home installation, unit, training location, exercise/event, and site-code metadata.
- Legacy free-text location migration using installation names/aliases when possible.
- Local Program Management Intelligence dashboard across all classes on the device.
- Scope filters: MAJCOM, home installation, tier, and course type.
- MAJCOM summary and installation summary tables.
- Cross-class first-pass, final-pass, remediation, critical-failure, and RCA completeness metrics.
- Cross-class normalized criterion-gap analysis.
- Cross-class structured RCA distribution.
- Data-quality panel for missing MAJCOM, missing installation, custom locations, and unclassified failures.
- Management Summary CSV.
- Enterprise Detail CSV using `TCCC_ANALYTICS_2.0`.
- Class-level Enterprise Detail CSV.
- Installation catalog version in enterprise exports.

### Preserved from v2.20.0
- Structured failure mode / primary contributor RCA.
- Required RCA classification for critical FAIL.
- One-tap noncritical FAIL with review-later classification.
- Field Mode / Review Mode.
- First-attempt vs final qualification analytics.
- Remediation reason/action and remediation-success analysis.
- Normalized criterion failure rates and scenario-coverage analysis.
- Student heat map without a leaderboard.
- Descriptive evaluator signals.
- Roster search/filters.
- Critical task, timer, NT, A2, finalization, modal, Next Unresolved, and export hardening.
- Approved tourniquet-conversion wording: **Wound could be closely monitored.**

### Preserved from uploaded v2.19.3
- MAJCOM/base relationship model.
- Home vs training-location distinction.
- Stable installation IDs.
- Host-command vs supported-command distinction.
- Location-rich analytics export concept.

### Data model
- Local database schema: **4**
- Enterprise analytics schema: **TCCC_ANALYTICS_2.0**
- Android versionCode: **22100**
- Installation catalog version: **2026.09.08**

### Deliberately deferred
- Central DAF system-of-record storage.
- Cross-device synchronization.
- RBAC / authoritative evaluator identity.
- MAJCOM/DAF enterprise longitudinal dashboards.
- True inter-rater agreement/calibration workflow.
- Server-side record integrity/retention.
