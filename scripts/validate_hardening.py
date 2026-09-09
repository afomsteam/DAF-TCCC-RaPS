from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
www = root / 'www'
app = (www / 'app.js').read_text(encoding='utf-8')
css = (www / 'styles.css').read_text(encoding='utf-8')
idx = (www / 'index.html').read_text(encoding='utf-8')
tiers = (www / 'tiers.js').read_text(encoding='utf-8')
version = (www / 'version.js').read_text(encoding='utf-8')
branding = (www / 'branding.js').read_text(encoding='utf-8')
harden = (root / 'scripts' / 'harden-android.mjs').read_text(encoding='utf-8')
branding_script = root / 'scripts' / 'apply-android-native-branding.sh'
package = json.loads((root / 'package.json').read_text(encoding='utf-8'))
test_workflow = (root / '.github' / 'workflows' / 'build-test-apk.yml').read_text(encoding='utf-8')
release_workflow = (root / '.github' / 'workflows' / 'build-release-apk.yml').read_text(encoding='utf-8')

name_match = re.search(r"versionName:\s*['\"]([^'\"]+)['\"]", version)
code_match = re.search(r"versionCode:\s*(\d+)", version)
version_name = name_match.group(1) if name_match else None
version_code = int(code_match.group(1)) if code_match else None

checks = {
    'authoritative version source parses': bool(version_name and version_code),
    'package version matches authoritative version': package.get('version') == version_name,
    'phase tabs use color status not symbols': ".tab.done{background" in css and ".tab.warn{background" in css and "content:'✓'" not in css and "content:'!'" not in css,
    'bottom next unresolved replaces review action': 'id="nextUnresolvedBottomBtn"' in idx and '>Next Unresolved</button>' in idx and "$('nextUnresolvedBottomBtn').onclick=nextUnresolved" in app,
    'contact privacy cleanup': 'mailto:' not in branding and 'tel:' not in branding and 'Contact: ${b.officeName}' in branding,
    'app reads version source': 'window.TCCC_BUILD?.versionName' in app,
    'modal override removed': '.view,.modal,.safetySplash{position:relative' not in css,
    'modal fixed and centered': re.search(r'\.modal\{position:fixed;inset:0;z-index:900;.*align-items:center;justify-content:center', css) is not None,
    'mass pass remains removed': 'function completeBlock(' not in app and 'block-closeout' not in app and 'function reviewRemaining()' not in app,
    'explicit NT justification': 'NT_REASONS' in app and 'requestNtReason' in app and 'Other' in app,
    'A2 remediation gate': "Attempt 2 is reserved for remediation" in app and "a1.finalResult==='FAIL'" in app,
    'pre-assessment start gate': 'Begin Assessment' in app and 'Evaluator ready check' in app,
    'void unfinished attempt': 'function voidCurrentAttempt()' in app and 'Void In-Progress Attempt' in idx,
    'monotonic timer': 'performance.now' in app and 'timerNeedsRecovery' in app and 'RECOVERY REQUIRED' in app,
    'CSV formula hardening': 'function csvValue' in app and "[=+\\-@]" in app,
    'Unicode-capable canvas PDF': "canvas.toDataURL('image/jpeg'" in app and 'fillText(o.text' in app and 'replace(/[^\\x20-\\x7E]/g' not in app,
    'tourniquet CMC wording': re.search(r'"id": "CMC-062"[\s\S]{0,500}Wound could be closely monitored', tiers) is not None,
    'tourniquet CPP wording': re.search(r'"id": "CPP-062"[\s\S]{0,500}Wound could be closely monitored', tiers) is not None,
    'bad tourniquet wording removed': 'Wound could not be closely monitored' not in tiers,
    '48px field controls': 'min-height:48px' in css and 'min-height:52px' in css,
    'native branding source exists': (root / 'native-android-res' / 'mipmap-xxxhdpi' / 'ic_launcher.png').is_file(),
    'native branding script exists': branding_script.is_file(),
    'Android hardener reads authoritative version': "www/version.js" in harden and "const VERSION_NAME = '2.17.0'" not in harden and 'const VERSION_CODE = 21700' not in harden,
    'test workflow uses existing branding script': 'bash scripts/apply-android-native-branding.sh' in test_workflow and 'apply_android_branding.py' not in test_workflow,
    'release workflow uses existing branding script': 'bash scripts/apply-android-native-branding.sh' in release_workflow and 'apply_android_branding.py' not in release_workflow,
    'test workflow regenerates Android before branding': test_workflow.find('npx cap add android') < test_workflow.find('bash scripts/apply-android-native-branding.sh'),
    'release workflow regenerates Android before branding': release_workflow.find('npx cap add android') < release_workflow.find('bash scripts/apply-android-native-branding.sh'),
    'v2.20 schema migration': 'x.schemaVersion=3' in app and 'db.schemaVersion=3' in app,
    'structured failure mode model': 'FAILURE_MODES' in app and 'FAILURE_CONTRIBUTORS' in app and 'failureDetails' in app,
    'critical failure RCA required': 'Critical failures require both a failure mode and a primary contributor.' in app and 'criticalCauseMissing' in app,
    'noncritical fail remains one tap': "mode:'unclassified',modeLabel:'Unclassified / review later'" in app,
    'remediation reason and action captured': 'remediationReason' in app and 'remediationAction' in app and 'Record the remediation reason and corrective action' in app,
    'class performance intelligence dashboard': 'classAnalyticsKpis' in idx and 'renderClassAnalytics' in app and 'classHeatmap' in idx,
    'normalized criterion gap rate': 'failRate:tested?fail/tested:null' in app and 'HIGHEST CRITERION FAILURE RATES' in app,
    'scenario coverage gap analytics': 'Scenario coverage gaps — highest NT rate' in app and "'Scenario coverage'" in app,
    'first pass vs final qualification analytics': "['First-pass'" in app and "['Final pass'" in app,
    'remediation and repeat failure analytics': "['Remediation success'" in app and "['Repeat failure'" in app,
    'student comparison without leaderboard ranking': 'studentComparison' in idx and 'Remediation gain' in app,
    'evaluator pattern signal capture': 'attemptEvaluatorId' in idx and 'evaluatorSignalStats' in app and 'Descriptive only — not inter-rater agreement' in app,
    'roster operational filters': 'data-roster-filter="not-started"' in idx and 'data-roster-filter="remediation"' in idx and 'rosterMatches' in app,
    'field and review modes': 'evalModeBtn' in idx and 'fieldMode' in app and '.fieldMode #reviewTimelineCard' in css,
    'collapsed evaluator header': '#evalHeader.collapsed' in css and 'updateEvalHeaderCollapse' in app,
    'analysis-ready export': 'classAnalyticsCsvBtn' in idx and 'exportClassAnalyticsCsv' in app and 'failure_mode_label' in app and 'primary_contributor_label' in app,
    'standardized site/course/scenario fields': 'siteCode' in app and 'courseType' in app and 'scenarioDifficulty' in app and 'curriculumId' in app,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS' if ok else 'FAIL') + ' - ' + name)
if failed:
    raise SystemExit('\nHardening validation failed: ' + ', '.join(failed))
print(f'\n{len(checks)} hardening checks passed for TCCC v{version_name} ({version_code}).')
