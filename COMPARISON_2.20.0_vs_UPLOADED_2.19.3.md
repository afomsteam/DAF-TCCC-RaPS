# TCCC Evaluation Suite — Comparison and Merge Basis

## Compared builds

- **Existing intelligence baseline:** Android source v2.20.0
- **Uploaded comparison APK:** v2.19.3 (`TCCC-v2.19.3-test(2).apk`)
- **Merged release:** v2.21.0 / Android versionCode 22100

The uploaded APK identifies itself as **v2.19.3**, not v2.20.0. The clinical checklist file (`tiers.js`) is byte-for-byte identical between the uploaded APK and the v2.20.0 baseline, so this merge does **not** require reconciling competing Tier 1–4 clinical criteria.

## Source-level comparison

| Area | Uploaded v2.19.3 | v2.20.0 baseline | v2.21.0 decision |
|---|---|---|---|
| Tier 1–4 clinical criteria | Same | Same | Preserve unchanged |
| MAJCOM / installation catalog | Strong | Free-text location/site code only | Merge v2.19.3 catalog and selectors |
| Home vs training location | Structured | Single location + site code | Preserve both structured locations + site code |
| Tenant/joint command relationships | Supported | Not modeled | Preserve supported-command array separately from host command |
| Enterprise criterion export | Location-rich | RCA/remediation-rich | Combine into Analytics Schema 2.0 |
| Structured RCA | Not present | Strong | Preserve v2.20.0 |
| Critical FAIL classification | Not present | Required | Preserve v2.20.0 |
| Remediation reason/action | Limited | Structured | Preserve v2.20.0 |
| First-pass vs final analytics | Limited | Strong | Preserve v2.20.0 |
| Normalized criterion failure rate | Limited | Strong | Preserve v2.20.0 |
| Heat map / class intelligence | Not present | Strong | Preserve v2.20.0 |
| Roster operational filters | Not present | Strong | Preserve v2.20.0 |
| Field / Review Mode | Not present | Strong | Preserve v2.20.0 |
| Cross-class local management | Not present | Not present | **New in v2.21.0** |
| MAJCOM/base rollups | Export groundwork | Not present | **New in v2.21.0** |
| Data-quality reporting | Not present | Not present | **New in v2.21.0** |

## Functions unique to the uploaded v2.19.3 branch

The comparison found the following major location/data capabilities that were not in the v2.20.0 baseline:

- `installationById`
- `commandById`
- `commandName`
- `installationDisplay`
- `inferInstallationId`
- `ensureLocationFields`
- `applyClassLocationFields`
- `classLocationExportValues`
- enterprise criterion-level location export

The uploaded APK also included a dedicated `installations.js` catalog.

## Functions unique to the v2.20.0 branch

The comparison found the following major performance-intelligence capabilities that were not in the uploaded v2.19.3 APK:

- `classAnalytics`
- `criterionGapStats`
- `criticalFailCount`
- `criticalFailureCauseMissing`
- `rootCauseStats`
- `evaluatorSignalStats`
- `renderClassAnalytics`
- `requestFailureClassification`
- `rosterMatches`
- `sectionHeatStatus`
- collapsed evaluator header logic
- class Performance Analytics CSV

## What v2.21.0 adds on top of the merge

v2.21.0 creates a local **Program Management Intelligence** layer across the classes stored on the device. It can scope data by:

1. supported MAJCOM / command,
2. home installation,
3. TCCC tier, and
4. course type.

It then calculates:

- number of classes and rostered students,
- first-attempt qualification,
- final qualification,
- remediation rate,
- remediation success,
- critical-failure rate,
- RCA classification completeness,
- normalized competency-gap rates,
- MAJCOM summaries,
- installation summaries,
- top structured root causes, and
- data-quality gaps that would weaken installation/MAJCOM comparisons.

## Installation model

The offline installation catalog contains **73 active-duty installation records and 11 command categories**. An installation has both:

- `hostCommand` — the host/owning command, and
- `commands[]` — commands for which the installation should be selectable because of host, tenant, joint, or supported relationships.

This distinction prevents a tenant mission from being forced into the host command simply because of geography.

Each class retains:

- component,
- supported/operational MAJCOM,
- home installation stable ID/name/state/country,
- installation host command,
- unit/organization,
- local site code,
- training-location type,
- training installation stable ID or custom expeditionary location,
- exercise/event,
- course type,
- scenario/version/difficulty/profile,
- evaluator identifiers,
- curriculum/content version.

Legacy classes with only a free-text `location` are migrated in-place where the text matches a catalog name or alias; otherwise the original text is retained as a custom location.

## Analytics Schema 2.0

The v2.21.0 Enterprise Detail CSV combines location metadata with the v2.20.0 performance-improvement model. It includes structured:

- MAJCOM / installation metadata,
- course/scenario/curriculum metadata,
- attempt and remediation metadata,
- criterion grading,
- NT reason,
- failure mode,
- primary contributor,
- contributing factor,
- timer-forced failure,
- application/content/catalog versions.

Student names are omitted from this cross-class export; local student ID and optional training ID are carried for downstream linkage. Free-text failure comments/criterion notes can still contain evaluator-entered information and should be governed appropriately before enterprise ingestion.

## Architecture boundary

v2.21.0 remains an **offline field collection + local management intelligence application**. It does not create a competing enterprise system of record. Central identity, authoritative storage, synchronization, RBAC, enterprise retention, MAJCOM/DAF-wide longitudinal reporting, and true inter-rater calibration remain responsibilities for the planned DAF backend.
