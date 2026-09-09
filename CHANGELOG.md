# Changelog

## 2.19.3 — 2026-09-08

### Added
- Cascading Supported MAJCOM / Command → Home Installation selection on New Class.
- Offline installation catalog with stable IDs and aliases (`www/installations.js`).
- Show-all override for tenant/joint/cross-command home-station cases.
- Unit / Organization field.
- Separate Training Location with same-as-home default.
- Expeditionary / Other training location support.
- Optional Exercise / Event field.
- Structured location metadata on class view.
- Structured location columns across class/individual CSV exports.
- Enterprise Analytics CSV with `TCCC_ANALYTICS_1.0` schema identifier.
- De-identified `student_anon_id` in enterprise analytics export.
- Source validation checks for installation uniqueness, PACAF cascade, and 2026 Luke/Holloman command changes.

### Changed
- Local database schema normalized from 2 to 3 while preserving legacy class records.
- Legacy free-text class `location` is migrated to structured location data when an exact catalog/alias match exists.
- CSV export cell handling hardened against spreadsheet formula prefixes.
- Visible/app build version updated to 2.19.3 / 21903.

### Preserved
- Tier 1–4 clinical criteria and scoring behavior from the supplied v2.19.2 APK.
- PASS / FAIL / NT / N/O model.
- Critical-task handling and finalization behavior.
- Attempt 1 / remediation Attempt 2 workflow.
- Timers, event history, roster workflow, PDF exports, backups, class closure, and local offline operation.

### Not included
- Power BI dashboard/model.
- Backend/API or synchronization.
- Root-cause/failure-mode capture UI (reserved for a later performance-intelligence release).
