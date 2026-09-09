# TCCC Evaluation Suite — Android / APK

**Release:** v2.20.0  
**Android versionCode:** 22000  
**Role:** Offline-first field evaluation and class-level performance intelligence

This repository is the complete source baseline for the Android TCCC evaluator. The generated `android/` project is intentionally not committed; GitHub Actions creates it, synchronizes Capacitor, reapplies the controlled TCCC launcher/splash resources, applies Android hardening/versioning, validates the release, and builds the APK.

## v2.20 purpose

v2.20 moves the field app from an electronic checklist toward a competency performance-improvement collector while keeping the evaluator—not an algorithm—in control of PASS/FAIL and certification.

### Evaluation workflow
- Field Mode reduces on-screen cognitive load during a lane.
- Review Mode exposes notes, provenance, timeline, sign-off, failure classification, and finalization.
- Critical FAIL requires a structured failure mode and primary contributor.
- Noncritical FAIL remains one-tap and can be classified during review.
- Attempt 2 requires a remediation reason and corrective action after finalized A1 FAIL.
- Existing critical-task, unresolved-item, timer, NT-justification, A2, and finalization safeguards remain in force.

### Class performance intelligence
- First-attempt qualification vs final qualification.
- Remediation burden, remediation success, repeat failure, critical-failure exposure, and median attempts to proficiency.
- Criterion gap ranking uses `FAIL / (PASS + FAIL)` rather than raw miss count.
- Scenario coverage shows tested vs NT exposure and highlights high-NT criteria.
- Root-cause and failure-mode distributions.
- Student competency heat map and descriptive student comparison without ranking students by a simplistic leaderboard.
- Descriptive evaluator pattern signals (not inter-rater agreement).
- Roster search and operational filters: Not Started, In Progress, Failed, Remediation, Qualified.
- Performance Analytics CSV for downstream analysis/DAF backend ingestion.

### Data captured for future backend use
Class/course records now carry standardized analysis fields including course type, location/site code, evaluator identifier, scenario difficulty/profile, curriculum ID, content version, remediation data, criterion failure classification, timestamps, and app version.

## Intentionally deferred to the DAF backend
This APK is **not** being made into a competing enterprise system of record. v2.20 does not implement MAJCOM/enterprise longitudinal dashboards, centralized RBAC, authoritative identity, cross-device synchronization, enterprise retention, or server-side record integrity. Those should live in the planned DAF backend.

Likewise, evaluator pattern signals in the class dashboard are descriptive. A real inter-rater reliability/calibration feature requires purposely double-scored observations and an enterprise analysis method.

## Build test APK
1. Push the repository to GitHub.
2. Open **Actions**.
3. Run **Build TCCC Test APK**.
4. Download `TCCC-v2.20.0-test.apk` from the workflow artifacts.

The workflow verifies required source/branding files before building.

## Build signed release APK
Use **Build TCCC Release APK** after configuring the signing secrets documented in the workflow. Do not commit signing keys to the repository.

## Repository layout
- `.github/workflows/` — test and release APK workflows
- `www/` — evaluator UI, scoring logic, TCCC content, graphics
- `native-android-res/` — controlled Android launcher/splash resources
- `scripts/` — content validation, Android branding/hardening, release checks
- `capacitor.config.json` — Capacitor configuration
- `package.json` — build dependencies/scripts

## Clinical/content note
The approved tourniquet-conversion criterion uses **“Wound could be closely monitored.”** Existing source provenance is preserved. Legacy curriculum/source dates shown in the embedded standards are not silently rewritten; formal curriculum governance and supersession should be adjudicated by the responsible TCCC program authority.

**Contact: John Garcia**
