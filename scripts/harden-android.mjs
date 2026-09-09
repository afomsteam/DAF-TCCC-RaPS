import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const manifest = path.join(root, 'android/app/src/main/AndroidManifest.xml');
if (!fs.existsSync(manifest)) throw new Error('AndroidManifest.xml not found. Run npx cap add android/sync first.');
let xml = fs.readFileSync(manifest, 'utf8');
xml = xml.replace(/\s*<uses-permission[^>]*android:name=["']android\.permission\.INTERNET["'][^>]*\/>/g, '');
xml = xml.replace(/<application\b([^>]*)>/, (m, attrs) => {
  const strip = attrs
    .replace(/\sandroid:allowBackup=["'][^"']*["']/g, '')
    .replace(/\sandroid:usesCleartextTraffic=["'][^"']*["']/g, '')
    .replace(/\sandroid:fullBackupContent=["'][^"']*["']/g, '');
  return `<application${strip} android:allowBackup="false" android:usesCleartextTraffic="false" android:fullBackupContent="false">`;
});
fs.writeFileSync(manifest, xml);

const src = path.join(root, 'assets/android-icons');
const res = path.join(root, 'android/app/src/main/res');
for (const density of ['mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']) {
  const from = path.join(src, `mipmap-${density}`);
  const to = path.join(res, `mipmap-${density}`);
  fs.mkdirSync(to, {recursive:true});
  for (const name of ['ic_launcher.png','ic_launcher_round.png','ic_launcher_foreground.png']) {
    fs.copyFileSync(path.join(from,name), path.join(to,name));
  }
}
fs.mkdirSync(path.join(res,'mipmap-anydpi-v26'), {recursive:true});
const adaptive = `<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n  <background android:drawable="@color/ic_launcher_background"/>\n  <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>\n`;
fs.writeFileSync(path.join(res,'mipmap-anydpi-v26/ic_launcher.xml'), adaptive);
fs.writeFileSync(path.join(res,'mipmap-anydpi-v26/ic_launcher_round.xml'), adaptive);
fs.mkdirSync(path.join(res,'values'), {recursive:true});
const valuesDir=path.join(res,'values');
let colorUpdated=false;
for (const name of fs.readdirSync(valuesDir).filter(n=>n.endsWith('.xml'))) {
  const f=path.join(valuesDir,name);let v=fs.readFileSync(f,'utf8');
  if (/name=["']ic_launcher_background["']/.test(v)) {
    v=v.replace(/(<color\s+name=["']ic_launcher_background["'][^>]*>)[^<]*(<\/color>)/, '$1#08131D$2');
    fs.writeFileSync(f,v);colorUpdated=true;break;
  }
}
if(!colorUpdated)fs.writeFileSync(path.join(valuesDir,'tccc_launcher_colors.xml'), `<?xml version="1.0" encoding="utf-8"?>\n<resources><color name="ic_launcher_background">#08131D</color></resources>\n`);
console.log('Android hardening and launcher assets applied.');
