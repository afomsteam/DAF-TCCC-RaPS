import fs from 'node:fs';
import vm from 'node:vm';

const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync('www/tiers.js', 'utf8'), context, { filename: 'tiers.js' });
const tiers = context.window.TCCC_TIERS;
if (!tiers) throw new Error('TCCC_TIERS did not load.');

const required = ['1','2','3','4'];
for (const id of required) {
  const t = tiers[id];
  if (!t) throw new Error(`Missing Tier ${id}.`);
  if (!Array.isArray(t.sections) || !t.sections.length) throw new Error(`Tier ${id} has no sections.`);
  const items = t.sections.flatMap(s => s.items || []);
  const ids = new Set();
  for (const item of items) {
    if (!item.id || !item.text) throw new Error(`Tier ${id} contains a criterion without id/text.`);
    if (ids.has(item.id)) throw new Error(`Tier ${id} duplicate criterion id: ${item.id}`);
    ids.add(item.id);
    if (!['source','daf'].includes(item.provenance || 'source')) throw new Error(`Tier ${id} invalid provenance on ${item.id}`);
  }
  for (const timer of (t.timers || [])) {
    if (!timer.id || !timer.label) throw new Error(`Tier ${id} has malformed timer.`);
    if (timer.linkedItemId && !ids.has(timer.linkedItemId)) throw new Error(`Tier ${id} timer ${timer.id} links to missing ${timer.linkedItemId}`);
  }
  if (!Array.isArray(t.ratings) || t.ratings.map(r=>r.key).join(',') !== 'pass,fail,nt,no') {
    throw new Error(`Tier ${id} ratings must remain PASS / FAIL / NT / N/O.`);
  }
  console.log(`Tier ${id}: ${items.length} criteria, ${items.filter(i=>i.critical).length} critical, ${(t.timers||[]).length} timers — OK`);
}
console.log('TCCC content validation passed.');
