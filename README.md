# TCCC Evaluation Suite v2.19.3 — GitHub Ready

This package is a complete Android/Capacitor source update derived from the supplied **TCCC v2.19.2 test APK**.

## Scope of v2.19.3

This is the **installation + analytics-export foundation**. It does **not** add Power BI, a network backend, SharePoint synchronization, or cloud connectivity.

### New Class improvements

New classes now capture structured location data:

- **Supported MAJCOM / Command**
- **Home Installation** filtered by the selected command
- **Show all active-duty installations** override for tenant/joint situations
- **Unit / Organization** (optional)
- **Training Location** separate from home station
- **Same as home installation** default
- **Expeditionary / Other location** option
- **Exercise / Event** (optional)

Example:

- Supported Command: `PACAF`
- Home Installation: `Joint Base Pearl Harbor-Hickam (Hickam), HI`
- Training Location: `Andersen AFB, GU`
- Exercise: `Mobility Guardian 26`

Selecting PACAF initially shows only the PACAF base set in the catalog. The evaluator can intentionally enable **Show all active-duty installations** when a tenant, joint, or cross-command situation requires it.

### Stable installation IDs

The app does not rely on free-text base names for new records. It stores stable IDs such as:

- `DYESS`
- `FAIRCHILD`
- `JBPHH`
- `RAMSTEIN`
- `OSAN`

This prevents future analytics from treating `Hickam`, `Hickam AFB`, `JBPHH`, and `Joint Base Pearl Harbor-Hickam` as separate locations.

The offline catalog is maintained in:

`www/installations.js`

Catalog version: **2026.09.08**.

The catalog includes active-duty USAF host installations plus selected joint/tenant locations needed for current active-duty MAJCOM workflows. ANG/AFRC-only installations are intentionally outside this release.

> **Why the field says “Supported MAJCOM / Command”:** AFMS administrative alignment is evolving. For this TCCC analytics use case, the field is intended to represent the operational/host command whose population or mission the class supports (for example PACAF, AMC, ACC), not to overwrite future AFMEDCOM personnel alignment.

### Legacy class migration

Existing v2.19.2 classes are preserved. During database normalization, the app attempts to match the old free-text `location` to a catalog installation/alias. If no exact match is found, the legacy text remains available rather than being discarded.

## CSV changes

The existing Summary, Criteria, Timers, Events, and Full Individual CSV exports now carry structured location fields:

- `component`
- `operational_majcom`
- `home_installation_id`
- `home_installation_name`
- `home_installation_host_command`
- `unit`
- `training_location_type`
- `training_installation_id`
- `training_location_name`
- `training_location_region`
- `training_location_country`
- `exercise`

### New: Enterprise Analytics CSV

The Class Export card now includes **Enterprise Analytics CSV**.

This is a long-form, criterion-level export intended for later Power BI/SharePoint/database use. Each row is one criterion result for one student attempt.

Important privacy behavior:

- Does **not** export student name
- Does **not** export rank
- Does **not** export training ID
- Uses the app's internal random student UUID as `student_anon_id`
- Includes class, command, installation, scenario, attempt, criterion, grade, timing-forced-failure indicator, content version, and app version

Schema identifier:

`TCCC_ANALYTICS_1.0`

This lets a future Power BI model or USAF backend identify the export schema without guessing based on column order.

## What is intentionally NOT in v2.19.3

- No Power BI files or code
- No SharePoint/OneDrive connection
- No network/API synchronization
- No backend/system of record
- No CAC/authentication
- No enterprise user permissions
- No new root-cause/failure-mode grading UI yet

Those can be layered on later without changing the location IDs introduced here.

## Current command-data notes

The catalog was checked against current official Air Force command information on 8 Sep 2026. Notable current changes reflected in the catalog include:

- Holloman AFB transitioned from AETC to ACC on 4 Jun 2026.
- Luke AFB transitioned from AETC to ACC on 17 Jul 2026.
- PACAF's base filter includes Hickam, Andersen, Eielson, JBER, Kadena, Kunsan, Misawa, Osan, and Yokota.
- USAFE-AFAFRICA's seven main operating bases are represented.
- AMC host installations and its major active-duty tenant locations are represented.

Because organizational relationships change, update `www/installations.js` rather than rewriting the class form.

## Repository layout

```text
.
├── .github/workflows/
│   ├── build-test-apk.yml
│   └── build-release-apk.yml
├── assets/android-icons/
├── scripts/
│   ├── apply_android_version.py
│   ├── harden-android.mjs
│   └── validate-content.mjs
├── www/
│   ├── assets/
│   ├── app.js
│   ├── branding.js
│   ├── installations.js
│   ├── index.html
│   ├── manifest.webmanifest
│   ├── styles.css
│   ├── sw.js
│   ├── tiers.js
│   └── version.js
├── capacitor.config.json
├── package.json
├── README.md
└── CHANGELOG.md
```

## Easiest GitHub update

1. Download and extract this package.
2. Create a safety branch in your TCCC GitHub repository, such as `v2.19.3-test`.
3. Copy **everything inside** the extracted `TCCC-Evaluation-Suite-v2.19.3` folder into the root of your cloned repository.
4. Replace matching files. Do not delete the hidden `.git` folder.
5. Commit and push.
6. On GitHub, open **Actions → Build TCCC Test APK → Run workflow**.
7. Download the `TCCC-v2.19.3-test` artifact.
8. Install and test the APK before merging to `main`.

## Recommended device test

Test at least these paths:

1. Create a PACAF class and confirm only PACAF locations initially appear.
2. Create an AMC class and confirm Fairchild appears.
3. Create an AFGSC class and confirm Dyess appears.
4. Enable Show All and choose a cross-command/tenant installation.
5. Set training location different from home station.
6. Use Expeditionary / Other location.
7. Add students and grade an attempt.
8. Export Summary, Criteria, Timers, Events, Full Individual, and Enterprise Analytics CSV.
9. Confirm the Enterprise Analytics CSV contains no student names/training IDs.
10. Restore an older class backup and confirm its old location is retained/migrated.
11. Export PDF and confirm PDF behavior is unchanged.
12. Close a class and confirm it remains read-only.

## Signed release workflow

Before running **Build TCCC Signed Release APK**, configure these repository secrets:

- `TCCC_KEYSTORE_BASE64`
- `TCCC_KEYSTORE_PASSWORD`
- `TCCC_KEY_ALIAS`
- `TCCC_KEY_PASSWORD`

Do not commit a release keystore or credentials to GitHub.

## Local/offline behavior

The Android build remains offline-first. The app stores working records locally and saves exports to the Android Documents folder through Capacitor Filesystem. The Android hardening script removes the INTERNET permission and disables cleartext traffic and Android backup.
