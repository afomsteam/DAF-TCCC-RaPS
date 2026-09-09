import fs from 'node:fs';
import vm from 'node:vm';

function read(p){ return fs.readFileSync(p,'utf8'); }
const version = read('www/version.js');
if (!version.includes("versionName: '2.19.3'") || !version.includes('versionCode: 21903')) throw new Error('version.js mismatch');
for (const f of ['www/app.js','www/index.html','www/styles.css','www/tiers.js','www/branding.js','www/installations.js']) if (!fs.existsSync(f)) throw new Error(`Missing ${f}`);
if (!read('www/index.html').includes('installations.js')) throw new Error('installations.js is not loaded by index.html');
if (!read('www/index.html').includes('enterpriseAnalyticsCsvBtn')) throw new Error('Enterprise analytics export button missing');
if (!read('www/app.js').includes("TCCC_ANALYTICS_1.0")) throw new Error('Analytics schema constant missing');

const sandbox={window:{}}; vm.createContext(sandbox); vm.runInContext(read('www/installations.js'),sandbox);
const d=sandbox.window.TCCC_INSTALLATION_DATA;
if (!d || !Array.isArray(d.installations) || d.installations.length < 65) throw new Error('Installation catalog appears incomplete');
const ids=new Set(); for (const i of d.installations){ if(ids.has(i.id)) throw new Error(`Duplicate installation id ${i.id}`); ids.add(i.id); }
for (const required of ['DYESS','FAIRCHILD','JBPHH','RAMSTEIN','OSAN','JBER','HURLBURT','BARKSDALE']) if(!ids.has(required)) throw new Error(`Missing required installation ${required}`);
const pacaf=d.installations.filter(i=>(i.commands||[]).includes('PACAF')).map(i=>i.id).sort();
const expected=['ANDERSEN','EIELSON','JBER','JBPHH','KADENA','KUNSAN','MISAWA','OSAN','YOKOTA'].sort();
if (JSON.stringify(pacaf)!==JSON.stringify(expected)) throw new Error(`PACAF filter mismatch: ${pacaf.join(', ')}`);
for (const moved of ['HOLLOMAN','LUKE']) { const i=d.installations.find(x=>x.id===moved); if(i.hostCommand!=='ACC'||!(i.commands||[]).includes('ACC')) throw new Error(`${moved} is not current under ACC`); }
console.log(`Validated v2.19.3: ${d.installations.length} catalog locations; PACAF cascade ${pacaf.length}/9; analytics export present.`);
