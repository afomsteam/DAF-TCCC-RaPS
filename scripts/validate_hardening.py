from pathlib import Path
import json, re
root=Path(__file__).resolve().parents[1]; www=root/'www'
def read(p): return p.read_text(encoding='utf-8')
app=read(www/'app.js'); css=read(www/'styles.css'); idx=read(www/'index.html'); tiers=read(www/'tiers.js'); version=read(www/'version.js'); branding=read(www/'branding.js'); installs=read(www/'installations.js'); harden=read(root/'scripts'/'harden-android.mjs')
package=json.loads(read(root/'package.json')); tw=read(root/'.github/workflows/build-test-apk.yml'); rw=read(root/'.github/workflows/build-release-apk.yml')
name=re.search(r"versionName:\s*['\"]([^'\"]+)['\"]",version).group(1); code=int(re.search(r'versionCode:\s*(\d+)',version).group(1))
# installation catalog is JSON inside Object.freeze(...)
m=re.search(r'Object\.freeze\((\{[\s\S]*\})\);\s*$',installs); catalog=json.loads(m.group(1)) if m else {}
commands={x['id'] for x in catalog.get('commands',[])}; bases=catalog.get('installations',[]); ids=[x.get('id') for x in bases]
struct=all(x.get('id') and x.get('name') and x.get('hostCommand') and isinstance(x.get('commands'),list) for x in bases)
refs=all(x.get('hostCommand') in commands and all(c in commands for c in x.get('commands',[])) for x in bases)
checks={
'authoritative version 2.21.0': name=='2.21.0' and code==22100,
'package version matches': package.get('version')==name,
'database schema v4': 'x.schemaVersion=4' in app and 'db.schemaVersion=4' in app and 'schemaVersion:4' in app,
'installation catalog loads before app': idx.find('installations.js')>0 and idx.find('installations.js')<idx.find('app.js'),
'installation catalog parses': bool(catalog),
'installation catalog has stable unique IDs': len(bases)>=70 and len(ids)==len(set(ids)) and struct,
'installation command references valid': refs and {'ACC','AETC','AFGSC','AFMC','AMC','AFSOC','PACAF','USAFE-AFAFRICA','AFDW','USAFA'}.issubset(commands),
'installation tenant relationships supported': any(len(x.get('commands',[]))>1 for x in bases),
'current JB Lindsey Graham alias retained': any(x.get('name')=='Joint Base Lindsey Graham' and 'Joint Base Charleston' in x.get('aliases',[]) for x in bases),
'MAJCOM/base class form': 'Supported MAJCOM / Command *' in app and 'Home installation *' in app and 'Show all active-duty installations' in app,
'training location separate from home': 'Training location is the same as home installation' in app and 'trainingLocationType' in app,
'location migration preserves legacy data': 'inferInstallationId(legacy)' in app and "c.location=c.trainingLocationName||c.homeInstallationName" in app,
'operational MAJCOM separate from host command': 'operational_majcom' in app and 'home_installation_host_command' in app and 'hostCommand' in app,
'site/unit/exercise retained': 'siteCode' in app and 'unit' in app and 'exercise' in app,
'program management dashboard present': all(x in idx for x in ['managementKpis','managementMajcomTable','managementInstallationTable','managementRootCauses','managementGapTable','managementDataQuality']),
'management MAJCOM/base/tier/course filters': all(x in idx for x in ['managementMajcom','managementInstallation','managementTier','managementCourseType']),
'multi-class normalized gap aggregation': 'aggregateManagement' in app and 'failRate:tested?g.fail/tested:null' in app and 'tierId:itemId' not in app,
'RCA management aggregation': 'classifiedFailObs' in app and 'rootCounts' in app and 'RCA classified' in app,
'MAJCOM and installation rollups': "managementGroupRows(scope,'majcom')" in app and "managementGroupRows(scope,'installation')" in app,
'data quality panel': 'classes missing MAJCOM' in app and 'classes missing home installation' in app and 'failed observations missing RCA' in app,
'management summary export': 'exportManagementSummaryCsv' in app and 'managementSummaryCsvBtn' in idx,
'enterprise detail schema v2': "TCCC_ANALYTICS_2.0" in app and 'installation_catalog_version' in app,
'enterprise detail includes location+RCA+remediation': all(x in app for x in ['operational_majcom','home_installation_id','remediation_reason','failure_mode_label','primary_contributor_label']),
'enterprise export excludes student names': "student_local_id" in app and "student_anon_id" not in app,
'class enterprise detail export': 'classEnterpriseCsvBtn' in idx and 'exportClassEnterpriseAnalyticsCsv' in app,
'phase tabs use color status': '.tab.done{background' in css and '.tab.warn{background' in css and "content:'✓'" not in css,
'next unresolved top/bottom': 'id="nextUnresolvedBottomBtn"' in idx and "$(`nextUnresolvedBottomBtn`)" not in app and "$('nextUnresolvedBottomBtn').onclick=nextUnresolved" in app,
'contact privacy': 'mailto:' not in branding and 'tel:' not in branding and 'Contact: ${b.officeName}' in branding,
'modal fixed': re.search(r'\.modal\{position:fixed;inset:0;z-index:900;.*align-items:center;justify-content:center',css) is not None,
'mass pass removed': 'function completeBlock(' not in app,
'NT justification': 'NT_REASONS' in app and 'requestNtReason' in app,
'A2 remediation gate': 'Attempt 2 is reserved for remediation' in app,
'pre-assessment gate': 'Evaluator ready check' in app and 'Begin Assessment' in app,
'void unfinished attempt': 'function voidCurrentAttempt()' in app,
'timer recovery': 'performance.now' in app and 'RECOVERY REQUIRED' in app,
'CSV formula hardening': 'function csvValue' in app and '[=+\\-@]' in app,
'Unicode canvas PDF': "canvas.toDataURL('image/jpeg'" in app,
'tourniquet CMC CAN wording': re.search(r'"id": "CMC-062"[\s\S]{0,500}Wound could be closely monitored',tiers) is not None,
'tourniquet CPP CAN wording': re.search(r'"id": "CPP-062"[\s\S]{0,500}Wound could be closely monitored',tiers) is not None,
'bad tourniquet wording removed': 'Wound could not be closely monitored' not in tiers,
'48px field controls': 'min-height:48px' in css and 'min-height:52px' in css,
'structured RCA model': 'FAILURE_MODES' in app and 'FAILURE_CONTRIBUTORS' in app and 'failureDetails' in app,
'critical failure RCA required': 'Critical failures require both a failure mode and a primary contributor.' in app,
'noncritical fail one tap': "mode:'unclassified',modeLabel:'Unclassified / review later'" in app,
'remediation reason/action': 'remediationReason' in app and 'remediationAction' in app,
'class analytics': 'classAnalyticsKpis' in idx and 'renderClassAnalytics' in app and 'classHeatmap' in idx,
'criterion rates normalized': 'failRate:tested?fail/tested:null' in app,
'first vs final analytics': "['First-pass'" in app and "['Final pass'" in app,
'roster filters': 'data-roster-filter="not-started"' in idx and 'data-roster-filter="remediation"' in idx,
'field/review modes': 'evalModeBtn' in idx and '.fieldMode #reviewTimelineCard' in css,
'collapsed evaluator header': '#evalHeader.collapsed' in css and 'updateEvalHeaderCollapse' in app,
'native branding resources': (root/'native-android-res/mipmap-xxxhdpi/ic_launcher.png').is_file(),
'workflows preflight installations': 'test -f www/installations.js' in tw and 'test -f www/installations.js' in rw,
'workflows syntax-check installations': 'node --check www/installations.js' in tw and 'node --check www/installations.js' in rw,
'workflows branding after Capacitor generation': tw.find('npx cap add android')<tw.find('run: bash scripts/apply-android-native-branding.sh') and rw.find('npx cap add android')<rw.find('run: bash scripts/apply-android-native-branding.sh'),
}
# fix walrus-created non-string key if any
checks={str(k):v for k,v in checks.items()}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS' if v else 'FAIL')+' - '+k)
if failed: raise SystemExit('\nValidation failed: '+', '.join(failed))
print(f'\n{len(checks)} release checks passed for TCCC v{name} ({code}); {len(bases)} installations / {len(commands)} commands validated.')
