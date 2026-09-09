import fs from 'node:fs';
import path from 'node:path';

const versionPath = path.resolve('www/version.js');
if (!fs.existsSync(versionPath)) {
  throw new Error('www/version.js not found.');
}

const versionSource = fs.readFileSync(versionPath, 'utf8');
const nameMatch = versionSource.match(/versionName:\s*['\"]([^'\"]+)['\"]/);
const codeMatch = versionSource.match(/versionCode:\s*(\d+)/);
if (!nameMatch || !codeMatch) {
  throw new Error('Could not read versionName/versionCode from www/version.js.');
}

const VERSION_NAME = nameMatch[1];
const VERSION_CODE = Number(codeMatch[1]);

const manifestPath = path.resolve('android/app/src/main/AndroidManifest.xml');
const gradleCandidates = [
  path.resolve('android/app/build.gradle'),
  path.resolve('android/app/build.gradle.kts')
];

if (!fs.existsSync(manifestPath)) {
  throw new Error('Android project not found. Run Capacitor Android generation first.');
}

let manifest = fs.readFileSync(manifestPath, 'utf8');
manifest = manifest.replace(/\s*<uses-permission\s+android:name="android\.permission\.INTERNET"\s*\/>\s*/g, '\n');

if (/android:allowBackup="[^"]*"/.test(manifest)) {
  manifest = manifest.replace(/android:allowBackup="[^"]*"/, 'android:allowBackup="false"');
} else {
  manifest = manifest.replace(/<application\b/, '<application android:allowBackup="false"');
}

if (/android:usesCleartextTraffic="[^"]*"/.test(manifest)) {
  manifest = manifest.replace(/android:usesCleartextTraffic="[^"]*"/, 'android:usesCleartextTraffic="false"');
} else {
  manifest = manifest.replace(/<application\b/, '<application android:usesCleartextTraffic="false"');
}

fs.writeFileSync(manifestPath, manifest);

const gradlePath = gradleCandidates.find((candidate) => fs.existsSync(candidate));
if (!gradlePath) {
  throw new Error('android/app/build.gradle(.kts) not found.');
}

let gradle = fs.readFileSync(gradlePath, 'utf8');
if (gradlePath.endsWith('.kts')) {
  const before = gradle;
  gradle = gradle.replace(/versionCode\s*=\s*\d+/, `versionCode = ${VERSION_CODE}`);
  gradle = gradle.replace(/versionName\s*=\s*"[^"]+"/, `versionName = "${VERSION_NAME}"`);
  if (gradle === before && (!gradle.includes(`versionCode = ${VERSION_CODE}`) || !gradle.includes(`versionName = "${VERSION_NAME}"`))) {
    throw new Error(`Could not patch version values in ${gradlePath}`);
  }
} else {
  const before = gradle;
  gradle = gradle.replace(/versionCode\s+\d+/, `versionCode ${VERSION_CODE}`);
  gradle = gradle.replace(/versionName\s+['"][^'"]+['"]/, `versionName "${VERSION_NAME}"`);
  if (gradle === before && (!gradle.includes(`versionCode ${VERSION_CODE}`) || !gradle.includes(`versionName "${VERSION_NAME}"`))) {
    throw new Error(`Could not patch version values in ${gradlePath}`);
  }
}

fs.writeFileSync(gradlePath, gradle);
console.log(`Android hardened: version ${VERSION_NAME} (${VERSION_CODE}), backups disabled, cleartext disabled, INTERNET permission removed.`);
